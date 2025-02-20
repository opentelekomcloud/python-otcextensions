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
from otcextensions.sdk.apig.v2 import _proxy
from otcextensions.sdk.apig.v2 import gateway as _gateway
from otcextensions.sdk.apig.v2 import az as _az
from otcextensions.sdk.apig.v2 import apienvironment as _env
from otcextensions.sdk.apig.v2 import apienvironmentvar as _var
from otcextensions.sdk.apig.v2 import apigroup as _api_group
from otcextensions.sdk.apig.v2 import throttling_policy as _tp
from otcextensions.sdk.apig.v2 import api
from openstack.tests.unit import test_proxy_base
from unittest import mock


class TestApiGatewayProxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestApiGatewayProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestApiGatewayFunctions(TestApiGatewayProxy):
    def test_gateways(self):
        self.verify_list(self.proxy.gateways, _gateway.Gateway)

    def test_azs(self):
        self.verify_list(self.proxy.azs, _az.AZ)

    def test_create_gateway(self):
        self.verify_create(self.proxy.create_gateway,
                           _gateway.Gateway)

    def test_delete_gateway(self):
        gateway = _gateway.Gateway()
        self.verify_delete(self.proxy.delete_gateway,
                           _gateway.Gateway,
                           method_args=[gateway],
                           expected_args=[gateway]
                           )

    def test_get_gateway(self):
        self.verify_get(self.proxy.get_gateway,
                        _gateway.Gateway)

    def test_update_gateway(self):
        self.verify_update(self.proxy.update_gateway,
                           _gateway.Gateway)

    def test_get_gateway_progress(self):
        gateway = _gateway.Gateway()
        self._verify(
            'otcextensions.sdk.apig.v2.gateway.'
            'Gateway._get_creation_progress',
            self.proxy.get_gateway_progress,
            method_args=[gateway],
            expected_args=[self.proxy, gateway]
        )

    def test_modify_spec(self):
        gateway = _gateway.Gateway()
        self._verify(
            'otcextensions.sdk.apig.v2.gateway.'
            'Gateway._modify_spec',
            self.proxy.modify_gateway_spec,
            method_args=[gateway],
            expected_args=[self.proxy, gateway]
        )

    def test_get_constraints(self):
        gateway = _gateway.Gateway()
        self._verify(
            'otcextensions.sdk.apig.v2.gateway.'
            'Gateway._get_constraints',
            self.proxy.get_constraints,
            method_args=[gateway],
            expected_args=[self.proxy, gateway]
        )

    def test_enable_public_access(self):
        gateway = _gateway.Gateway()
        self._verify(
            'otcextensions.sdk.apig.v2.gateway.'
            'Gateway._enable_public_access',
            self.proxy.enable_public_access,
            method_args=[gateway],
            expected_args=[self.proxy, gateway]
        )

    def test_update_public_access(self):
        gateway = _gateway.Gateway()
        self._verify(
            'otcextensions.sdk.apig.v2.gateway.'
            'Gateway._update_public_access',
            self.proxy.update_public_access,
            method_args=[gateway],
            expected_args=[self.proxy, gateway]
        )

    def test_disable_public_access(self):
        gateway = _gateway.Gateway()
        self._verify(
            'otcextensions.sdk.apig.v2.gateway.'
            'Gateway._disable_public_access',
            self.proxy.disable_public_access,
            method_args=[gateway],
            expected_args=[self.proxy, gateway]
        )

    def test_bind_eip(self):
        gateway = _gateway.Gateway()
        self.proxy._get_resource = mock.Mock(return_value=gateway)
        self._verify(
            'otcextensions.sdk.apig.v2.gateway.'
            'Gateway._bind_eip',
            self.proxy.bind_eip,
            method_args=[gateway],
            expected_args=[self.proxy, gateway]
        )

    def test_unbind_eip(self):
        gateway = _gateway.Gateway()
        self._verify(
            'otcextensions.sdk.apig.v2.gateway.'
            'Gateway._unbind_eip',
            self.proxy.unbind_eip,
            method_args=[gateway],
            expected_args=[self.proxy, gateway]
        )

    def test_enable_ingress(self):
        gateway = _gateway.Gateway()
        self._verify(
            'otcextensions.sdk.apig.v2.gateway.'
            'Gateway._enable_ingress',
            self.proxy.enable_ingress,
            method_args=[gateway],
            expected_args=[self.proxy, gateway]
        )

    def test_update_ingress(self):
        gateway = _gateway.Gateway()
        self._verify(
            'otcextensions.sdk.apig.v2.gateway.'
            'Gateway._update_ingress',
            self.proxy.update_ingress,
            method_args=[gateway],
            expected_args=[self.proxy, gateway]
        )

    def test_disable_ingress(self):
        gateway = _gateway.Gateway()
        self._verify(
            'otcextensions.sdk.apig.v2.gateway.'
            'Gateway._disable_ingress',
            self.proxy.disable_ingress,
            method_args=[gateway],
            expected_args=[self.proxy, gateway]
        )

    def test_create_env(self):
        gateway = _gateway.Gateway()
        self.verify_create(self.proxy.create_environment,
                           _env.ApiEnvironment,
                           method_args=[gateway],
                           expected_args=[],
                           method_kwargs={},
                           expected_kwargs={'gateway_id': None}
                           )

    def test_update_env(self):
        gateway = _gateway.Gateway()
        env = _env.ApiEnvironment()
        self._verify(
            'otcextensions.sdk.apig.v2.apienvironment.'
            'ApiEnvironment._update_env',
            self.proxy.update_environment,
            method_args=[gateway, env],
            expected_args=[self.proxy, gateway]
        )

    def test_delete_env(self):
        gateway = _gateway.Gateway()
        env = _env.ApiEnvironment()
        self.verify_delete(self.proxy.delete_environment,
                           _env.ApiEnvironment,
                           method_args=[gateway, env],
                           expected_args=[gateway],
                           expected_kwargs={'gateway_id': None}
                           )

    def test_list_envs(self):
        gateway = _gateway.Gateway()
        self.verify_list(self.proxy.environments,
                         _env.ApiEnvironment,
                         method_args=[gateway],
                         expected_args=[],
                         expected_kwargs={'gateway_id': None}
                         )

    def test_create_api_group(self):
        gateway = _gateway.Gateway()
        self.verify_create(self.proxy.create_api_group,
                           _api_group.ApiGroup,
                           method_args=[gateway],
                           expected_args=[],
                           method_kwargs={},
                           expected_kwargs={'gateway_id': None}
                           )

    def test_update_api_group(self):
        gateway = _gateway.Gateway()
        api_group = _api_group.ApiGroup()
        self._verify(
            'otcextensions.sdk.apig.v2.apigroup.'
            'ApiGroup._update_group',
            self.proxy.update_api_group,
            method_args=[gateway, api_group],
            expected_args=[self.proxy],
            expected_kwargs={'gateway': gateway}
        )

    def test_delete_api_group(self):
        gateway = _gateway.Gateway()
        api_group = _api_group.ApiGroup()
        self.verify_delete(self.proxy.delete_api_group,
                           _api_group.ApiGroup,
                           method_args=[gateway, api_group],
                           expected_args=[gateway],
                           method_kwargs={},
                           expected_kwargs={'gateway_id': None}
                           )

    def test_list_api_groups(self):
        gateway = _gateway.Gateway()
        self.verify_list(self.proxy.api_groups,
                         _api_group.ApiGroup,
                         method_args=[gateway],
                         expected_args=[],
                         expected_kwargs={'gateway_id': None}
                         )

    def test_get_api_group(self):
        gateway = _gateway.Gateway()
        api_group = _api_group.ApiGroup()
        self.verify_get(self.proxy.get_api_group,
                        _api_group.ApiGroup,
                        method_args=[gateway, api_group],
                        expected_args=[api_group],
                        expected_kwargs={'gateway_id': None}
                        )

    def test_verify_name(self):
        gateway = _gateway.Gateway()
        self._verify(
            'otcextensions.sdk.apig.v2.apigroup.'
            'ApiGroup._verify_name',
            self.proxy.verify_api_group_name,
            method_args=[gateway],
            expected_args=[self.proxy],
            expected_kwargs={'gateway': gateway}
        )


class TestApiEnvVars(TestApiGatewayProxy):
    def test_environment_variables(self):
        gateway = _gateway.Gateway()
        self.verify_list(
            self.proxy.environment_variables,
            _var.ApiEnvironmentVar,
            method_args=[gateway],
            expected_args=[],
            expected_kwargs={"gateway_id": None}
        )

    def test_create_environment_variable(self):
        gateway = _gateway.Gateway()
        attrs = {
            "variable_name": "address",
            "variable_value": "192.168.1.5",
            "env_id": "env_id",
            "group_id": "group_id"
        }
        self.verify_create(
            self.proxy.create_environment_variable,
            _var.ApiEnvironmentVar,
            method_args=[gateway],
            expected_args=[],
            method_kwargs={**attrs},
            expected_kwargs={**attrs, "gateway_id": None}
        )

    def test_delete_environment_variable(self):
        gateway = _gateway.Gateway()
        var = _var.ApiEnvironmentVar()
        self.verify_delete(
            self.proxy.delete_environment_variable,
            _var.ApiEnvironmentVar,
            method_args=[gateway, var],
            expected_args=[var],
            expected_kwargs={"gateway_id": None}
        )

    def test_get_environment_variable(self):
        gateway = _gateway.Gateway()
        var = _var.ApiEnvironmentVar()
        self.verify_get(
            self.proxy.get_environment_variable,
            _var.ApiEnvironmentVar,
            method_args=[gateway, var],
            expected_args=[var],
            expected_kwargs={"gateway_id": None}
        )

    def test_update_environment_variable(self):
        gateway = _gateway.Gateway()
        var = _var.ApiEnvironmentVar()
        attrs = {
            "variable_value": "192.168.1.5",
        }
        self.verify_update(
            self.proxy.update_environment_variable,
            _var.ApiEnvironmentVar,
            method_args=[gateway, var],
            expected_args=[var],
            method_kwargs={**attrs},
            expected_kwargs={**attrs, "gateway_id": None}
        )


class TestThrottlingPolicy(TestApiGatewayProxy):
    def test_throttling_policies(self):
        gateway = _gateway.Gateway()
        self.verify_list(
            self.proxy.throttling_policies,
            _tp.ThrottlingPolicy,
            method_args=[gateway],
            expected_args=[],
            expected_kwargs={"gateway_id": None}
        )

    def test_create_throttling_policy(self):
        gateway = _gateway.Gateway()
        attrs = {
            "api_call_limits": 100,
            "app_call_limits": 60,
            "enable_adaptive_control": "FALSE",
            "ip_call_limits": 60,
            "name": "throttle_demo",
            "remark": "Total: 800 calls/second;"
                      " user: 500 calls/second;"
                      " app: 300 calls/second;"
                      " IP address: 600 calls/second",
            "time_interval": 1,
            "time_unit": "SECOND",
            "type": 1,
            "user_call_limits": 60
        }
        self.verify_create(
            self.proxy.create_throttling_policy,
            _tp.ThrottlingPolicy,
            method_args=[gateway],
            expected_args=[],
            method_kwargs={**attrs},
            expected_kwargs={**attrs, "gateway_id": None}
        )

    def test_delete_throttling_policy(self):
        gateway = _gateway.Gateway()
        policy = _tp.ThrottlingPolicy()
        self.verify_delete(
            self.proxy.delete_throttling_policy,
            _tp.ThrottlingPolicy,
            method_args=[gateway, policy],
            expected_args=[policy],
            expected_kwargs={"gateway_id": None}
        )

    def test_get_throttling_policy(self):
        gateway = _gateway.Gateway()
        policy = _tp.ThrottlingPolicy()
        self.verify_get(
            self.proxy.get_throttling_policy,
            _tp.ThrottlingPolicy,
            method_args=[gateway, policy],
            expected_args=[policy],
            expected_kwargs={"gateway_id": None}
        )

    def test_update_throttling_policy(self):
        gateway = _gateway.Gateway()
        policy = _tp.ThrottlingPolicy()
        attrs = {
            "time_unit": "SECOND",
            "name": "throttle_demo",
            "api_call_limits": 100,
            "time_interval": 1,
            "remark": "Total: 800 calls/second;"
                      " user: 500 calls/second;"
                      " app: 300 calls/second;"
                      " IP address: 600 calls/second",
        }
        self.verify_update(
            self.proxy.update_throttling_policy,
            _tp.ThrottlingPolicy,
            method_args=[gateway, policy],
            expected_args=[policy],
            method_kwargs={**attrs},
            expected_kwargs={**attrs, "gateway_id": None}
        )


class TestApi(TestApiGatewayProxy):
    def test_apis(self):
        gateway = _gateway.Gateway()
        self.verify_list(
            self.proxy.apis,
            api.Api,
            method_args=[gateway],
            expected_args=[],
            expected_kwargs={"gateway_id": None}
        )

    def test_create_api(self):
        gateway = _gateway.Gateway()
        attrs = {
            "group_id": "id",
            "name": "test_api_001",
            "auth_type": "IAM",
            "backend_type": "HTTP",
            "req_protocol": "HTTP",
            "req_uri": "/test/http",
            "remark": "Mock backend API",
            "type": 2,
            "req_method": "GET",
            "result_normal_sample": "Example success response",
            "result_failure_sample": "Example failure response",
            "tags": ["httpApi"],
            "backend_api": {
                "req_protocol": "HTTP",
                "req_method": "GET",
                "req_uri": "/test/benchmark",
                "timeout": 5000,
                "retry_count": "-1",
                "url_domain": "192.168.189.156:12346"
            },
        }
        self.verify_create(
            self.proxy.create_api,
            api.Api,
            method_args=[gateway],
            expected_args=[],
            method_kwargs={**attrs},
            expected_kwargs={**attrs, "gateway_id": None}
        )

    def test_delete_api(self):
        gateway = _gateway.Gateway()
        a = api.Api()
        self.verify_delete(
            self.proxy.delete_api,
            api.Api,
            method_args=[gateway, a],
            expected_args=[a],
            expected_kwargs={"gateway_id": None}
        )

    def test_get_api(self):
        gateway = _gateway.Gateway()
        a = api.Api()
        self.verify_get(
            self.proxy.get_api,
            api.Api,
            method_args=[gateway, a],
            expected_args=[a],
            expected_kwargs={"gateway_id": None}
        )

    def test_update_api(self):
        gateway = _gateway.Gateway()
        a = api.Api()
        attrs = {
            "group_id": "id",
            "name": "test_api_001",
            "auth_type": "IAM",
            "backend_type": "HTTP",
            "req_protocol": "HTTP",
            "req_uri": "/test/http",
            "remark": "Mock backend API",
            "type": 2,
            "req_method": "GET",
            "result_normal_sample": "Example success response",
            "result_failure_sample": "Example failure response",
            "tags": ["httpApi"],
            "backend_api": {
                "req_protocol": "HTTP",
                "req_method": "GET",
                "req_uri": "/test/benchmark",
                "timeout": 5000,
                "retry_count": "-1",
                "url_domain": "192.168.189.156:12346"
            },
        }
        self.verify_update(
            self.proxy.update_api,
            api.Api,
            method_args=[gateway, a],
            expected_args=[a],
            method_kwargs={**attrs},
            expected_kwargs={**attrs, "gateway_id": None}
        )
