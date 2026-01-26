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
from otcextensions.sdk.apig.v2 import app as _app
from otcextensions.sdk.apig.v2 import appcode as _app_code
from otcextensions.sdk.apig.v2 import signature as _sign
from otcextensions.sdk.apig.v2 import signature_binding as _sign_bind
from otcextensions.sdk.apig.v2 import throttling_policy_binding as _tpb
from otcextensions.sdk.apig.v2 import throttling_excluded as _tx
from otcextensions.sdk.apig.v2 import gateway_features as _gwf
from otcextensions.sdk.apig.v2 import resource_query as _rq
from otcextensions.sdk.apig.v2 import domain_name as _domain
from otcextensions.sdk.apig.v2 import certificate as _c
from otcextensions.sdk.apig.v2 import api_auth as _auth
from otcextensions.sdk.apig.v2 import acl_policy as _acl
from otcextensions.sdk.apig.v2 import acl_api_binding as _acl_api_binding
from otcextensions.sdk.apig.v2 import custom_authorizer as _custom_auth
from otcextensions.sdk.apig.v2 import export_api as _export_api
from otcextensions.sdk.apig.v2 import vpc_channel as _vpc_channel
from otcextensions.sdk.apig.v2 import backend_server_group as _backend_group
from otcextensions.sdk.apig.v2 import backend_server as _backend_server
from otcextensions.sdk.apig.v2 import api_call as _api_call
from otcextensions.sdk.apig.v2 import metric_data as _metric_data
from otcextensions.sdk.apig.v2 import group_response as _group_response
from otcextensions.sdk.apig.v2 import error_response as _error_response
from otcextensions.sdk.apig.v2 import ssl_certificate as _ssl_certificate
from otcextensions.sdk.apig.v2 import ssl_domain as _ssl_domain
from otcextensions.sdk.apig.v2 import tag as _tag
from otcextensions.sdk.apig.v2 import config as _config
from otcextensions.sdk.apig.v2 import vpc_endpoint as _vpc_endpoint


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

    # ======== Signature Keys Methods ========

    def create_signature(self, gateway, **attrs):
        """Create a new Signature for a specific API Gateway.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: Additional attributes for the Signature creation.

        :returns: An instance of Signature
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._create(_sign.Signature,
                            gateway_id=gateway.id,
                            **attrs)

    def update_signature(self, gateway, sign, **attrs):
        """Update an existing Signature for a specific API Gateway.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param sign: The ID of the Signature or an instance of Signature
        :param attrs: Additional attributes to update the Signature.

        :returns: Updated instance of Signature
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        sign = self._get_resource(_sign.Signature, sign)
        return self._update(
            _sign.Signature,
            sign,
            gateway_id=gateway.id,
            **attrs
        )

    def delete_signature(self, gateway, sign, ignore_missing=False):
        """Delete an existing Signature from a specific API Gateway.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param sign: The ID of the Signature or an instance of Signature

        :returns: None
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        sign = self._get_resource(_sign.Signature, sign)
        return self._delete(
            _sign.Signature,
            sign,
            gateway_id=gateway.id,
            ignore_missing=ignore_missing
        )

    def signatures(self, gateway, **attrs):
        """List all Signatures for a specific API Gateway.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: Additional filters for listing Signature.

        :returns: A list of instances of Signature
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._list(
            _sign.Signature,
            paginated=False,
            gateway_id=gateway.id,
            **attrs
        )

    # ======== Signature Binding Methods ========

    def bind_signature(self, gateway, **attrs):
        """Bind a Signature for a specific API.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: Additional attributes for the Signature bind.

        :returns: An instance of SignatureBind
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._create(
            _sign_bind.SignatureBind,
            gateway_id=gateway.id,
            **attrs)

    def unbind_signature(self, gateway, bind, ignore_missing=False):
        """Unbind a bound Signature from a specific API.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param bind: The ID of the SignatureBind or an instance
            of SignatureBind

        :returns: None
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        bind = self._get_resource(_sign_bind.SignatureBind, bind)
        return self._delete(
            _sign_bind.SignatureBind,
            bind,
            gateway_id=gateway.id,
            ignore_missing=ignore_missing
        )

    def bound_signatures(self, gateway, **query):
        """List all Signatures bound a specific API.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param query: Additional filters for listing SignatureBind.

        :returns: A list of instances of SignatureBind
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        bp = '/apigw/instances/%(gateway_id)s/sign-bindings/binded-signs'
        return self._list(
            _sign_bind.SignatureBind,
            paginated=False,
            gateway_id=gateway.id,
            base_path=bp,
            **query
        )

    def not_bound_apis(self, gateway, **query):
        """List all APIs to which a signature key has not been bound.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param query: Additional filters for listing NotBoundApi.

        :returns: A list of instances of NotBoundApi
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._list(
            _sign_bind.NotBoundApi,
            paginated=False,
            gateway_id=gateway.id,
            **query
        )

    def bound_apis(self, gateway, **query):
        """List all APIs to which a signature key has been bound.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param query: Additional filters for listing BoundApi.

        :returns: A list of instances of BoundApi
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._list(
            _sign_bind.BoundApi,
            paginated=False,
            gateway_id=gateway.id,
            **query
        )

    # ======== Throttling Policy Binding Methods ========

    def bind_throttling_policy(self, gateway, **attrs):
        """Bind a throttling policy to a specific API.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: Additional attributes for the ThrottlingPolicy bind.

        :returns: An instance of ThrottlingPolicyBind
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._create(
            _tpb.ThrottlingPolicyBind,
            gateway_id=gateway.id,
            **attrs)

    def unbind_throttling_policy(self, gateway, bind, ignore_missing=False):
        """Unbind a bound Signature from a specific API.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param bind: The ID of the SignatureBind or an instance
            of ThrottlingPolicyBind

        :returns: None
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        bind = self._get_resource(_tpb.ThrottlingPolicyBind, bind)
        return self._delete(
            _tpb.ThrottlingPolicyBind,
            bind,
            gateway_id=gateway.id,
            ignore_missing=ignore_missing
        )

    def unbind_throttling_policies(self, gateway, throttle_bindings: list):
        """Unbind a bound Signature from a specific API.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param throttle_bindings: The IDs of the request throttling
            policy binding records to be canceled.

        :returns: None
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        bind = self._get_resource(_tpb.ThrottlingPolicyBind, "")
        return bind.unbind_policies(
            self,
            gateway_id=gateway.id,
            throttle_bindings=throttle_bindings
        )

    def bound_throttling_policy_apis(self, gateway, **query):
        """List all APIs to which a specified request
            throttling policy has been bound.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param query: Additional filters for listing ThrottlingPolicyBind.

        :returns: A list of instances of ThrottlingPolicyBind
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        bp = '/apigw/instances/%(gateway_id)s/throttle-bindings/binded-apis'
        return self._list(
            _tpb.ThrottlingPolicyBind,
            paginated=False,
            gateway_id=gateway.id,
            base_path=bp,
            **query
        )

    def not_bound_throttling_policy_apis(self, gateway, **query):
        """List all APIs to which a request throttling
            policy has not been bound.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param query: Additional filters for listing NotBoundApi.

        :returns: A list of instances of NotBoundApi
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._list(
            _tpb.NotBoundApi,
            paginated=False,
            gateway_id=gateway.id,
            **query
        )

    def bound_throttling_policies(self, gateway, **query):
        """List all throttling policies that have been bound to an API.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param query: Additional filters for listing BoundApi.

        :returns: A list of instances of BoundThrottles
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._list(
            _tpb.BoundThrottles,
            paginated=False,
            gateway_id=gateway.id,
            **query
        )

    # ======== Throttling Policy Methods ========

    def create_throttling_excluded_policy(self, gateway, policy, **attrs):
        """Creating an Excluded Request Throttling Configuration.

        :param policy: The ID of the throttling policy or an instance of
            :class:`~otcextensions.sdk.apig.v2.throttling_policy.
            ThrottlingPolicy`
        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: Additional attributes for the excluded throttling policy
            creation.

        :returns: An instance of ThrottlingExcludedPolicy
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        policy = self._get_resource(_tp.ThrottlingPolicy, policy)
        return self._create(_tx.ThrottlingExcludedPolicy,
                            gateway_id=gateway.id,
                            throttle_id=policy.id,
                            **attrs)

    def update_throttling_excluded_policy(
            self, gateway, policy, exclude, **attrs):
        """Update an Excluded Request Throttling Configuration.

        :param exclude: The ID of the excluded throttling policy or
            an instance of
            :class:`~otcextensions.sdk.apig.v2.throttling_excluded.
            ThrottlingExcludedPolicy`
        :param policy: The ID of the throttling policy or an instance of
            :class:`~otcextensions.sdk.apig.v2.throttling_policy.
            ThrottlingPolicy`
        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: Additional attributes to update the
            excluded throttling policy.

        :returns: Updated instance of ThrottlingExcludedPolicy
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        policy = self._get_resource(_tp.ThrottlingPolicy, policy)
        exclude = self._get_resource(_tx.ThrottlingExcludedPolicy, exclude)
        return self._update(
            _tx.ThrottlingExcludedPolicy,
            exclude,
            gateway_id=gateway.id,
            throttle_id=policy.id,
            **attrs
        )

    def delete_throttling_excluded_policy(
            self, gateway, policy, exclude, ignore_missing=False):
        """Deleting an Excluded Request Throttling Configuration.

        :param exclude: The ID of the excluded throttling policy or
            an instance of
            :class:`~otcextensions.sdk.apig.v2.throttling_excluded.
            ThrottlingExcludedPolicy`
        :param policy: The ID of the throttling policy or an instance of
            :class:`~otcextensions.sdk.apig.v2.throttling_policy.
            ThrottlingPolicy`
        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`

        :returns: None
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        policy = self._get_resource(_tp.ThrottlingPolicy, policy)
        exclude = self._get_resource(_tx.ThrottlingExcludedPolicy, exclude)
        return self._delete(
            _tx.ThrottlingExcludedPolicy,
            exclude,
            gateway_id=gateway.id,
            throttle_id=policy.id,
            ignore_missing=ignore_missing
        )

    def throttling_excluded_policies(self, gateway, policy, **query):
        """List all Excluded Request Throttling Configurations.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param policy: The ID of the throttling policy or an instance of
            :class:`~otcextensions.sdk.apig.v2.throttling_policy.
            ThrottlingPolicy`
        :param query: Additional filters for listing excluded throttling
            policies.

        :returns: A list of instances of ThrottlingExcludedPolicy
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        policy = self._get_resource(_tp.ThrottlingPolicy, policy)
        return self._list(
            _tx.ThrottlingExcludedPolicy,
            paginated=False,
            gateway_id=gateway.id,
            throttle_id=policy.id,
            **query
        )

    # ======== Gateway Features Methods ========

    def configure_gateway_feature(self, gateway, **attrs):
        """Configuring a feature for a Gateway.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: Additional attributes for the GatewayFeatures.

        :returns: An instance of GatewayFeatures
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._create(
            _gwf.GatewayFeatures,
            gateway_id=gateway.id,
            **attrs)

    def gateway_features(self, gateway, **query):
        """List all Gateway Features.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param query:  Additional filters for listing GatewayFeatures.

        :returns: A list of instances of GatewayFeatures
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._list(
            _gwf.GatewayFeatures,
            gateway_id=gateway.id,
            **query)

    def supported_gateway_features(self, gateway, **query):
        """List all the supported features of a Gateway.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param query:  Additional filters for listing GatewayFeatures.

        :returns: A list of instances of features names
        """

        gateway = self._get_resource(_gateway.Gateway, gateway)
        feat = self._get_resource(_gwf.GatewayFeatures, "")
        return feat._supported_features(self, gateway, **query)

    # ======== Resource Query Methods ========

    def get_api_quantities(self, gateway):
        """Get the number of APIs that have been published in the RELEASE
            environment and the number of APIs that have not been
            published in this environment.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`

        :returns: An instance of ApiQuantities
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._get(
            _rq.ApiQuantities,
            gateway_id=gateway.id,
            requires_id=False,
        )

    def get_api_group_quantities(self, gateway):
        """Get the number of API groups.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`

        :returns: An instance of ApiGroupQuantities
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._get(
            _rq.ApiGroupQuantities,
            gateway_id=gateway.id,
            requires_id=False,
        )

    def get_app_quantities(self, gateway):
        """Get the number of apps that have been authorized to access APIs
            and the number of apps that have not been authorized to access
            any APIs.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`

        :returns: An instance of AppQuantities
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._get(
            _rq.AppQuantities,
            gateway_id=gateway.id,
            requires_id=False,
        )

    # ======== Domain Name Methods ========

    def bind_domain_name(self, gateway, group, **attrs):
        """Bind domain name to group.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param group: The ID of the group or an instance of
            :class:`~otcextensions.sdk.apig.v2.apigroup.ApiGroup`
        :param attrs: Additional attributes for the DomainName.

        :returns: An instance of DomainName
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        group = self._get_resource(_api_group.ApiGroup, group)
        return self._create(
            _domain.DomainName,
            gateway_id=gateway.id,
            group_id=group.id,
            **attrs)

    def unbind_domain_name(
            self, gateway, group, domain, ignore_missing=False):
        """Unbind domain name from group.

        :param domain: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.domain_name.DomainName`
        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param group: The ID of the group or an instance of
            :class:`~otcextensions.sdk.apig.v2.apigroup.ApiGroup`

        :returns: None
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        group = self._get_resource(_api_group.ApiGroup, group)
        domain = self._get_resource(_domain.DomainName, domain)
        return self._delete(
            _domain.DomainName,
            domain,
            gateway_id=gateway.id,
            group_id=group.id,
            ignore_missing=ignore_missing
        )

    def update_domain_name_bound(
            self, gateway, group, domain, **attrs):
        """Update a bound of domain name to group.

        :param domain: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.domain_name.DomainName`
        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param group: The ID of the group or an instance of
            :class:`~otcextensions.sdk.apig.v2.apigroup.ApiGroup`
        :param attrs: Additional attributes to update the
            DomainName bind.

        :returns: Updated instance of DomainName
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        group = self._get_resource(_api_group.ApiGroup, group)
        domain = self._get_resource(_domain.DomainName, domain)
        return self._update(
            _domain.DomainName,
            domain,
            gateway_id=gateway.id,
            group_id=group.id,
            **attrs
        )

    def create_certificate_for_domain_name(
            self, gateway, group, domain, **attrs):
        """Add certificate to domain name.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param group: The ID of the group or an instance of
            :class:`~otcextensions.sdk.apig.v2.apigroup.ApiGroup`
        :param domain: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.domain_name.DomainName`
        :param attrs: Additional attributes for the DomainName.

        :returns: An instance of Certificate
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        group = self._get_resource(_api_group.ApiGroup, group)
        domain = self._get_resource(_domain.DomainName, domain)
        return self._create(
            _domain.Certificate,
            gateway_id=gateway.id,
            group_id=group.id,
            domain_id=domain.id,
            **attrs)

    def unbind_certificate_from_domain_name(
            self, gateway, group, domain,
            certificate, ignore_missing=False):
        """Unbind certificate from domain name.

        :param certificate: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.certificate.Certificate`
        :param domain: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.domain_name.DomainName`
        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param group: The ID of the group or an instance of
            :class:`~otcextensions.sdk.apig.v2.apigroup.ApiGroup`
        :param group: The ID of the certificate

        :returns: None
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        group = self._get_resource(_api_group.ApiGroup, group)
        domain = self._get_resource(_domain.DomainName, domain)
        certificate = self._get_resource(_c.Certificate, certificate)
        return self._delete(
            _domain.DomainName,
            domain,
            gateway_id=gateway.id,
            group_id=group.id,
            domain_id=domain.id,
            certificate_id=certificate.id,
            ignore_missing=ignore_missing
        )

    def enable_debug_domain_name(self, gateway, group, domain, enable):
        """Disable or Enable the debugging domain name bound to an API group.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param group: The ID of the group or an instance of
            :class:`~otcextensions.sdk.apig.v2.apigroup.ApiGroup`
        :param domain: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.domain_name.DomainName`
        :param enable: Specifies whether the debugging domain name
            is accessible. Options: true and false.

        :returns: An instance of DomainDebug
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        group = self._get_resource(_api_group.ApiGroup, group)
        domain = self._get_resource(_domain.DomainName, domain)
        return self._update(
            _domain.DomainDebug,
            gateway_id=gateway.id,
            group_id=group.id,
            domain_id=domain.id,
            sl_domain_access_enabled=enable)

    def get_bound_certificate(self, gateway, group, domain, certificate):
        """Get the details of the certificate bound to a domain name.

        :param certificate: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.certificate.Certificate`
        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param group: The ID of the group or an instance of
            :class:`~otcextensions.sdk.apig.v2.apigroup.ApiGroup`
        :param domain: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.domain_name.DomainName`

        :returns: An instance of Certificate
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        group = self._get_resource(_api_group.ApiGroup, group)
        domain = self._get_resource(_domain.DomainName, domain)
        certificate = self._get_resource(_c.Certificate, certificate)
        return self._get(
            _domain.Certificate,
            gateway_id=gateway.id,
            group_id=group.id,
            domain_id=domain.id,
            id=certificate.id
        )

    # ======== Certificate Methods ========

    def delete_certificate(self, certificate, ignore_missing=False):
        """Delete an SSL certificate.

        :param certificate: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.certificate.Certificate`

        :returns: None
        """
        certificate = self._get_resource(_c.Certificate, certificate)
        return self._delete(
            _c.Certificate,
            certificate,
            ignore_missing=ignore_missing
        )

    # ======== Credentials Management Methods ========

    def create_app(self, gateway, **attrs):
        """Create a new identity for accessing a specific API Gateway.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: Additional attributes for the App creation.

        :returns: An instance of App
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._create(_app.App,
                            gateway_id=gateway.id,
                            **attrs)

    def get_app(self, gateway, app):
        """Retrieve details of a specific App.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param app: The ID of the App or an instance of App

        :returns: An instance of App
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        app = self._get_resource(_app.App, app)
        return self._get(
            _app.App,
            app,
            gateway_id=gateway.id
        )

    def update_app(self, gateway, app, **attrs):
        """Update an existing App for a specific API Gateway.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param app: The ID of the App or an instance of App
        :param attrs: Additional attributes to update the App.

        :returns: Updated instance of App
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        app = self._get_resource(_app.App, app)
        return self._update(
            _app.App,
            app,
            gateway_id=gateway.id,
            **attrs
        )

    def delete_app(self, gateway, app, ignore_missing=False):
        """Delete an existing identity from a specific API Gateway.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param app: The ID of the App or an instance of App

        :returns: None
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        app = self._get_resource(_app.App, app)
        return self._delete(
            _app.App,
            app,
            gateway_id=gateway.id,
            ignore_missing=ignore_missing
        )

    def apps(self, gateway, **attrs):
        """Retrieve the list of Apps for a specific API Gateway.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`

        :returns: An instance of App
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._list(
            _app.App,
            gateway_id=gateway.id,
            **attrs
        )

    def verify_app(self, gateway, app):
        """Verify if the App exists

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param app: The ID of the App or an instance of App

        :returns: An instance of App
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        app = self._get_resource(_app.App, app)
        return app._verify_app(self, gateway)

    def reset_app_secret(self, gateway, app, **attrs):
        """Reset the App secret

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param app: The ID of the App or an instance of App
        :param attrs: Additional attributes to update the App secret.

        :returns: An instance of App
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        app = self._get_resource(_app.App, app)
        return app._reset_secret(self, gateway, **attrs)

    def get_app_code(self, gateway, app, app_code):
        """Retrieve details of a specific application code.

        This method retrieves the details of an application code associated
        with the given API Gateway and application.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param app: The ID of the application or an instance of
            :class:`~otcextensions.sdk.apig.v2.app.App`
        :param app_code: The ID of the application code or an instance of
            :class:`~otcextensions.sdk.apig.v2.app_code.AppCode`

        :returns: An instance of
            :class:`~otcextensions.sdk.apig.v2.app_code.AppCode`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        app = self._get_resource(_app.App, app)
        app_code = self._get_resource(_app_code.AppCode, app_code)
        return self._get(
            _app_code.AppCode,
            app_code,
            gateway_id=gateway.id,
            app_id=app.id,
        )

    def create_app_code(self, gateway, app, **attrs):
        """Create a new application code for a specific application.

        This method creates an application code associated with
        the given API Gateway and application.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param app: The ID of the application or an instance of
            :class:`~otcextensions.sdk.apig.v2.app.App`
        :param attrs: Additional attributes for creating the application code.

        :returns: An instance of
            :class:`~otcextensions.sdk.apig.v2.app_code.AppCode`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        app = self._get_resource(_app.App, app)
        return self._create(
            _app_code.AppCode,
            gateway_id=gateway.id,
            app_id=app.id,
            **attrs
        )

    def generate_app_code(self, gateway, app, **attrs):
        """Generate a new application code for a specific application.

        This method generates a new application code associated with
        the given API Gateway and application.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param app: The ID of the application or an instance of
            :class:`~otcextensions.sdk.apig.v2.app.App`
        :param attrs: Additional attributes for generating the app code.

        :returns: An instance of
            :class:`~otcextensions.sdk.apig.v2.app_code.AppCode`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        app = self._get_resource(_app.App, app)
        app_code = _app_code.AppCode()
        return app_code._generate_app_code(self, gateway, app, **attrs)

    def app_codes(self, gateway, app, **attrs):
        """List all application codes for a specific application.

        This method retrieves a list of application codes associated with
        the given API Gateway and application.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param app: The ID of the application or an instance of
            :class:`~otcextensions.sdk.apig.v2.app.App`
        :param attrs: Additional filters for listing application codes.

        :returns: A list of instances of
            :class:`~otcextensions.sdk.apig.v2.app_code.AppCode`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        app = self._get_resource(_app.App, app)
        return self._list(
            _app_code.AppCode,
            gateway_id=gateway.id,
            app_id=app.id,
            **attrs
        )

    def delete_app_code(self, gateway, app, app_code, ignore_missing=False):
        """Delete a specific application code.

        This method deletes an application code associated with
        the given API Gateway and application.

        :param gateway: The ID of the gateway or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param app: The ID of the application or an instance of
            :class:`~otcextensions.sdk.apig.v2.app.App`
        :param app_code: The ID of the application code or an instance of
            :class:`~otcextensions.sdk.apig.v2.app_code.AppCode`
        :param ignore_missing: When set to True, no exception will be raised
            if the application code does not exist. Default is False.

        :returns: None
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        app = self._get_resource(_app.App, app)
        app_code = self._get_resource(_app_code.AppCode, app_code)
        return self._delete(
            _app_code.AppCode,
            app_code,
            gateway_id=gateway.id,
            app_id=app.id,
            ignore_missing=ignore_missing
        )

    def quotas(self, gateway, app, **attrs):
        """Retrieve quotas associated with a credential.

        This method retrieves the quota details associated with
        the given API Gateway instance and application.

        :param gateway: The ID of the API Gateway instance or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param app: The ID of the application or an instance of
            :class:`~otcextensions.sdk.apig.v2.app.App`
        :param attrs: Additional filters for retrieving quota details.

        :returns: An instance of
            :class:`~otcextensions.sdk.apig.v2.quota.Quota`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        app = self._get_resource(_app.App, app)
        return self._get(
            _app.Quota,
            gateway_id=gateway.id,
            app_id=app.id,
            requires_id=False,
            **attrs
        )
    #
    # def access_controls(self, gateway, app, **attrs):
    #     """Retrieve access control details for a specific application.
    #
    #     :param gateway: The ID of the API Gateway instance or an instance of
    #         :class:`~otcextensions.sdk.apig.v2.instance.Instance`
    #     :param app: The ID of the application or an instance of
    #         :class:`~otcextensions.sdk.apig.v2.app.App`
    #     :param attrs: Additional filters for access control details.
    #
    #     :returns: An instance of
    #         :class:`~otcextensions.sdk.apig.v2.access_control.AccessControl`
    #     """
    #     gateway = self._get_resource(_gateway.Gateway, gateway)
    #     app = self._get_resource(_app.App, app)
    #     return self._get(
    #         _ac.AccessControl,
    #         gateway_id = gateway.id,
    #         app_url_id = app.id,
    #         requires_id=False,
    #         **attrs
    #     )
    #
    # def delete_access_control(self, gateway, app, **attrs):
    #     """Delete access control details for a specific application.
    #
    #     :param gateway: The ID of the API Gateway instance or an instance of
    #         :class:`~otcextensions.sdk.apig.v2.instance.Instance`
    #     :param app: The ID of the application or an instance of
    #         :class:`~otcextensions.sdk.apig.v2.app.App`
    #
    #     :returns: None
    #     """
    #     gateway = self._get_resource(_gateway.Gateway, gateway)
    #     app = self._get_resource(_app.App, app)
    #     access_control = _ac.AccessControl()
    #     return access_control._delete(
    #         self,
    #         gateway = gateway,
    #         app = app,
    #         **attrs
    #     )
    #
    # def configure_access_control(self, gateway, app, **attrs):
    #     """Configure access control details for a specific application.
    #
    #     :param gateway: The ID of the API Gateway instance or an instance of
    #         :class:`~otcextensions.sdk.apig.v2.instance.Instance`
    #     :param app: The ID of the application or an instance of
    #         :class:`~otcextensions.sdk.apig.v2.app.App`
    #     :param attrs: Additional attributes for configuring access control.
    #
    #     :returns: An instance of
    #         :class:`~otcextensions.sdk.apig.v2.access_control.AccessControl`
    #     """
    #     gateway = self._get_resource(_gateway.Gateway, gateway)
    #     app = self._get_resource(_app.App, app)
    #     access_control = _ac.AccessControl()
    #     return access_control._configure(self, gateway, app, **attrs)

    # ======== App Authorization Methods ========

    def list_api_bound_to_app(self, gateway, **attrs):
        """List all APIs authorized (bound) to a specific application.

        This method retrieves a list of APIs that are bound (authorized)
        to the given application within the specified API Gateway instance.

        :param gateway: The ID of the API Gateway instance or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: Additional filters, such as app_id, env_id, or API name.

        :returns: A list of instances of
            :class:`~otcextensions.sdk.apig.v2.auth.ApiAuthInfo`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._list(
            _auth.ApiAuthInfo,
            paginated=False,
            base_path=f'{_auth.ApiAuthInfo.base_path}/binded-apis',
            gateway_id=gateway.id,
            **attrs
        )

    def list_apps_bound_to_api(self, gateway, **attrs):
        """List all applications authorized (bound) to a specific API.

        This method gets a list of applications that are bound (authorized)
        to the given API within the specified API Gateway instance.

        :param gateway: The ID of the API Gateway instance or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: Additional filters, such as api_id or environment ID.

        :returns: A list of instances of
            :class:`~otcextensions.sdk.apig.v2.auth.ApiAuthInfo`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._list(
            _auth.ApiAuthInfo,
            paginated=False,
            base_path=f'{_auth.ApiAuthInfo.base_path}/binded-apps',
            gateway_id=gateway.id,
            **attrs
        )

    def list_api_not_bound_to_app(self, gateway, **attrs):
        """List all APIs not authorized (not bound) to a specific application.

        This method retrieves a list of APIs that are not bound (unauthorized)
        to the given application within the specified API Gateway instance.

        :param gateway: The ID of the API Gateway instance or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: Additional filters, such as app_id or environment ID.

        :returns: A list of instances of
            :class:`~otcextensions.sdk.apig.v2.auth.ApiAuth`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._list(
            _auth.ApiAuth,
            paginated=False,
            base_path=f'{_auth.ApiAuthInfo.base_path}/unbinded-apis',
            gateway_id=gateway.id,
            **attrs
        )

    def create_auth_in_api(self, gateway, **attrs):
        """Authorize one or more applications to access a specific API.

        This method binds applications to the specified API within the given
        API Gateway instance, effectively authorizing them to access the API.

        :param gateway: The ID of the API Gateway instance or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: Attributes required for authorization, including:
            - api_id: ID of the API to authorize.
            - app_ids: List of application IDs to bind to the API.
            - env_id: ID of the environment in which the API is published.

        :returns: An instance of
            :class:`~otcextensions.sdk.apig.v2.auth.ApiAuthInfo`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        auth = _auth.ApiAuthInfo()
        return auth._authorize_apps(
            self,
            gateway_id=gateway.id,
            **attrs
        )

    def delete_auth_from_api(self, gateway, auth_id):
        """Delete an API authorization from an application.

        This method removes the authorization binding between a specific
        API and an application within the given API Gateway instance.

        :param gateway: The ID of the API Gateway instance or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param auth_id: The ID of the authorization binding to be deleted.

        :returns: None
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        auth = _auth.ApiAuthInfo()
        return auth._cancel_auth(
            self,
            gateway_id=gateway.id,
            app_auth_id=auth_id
        )

    # ======== Access Control Policy Methods ========

    def create_acl_policy(self, gateway, **attrs):
        """Create an access control policy.

        :param gateway: The ID of the API Gateway instance or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: Attributes required to create the ACL policy

        :returns: An instance of
            :class:`~otcextensions.sdk.apig.v2.acl_policy.AclPolicy`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._create(
            _acl.AclPolicy,
            gateway_id=gateway.id,
            **attrs
        )

    def update_acl_policy(self, gateway, acl_policy, **attrs):
        """Update an existing access control policy.

        This method updates an existing ACL (access control list) policy
        in the specified API Gateway instance.

        :param gateway: The ID of the API Gateway instance or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param acl_policy: The ID of the ACL policy or an instance of
            :class:`~otcextensions.sdk.apig.v2.acl_policy.AclPolicy`
        :param attrs: Attributes to update

        :returns: The updated instance of
            :class:`~otcextensions.sdk.apig.v2.acl_policy.AclPolicy`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        acl_policy = self._get_resource(_acl.AclPolicy, acl_policy)
        return self._update(
            _acl.AclPolicy,
            acl_policy,
            gateway_id=gateway.id,
            **attrs
        )

    def delete_acl_policy(self, gateway, acl_policy, ignore_missing=True,
                          **attrs):
        """Delete an access control policy.

        This method deletes an existing access control (ACL) policy from
        the specified API Gateway instance.

        :param gateway: The ID of the API Gateway instance or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param acl_policy: The ID of the ACL policy or an instance of
            :class:`~otcextensions.sdk.apig.v2.acl_policy.AclPolicy`
        :param ignore_missing: If True, no exception is raised when the ACL
            policy does not exist
        :param attrs: Additional attributes for the delete operation

        :returns: None
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        acl_policy = self._get_resource(_acl.AclPolicy, acl_policy)
        return self._delete(
            _acl.AclPolicy,
            acl_policy,
            gateway_id=gateway.id,
            ignore_missing=ignore_missing,
            **attrs
        )

    def delete_acl_policies(self, gateway, **attrs):
        """Delete multiple access control policies in batch.

        This method deletes multiple ACL (access control list) policies at once
        within the specified API Gateway instance.

        :param gateway: The ID of the API Gateway instance or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: Attributes for batch deletion

        :returns: A response indicating the result of the batch deletion.
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        acl = _acl.AclPolicy()
        return acl._delete_multiple_acls(
            self,
            gateway_id=gateway.id,
            **attrs
        )

    def acl_policies(self, gateway, **attrs):
        """List all access control policies in an API Gateway instance.

        This method retrieves a list of all ACL (access control list) policies
        defined in the specified API Gateway instance.

        :param gateway: The ID of the API Gateway instance or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: Additional filters for listing ACL policies

        :returns: A list of instances of
            :class:`~otcextensions.sdk.apig.v2.acl_policy.AclPolicy`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._list(
            _acl.AclPolicy,
            paginated=False,
            gateway_id=gateway.id,
            **attrs
        )

    def get_acl_policy(self, gateway, acl_policy, **attrs):
        """Retrieve details of a specific access control policy.

        This method retrieves detailed information about an existing ACL
        policy within the specified API Gateway instance.

        :param gateway: The ID of the API Gateway instance or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param acl_policy: The ID of the ACL policy or an instance of
            :class:`~otcextensions.sdk.apig.v2.acl_policy.AclPolicy`
        :param attrs: Additional parameters for retrieving the ACL policy.

        :returns: An instance of
            :class:`~otcextensions.sdk.apig.v2.acl_policy.AclPolicy`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        acl_policy = self._get_resource(_acl.AclPolicy, acl_policy)
        return self._get(
            _acl.AclPolicy,
            acl_policy,
            gateway_id=gateway.id,
            **attrs
        )

    # ======== Binding/Unbinding Access Control Policies Methods ========

    def list_apis_for_acl(self, gateway, **attrs):
        """List all APIs bound to a specific access control policy.

        This method retrieves a list of APIs that are associated with
        the specified ACL policy in the given API Gateway instance.

        :param gateway: The ID of the API Gateway instance or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: Additional filters

        :returns: A list of instances of
            :class:`~otcextensions.sdk.apig.v2.acl_api_binding.ApiForAcl`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._list(
            _acl_api_binding.ApiForAcl,
            paginated=False,
            gateway_id=gateway.id,
            **attrs
        )

    def list_api_not_bound_to_acl(self, gateway, **attrs):
        """List all APIs not bound to a specific access control policy.

        This method retrieves a list of APIs that are not associated with
        the specified ACL policy in the given API Gateway instance.

        :param gateway: The ID of the API Gateway instance or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: Additional filters

        :returns: A list of instances of
            :class:`~otcextensions.sdk.apig.v2.acl_api_binding.UnbindApiForAcl`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._list(
            _acl_api_binding.UnbindApiForAcl,
            paginated=False,
            gateway_id=gateway.id,
            **attrs
        )

    def list_acl_for_api(self, gateway, **attrs):
        """List all access control policies bound to a specific API.

        This method retrieves a list of ACL policies that are associated with
        the specified API in the given API Gateway instance.

        :param gateway: The ID of the API Gateway instance or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: Additional filters

        :returns: A list of instances of
            :class:`~otcextensions.sdk.apig.v2.acl_api_binding.AclForApi`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._list(
            _acl_api_binding.AclForApi,
            paginated=False,
            gateway_id=gateway.id,
            **attrs
        )

    def bind_acl_to_api(self, gateway, **attrs):
        """Bind an access control policy to one or more APIs.

        This method binds an existing ACL policy to one
        or more APIs within the specified API Gateway instance.

        :param gateway: The ID of the API Gateway instance or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: Attributes for the binding

        :returns: An instance of
            :class:`~otcextensions.sdk.apig.v2.acl_api_binding.AclApiBinding`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        acl = _acl_api_binding.AclApiBinding()
        return acl._bind_to_api(
            self,
            gateway_id=gateway.id,
            **attrs
        )

    def unbind_acl(self, gateway, acl, ignore_missing=True):
        """Unbind an access control policy from an API.

        This method removes the binding between an ACL (access control list)
        policy and an API within the specified API Gateway instance.

        :param gateway: The ID of the API Gateway instance or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param acl: The ID of the ACL binding or an instance of
            :class:`~otcextensions.sdk.apig.v2.acl_api_binding.AclApiBinding`
        :param ignore_missing: If True, no exception is raised if the binding
            does not exist

        :returns: None
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        acl = self._get_resource(_acl_api_binding.AclApiBinding, acl)
        return self._delete(
            _acl_api_binding.AclApiBinding,
            acl,
            gateway_id=gateway.id,
            ignore_missing=ignore_missing
        )

    def unbind_acls(self, gateway, **attrs):
        """Unbind multiple access control policies from APIs in batch.

        This method removes bindings between one or more ACL policies
        and APIs within the specified API Gateway instance

        :param gateway: The ID of the API Gateway instance or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: Attributes for the unbinding operation

        :returns: An instance of
            :class:`~otcextensions.sdk.apig.v2.acl_api_binding.
            AclBindingFailure`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        acl = _acl_api_binding.AclBindingFailure()
        return acl._unbind_multiple_acls(
            self,
            gateway_id=gateway.id,
            **attrs
        )

    # ======== Custom Authorizer Methods ========

    def custom_authorizers(self, gateway, **attrs):
        """List all custom authorizers in an API Gateway instance

        This method retrieves a list of custom authorizers configured within
        the specified API Gateway instance. Custom authorizers allow you to
        define your own logic for validating access tokens and identities

        :param gateway: The ID of the API Gateway instance or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: Additional filters for listing custom authorizers,
            such as name or type

        :returns: A list of instances of
            :class:`~otcextensions.sdk.apig.v2.custom_authorizer.
            CustomAuthorizer`
            """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._list(
            _custom_auth.CustomAuthorizer,
            paginated=False,
            gateway_id=gateway.id,
            **attrs
        )

    def get_custom_authorizer(self, gateway, custom_authorizer, **attrs):
        """Retrieve details of a specific custom authorizer

        This method retrieves detailed information about a custom authorizer
        within the specified API Gateway instance

        :param gateway: The ID of the API Gateway instance or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param custom_authorizer: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.custom_authorizer
            CustomAuthorizer`
        :param attrs: Additional parameters for retrieving
            the custom authorizer

        :returns: An instance of
            :class:`~otcextensions.sdk.apig.v2.custom_authorizer.
            CustomAuthorizer`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        custom_authorizer = self._get_resource(_custom_auth.CustomAuthorizer,
                                               custom_authorizer)
        return self._get(
            _custom_auth.CustomAuthorizer,
            custom_authorizer,
            gateway_id=gateway.id,
            **attrs
        )

    def create_custom_authorizer(self, gateway, **attrs):
        """Create a custom authorizer in an API Gateway instance

            This method creates a new custom authorizer within the specified
            API Gateway instance. Custom authorizers enable custom
            authentication and authorization logic for APIs

            :param gateway: The ID of the API Gateway or an instance of
                :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
            :param attrs: Attributes required to create the custom authorizer

            :returns: An instance of
                :class:`~otcextensions.sdk.apig.v2.custom_authorizer.
                CustomAuthorizer`
            """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._create(
            _custom_auth.CustomAuthorizer,
            gateway_id=gateway.id,
            **attrs
        )

    def update_custom_authorizer(self, gateway, custom_authorizer, **attrs):
        """Update a custom authorizer

        This method updates an existing custom authorizer within the specified
        API Gateway instance

        :param gateway: The ID of the API Gateway instance or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param custom_authorizer: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.custom_authorizer.
            CustomAuthorizer`
        :param attrs: Attributes to update

        :returns: The updated instance of
            :class:`~otcextensions.sdk.apig.v2.custom_authorizer.
            CustomAuthorizer`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        custom_authorizer = self._get_resource(_custom_auth.CustomAuthorizer,
                                               custom_authorizer)
        return self._update(
            _custom_auth.CustomAuthorizer,
            custom_authorizer,
            gateway_id=gateway.id,
            **attrs
        )

    def delete_custom_authorizer(self, gateway, custom_authorizer,
                                 ignore_missing=False,
                                 **attrs):
        """Delete a custom authorizer

        This method deletes a custom authorizer from the specified
        API Gateway instance

        :param gateway: The ID of the API Gateway instance or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param custom_authorizer: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.custom_authorizer.
            CustomAuthorizer`
        :param ignore_missing: If True, no exception is raised if
            the authorizer does not exist
        :param attrs: Additional parameters for the delete operation

        :returns: None
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        custom_authorizer = self._get_resource(_custom_auth.CustomAuthorizer,
                                               custom_authorizer)
        return self._delete(
            _custom_auth.CustomAuthorizer,
            custom_authorizer,
            gateway_id=gateway.id,
            ignore_missing=ignore_missing,
            **attrs
        )

    def import_api(self, gateway, **attrs):
        """Import an API definition into API Gateway

        This method imports an API from an OpenAPI/Swagger definition or
        other supported format into the specified API Gateway instance.

        :param gateway: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: Dictionary of parameters required for import.

        :returns: An instance of
            :class:`~otcextensions.sdk.apig.v2.export_import.ImportApi`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        import_api = _export_api.ImportApi()
        return import_api._import_api(
            self,
            gateway_id=gateway.id,
            **attrs
        )

    def export_api(self, gateway, full_path, **attrs):
        """Export an API definition from API Gateway

        This method exports an API definition (e.g. in Swagger/OpenAPI format)
        from the specified API Gateway instance to a file.

        :param gateway: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param full_path: Path where the exported file will be stored
        :param attrs: Optional parameters for export.

        :returns: An instance of
            :class:`~otcextensions.sdk.apig.v2.export_import.ExportApi`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        export_api = _export_api.ExportApi()
        return export_api._export_api(
            self,
            gateway_id=gateway.id,
            full_path=full_path,
            **attrs
        )
    # ======== VPC Channel Methods ========

    def create_vpc_channel(self, gateway, **attrs):
        """Create a VPC channel under the specified API Gateway instance

        This method creates a new VPC channel, which defines how the
        gateway communicates with backend services.

        :param gateway: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: Dictionary of parameters for VPC channel creation.

        :returns: An instance of
            :class:`~otcextensions.sdk.apig.v2.vpc_channel.VpcChannel`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._create(
            _vpc_channel.VpcChannel,
            gateway_id=gateway.id,
            **attrs
        )

    def update_vpc_channel(self, gateway, vpc_channel, **attrs):
        """Update an existing VPC channel

        This method updates the properties of a VPC channel under the
        specified API Gateway instance.

        :param gateway: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param vpc_channel: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.vpc_channel.VpcChannel`
        :param attrs: Dictionary of attributes to update on the VPC channel

        :returns: An updated instance of
            :class:`~otcextensions.sdk.apig.v2.vpc_channel.VpcChannel`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        vpc_channel = self._get_resource(_vpc_channel.VpcChannel, vpc_channel)
        return self._update(
            _vpc_channel.VpcChannel,
            vpc_channel,
            gateway_id=gateway.id,
            **attrs
        )

    def delete_vpc_channel(self, gateway, vpc_channel, ignore_missing=False):
        """Delete a VPC channel

        This method deletes the specified VPC channel from the given
        API Gateway instance.

        :param gateway: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param vpc_channel: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.vpc_channel.VpcChannel`
        :param ignore_missing: When set to True, no exception will be raised
            if the application code does not exist. Default is False.

        :returns: None
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        vpc_channel = self._get_resource(_vpc_channel.VpcChannel, vpc_channel)
        return self._delete(
            _vpc_channel.VpcChannel,
            vpc_channel,
            gateway_id=gateway.id,
            ignore_missing=ignore_missing
        )

    def get_vpc_channel(self, gateway, vpc_channel):
        """Retrieve details of a VPC channel

        This method fetches the details of the specified VPC channel
        under the given API Gateway instance.

        :param gateway: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param vpc_channel: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.vpc_channel.VpcChannel`

        :returns: An instance of
            :class:`~otcextensions.sdk.apig.v2.vpc_channel.VpcChannel`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._get(_vpc_channel.VpcChannel,
                         vpc_channel,
                         gateway_id=gateway.id)

    def vpc_channels(self, gateway, **attrs):
        """List all VPC channels under a gateway

        This method retrieves all VPC channels configured for the specified
        API Gateway instance.

        :param gateway: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: Optional query parameters for filtering the list

        :returns: A generator of
            :class:`~otcextensions.sdk.apig.v2.vpc_channel.VpcChannel`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._list(
            _vpc_channel.VpcChannel,
            gateway_id=gateway.id,
            **attrs
        )

    def modify_vpc_channel_healthcheck(self, gateway, vpc_channel, **attrs):
        """Update the health check configuration of a VPC channel

        This method modifies the health check settings (e.g. path, interval,
        timeout, thresholds) for the specified VPC channel.

        :param gateway: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param vpc_channel: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.vpc_channel.VpcChannel`
        :param attrs: Dictionary of health check configuration parameters.

        :returns: An updated instance of
            :class:`~otcextensions.sdk.apig.v2.vpc_channel.VpcChannel`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        vpc_channel = self._get_resource(_vpc_channel.VpcChannel, vpc_channel)
        return vpc_channel.modify_healthcheck(
            self,
            gateway_id=gateway.id,
            vpc_channel_id=vpc_channel.id,
            **attrs
        )

    def add_or_update_backend_server_group(self, gateway, vpc_channel,
                                           **attrs):
        """Add or update a backend server group for a VPC channel

        This method creates or updates a backend server group within the
        specified VPC channel of an API Gateway instance.

        :param gateway: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param vpc_channel: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.vpc_channel.VpcChannel`
        :param attrs: Dictionary of parameters for creation or update.

        :returns: An instance of
            :class:`~otcextensions.sdk.apig.v2.backend_server_group.
            BackendServerGroup`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        vpc_channel = self._get_resource(_vpc_channel.VpcChannel, vpc_channel)
        member_group = _backend_group.BackendServerGroup()
        return member_group.create_group(
            self,
            gateway_id=gateway.id,
            vpc_channel_id=vpc_channel.id,
            **attrs
        )

    def backend_server_groups(self, gateway, vpc_channel, **attrs):
        """List backend server groups under a VPC channel

        This method retrieves all backend server groups configured within the
        specified VPC channel of an API Gateway instance.

        :param gateway: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param vpc_channel: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.vpc_channel.VpcChannel`
        :param attrs: Optional query parameters for filtering the list

        :returns: A generator of
            :class:`~otcextensions.sdk.apig.v2.backend_server_group.
            BackendServerGroup` instances
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        vpc_channel = self._get_resource(_vpc_channel.VpcChannel, vpc_channel)
        return self._list(
            _backend_group.BackendServerGroup,
            gateway_id=gateway.id,
            vpc_channel_id=vpc_channel.id,
            **attrs
        )

    def get_backend_server_group(self, gateway, vpc_channel, backend_group):
        """Retrieve details of a backend server group

        This method fetches details of the specified backend server group
        under a given VPC channel of an API Gateway instance.

        :param gateway: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param vpc_channel: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.vpc_channel.VpcChannel`
        :param backend_group: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.backend_server_group.
            BackendServerGroup`

        :returns: An instance of
            :class:`~otcextensions.sdk.apig.v2.backend_server_group.
            BackendServerGroup`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        vpc_channel = self._get_resource(_vpc_channel.VpcChannel, vpc_channel)
        backend_group = self._get_resource(_backend_group.BackendServerGroup,
                                           backend_group)
        return self._get(
            _backend_group.BackendServerGroup,
            backend_group.member_group_id,
            gateway_id=gateway.id,
            vpc_channel_id=vpc_channel.id
        )

    def update_backend_server_group(self, gateway, vpc_channel, backend_group,
                                    **attrs):
        """Update a backend server group

        This method updates the specified backend server group under a given
        VPC channel of an API Gateway instance.

        :param gateway: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param vpc_channel: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.vpc_channel.VpcChannel`
        :param backend_group: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.backend_server_group.
            BackendServerGroup`
        :param attrs: Dictionary of attributes to update on the backend group.

        :returns: An updated instance of
            :class:`~otcextensions.sdk.apig.v2.backend_server_group.
            BackendServerGroup`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        vpc_channel = self._get_resource(_vpc_channel.VpcChannel, vpc_channel)
        backend_group = self._get_resource(_backend_group.BackendServerGroup,
                                           backend_group)
        return self._update(
            _backend_group.BackendServerGroup,
            backend_group.member_group_id,
            gateway_id=gateway.id,
            vpc_channel_id=vpc_channel.id,
            **attrs
        )

    def delete_backend_server_group(self, gateway, vpc_channel, backend_group,
                                    ignore_missing=False):
        """Delete a backend server group

        This method deletes the specified backend server group from a VPC
        channel under an API Gateway instance.

        :param gateway: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param vpc_channel: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.vpc_channel.VpcChannel`
        :param backend_group: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.backend_server_group.
            BackendServerGroup`
        :param ignore_missing: When set to True, no exception will be raised
            if the application code does not exist. Default is False.

        :returns: None
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        vpc_channel = self._get_resource(_vpc_channel.VpcChannel, vpc_channel)
        backend_group = self._get_resource(_backend_group.BackendServerGroup,
                                           backend_group)
        self._delete(
            _backend_group.BackendServerGroup,
            backend_group.member_group_id,
            gateway_id=gateway.id,
            vpc_channel_id=vpc_channel.id,
            ignore_missing=ignore_missing
        )

    def add_or_update_backend_servers(self, gateway, vpc_channel, **attrs):
        """Add or update backend server instances

        This method adds or updates backend server instances directly
        under a VPC channel of the specified API Gateway instance.

        :param gateway: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param vpc_channel: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.vpc_channel.VpcChannel`
        :param attrs: Dictionary containing list of members to add or update.

        :returns: A list of
            :class:`~otcextensions.sdk.apig.v2.backend_server.BackendServer`
            instances
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        vpc_channel = self._get_resource(_vpc_channel.VpcChannel, vpc_channel)
        member = _backend_server.BackendServer()
        return member.create_members(
            self,
            gateway_id=gateway.id,
            vpc_channel_id=vpc_channel.id,
            **attrs
        )

    def list_backend_servers(self, gateway, vpc_channel, **attrs):
        """List backend server instances

        This method retrieves all backend server instances configured
        under a specified VPC channel in an API Gateway instance.

        :param gateway: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param vpc_channel: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.vpc_channel.VpcChannel`
        :param attrs: Optional query parameters for filtering

        :returns: A generator of
            :class:`~otcextensions.sdk.apig.v2.backend_server.BackendServer`
            instances
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        vpc_channel = self._get_resource(_vpc_channel.VpcChannel, vpc_channel)
        return self._list(
            _backend_server.BackendServer,
            gateway_id=gateway.id,
            vpc_chan_id=vpc_channel.id,
            **attrs
        )

    def update_backend_server(self, gateway, vpc_channel, **attrs):
        """Update backend server instance(s)

        This method updates one or more backend server instances
        under a specified VPC channel.

        :param gateway: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param vpc_channel: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.vpc_channel.VpcChannel`
        :param attrs: Dictionary with the list of members to update.

        :returns: A list of
            :class:`~otcextensions.sdk.apig.v2.backend_server.BackendServer`
            instances
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        vpc_channel = self._get_resource(_vpc_channel.VpcChannel, vpc_channel)
        member = _backend_server.BackendServer()
        return member.update_members(
            self,
            gateway_id=gateway.id,
            vpc_channel_id=vpc_channel.id,
            **attrs
        )

    def remove_backend_server(self, gateway, vpc_channel, backend_server,
                              ignore_missing=False):
        """Delete a backend server instance

        This method deletes a specific backend server from a VPC channel
        under the specified API Gateway instance.

        :param gateway: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param vpc_channel: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.vpc_channel.VpcChannel`
        :param backend_server: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.backend_server.BackendServer`
        :param ignore_missing: When set to True, no exception will be raised
            if the application code does not exist. Default is False.

        :returns: None
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        vpc_channel = self._get_resource(_vpc_channel.VpcChannel, vpc_channel)
        backend_server = self._get_resource(_backend_server.BackendServer,
                                            backend_server)
        self._delete(
            _backend_server.BackendServer,
            backend_server,
            gateway_id=gateway.id,
            vpc_chan_id=vpc_channel.id,
            ignore_missing=ignore_missing
        )

    def enable_backend_server(self, gateway, vpc_channel, backend_server,
                              **attrs):
        """Enable a backend server instance

        This method enables a specific backend server instance by sending
        a batch-enable request with the server's ID.

        :param gateway: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param vpc_channel: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.vpc_channel.VpcChannel`
        :param backend_server: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.backend_server.BackendServer`
        :param attrs: Optional parameters for the enable operation.

        :returns: None
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        vpc_channel = self._get_resource(_vpc_channel.VpcChannel, vpc_channel)
        backend_server = self._get_resource(_backend_server.BackendServer,
                                            backend_server)
        backend_server.enable_server(
            self,
            gateway_id=gateway.id,
            vpc_chan_id=vpc_channel.id,
            **attrs
        )

    def disable_backend_server(self, gateway, vpc_channel, backend_server,
                               **attrs):
        """Disable a backend server instance

        This method disables a specific backend server instance by sending
        a batch-disable request with the server's ID.

        :param gateway: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param vpc_channel: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.vpc_channel.VpcChannel`
        :param backend_server: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.backend_server.BackendServer`
        :param attrs: Optional parameters for the disable operation.

        :returns: None
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        vpc_channel = self._get_resource(_vpc_channel.VpcChannel, vpc_channel)
        backend_server = self._get_resource(_backend_server.BackendServer,
                                            backend_server)
        backend_server.disable_server(
            self,
            gateway_id=gateway.id,
            vpc_chan_id=vpc_channel.id,
            **attrs
        )

    # ======== Monitoring Information Query Methods ========

    def list_api_calls_for_period(self, gateway, **attrs):
        """List API call statistics for a specified period

        This method retrieves API call statistics for the specified
        API Gateway instance over a defined time period.

        :param gateway: The ID of the API Gateway instance or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: Additional parameters for filtering the results,
            such as start and end time, API ID, etc.

        :returns: A list of instances of
            :class:`~otcextensions.sdk.apig.v2.api_call.ApiCallResult`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        api_call = _api_call.ApiCallResult()
        return api_call.get_api_calls_for_period(
            self,
            gateway_id=gateway.id,
            **attrs
        )

    def list_api_calls_for_group(self, gateway, **attrs):
        """List API call statistics for a specific group

        This method retrieves API call statistics for a specific group
        within the specified API Gateway instance.

        :param gateway: The ID of the API Gateway instance or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: Additional parameters for filtering the results,
            such as group ID, start and end time, etc.

        :returns: A list of instances of
            :class:`~otcextensions.sdk.apig.v2.api_call.ApiCallResult`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        api_call = _api_call.ApiCallResult()
        return api_call.get_api_calls_for_group(
            self,
            gateway_id=gateway.id,
            **attrs
        )

    def list_metric_data(self, gateway, **attrs):
        """List metric data for the API Gateway instance

        This method retrieves metric data for the specified API Gateway
        instance, allowing you to monitor performance and usage statistics.

        :param gateway: The ID of the API Gateway instance or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: Additional parameters for filtering the results,
            such as metric name, time range, etc.

        :returns: A list of instances of
            :class:`~otcextensions.sdk.apig.v2.metric_data.MetricData`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        metric_data = _metric_data.MetricData()
        return metric_data.get_metric_data(
            self,
            gateway_id=gateway.id,
            **attrs
        )

    # ======== Group Response Management Methods ========

    def create_group_response(self, gateway, group, **attrs):
        """Create a custom response for an API group

        This method creates a custom response that can be returned by the
        API Gateway when certain conditions are met (e.g., errors).

        :param gateway: The ID of the API Gateway instance or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param group: The ID of the API group or an instance of
            :class:`~otcextensions.sdk.apig.v2.group.Group`
        :param attrs: Attributes for the custom response

        :returns: An instance of
            :class:`~otcextensions.sdk.apig.v2.group_response.GroupResponse`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        group = self._get_resource(_api_group.ApiGroup, group)
        return self._create(
            _group_response.GroupResponse,
            gateway_id=gateway.id,
            group_id=group.id,
            **attrs
        )

    def get_group_response(self, gateway, group, response):
        """Retrieve a specific group response

        This method fetches details of a specific custom response for an API
        group within the specified API Gateway instance.

        :param gateway: The ID of the API Gateway instance or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param group: The ID of the API group or an instance of
            :class:`~otcextensions.sdk.apig.v2.group.Group`
        :param response: The ID of the group response or an instance of
            :class:`~otcextensions.sdk.apig.v2.group_response.GroupResponse`

        :returns: An instance of
            :class:`~otcextensions.sdk.apig.v2.group_response.GroupResponse`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        group = self._get_resource(_api_group.ApiGroup, group)
        response = self._get_resource(_group_response.GroupResponse, response)
        return self._get(
            _group_response.GroupResponse,
            response.id,
            gateway_id=gateway.id,
            group_id=group.id
        )

    def group_responses(self, gateway, group, **attrs):
        """List all custom responses for an API group
        This method retrieves all custom responses defined for a specific
        API group within the specified API Gateway instance.

        :param gateway: The ID of the API Gateway instance or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param group: The ID of the API group or an instance of
            :class:`~otcextensions.sdk.apig.v2.group.Group`
        :param attrs: Additional parameters for filtering the list,
            such as limit, offset, or specific response attributes

        :returns: A generator of
            :class:`~otcextensions.sdk.apig.v2.group_response.GroupResponse`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        group = self._get_resource(_api_group.ApiGroup, group)
        return self._list(
            _group_response.GroupResponse,
            gateway_id=gateway.id,
            group_id=group.id,
            **attrs
        )

    def update_group_response(self, gateway, group, response, **attrs):
        """Update a custom response for an API group
        This method updates an existing custom response for a specific API
        group within the specified API Gateway instance.

        :param gateway: The ID of the API Gateway instance or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param group: The ID of the API group or an instance of
            :class:`~otcextensions.sdk.apig.v2.group.Group`
        :param response: The ID of the group response or an instance of
            :class:`~otcextensions.sdk.apig.v2.group_response.GroupResponse`
        :param attrs: Attributes to update in the group response

        :returns: The updated instance of
            :class:`~otcextensions.sdk.apig.v2.group_response.GroupResponse`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        group = self._get_resource(_api_group.ApiGroup, group)
        response = self._get_resource(_group_response.GroupResponse, response)
        return self._update(
            _group_response.GroupResponse,
            response.id,
            gateway_id=gateway.id,
            group_id=group.id,
            **attrs
        )

    def delete_group_response(self, gateway, group, response,
                              ignore_missing=False):
        """Delete a custom response for an API group
        This method deletes a specific custom response for an API group
        within the specified API Gateway instance.

        :param gateway: The ID of the API Gateway instance or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param group: The ID of the API group or an instance of
            :class:`~otcextensions.sdk.apig.v2.group.Group`
        :param response: The ID of the group response or an instance of
            :class:`~otcextensions.sdk.apig.v2.group_response.GroupResponse`
        :param ignore_missing: If True, no exception is raised if the
            response does not exist. Default is False.

        :returns: None
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        group = self._get_resource(_api_group.ApiGroup, group)
        response = self._get_resource(_group_response.GroupResponse, response)
        return self._delete(
            _group_response.GroupResponse,
            response.id,
            gateway_id=gateway.id,
            group_id=group.id,
            ignore_missing=ignore_missing
        )

    def get_error_response(self, gateway, group, response, response_type):
        """
        Retrieve a specific error response for an API group
        This method fetches details of a specific error response for an API
        group within the specified API Gateway instance.

        :param gateway: The ID of the API Gateway instance or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param group: The ID of the API group or an instance of
            :class:`~otcextensions.sdk.apig.v2.group.Group`
        :param response: The ID of the group response or an instance of
            :class:`~otcextensions.sdk.apig.v2.group_response.GroupResponse`
        :param response_type: The type of the error response (e.g., 'default',
            'unauthorized', 'not_found', etc.)

        :returns: An instance of
            :class:`~otcextensions.sdk.apig.v2.error_response.ErrorResponse`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        group = self._get_resource(_api_group.ApiGroup, group)
        response = self._get_resource(_group_response.GroupResponse, response)
        error_response = _error_response.ErrorResponse()
        return error_response._get(
            self,
            gateway_id=gateway.id,
            group_id=group.id,
            response_id=response.id,
            response_type=response_type
        )

    def update_error_response(self, gateway, group, response, response_type,
                              **attrs):
        """Update a custom error response for an API group
        This method updates an existing custom error response for a specific
        API group within the specified API Gateway instance.

        :param gateway: The ID of the API Gateway instance or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param group: The ID of the API group or an instance of
            :class:`~otcextensions.sdk.apig.v2.group.Group`
        :param response: The ID of the group response or an instance of
            :class:`~otcextensions.sdk.apig.v2.group_response.GroupResponse`
        :param response_type: The type of the error response (e.g., 'default',
            'unauthorized', 'not_found', etc.)
        :param attrs: Attributes to update in the error response

        :returns: The updated instance of
            :class:`~otcextensions.sdk.apig.v2.error_response.ErrorResponse`
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        response = self._get_resource(_group_response.GroupResponse, response)
        group = self._get_resource(_api_group.ApiGroup, group)
        error_response = _error_response.ErrorResponse()
        return error_response._update(
            self,
            gateway_id=gateway.id,
            group_id=group.id,
            response_id=response.id,
            response_type=response_type,
            **attrs
        )

    def delete_error_response(self, gateway, group, response, response_type):
        """
        Delete a custom error response for an API group
        This method deletes a specific custom error response for an API group
        within the specified API Gateway instance.

        :param gateway: The ID of the API Gateway instance or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param group: The ID of the API group or an instance of
            :class:`~otcextensions.sdk.apig.v2.group.Group`
        :param response: The ID of the group response or an instance of
            :class:`~otcextensions.sdk.apig.v2.group_response.GroupResponse`
        :param response_type: The type of the error response (e.g., 'default',
            'unauthorized', 'not_found', etc.)

        :returns: None
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        group = self._get_resource(_api_group.ApiGroup, group)
        response = self._get_resource(_group_response.GroupResponse, response)
        error_response = _error_response.ErrorResponse()
        return error_response._delete(
            self,
            gateway_id=gateway.id,
            group_id=group.id,
            response_id=response.id,
            response_type=response_type,
        )

    # ======== Tag Management Methods ========
    def tags(self, gateway):
        """List all tags for an API Gateway instance

        This method retrieves all tags associated with the specified API
        Gateway instance.

        :param gateway: The ID of the API Gateway instance or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`

        :returns: A generator of
            :class:`~otcextensions.sdk.apig.v2.tag.Tag` instances
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._list(
            _tag.Tag,
            gateway_id=gateway.id
        )

    # ======== SSL Certificate Management Methods ========

    def create_ssl_certificate(self, **attrs):
        """Create a new SSL certificate
        This method creates a new SSL certificate for the specified API
        Gateway instance.

        :param attrs: Attributes for the SSL certificate, such as name,
            cert_content, private_key, type, etc.

        :returns: An instance of
            :class:`~otcextensions.sdk.apig.v2.ssl_certificate.SslCertificate`
        """
        return self._create(
            _ssl_certificate.SslCertificate,
            **attrs
        )

    def get_ssl_certificate(self, ssl_certificate):
        """Retrieve details of an SSL certificate

        This method fetches the details of a specific SSL certificate
        associated with the given API Gateway instance.

        :param ssl_certificate: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.ssl_certificate.SslCertificate`

        :returns: An instance of
            :class:`~otcextensions.sdk.apig.v2.ssl_certificate.SslCertificate`
        """
        ssl_certificate = self._get_resource(
            _ssl_certificate.SslCertificate, ssl_certificate
        )
        return self._get(
            _ssl_certificate.SslCertificate,
            ssl_certificate.id,
        )

    def ssl_certificates(self, **attrs):
        """List all SSL certificates

        This method retrieves all SSL certificates associated with the API
        Gateway instance.

        :param attrs: Optional query parameters for filtering the list,
            such as limit, offset, common_name, etc.

        :returns: A generator of
            :class:`~otcextensions.sdk.apig.v2.ssl_certificate.SslCertificate`
        """
        return self._list(
            _ssl_certificate.SslCertificate,
            paginated=False,
            **attrs
        )

    def update_ssl_certificate(self, ssl_certificate, **attrs):
        """Update an existing SSL certificate

        This method updates the specified SSL certificate with new attributes.

        :param ssl_certificate: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.ssl_certificate.SslCertificate`
        :param attrs: Attributes to update in the SSL certificate

        :returns: The updated instance of
            :class:`~otcextensions.sdk.apig.v2.ssl_certificate.SslCertificate`
        """
        ssl_certificate = self._get_resource(
            _ssl_certificate.SslCertificate, ssl_certificate
        )
        return self._update(
            _ssl_certificate.SslCertificate,
            ssl_certificate.id,
            **attrs
        )

    def delete_ssl_certificate(self, ssl_certificate, ignore_missing=False):
        """Delete an SSL certificate

        This method deletes the specified SSL certificate from the API
        Gateway instance.

        :param ssl_certificate: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.ssl_certificate.SslCertificate`
        :param ignore_missing: If True, no exception is raised if the
            certificate does not exist. Default is False.

        :returns: None
        """
        ssl_certificate = self._get_resource(
            _ssl_certificate.SslCertificate, ssl_certificate
        )
        self._delete(
            _ssl_certificate.SslCertificate,
            ssl_certificate.id,
            ignore_missing=ignore_missing
        )

    def bind_domain_to_certificate(self, gateway, group, domain, **attrs):
        """Bind an SSL certificate to a domain

        This method binds the specified SSL certificate to a domain within
        an API Gateway instance.

        :param gateway: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param group: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.group.Group`
        :param domain: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.domain.Domain`

        :returns: None
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        group = self._get_resource(_api_group.ApiGroup, group)
        domain = self._get_resource(_ssl_domain.SslDomain, domain)
        ssl_certificate = _ssl_certificate.SslCertificate()
        return ssl_certificate._bind_domain(
            self,
            gateway_id=gateway.id,
            group_id=group.id,
            domain_id=domain.id,
            **attrs
        )

    def unbind_domain_from_certificate(self, gateway, group, domain, **attrs):
        """Unbind an SSL certificate from a domain

        This method unbinds the specified SSL certificate from a domain
        within an API Gateway instance.

        :param gateway: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param group: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.group.Group`
        :param domain: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.domain.Domain`

        :returns: None
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        group = self._get_resource(_api_group.ApiGroup, group)
        domain = self._get_resource(_ssl_domain.SslDomain, domain)
        ssl_certificate = _ssl_certificate.SslCertificate()
        return ssl_certificate._unbind_domain(
            self,
            gateway_id=gateway.id,
            group_id=group.id,
            domain_id=domain.id,
            **attrs
        )

    def domains_for_certificate(self, ssl_certificate, **attrs):
        """List all domains bound to an SSL certificate

        This method retrieves all domains that are currently bound to the
        specified SSL certificate within an API Gateway instance.

        :param ssl_certificate: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.ssl_certificate.SslCertificate`
        :param attrs: Optional query parameters for filtering the list

        :returns: A generator of
            :class:`~otcextensions.sdk.apig.v2.ssl_domain.SslDomain` instances
        """
        ssl_certificate = self._get_resource(
            _ssl_certificate.SslCertificate, ssl_certificate
        )
        return self._list(
            _ssl_domain.SslDomain,
            certificate_id=ssl_certificate.id,
            **attrs
        )

    def bind_ssl_certificates_for_domain(self, ssl_certificate, **attrs):
        """List all SSL certificates bound to a domain
        This method retrieves all SSL certificates that are currently bound
        to the specified domain within an API Gateway instance.

        :param ssl_certificate: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.ssl_certificate.SslCertificate`
        :param attrs: Optional query parameters for filtering the list

        :returns: None
        """
        ssl_certificate = self._get_resource(
            _ssl_certificate.SslCertificate, ssl_certificate
        )
        domain = _ssl_domain.SslDomain()
        return domain._bind_certificate(
            self,
            certificate_id=ssl_certificate.id,
            **attrs
        )

    def unbind_ssl_certificates_for_domain(self, ssl_certificate, **attrs):
        """Unbind an SSL certificate from a domain
        This method unbinds the specified SSL certificate from a domain
        within an API Gateway instance.

        :param ssl_certificate: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.ssl_certificate.SslCertificate`
        :param attrs: Optional parameters for the unbind operation

        :returns: None
        """
        ssl_certificate = self._get_resource(
            _ssl_certificate.SslCertificate, ssl_certificate
        )
        domain = _ssl_domain.SslDomain()
        return domain._unbind_certificate(
            self,
            certificate_id=ssl_certificate.id,
            **attrs
        )

    # ======== Configuration Management Methods ========

    def configs(self, **attrs):
        """List all configuration items

        This method retrieves all configuration items for the API Gateway
        instance.

        :param attrs: Optional query parameters for filtering the list,
            such as limit, offset, or specific config attributes

        :returns: A generator of
            :class:`~otcextensions.sdk.apig.v2.config.Config` instances
        """
        return self._list(
            _config.Config,
            paginated=False,
            **attrs
        )

    def configs_for_gateway(self, gateway_id, **attrs):
        """Get configuration items for a specific gateway.

        :param gateway_id: The ID of the gateway.
        :param attrs: Additional parameters to be passed to the
                       underlying `Session.get` method.
        :returns: A generator of configuration items.
        """
        base_path = f'/apigw/instances/{gateway_id}/project/configs'
        return self._list(
            _config.Config,
            paginated=False,
            base_path=base_path,
            **attrs,)

    # ======== VPC Endpoint Management Methods ========

    def vpc_endpoints(self, gateway, **attrs):
        """List all VPC endpoints

        This method retrieves all VPC endpoints associated with the specified
        API Gateway instance.

        :param gateway: The ID or an instance of
            :class:`~otcextensions.sdk.apig.v2.gateway.Gateway`
        :param attrs: Optional query parameters for filtering the list,
            such as limit, offset, id, marker_id, status

        :returns: A generator of
            :class:`~otcextensions.sdk.apig.v2.vpc_endpoint.VpcEndpoint`
            instances
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return self._list(
            _vpc_endpoint.VpcEndpoint,
            gateway_id=gateway.id,
            **attrs
        )
