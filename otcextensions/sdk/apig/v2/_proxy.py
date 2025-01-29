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
from openstack import proxy
from openstack import resource

from otcextensions.common.utils import extract_url_parts
from otcextensions.sdk.apig.v2 import gateway as _gateway
from otcextensions.sdk.apig.v2 import az as _az

class Proxy(proxy.Proxy):
    skip_discovery = True

    def _extract_name(self, url, service_type=None, project_id=None):
        return extract_url_parts(url, project_id)

    def gateways(self, **attrs):
        """Query gateways

        :returns: A generator of gateway object of a
            :class:`~otcextensions.sdk.apig.gateway.Gateway`
        """
        return self._list(_gateway.Gateway, paginated=False, **attrs)

    def create_gateway(self, **attrs):
        """Create gateway

        :returns: A gateway object
        :rtype: :class:`~otcextensions.sdk.apig.gateway.Gateway`
        """
        return self._create(_gateway.Gateway, **attrs)

    def wait_for_gateway(self, gateway, status='Running', failures=None,
                         interval=2, wait=960):
        """Wait for specific gateway status
        :param gateway: key id or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param status: Specific status of the gateway.
        :param failures: Specific failure status of the gateway.
        :param interval: Seconds between checking the gateway.
        :param wait: Seconds between checking the gateway.

        %returns: instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        if failures is None:
            failures = ['ERROR']
        return resource.wait_for_status(
            self, gateway, status, failures, interval, wait)

    def get_gateway(self, gateway):
        """Get details of specific gateway
        :param gateway: key id or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`

        :returns: instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        """
        return self._get(_gateway.Gateway, gateway)

    def update_gateway(self, gateway, **attrs):
        return self._update(_gateway.Gateway, gateway, **attrs)

    def delete_gateway(self, gateway):
        """Delete specific gateway
        :param gateway: key id or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`

        :returns: 'None'
        """
        return self._delete(_gateway.Gateway, gateway)

    def get_gateway_progress(self, gateway):
        """Get specific gateway progress
        :param gateway: key id or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`

        %returns: instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return gateway._get_creation_progress(self, gateway)

    def get_constraints(self, gateway):
        """Get gateway constraints

        :param gateway: key id or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`

        %returns: instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return gateway._get_constraints(self, gateway)

    def enable_public_access(self, gateway, **attrs):
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return gateway._enable_public_access(self, gateway, **attrs)

    def update_public_access(self, gateway, **attrs):
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return gateway._update_public_access(self, gateway, **attrs)

    def disable_public_access(self, gateway):
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return gateway._disable_public_access(self, gateway)

    def modify_gateway_spec(self, gateway, **attrs):
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return gateway._modify_spec(self, gateway, **attrs)

    def bind_eip(self, gateway, **attrs):
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return gateway._bind_eip(self, gateway, **attrs)

    def azs(self, **attrs):
        return self._list(_az.AZ, paginated=False, **attrs)

    def enable_ingress(self, gateway, **attrs):
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return gateway._enable_ingress(self, gateway, **attrs)

    def update_ingress(self, gateway, **attrs):
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return gateway._update_ingress(self, gateway, **attrs)

    def disable_ingress(self, gateway):
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return gateway._disable_ingress(self, gateway)

    # modifying specs
    # bind/unbind eip

