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
from otcextensions.sdk.apig.v2 import apienvironmentvar as _api_var
from otcextensions.sdk.apig.v2 import throttling_policy as _tp
from otcextensions.sdk.apig.v2 import api as _api
from otcextensions.sdk.apig.v2 import api_supplements as _supp


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
        """Create a new API group for a specific API Gateway.

        This method creates an API group associated with the given API Gateway.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: Additional attributes for creating the API group.

        :returns: An instance of
            :class:`~otcextensions.sdk.apig.v2.api_group.ApiGroup`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._create(_api_group.ApiGroup,
                            gateway_id=gateway.id,
                            **attrs)

    def update_api_group(self, gateway, api_group, **attrs):
        """Update an existing API group for a specific API Gateway.

        This method updates the attributes of an API group associated with
        the given API Gateway.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param api_group: The ID of the API group or an instance of
            :class:`~otcextensions.sdk.apig.v2.api_group.ApiGroup`
        :param attrs: Additional attributes for updating the API group.

        :returns: The updated instance of
            :class:`~otcextensions.sdk.apig.v2.api_group.ApiGroup`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        api_group = self._get_resource(_api_group.ApiGroup, api_group)
        return api_group._update_group(self, gateway=gateway, **attrs)

    def delete_api_group(self, gateway, api_group, **attrs):
        """Delete an API group from a specific API Gateway.

        This method deletes the specified API group associated with
        the given API Gateway.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param api_group: The ID of the API group or an instance of
            :class:`~otcextensions.sdk.apig.v2.api_group.ApiGroup`
        :param attrs: Additional parameters for deleting the API group.

        :returns: None
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        api_group = self._get_resource(_api_group.ApiGroup, api_group)
        return self._delete(_api_group.ApiGroup,
                            api_group,
                            gateway_id=gateway.id,
                            **attrs)

    def get_api_group(self, gateway, api_group):
        """Retrieve details of a specific API group.

        This method retrieves the details of an API group associated
        with the given API Gateway.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param api_group: The ID of the API group or an instance of
            :class:`~otcextensions.sdk.apig.v2.api_group.ApiGroup`

        :returns: An instance of
            :class:`~otcextensions.sdk.apig.v2.api_group.ApiGroup`
        """
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
        api_group = _api_group.ApiGroup()
        return api_group._verify_name(self, gateway=gateway, **attrs)

    # ======== Environment Variable Methods ========

    def create_environment_variable(self, gateway, **attrs):
        """Create a new environment variable for a specific API Gateway.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: Additional attributes for the environment variable
            creation.

        :returns: An instance of ApiEnvironmentVar
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._create(_api_var.ApiEnvironmentVar,
                            gateway_id=gateway.id,
                            **attrs)

    def update_environment_variable(self, gateway, var, **attrs):
        """Update an existing environment variable for a specific API Gateway.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param var: The ID of the environment var or an instance of
            ApiEnvironmentVar
        :param attrs: Additional attributes to update the environment.

        :returns: Updated instance of ApiEnvironmentVar
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        var = self._get_resource(
            _api_var.ApiEnvironmentVar,
            var)
        return self._update(
            _api_var.ApiEnvironmentVar,
            var,
            gateway_id=gateway.id,
            **attrs
        )

    def delete_environment_variable(self, gateway, var, ignore_missing=False):
        """Delete an existing environment variable from a specific API Gateway.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param var: The ID of the environment or an instance of
            ApiEnvironmentVar

        :returns: None
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        var = self._get_resource(
            _api_var.ApiEnvironmentVar,
            var)
        return self._delete(
            _api_var.ApiEnvironmentVar,
            var,
            gateway_id=gateway.id,
            ignore_missing=ignore_missing
        )

    def environment_variables(self, gateway, **attrs):
        """List all environment vars for a specific API Gateway.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: Additional filters for listing environment vars.

        :returns: A list of instances of ApiEnvironmentVar
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._list(_api_var.ApiEnvironmentVar,
                          paginated=False,
                          gateway_id=gateway.id,
                          **attrs)

    def get_environment_variable(self, gateway, var):
        """Retrieve details of a specific environment variable.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param var: The ID of the variable or an instance of
            ApiEnvironmentVar

        :returns: An instance of ApiEnvironmentVar
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        var = self._get_resource(
            _api_var.ApiEnvironmentVar,
            var
        )
        return self._get(
            _api_var.ApiEnvironmentVar,
            var,
            gateway_id=gateway.id
        )

    # ======== Throttling Policy Methods ========

    def create_throttling_policy(self, gateway, **attrs):
        """Create a new throttling policy for a specific API Gateway.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: Additional attributes for the throttling policy
            creation.

        :returns: An instance of ThrottlingPolicy
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._create(_tp.ThrottlingPolicy,
                            gateway_id=gateway.id,
                            **attrs)

    def update_throttling_policy(self, gateway, policy, **attrs):
        """Update an existing throttling policy for a specific API Gateway.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param tp: The ID of the throttling policy or an instance of
            ThrottlingPolicy
        :param attrs: Additional attributes to update the throttling policy.

        :returns: Updated instance of ThrottlingPolicy
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        policy = self._get_resource(
            _tp.ThrottlingPolicy,
            policy)
        return self._update(
            _tp.ThrottlingPolicy,
            policy,
            gateway_id=gateway.id,
            **attrs
        )

    def delete_throttling_policy(self, gateway, policy, ignore_missing=False):
        """Delete an existing throttling policy from a specific API Gateway.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param policy: The ID of the throttling policy or an instance of
            ThrottlingPolicy

        :returns: None
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        policy = self._get_resource(
            _tp.ThrottlingPolicy,
            policy)
        return self._delete(
            _tp.ThrottlingPolicy,
            policy,
            gateway_id=gateway.id,
            ignore_missing=ignore_missing
        )

    def throttling_policies(self, gateway, **attrs):
        """List all throttling policies for a specific API Gateway.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: Additional filters for listing throttling policies.

        :returns: A list of instances of ThrottlingPolicy
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._list(_tp.ThrottlingPolicy,
                          paginated=False,
                          gateway_id=gateway.id,
                          **attrs)

    def get_throttling_policy(self, gateway, policy):
        """Retrieve details of a specific throttling policy.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param policy: The ID of the throttling policy or an instance of
            ThrottlingPolicy

        :returns: An instance of ThrottlingPolicy
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        policy = self._get_resource(
            _tp.ThrottlingPolicy,
            policy
        )
        return self._get(
            _tp.ThrottlingPolicy,
            policy,
            gateway_id=gateway.id
        )

    # ======== Api Methods ========

    def create_api(self, gateway, **attrs):
        """Create a new API for a specific API Gateway.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: Additional attributes for the Api creation.

        :returns: An instance of Api
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._create(_api.Api,
                            gateway_id=gateway.id,
                            **attrs)

    def update_api(self, gateway, api, **attrs):
        """Update an existing API for a specific API Gateway.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param api: The ID of the Api or an instance of Api
        :param attrs: Additional attributes to update the Api.

        :returns: Updated instance of Api
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        api = self._get_resource(_api.Api, api)
        return self._update(
            _api.Api,
            api,
            gateway_id=gateway.id,
            **attrs
        )

    def delete_api(self, gateway, api, ignore_missing=False):
        """Delete an existing API from a specific API Gateway.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param api: The ID of the Api or an instance of Api

        :returns: None
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        api = self._get_resource(_api.Api, api)
        return self._delete(
            _api.Api,
            api,
            gateway_id=gateway.id,
            ignore_missing=ignore_missing
        )

    def apis(self, gateway, **attrs):
        """List all APIs for a specific API Gateway.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: Additional filters for listing Api.

        :returns: A list of instances of Api
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._list(_api.Api,
                          paginated=False,
                          gateway_id=gateway.id,
                          **attrs)

    def get_api(self, gateway, api):
        """Retrieve details of a specific API.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param api: The ID of the Api or an instance of Api

        :returns: An instance of Api
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        api = self._get_resource(_api.Api, api)
        return self._get(
            _api.Api,
            api,
            gateway_id=gateway.id
        )

    def publish_api(self, gateway, env, api, **attrs):
        """Publish an API.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param api: The ID of the Api or an instance of Api
        :param env: The ID of the Environment or an instance of it
        :param attrs: Additional attributes

        :returns: An instance of PublishApi
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        env = self._get_resource(_api_environment.ApiEnvironment, env)
        api = self._get_resource(_api.Api, api)
        action = self._get_resource(_supp.PublishApi, "")
        return action.publish_api(
            self,
            api_id=api.id,
            env_id=env.id,
            gateway_id=gateway.id,
            **attrs
        )

    def offline_api(self, gateway, env, api, **attrs):
        """Take API offline.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param api: The ID of the Api or an instance of Api
        :param env: The ID of the Environment or an instance of it
        :param attrs: Additional attributes

        :returns: An instance of PublishApi
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        env = self._get_resource(_api_environment.ApiEnvironment, env)
        api = self._get_resource(_api.Api, api)
        action = self._get_resource(_supp.PublishApi, "")
        return action.take_api_offline(
            self,
            api_id=api.id,
            env_id=env.id,
            gateway_id=gateway.id,
            **attrs
        )

    def check_api(self, gateway, **attrs):
        """Verify the API definition.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: Additional attributes

        :returns: An instance of CheckApi
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._create(
            _supp.CheckApi,
            gateway_id=gateway.id,
            **attrs)

    def debug_api(self, gateway, api, **attrs):
        """Debug an API in a specified environment.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param api: The ID of the Api or an instance of Api
        :param attrs: Additional attributes

        :returns: An instance of DebugApi
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        api = self._get_resource(_api.Api, api)
        return self._create(
            _supp.DebugApi,
            gateway_id=gateway.id,
            api_id=api.id,
            **attrs)

    def publish_apis(self, gateway, env, **attrs):
        """Publish an APIs.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param env: The ID of the Environment or an instance of it
        :param attrs: Additional attributes

        :returns: An instance of PublishApis
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        env = self._get_resource(_api_environment.ApiEnvironment, env)
        action = self._get_resource(_supp.PublishApis, "")
        return action.publish_apis(
            self,
            env_id=env.id,
            gateway_id=gateway.id,
            **attrs
        )

    def offline_apis(self, gateway, env, **attrs):
        """Takes offline an APIs.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param env: The ID of the Environment or an instance of it
        :param attrs: Additional attributes

        :returns: An instance of PublishApis
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        env = self._get_resource(_api_environment.ApiEnvironment, env)
        action = self._get_resource(_supp.PublishApis, "")
        return action.take_apis_offline(
            self,
            env_id=env.id,
            gateway_id=gateway.id,
            **attrs
        )

    def api_versions(self, gateway, api):
        """Retrieve the historical versions of an API.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param api: The ID of the Api or an instance of Api

        :returns: An instance of PublishApis
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        api = self._get_resource(_supp.PublishApis, api)
        base_path = f'/apigw/instances/%(gateway_id)s/apis/publish/%(api_id)s'
        return self._list(
            _supp.PublishApis,
            api_id=api.id,
            gateway_id=gateway.id,
            base_path=base_path,
        )

    def switch_version(self, gateway, api, version_id):
        """Switch the version of an API.

        :param version_id: API version ID.
        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param api: The ID of the Api or an instance of Api

        :returns: An instance of PublishApis
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        api = self._get_resource(_supp.PublishApis, api)
        return self._update(
            _supp.PublishApis,
            id=api.id,
            gateway_id=gateway.id,
            version_id=version_id,
        )

    def api_runtime_definitions(self, gateway, api, **query):
        """Retrieve the runtime definition of an API.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param api: The ID of the Api or an instance of Api

        :returns: An instance of RuntimeDefinitionApi
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        api = self._get_resource(_supp.PublishApis, api)
        return self._list(
            _supp.RuntimeDefinitionApi,
            api_id=api.id,
            gateway_id=gateway.id,
            **query
        )

    def api_version_details(self, gateway, version_id):
        """Retrieve the details of specified API version.

        :param version_id: API version.
        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`

        :returns: An instance of RuntimeDefinitionApi
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._list(
            _supp.VersionsApi,
            gateway_id=gateway.id,
            version_id=version_id
        )

    def take_api_version_offline(
            self, gateway, version_id, ignore_missing=False
    ):
        """Remove an effective version of an API.

        :param version_id: API version.
        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`

        :returns: None
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._delete(
            _supp.VersionsApi,
            gateway_id=gateway.id,
            version_id=version_id,
            ignore_missing=ignore_missing
        )
