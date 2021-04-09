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
from urllib.parse import urlparse
import warnings

from openstack import exceptions

from openstack import service_description

from otcextensions.sdk.vlb.v3 import _proxy


class VlbService(service_description.ServiceDescription):
    """The VLB (v3 Enhanced Load Balancer)."""

    supported_versions = {
        '3': _proxy.Proxy,
    }

    def _make_proxy(self, instance):
        """Create a Proxy for the service in question.

        :param instance:
          The `openstack.connection.Connection` we're working with.
        """
        config = instance.config

        # First, check to see if we've got config that matches what we
        # understand in the SDK.
        version_string = '3'  #  config.get_api_version('elbv3') or '3'
        endpoint_override = config.get_endpoint('elbv3')
#        ep = urlparse(config.get_service_catalog().url_for(
#            service_type='elbv3',
#            region_name=config.region_name))
        ep = urlparse('https://elb.eu-nl.otc.t-systems.com')

        epo = '%(schema)s://%(base)s/v3/' % {
            'schema': ep.scheme,
            'base': ep.netloc,
        }
        if version_string == '3':
            epo += '%(project_id)s/'

        if epo and not endpoint_override:
            endpoint_override = epo

        # If the user doesn't give a version in config, but we only support
        # one version, then just use that version.
        if not version_string and len(self.supported_versions) == 1:
            version_string = list(self.supported_versions)[0]

        proxy_obj = None
        if endpoint_override and version_string and self.supported_versions:
            # Both endpoint override and version_string are set, we don't
            # need to do discovery - just trust the user.
            proxy_class = self.supported_versions.get(version_string[0])
            if proxy_class:
                proxy_obj = config.get_session_client(
                    'elbv3',
                    constructor=proxy_class,
                )
                proxy_obj.endpoint_override = endpoint_override
                # proxy_obj.additional_headers = {
                #     'Content-Type': 'application/json'}

            else:
                warnings.warn(
                    "The configured version, {version} for service"
                    " {service_type} is not known or supported by"
                    " openstacksdk. The resulting Proxy object will only"
                    " have direct passthrough REST capabilities.".format(
                        version=version_string,
                        service_type='elbv3'),
                    category=exceptions.UnsupportedServiceVersion)
        elif endpoint_override and self.supported_versions:
            temp_adapter = config.get_session_client(
                'elbv3'
            )
            api_version = temp_adapter.get_endpoint_data().api_version
            proxy_class = self.supported_versions.get(str(api_version[0]))
            if proxy_class:
                proxy_obj = config.get_session_client(
                    'elbv3',
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
                        service_type='elbv3'),
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
                    'elbv3',
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
            'elbv3',
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
                        cloud=instance.name,
                        region_name=instance.config.region_name))
            else:
                raise exceptions.NotSupported(
                    "The {service_type} service for {cloud}:{region_name}"
                    " exists but no version was discoverable.".format(
                        service_type=self.service_type,
                        cloud=instance.name,
                        region_name=instance.config.region_name))
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
            'elbv3',
            allow_version_hack=True,
            **version_kwargs
        )
