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
from otcextensions.sdk.apig.v2 import apienvironment as _api_environment
from otcextensions.sdk.apig.v2 import apigroup as _api_group


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
        """Update an existing API Gateway.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: The attributes to update on the gateway.

        :returns: Updated instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        """
        return self._update(_gateway.Gateway, gateway, **attrs)

    def delete_gateway(self, gateway, **attrs):
        """Delete specific gateway
        :param gateway: key id or an instance of
        :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`

        :returns: 'None'
        """
        return self._delete(_gateway.Gateway, gateway, **attrs)

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
        """Enable public access for a specific API Gateway.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: Additional attributes to configure public access.

        :returns: Updated instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return gateway._enable_public_access(self, gateway, **attrs)

    def update_public_access(self, gateway, **attrs):
        """Update public access settings for a specific API Gateway.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: The attributes to update public access settings.

        :returns: Updated instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return gateway._update_public_access(self, gateway, **attrs)

    def disable_public_access(self, gateway):
        """Disable public access for a specific API Gateway.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`

        :returns: Updated instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return gateway._disable_public_access(self, gateway)

    def modify_gateway_spec(self, gateway, **attrs):
        """Modify the specifications of a specific API Gateway.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: The attributes to modify the gateway specifications.

        :returns: Updated instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return gateway._modify_spec(self, gateway, **attrs)

    def bind_eip(self, gateway, **attrs):
        """Bind an Elastic IP (EIP) to a specific API Gateway.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: The attributes required for binding the EIP.

        :returns: Updated instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return gateway._bind_eip(self, gateway, **attrs)

    def unbind_eip(self, gateway):
        """Unbind an Elastic IP (EIP) from a specific API Gateway.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`

        :returns: Updated instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return gateway._unbind_eip(self, gateway)

    def azs(self, **attrs):
        """Retrieve availability zones (AZs) for API Gateway service.

        :param attrs: Optional filters for querying availability zones.

        :returns: A list of availability zones.
        :rtype: list of :class:`~otcextensions.sdk.apig.v2.az.AZ`
        """
        return self._list(_az.AZ, paginated=False, **attrs)

    def enable_ingress(self, gateway, **attrs):
        """Enable public inbound access for a specific API Gateway.

        This method binds a public IP to an API Gateway to allow
        public inbound traffic from the internet.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`

        :param attrs: Additional attributes required for enabling public
            inbound access

        :returns: Updated instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`

        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return gateway._enable_ingress(self, gateway, **attrs)

    def update_ingress(self, gateway, **attrs):
        """Update public inbound access bandwidth of a specific API Gateway.

        This method modifies the inbound bandwidth settings for an API Gateway
        that has public access enabled.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`

        :param attrs: Additional attributes required for updating the ingress
            bandwidth

        :returns: Updated instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`

        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return gateway._update_ingress(self, gateway, **attrs)

    def disable_ingress(self, gateway):
        """Disable public inbound access for a specific API Gateway.

        This method removes public inbound access from an API Gateway
        by unbinding the associated public IP.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`

        :returns: Updated instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return gateway._disable_ingress(self, gateway)

    def create_environment(self, gateway, **attrs):
        """Create a new environment for a specific API Gateway.

        This method creates an environment within the given API Gateway
        by associating it with the specified attributes.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: Additional attributes for the environment creation.

        :returns: An instance of
            :class:`~otcextensions.sdk.apig.v2.api_environment.ApiEnvironment`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._create(_api_environment.ApiEnvironment,
                            gateway_id=gateway.id,
                            **attrs)

    def update_environment(self, gateway, environment, **attrs):
        """Update an existing environment for a specific API Gateway.

        This method updates the specified environment within the API Gateway
        by applying the provided attributes.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param environment: The ID of the environment or an instance of
            :class:`~otcextensions.sdk.apig.v2.environment.ApiEnvironment`
        :param attrs: Additional attributes to update the environment.

        :returns: Updated instance of
            :class:`~otcextensions.sdk.apig.v2.environment.ApiEnvironment`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        environment = self._get_resource(_api_environment.ApiEnvironment,
                                         environment)
        return environment._update_env(self, gateway, **attrs)

    def delete_environment(self, gateway, environment, **attrs):
        """Delete an existing environment from a specific API Gateway.

        This method removes the specified environment from the API Gateway.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param environment: The ID of the environment or an instance of
            :class:`~otcextensions.sdk.apig.v2.environment.ApiEnvironment`
        :param attrs: Additional attributes for the delete operation.

        :returns: None
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        environment = self._get_resource(_api_environment.ApiEnvironment,
                                         environment)
        return self._delete(_api_environment.ApiEnvironment,
                            environment,
                            gateway_id=gateway.id,
                            **attrs)

    def environments(self, gateway, **attrs):
        """List all environments for a specific API Gateway.

        This method retrieves a list of environments associated with
        the given API Gateway.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: Additional filters for listing environments.

        :returns: A list of instances of
            :class:`~otcextensions.sdk.apig.v2.environment.ApiEnvironment`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._list(_api_environment.ApiEnvironment,
                          paginated=False,
                          gateway_id=gateway.id,
                          **attrs)

    def create_api_group(self, gateway, **attrs):
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._create(_api_group.ApiGroup,
                            gateway_id=gateway.id,
                            **attrs)

    def update_api_group(self, gateway, api_group, **attrs):
        gateway = self._get_resource(_gateway.Gateway, gateway)
        api_group = self._get_resource(_api_group.ApiGroup, api_group)
        return api_group._update_group(self, gateway=gateway, **attrs)

    def delete_api_group(self, gateway, api_group):
        gateway = self._get_resource(_gateway.Gateway, gateway)
        api_group = self._get_resource(_api_group.ApiGroup, api_group)
        return self._delete(_api_group.ApiGroup,
                            api_group,
                            gateway_id=gateway.id)

    def get_api_group(self, gateway, api_group):
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._get(_api_group.ApiGroup,
                         api_group,
                         gateway_id=gateway.id)

    def api_groups(self, gateway, **attrs):
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._list(_api_group.ApiGroup,
                          paginated=False,
                          gateway_id=gateway.id,
                          **attrs)

    def verify_api_group_name(self, gateway, **attrs):
        gateway = self._get_resource(_gateway.Gateway, gateway)
        api_group = _api_group.ApiGroup(gateway_id=gateway.id)
        return api_group._verify_name(self, gateway=gateway, **attrs)
