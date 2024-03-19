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
from urllib.parse import urlparse

from openstack import exceptions
from openstack import service_description

from otcextensions.sdk.vpcep.v1 import _proxy


class VpcepService(service_description.ServiceDescription):
    """The VPCEP service."""

    supported_versions = {
        '1': _proxy.Proxy
    }

    def _make_proxy(self, instance):
        """Create a Proxy for the service in question.

        :param instance:
          The `openstack.connection.Connection` we're working with.
        """
        config = instance.config

        # First, check to see if we've got config that matches what we
        # understand in the SDK.
        version_string = '1'
        endpoint_override = config.get_endpoint(self.service_type)
        ep = config.get_service_catalog().url_for(
            service_type=self.service_type,
            region_name=config.region_name)
        _base = urlparse(ep)

        epo = '%(scheme)s://%(base)s' % {
            'scheme': _base.scheme,
            'base': _base.netloc
        }

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
            return proxy_obj
