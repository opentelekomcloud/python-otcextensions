# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import warnings
from openstack import exceptions
from openstack import warnings as os_warnings


class ServiceProxy:
    def __init__(self, instance, service_type, supported_versions):
        self.instance = instance
        self.service_type = service_type
        self.supported_versions = supported_versions

    def create_proxy(self, base_service="aomv2", target_service="apig"):
        config = self.instance.config

        # Retrieve API version and endpoint configuration
        version_string = config.get_api_version(base_service) or '2'
        endpoint_override = config.get_endpoint(self.service_type)

        # Fetch service catalog URL and adjust the endpoint if necessary
        ep = config.get_service_catalog().url_for(service_type=base_service, region_name=config.region_name)
        epo = f"{ep.replace(base_service.split('v')[0], target_service)}"  # Flexible endpoint substitution

        if epo and not endpoint_override:
            endpoint_override = epo

        # Default to the only supported version if no version string is provided
        if not version_string and len(self.supported_versions) == 1:
            version_string = list(self.supported_versions)[0]

        # Attempt to create a proxy object with the specified endpoint and version
        proxy_obj = self._get_proxy_object(config, version_string, endpoint_override)
        if proxy_obj:
            return self._handle_discovery(proxy_obj, config)

        # If no specific endpoint or version, allow discovery with version constraints
        return self._create_discovery_adapter(config, version_string)

    def _get_proxy_object(self, config, version_string, endpoint_override):
        proxy_class = None
        if endpoint_override and version_string and self.supported_versions:
            proxy_class = self.supported_versions.get(version_string[0])
            if proxy_class:
                return self._construct_proxy(config, proxy_class, endpoint_override)
            else:
                warnings.warn(
                    f"The configured version {version_string} for service {self.service_type} "
                    "is not known or supported. The resulting Proxy object will only have direct "
                    "passthrough REST capabilities.",
                    category=os_warnings.UnsupportedServiceVersion)
        elif endpoint_override and self.supported_versions:
            temp_adapter = config.get_session_client(self.service_type)
            api_version = temp_adapter.get_endpoint_data().api_version
            proxy_class = self.supported_versions.get(str(api_version[0]))
            if proxy_class:
                return self._construct_proxy(config, proxy_class, endpoint_override)
            else:
                warnings.warn(
                    f"Service {self.service_type} has an endpoint override set, "
                    f"but the version discovered ({api_version}) is not supported. "
                    "The resulting Proxy object will only have direct passthrough REST capabilities.",
                    category=os_warnings.UnsupportedServiceVersion)

    def _construct_proxy(self, config, proxy_class, endpoint_override):
        proxy_obj = config.get_session_client(
            self.service_type,
            constructor=proxy_class,
        )
        proxy_obj.endpoint_override = endpoint_override
        proxy_obj.additional_headers = {'Content-Type': 'application/json'}
        return proxy_obj

    def _handle_discovery(self, proxy_obj, config):
        if getattr(proxy_obj, 'skip_discovery', False):
            return proxy_obj

        data = proxy_obj.get_endpoint_data()
        if data.catalog_url != data.service_url:
            ep_key = f'{self.service_type}_endpoint_override'
            config.config[ep_key] = data.service_url
            proxy_obj = config.get_session_client(self.service_type)
        return proxy_obj

    def _create_discovery_adapter(self, config, version_string):
        version_kwargs = {}
        if version_string:
            version_kwargs['version'] = version_string
        elif self.supported_versions:
            supported_versions = sorted(int(f) for f in self.supported_versions)
            version_kwargs['min_version'] = str(supported_versions[0])
            version_kwargs['max_version'] = f"{supported_versions[-1]}.latest"

        temp_adapter = config.get_session_client(
            self.service_type,
            allow_version_hack=True,
            **version_kwargs
        )
        found_version = temp_adapter.get_api_major_version()
        if found_version is None:
            raise exceptions.NotSupported(
                f"The {self.service_type} service for {self.instance.name}:{config.region_name} "
                "exists but does not have any supported versions."
            )
        proxy_class = self.supported_versions.get(str(found_version[0]))
        if proxy_class:
            version_kwargs['constructor'] = proxy_class
        else:
            warnings.warn(
                f"Service {self.service_type} has no discoverable version. "
                "The resulting Proxy object will only have direct passthrough REST capabilities.",
                category=os_warnings.UnsupportedServiceVersion)
        return config.get_session_client(self.service_type, allow_version_hack=True, **version_kwargs)
