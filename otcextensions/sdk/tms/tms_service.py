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
from openstack import service_description

from otcextensions.sdk.tms.v1 import _proxy


class TmsService(service_description.ServiceDescription):
    """The TMS service."""

    supported_versions = {
        '1': _proxy.Proxy
    }

    def _make_proxy(self, conn):
        """Create a Proxy for the tms service.

        :param conn:
          The `openstack.connection.Connection` we're working with.
        """
        config = conn.config
        ep = ''
        region = 'eu-de'
        version_string = config.get_api_version('tms') or '1'
        endpoint_override = config.get_endpoint(self.service_type)

        endpoints = list(conn.identity.endpoints())
        extracted_eps = []
        # Iterate through the endpoints and extract only tms
        for endpoint in endpoints:
            url = endpoint.get("url", "")
            if 'tms' in url:
                extracted_eps.append(url)

        if config.region_name:
            region = config.region_name
        if extracted_eps:
            for url in extracted_eps:
                if region in url:
                    ep = url
        epo = '%(base)s/' % {'base': ep}

        if epo and not endpoint_override:
            endpoint_override = epo

        proxy_obj = None
        if endpoint_override and self.supported_versions:
            proxy_class = self.supported_versions.get(version_string[0])
            if proxy_class:
                proxy_obj = config.get_session_client(
                    self.service_type,
                    constructor=proxy_class,
                )
                proxy_obj.endpoint_override = endpoint_override
                proxy_obj.additional_headers = {
                    'Content-Type': 'application/json'}
            else:
                warnings.warn(
                    "The configured version, {version} for service"
                    " {service_type} is not known or supported by"
                    " openstacksdk. The resulting Proxy object will only"
                    " have direct passthrough REST capabilities.".format(
                        version=version_string,
                        service_type=self.service_type),
                    category=exceptions.UnsupportedServiceVersion)
        elif endpoint_override and self.supported_versions:
            temp_adapter = config.get_session_client(
                self.service_type
            )
            api_version = temp_adapter.get_endpoint_data().api_version
            proxy_class = self.supported_versions.get(str(api_version[0]))
            if proxy_class:
                proxy_obj = config.get_session_client(
                    self.service_type,
                    constructor=proxy_class,
                )
            else:
                warnings.warn(
                    "Service {service_type} has an endpoint override set"
                    " but the version discovered at that endpoint, {version}"
                    " is not supported by openstacksdk. The resulting Proxy"
                    " object will only have direct passthrough REST"
                    " capabilities.".format(
                        version=api_version,
                        service_type=self.service_type),
                    category=exceptions.UnsupportedServiceVersion)

        if proxy_obj:
            if getattr(proxy_obj, 'skip_discovery', False):
                # Some services, like swift, don't have discovery. While
                # keystoneauth will behave correctly and handle such
                # scenarios, it's not super efficient as it involves trying
                # and falling back a few times.
                return proxy_obj

            data = proxy_obj.get_endpoint_data()
            # If we've gotten here with a proxy object it means we have
            # an endpoint_override in place. If the catalog_url and
            # service_url don't match, which can happen if there is a
            # None plugin and auth.endpoint like with standalone ironic,
            # we need to be explicit that this service has an endpoint_override
            # so that subsequent discovery calls don't get made incorrectly.
            if data.catalog_url != data.service_url:
                ep_key = '{service_type}_endpoint_override'.format(
                    service_type=self.service_type)
                config.config[ep_key] = data.service_url
                proxy_obj = config.get_session_client(
                    self.service_type,
                    constructor=proxy_class,
                )
            return proxy_obj

        # Make an adapter to let discovery take over
        version_kwargs = {}
        if version_string:
            version_kwargs['version'] = version_string
        elif self.supported_versions:
            supported_versions = sorted([
                int(f) for f in self.supported_versions])
            version_kwargs['min_version'] = str(supported_versions[0])
            version_kwargs['max_version'] = '{version}.latest'.format(
                version=str(supported_versions[-1]))

        temp_adapter = config.get_session_client(
            self.service_type,
            allow_version_hack=True,
            **version_kwargs
        )
        found_version = temp_adapter.get_api_major_version()
        if found_version is None:
            if version_kwargs:
                raise exceptions.NotSupported(
                    "The {service_type} service for {cloud}:{region_name}"
                    " exists but does not have any supported versions.".format(
                        service_type=self.service_type,
                        cloud=conn.name,
                        region_name=conn.config.region_name))
            else:
                raise exceptions.NotSupported(
                    "The {service_type} service for {cloud}:{region_name}"
                    " exists but no version was discoverable.".format(
                        service_type=self.service_type,
                        cloud=conn.name,
                        region_name=conn.config.region_name))
        proxy_class = self.supported_versions.get(str(found_version[0]))
        if not proxy_class:
            # Maybe openstacksdk is being used for the passthrough
            # REST API proxy layer for an unknown service in the
            # service catalog that also doesn't have any useful
            # version discovery?
            warnings.warn(
                "Service {service_type} has no discoverable version."
                " The resulting Proxy object will only have direct"
                " passthrough REST capabilities.".format(
                    service_type=self.service_type),
                category=exceptions.UnsupportedServiceVersion)
            return temp_adapter
        proxy_class = self.supported_versions.get(str(found_version[0]))
        if proxy_class:
            version_kwargs['constructor'] = proxy_class
        return config.get_session_client(
            self.service_type,
            allow_version_hack=True,
            **version_kwargs
        )