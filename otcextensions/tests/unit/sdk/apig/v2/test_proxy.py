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
from otcextensions.sdk.apig.v2 import api_supplements as _as
from otcextensions.sdk.apig.v2 import signature as _sign
from otcextensions.sdk.apig.v2 import signature_binding as _sb
from otcextensions.sdk.apig.v2 import throttling_policy_binding as _tb
from otcextensions.sdk.apig.v2 import throttling_excluded as _tx
from otcextensions.sdk.apig.v2 import gateway_features as _gwf
from otcextensions.sdk.apig.v2 import domain_name
from otcextensions.sdk.apig.v2 import certificate
from otcextensions.sdk.apig.v2 import resource_query as _rq
from otcextensions.sdk.apig.v2 import app as _app
from otcextensions.sdk.apig.v2 import appcode as _appcode
from otcextensions.sdk.apig.v2 import api_auth as _auth
from otcextensions.sdk.apig.v2 import acl_policy as _ac
from otcextensions.sdk.apig.v2 import acl_api_binding as _acl_api
from otcextensions.sdk.apig.v2 import custom_authorizer as _custom_auth
from otcextensions.sdk.apig.v2 import vpc_channel as _vpc
from otcextensions.sdk.apig.v2 import backend_server_group as _vpc_sg
from otcextensions.sdk.apig.v2 import backend_server as _vpc_s
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


class TestApiSupplements(TestApiGatewayProxy):
    def test_online_api(self):
        gateway = _gateway.Gateway()
        environment = _env.ApiEnvironment()
        a = api.Api()
        self._verify(
            'otcextensions.sdk.apig.v2.api_supplements.'
            'PublishApi.publish_api',
            self.proxy.publish_api,
            method_args=[gateway, environment, a],
            expected_args=[self.proxy],
            expected_kwargs={
                "api_id": None,
                "env_id": None,
                "gateway_id": None
            }
        )

    def test_offline_api(self):
        gateway = _gateway.Gateway()
        environment = _env.ApiEnvironment()
        a = api.Api()
        self._verify(
            'otcextensions.sdk.apig.v2.api_supplements.'
            'PublishApi.take_api_offline',
            self.proxy.offline_api,
            method_args=[gateway, environment, a],
            expected_args=[self.proxy],
            expected_kwargs={
                "api_id": None,
                "env_id": None,
                "gateway_id": None
            }
        )

    def test_check_api(self):
        gateway = _gateway.Gateway()
        attrs = {
            "type": "name",
            "name": "test"
        }
        self.verify_create(
            self.proxy.check_api,
            _as.CheckApi,
            method_args=[gateway],
            expected_args=[],
            method_kwargs={**attrs},
            expected_kwargs={
                **attrs,
                "gateway_id": None
            }
        )

    def test_debug_api(self):
        gateway = _gateway.Gateway()
        a = api.Api()
        attrs = {
            "mode": "DEVELOPER",
            "scheme": "HTTP",
            "method": "GET",
            "path": "/test/http"
        }
        self.verify_create(
            self.proxy.debug_api,
            _as.DebugApi,
            method_args=[gateway, a],
            expected_args=[],
            method_kwargs={**attrs},
            expected_kwargs={
                **attrs,
                "api_id": None,
                "gateway_id": None
            }
        )

    def test_online_apis(self):
        gateway = _gateway.Gateway()
        environment = _env.ApiEnvironment()
        self._verify(
            'otcextensions.sdk.apig.v2.api_supplements.'
            'PublishApis.publish_apis',
            self.proxy.publish_apis,
            method_args=[gateway, environment],
            expected_args=[self.proxy],
            expected_kwargs={
                "env_id": None,
                "gateway_id": None
            }
        )

    def test_offline_apis(self):
        gateway = _gateway.Gateway()
        environment = _env.ApiEnvironment()
        self._verify(
            'otcextensions.sdk.apig.v2.api_supplements.'
            'PublishApis.take_apis_offline',
            self.proxy.offline_apis,
            method_args=[gateway, environment],
            expected_args=[self.proxy],
            expected_kwargs={
                "env_id": None,
                "gateway_id": None
            }
        )

    def test_api_versions(self):
        gateway = _gateway.Gateway()
        a = api.Api()
        self.verify_list(
            self.proxy.api_versions,
            _as.PublishApis,
            method_args=[gateway, a],
            expected_args=[],
            expected_kwargs={
                "api_id": a,
                "gateway_id": None
            }
        )

    def test_switch_version(self):
        gateway = _gateway.Gateway()
        a = api.Api()
        version_id = 'id'
        self._verify(
            'openstack.proxy.Proxy._update',
            self.proxy.switch_version,
            # expected_result=_as.PublishApis(),
            method_args=[gateway, a, version_id],
            method_kwargs={},
            expected_args=[_as.PublishApis],
            expected_kwargs={
                "id": a,
                "version_id": 'id',
                "gateway_id": None
            }
        )

    def test_api_runtime_definitions(self):
        gateway = _gateway.Gateway()
        a = api.Api()
        self.verify_list(
            self.proxy.api_runtime_definitions,
            _as.RuntimeDefinitionApi,
            method_args=[gateway, a],
            expected_args=[],
            expected_kwargs={
                "api_id": a,
                "gateway_id": None
            }
        )

    def test_api_version_details(self):
        gateway = _gateway.Gateway()
        version_id = 'id'
        self.verify_list(
            self.proxy.api_version_details,
            _as.VersionsApi,
            method_args=[gateway, version_id],
            expected_args=[],
            expected_kwargs={
                "version_id": 'id',
                "gateway_id": None
            }
        )

    def test_take_api_version_offline(self):
        gateway = _gateway.Gateway()
        version_id = 'id'
        self.verify_delete(
            self.proxy.take_api_version_offline,
            _as.VersionsApi,
            method_args=[gateway, version_id],
            expected_args=[],
            expected_kwargs={
                "version_id": 'id',
                "gateway_id": None
            }
        )


class TestSignature(TestApiGatewayProxy):
    def test_signatures(self):
        gateway = _gateway.Gateway()
        self.verify_list(
            self.proxy.signatures,
            _sign.Signature,
            method_args=[gateway],
            expected_args=[],
            expected_kwargs={"gateway_id": None}
        )

    def test_create_signature(self):
        gateway = _gateway.Gateway()
        attrs = {
            "name": "otce_signature_1",
            "sign_type": "aes",
            "sign_algorithm": "aes-256-cfb",
        }
        self.verify_create(
            self.proxy.create_signature,
            _sign.Signature,
            method_args=[gateway],
            expected_args=[],
            method_kwargs={**attrs},
            expected_kwargs={**attrs, "gateway_id": None}
        )

    def test_delete_signature(self):
        gateway = _gateway.Gateway()
        s = _sign.Signature()
        self.verify_delete(
            self.proxy.delete_signature,
            _sign.Signature,
            method_args=[gateway, s],
            expected_args=[s],
            expected_kwargs={"gateway_id": None}
        )

    def test_update_api(self):
        gateway = _gateway.Gateway()
        s = _sign.Signature()
        attrs = {
            "name": "otce_signature_1",
            "sign_type": "aes",
            "sign_algorithm": "aes-128-cfb",
        }
        self.verify_update(
            self.proxy.update_signature,
            _sign.Signature,
            method_args=[gateway, s],
            expected_args=[s],
            method_kwargs={**attrs},
            expected_kwargs={**attrs, "gateway_id": None}
        )


class TestSignatureBind(TestApiGatewayProxy):
    def test_bound_signatures(self):
        gateway = _gateway.Gateway()
        self.verify_list(
            self.proxy.bound_signatures,
            _sb.SignatureBind,
            method_args=[gateway],
            expected_args=[],
            expected_kwargs={"gateway_id": None}
        )

    def test_not_bound_apis(self):
        gateway = _gateway.Gateway()
        self.verify_list(
            self.proxy.not_bound_apis,
            _sb.NotBoundApi,
            method_args=[gateway],
            expected_args=[],
            expected_kwargs={"gateway_id": None}
        )

    def test_bound_apis(self):
        gateway = _gateway.Gateway()
        self.verify_list(
            self.proxy.bound_apis,
            _sb.BoundApi,
            method_args=[gateway],
            expected_args=[],
            expected_kwargs={"gateway_id": None}
        )

    def test_bind_signature(self):
        gateway = _gateway.Gateway()
        attrs = {
            "name": "otce_signature",
            "sign_type": "aes",
            "sign_algorithm": "aes-256-cfb",
        }
        self.verify_create(
            self.proxy.bind_signature,
            _sb.SignatureBind,
            method_args=[gateway],
            expected_args=[],
            method_kwargs={**attrs},
            expected_kwargs={**attrs, "gateway_id": None}
        )

    def test_unbind_signature(self):
        gateway = _gateway.Gateway()
        s = _sb.SignatureBind()
        self.verify_delete(
            self.proxy.unbind_signature,
            _sb.SignatureBind,
            method_args=[gateway, s],
            expected_args=[s],
            expected_kwargs={"gateway_id": None}
        )


class TestThrottlesBind(TestApiGatewayProxy):
    def test_bound_throttling_policies(self):
        gateway = _gateway.Gateway()
        self.verify_list(
            self.proxy.bound_throttling_policies,
            _tb.BoundThrottles,
            method_args=[gateway],
            expected_args=[],
            expected_kwargs={"gateway_id": None}
        )

    def test_not_bound_throttling_policy_apis(self):
        gateway = _gateway.Gateway()
        self.verify_list(
            self.proxy.not_bound_throttling_policy_apis,
            _tb.NotBoundApi,
            method_args=[gateway],
            expected_args=[],
            expected_kwargs={"gateway_id": None}
        )

    def test_bound_throttling_policy_apis(self):
        gateway = _gateway.Gateway()
        self.verify_list(
            self.proxy.bound_throttling_policy_apis,
            _tb.ThrottlingPolicyBind,
            method_args=[gateway],
            expected_args=[],
            expected_kwargs={"gateway_id": None}
        )

    def test_bind_throttling_policy(self):
        gateway = _gateway.Gateway()
        attrs = {
            "throttle_id": "id",
            "publish_ids": ["publish_id"]
        }
        self.verify_create(
            self.proxy.bind_throttling_policy,
            _tb.ThrottlingPolicyBind,
            method_args=[gateway],
            expected_args=[],
            method_kwargs={**attrs},
            expected_kwargs={**attrs, "gateway_id": None}
        )

    def test_unbind_throttling_policy(self):
        gateway = _gateway.Gateway()
        t = _tb.ThrottlingPolicyBind()
        self.verify_delete(
            self.proxy.unbind_throttling_policy,
            _tb.ThrottlingPolicyBind,
            method_args=[gateway, t],
            expected_args=[t],
            expected_kwargs={"gateway_id": None}
        )

    def test_unbind_throttling_policies(self):
        gateway = _gateway.Gateway()
        self._verify(
            'otcextensions.sdk.apig.v2.throttling_policy_binding.'
            'ThrottlingPolicyBind.unbind_policies',
            self.proxy.unbind_throttling_policies,
            method_args=[gateway, ["t"]],
            expected_args=[self.proxy],
            expected_kwargs={"gateway_id": None, "throttle_bindings": ["t"]}
        )


class TestThrottlingExcludePolicy(TestApiGatewayProxy):
    def test_throttling_excluded_policies(self):
        gateway = _gateway.Gateway()
        policy = _tp.ThrottlingPolicy()
        self.verify_list(
            self.proxy.throttling_excluded_policies,
            _tx.ThrottlingExcludedPolicy,
            method_args=[gateway, policy],
            expected_args=[],
            expected_kwargs={
                "gateway_id": None,
                "throttle_id": None
            }
        )

    def test_create_throttling_excluded_policy(self):
        gateway = _gateway.Gateway()
        policy = _tp.ThrottlingPolicy()
        attrs = {
            "call_limits": 50,
            "object_id": "id",
            "object_type": "USER"
        }
        self.verify_create(
            self.proxy.create_throttling_excluded_policy,
            _tx.ThrottlingExcludedPolicy,
            method_args=[gateway, policy],
            expected_args=[],
            method_kwargs={**attrs},
            expected_kwargs={
                **attrs,
                "gateway_id": None,
                "throttle_id": None
            }
        )

    def test_delete_throttling_excluded_policy(self):
        gateway = _gateway.Gateway()
        policy = _tp.ThrottlingPolicy()
        ex = _tx.ThrottlingExcludedPolicy()
        self.verify_delete(
            self.proxy.delete_throttling_excluded_policy,
            _tx.ThrottlingExcludedPolicy,
            method_args=[gateway, policy, ex],
            expected_args=[ex],
            expected_kwargs={
                "gateway_id": None,
                "throttle_id": None
            }
        )

    def test_update_throttling_excluded_policy(self):
        gateway = _gateway.Gateway()
        policy = _tp.ThrottlingPolicy()
        ex = _tx.ThrottlingExcludedPolicy()
        attrs = {
            "call_limits": 30
        }
        self.verify_update(
            self.proxy.update_throttling_excluded_policy,
            _tx.ThrottlingExcludedPolicy,
            method_args=[gateway, policy, ex],
            expected_args=[ex],
            method_kwargs={**attrs},
            expected_kwargs={
                **attrs,
                "gateway_id": None,
                "throttle_id": None
            }
        )


class TestGwFeatures(TestApiGatewayProxy):
    def test_list_gateway_features(self):
        gateway = _gateway.Gateway()
        self.verify_list(
            self.proxy.gateway_features,
            _gwf.GatewayFeatures,
            method_args=[gateway],
            expected_args=[],
            expected_kwargs={"gateway_id": None}
        )

    def test_configure_gateway_feature(self):
        gateway = _gateway.Gateway()
        attrs = {
            "name": "route",
            "enable": False,
            "config": "{\"user_routes\":[]}",
        }
        self.verify_create(
            self.proxy.configure_gateway_feature,
            _gwf.GatewayFeatures,
            method_args=[gateway],
            expected_args=[],
            method_kwargs={**attrs},
            expected_kwargs={**attrs, "gateway_id": None}
        )

    def test_supported_gateway_features(self):
        gateway = _gateway.Gateway()
        self._verify(
            'otcextensions.sdk.apig.v2.gateway_features.'
            'GatewayFeatures._supported_features',
            self.proxy.supported_gateway_features,
            method_args=[gateway],
            expected_args=[self.proxy, gateway],
            expected_kwargs={}
        )


class TestResourceQuery(TestApiGatewayProxy):
    def test_get_api_quantities(self):
        gateway = _gateway.Gateway()
        self.verify_get(
            self.proxy.get_api_quantities,
            _rq.ApiQuantities,
            method_args=[gateway],
            expected_args=[],
            expected_kwargs={
                'gateway_id': None,
                'requires_id': False
            }
        )

    def test_get_api_group_quantities(self):
        gateway = _gateway.Gateway()
        self.verify_get(
            self.proxy.get_api_group_quantities,
            _rq.ApiGroupQuantities,
            method_args=[gateway],
            expected_args=[],
            expected_kwargs={
                'gateway_id': None,
                'requires_id': False
            }
        )

    def test_get_app_quantities(self):
        gateway = _gateway.Gateway()
        self.verify_get(
            self.proxy.get_app_quantities,
            _rq.AppQuantities,
            method_args=[gateway],
            expected_args=[],
            expected_kwargs={
                'gateway_id': None,
                'requires_id': False
            }
        )


class TestDomain(TestApiGatewayProxy):
    def test_bind_domain_name(self):
        gateway = _gateway.Gateway()
        group = _api_group.ApiGroup()
        attrs = {
            "url_domain": "name"
        }
        self.verify_create(
            self.proxy.bind_domain_name,
            domain_name.DomainName,
            method_args=[gateway, group],
            expected_args=[],
            method_kwargs={**attrs},
            expected_kwargs={
                **attrs,
                "gateway_id": None,
                "group_id": None
            }
        )

    def test_unbind_domain_name(self):
        gateway = _gateway.Gateway()
        group = _api_group.ApiGroup()
        domain = domain_name.DomainName()
        self.verify_delete(
            self.proxy.unbind_domain_name,
            domain_name.DomainName,
            method_args=[gateway, group, domain],
            expected_args=[domain],
            expected_kwargs={
                "gateway_id": None,
                "group_id": None,
                "ignore_missing": True
            }
        )

    def test_update_domain_name_bound(self):
        gateway = _gateway.Gateway()
        group = _api_group.ApiGroup()
        domain = domain_name.DomainName()
        attrs = {
            "min_ssl_version": "TLSv1.2"
        }
        self.verify_update(
            self.proxy.update_domain_name_bound,
            domain_name.DomainName,
            method_args=[gateway, group, domain],
            expected_args=[domain],
            method_kwargs={**attrs},
            expected_kwargs={
                **attrs,
                "gateway_id": None,
                "group_id": None
            }
        )

    def test_create_certificate_for_domain_name(self):
        gateway = _gateway.Gateway()
        group = _api_group.ApiGroup()
        domain = domain_name.DomainName()
        attrs = {
            "name": "test",
            "private_key": "private_key",
            "cert_content": "content"
        }
        self.verify_create(
            self.proxy.create_certificate_for_domain_name,
            domain_name.Certificate,
            method_args=[gateway, group, domain],
            expected_args=[],
            method_kwargs={**attrs},
            expected_kwargs={
                **attrs,
                "gateway_id": None,
                "group_id": None,
                "domain_id": None
            }
        )

    def test_unbind_certificate_from_domain_name(self):
        gateway = _gateway.Gateway()
        group = _api_group.ApiGroup()
        domain = domain_name.DomainName()
        cert = certificate.Certificate()
        self.verify_delete(
            self.proxy.unbind_certificate_from_domain_name,
            domain_name.DomainName,
            method_args=[gateway, group, domain, cert],
            expected_args=[domain],
            expected_kwargs={
                "gateway_id": None,
                "group_id": None,
                "domain_id": None,
                "certificate_id": None,
                "ignore_missing": True
            }
        )

    def test_enable_debug_domain_name(self):
        gateway = _gateway.Gateway()
        group = _api_group.ApiGroup()
        domain = domain_name.DomainName()
        self._verify(
            'openstack.proxy.Proxy._update',
            self.proxy.enable_debug_domain_name,
            method_args=[gateway, group, domain, False],
            expected_args=[domain_name.DomainDebug],
            method_kwargs={},
            expected_kwargs={
                "gateway_id": None,
                "group_id": None,
                "domain_id": None,
                "sl_domain_access_enabled": False
            }
        )

    def test_get_bound_certificate(self):
        gateway = _gateway.Gateway()
        group = _api_group.ApiGroup()
        domain = domain_name.DomainName()
        cert = certificate.Certificate()
        self.verify_get(
            self.proxy.get_bound_certificate,
            domain_name.Certificate,
            method_args=[gateway, group, domain, cert],
            expected_args=[],
            method_kwargs={},
            expected_kwargs={
                "gateway_id": None,
                "group_id": None,
                "domain_id": None,
                "id": None
            }
        )


class TestCertificate(TestApiGatewayProxy):
    def test_delete_certificate(self):
        cert = certificate.Certificate()
        self.verify_delete(
            self.proxy.delete_certificate,
            certificate.Certificate,
            method_args=[cert],
            expected_args=[cert],
            expected_kwargs={
                "ignore_missing": True
            }
        )


class TestApp(TestApiGatewayProxy):
    def test_create_app(self):
        gateway = _gateway.Gateway()
        self.verify_create(self.proxy.create_app,
                           _app.App,
                           method_args=[gateway],
                           expected_args=[],
                           method_kwargs={},
                           expected_kwargs={'gateway_id': None}
                           )

    def test_get_app(self):
        gateway = _gateway.Gateway()
        app = _app.App()
        self.verify_get(self.proxy.get_app,
                        _app.App,
                        method_args=[gateway, app],
                        expected_args=[app],
                        method_kwargs={},
                        expected_kwargs={'gateway_id': None}
                        )

    def test_update_app(self):
        gateway = _gateway.Gateway()
        app = _app.App()
        self.verify_update(self.proxy.update_app,
                           _app.App,
                           method_args=[gateway, app],
                           expected_args=[app],
                           method_kwargs={},
                           expected_kwargs={'gateway_id': None}
                           )

    def test_delete_app(self):
        gateway = _gateway.Gateway()
        app = _app.App()
        self.verify_delete(self.proxy.delete_app,
                           _app.App,
                           method_args=[gateway, app],
                           expected_args=[app],
                           method_kwargs={},
                           expected_kwargs={'gateway_id': None}
                           )

    def test_list_apps(self):
        gateway = _gateway.Gateway()
        self.verify_list(self.proxy.apps,
                         _app.App,
                         method_args=[gateway, ],
                         expected_args=[],
                         method_kwargs={},
                         expected_kwargs={'gateway_id': None}
                         )

    def test_verify_app(self):
        gateway = _gateway.Gateway()
        app = _app.App()
        self._verify(
            'otcextensions.sdk.apig.v2.app.'
            'App._verify_app',
            self.proxy.verify_app,
            method_args=[gateway, app],
            expected_args=[self.proxy, gateway]
        )

    def test_reset_app_secret(self):
        gateway = _gateway.Gateway()
        app = _app.App()
        self._verify(
            'otcextensions.sdk.apig.v2.app.'
            'App._reset_secret',
            self.proxy.reset_app_secret,
            method_args=[gateway, app],
            expected_args=[self.proxy, gateway]
        )


class TestAppCode(TestApiGatewayProxy):
    def test_get_app_code(self):
        gateway = _gateway.Gateway()
        app = _app.App()
        app_code = _appcode.AppCode()
        self.verify_get(self.proxy.get_app_code,
                        _appcode.AppCode,
                        method_args=[gateway, app, app_code],
                        expected_args=[app_code],
                        method_kwargs={},
                        expected_kwargs={'gateway_id': None,
                                         'app_id': None}
                        )

    def test_create_app_code(self):
        gateway = _gateway.Gateway()
        app = _app.App()
        self.verify_create(self.proxy.create_app_code,
                           _appcode.AppCode,
                           method_args=[gateway, app],
                           expected_args=[],
                           method_kwargs={},
                           expected_kwargs={'gateway_id': None,
                                            'app_id': None}
                           )

    def test_generate_app_code(self):
        gateway = _gateway.Gateway()
        app = _app.App()
        self._verify(
            'otcextensions.sdk.apig.v2.appcode.'
            'AppCode._generate_app_code',
            self.proxy.generate_app_code,
            method_args=[gateway, app],
            expected_args=[self.proxy, gateway, app]
        )

    def test_list_app_codes(self):
        gateway = _gateway.Gateway()
        app = _app.App()
        self.verify_list(self.proxy.app_codes,
                         _appcode.AppCode,
                         method_args=[gateway, app],
                         expected_args=[],
                         method_kwargs={},
                         expected_kwargs={'gateway_id': None,
                                          'app_id': None}
                         )

    def test_delete_app_code(self):
        gateway = _gateway.Gateway()
        app = _app.App()
        self.verify_delete(self.proxy.delete_app,
                           _app.App,
                           method_args=[gateway, app],
                           expected_args=[app],
                           method_kwargs={},
                           expected_kwargs={'gateway_id': None}
                           )


class TestQuota(TestApiGatewayProxy):
    def test_quotas(self):
        gateway = _gateway.Gateway()
        app = _app.App()
        self.verify_get(self.proxy.quotas,
                        _app.Quota,
                        method_args=[gateway, app, ],
                        expected_args=[],
                        method_kwargs={},
                        expected_kwargs={'gateway_id': None,
                                         'app_id': None,
                                         'requires_id': False}
                        )


class TestAuth(TestApiGatewayProxy):
    def test_list_api_bound_to_app(self):
        gateway = _gateway.Gateway()
        self.verify_list(self.proxy.list_api_bound_to_app,
                         _auth.ApiAuthInfo,
                         method_args=[gateway],
                         expected_args=[],
                         method_kwargs={},
                         expected_kwargs={'gateway_id': None}
                         )

    def test_list_api_not_bound_to_app(self):
        gateway = _gateway.Gateway()
        self.verify_list(self.proxy.list_apps_bound_to_api,
                         _auth.ApiAuthInfo,
                         method_args=[gateway],
                         expected_args=[],
                         method_kwargs={},
                         expected_kwargs={'gateway_id': None}
                         )

    def test_list_app_bound_to_api(self):
        gateway = _gateway.Gateway()
        self.verify_list(self.proxy.list_api_not_bound_to_app,
                         _auth.ApiAuth,
                         method_args=[gateway],
                         expected_args=[],
                         method_kwargs={},
                         expected_kwargs={'gateway_id': None}
                         )

    def test_create_auth(self):
        gateway = _gateway.Gateway()
        self._verify(
            'otcextensions.sdk.apig.v2.api_auth.'
            'ApiAuthInfo._authorize_apps',
            self.proxy.create_auth_in_api,
            method_args=[gateway],
            expected_args=[self.proxy],
            expected_kwargs={'gateway_id': None}
        )

    def test_delete_auth(self):
        gateway = _gateway.Gateway()
        self._verify(
            'otcextensions.sdk.apig.v2.api_auth.'
            'ApiAuthInfo._cancel_auth',
            self.proxy.delete_auth_from_api,
            method_args=[gateway],
            expected_args=[self.proxy],
            method_kwargs={'auth_id': None},
            expected_kwargs={'app_auth_id': None,
                             'gateway_id': None}
        )


class TestAclPolicy(TestApiGatewayProxy):
    def test_create_acl_policy(self):
        gateway = _gateway.Gateway()
        self.verify_create(self.proxy.create_acl_policy,
                           _ac.AclPolicy,
                           method_args=[gateway],
                           expected_args=[],
                           method_kwargs={},
                           expected_kwargs={'gateway_id': None}
                           )

    def test_update_acl_policy(self):
        gateway = _gateway.Gateway()
        ac = _ac.AclPolicy()
        self.verify_update(self.proxy.update_acl_policy,
                           _ac.AclPolicy,
                           method_args=[gateway, ac],
                           expected_args=[ac],
                           method_kwargs={},
                           expected_kwargs={'gateway_id': None}
                           )

    def test_delete_acl_policy(self):
        gateway = _gateway.Gateway()
        ac = _ac.AclPolicy()
        self.verify_delete(self.proxy.delete_acl_policy,
                           _ac.AclPolicy,
                           method_args=[gateway, ac],
                           expected_args=[ac],
                           method_kwargs={},
                           expected_kwargs={'gateway_id': None}
                           )

    def test_list_acl_policies(self):
        gateway = _gateway.Gateway()
        self.verify_list(self.proxy.acl_policies,
                         _ac.AclPolicy,
                         method_args=[gateway],
                         expected_args=[],
                         method_kwargs={},
                         expected_kwargs={'gateway_id': None}
                         )

    def test_get_acl_policy(self):
        gateway = _gateway.Gateway()
        ac = _ac.AclPolicy()
        self.verify_get(self.proxy.get_acl_policy,
                        _ac.AclPolicy,
                        method_args=[gateway, ac],
                        expected_args=[ac],
                        method_kwargs={},
                        expected_kwargs={'gateway_id': None}
                        )

    def test_delete_acl_policies(self):
        gateway = _gateway.Gateway()
        self._verify(
            'otcextensions.sdk.apig.v2.acl_policy.'
            'AclPolicy._delete_multiple_acls',
            self.proxy.delete_acl_policies,
            method_args=[gateway],
            expected_args=[self.proxy],
            expected_kwargs={'gateway_id': None}
        )


class TestAclPolicyBinding(TestApiGatewayProxy):
    def test_list_apis_for_acl(self):
        gateway = _gateway.Gateway()
        self.verify_list(self.proxy.list_apis_for_acl,
                         _acl_api.ApiForAcl,
                         method_args=[gateway],
                         expected_args=[],
                         method_kwargs={},
                         expected_kwargs={'gateway_id': None}
                         )

    def test_list_api_not_bound_to_acl(self):
        gateway = _gateway.Gateway()
        self.verify_list(self.proxy.list_api_not_bound_to_acl,
                         _acl_api.UnbindApiForAcl,
                         method_args=[gateway],
                         expected_args=[],
                         method_kwargs={},
                         expected_kwargs={'gateway_id': None}
                         )

    def test_list_acl_for_api(self):
        gateway = _gateway.Gateway()
        self.verify_list(self.proxy.list_acl_for_api,
                         _acl_api.AclForApi,
                         method_args=[gateway],
                         expected_args=[],
                         method_kwargs={},
                         expected_kwargs={'gateway_id': None}
                         )

    def test_bind_acl_to_api(self):
        gateway = _gateway.Gateway()
        self._verify(
            'otcextensions.sdk.apig.v2.acl_api_binding.'
            'AclApiBinding._bind_to_api',
            self.proxy.bind_acl_to_api,
            method_args=[gateway],
            expected_args=[self.proxy],
            expected_kwargs={'gateway_id': None}
        )

    def test_unbind_acl(self):
        gateway = _gateway.Gateway()
        acl = _acl_api.AclApiBinding()
        self.verify_delete(self.proxy.unbind_acl,
                           _acl_api.AclApiBinding,
                           method_args=[gateway, acl],
                           expected_args=[acl],
                           method_kwargs={},
                           expected_kwargs={'gateway_id': None}
                           )

    def test_unbind_acls(self):
        gateway = _gateway.Gateway()
        self._verify(
            'otcextensions.sdk.apig.v2.acl_api_binding.'
            'AclBindingFailure._unbind_multiple_acls',
            self.proxy.unbind_acls,
            method_args=[gateway],
            expected_args=[self.proxy],
            expected_kwargs={'gateway_id': None}
        )


class TestCustomAuthorizer(TestApiGatewayProxy):
    def test_list_custom_authorizers(self):
        gateway = _gateway.Gateway()
        self.verify_list(self.proxy.custom_authorizers,
                         _custom_auth.CustomAuthorizer,
                         method_args=[gateway],
                         expected_args=[],
                         method_kwargs={},
                         expected_kwargs={'gateway_id': None}
                         )

    def test_get_custom_authorizer(self):
        gateway = _gateway.Gateway()
        custom_auth = _custom_auth.CustomAuthorizer()
        self.verify_get(self.proxy.get_custom_authorizer,
                        _custom_auth.CustomAuthorizer,
                        method_args=[gateway, custom_auth],
                        expected_args=[custom_auth],
                        method_kwargs={},
                        expected_kwargs={'gateway_id': None}
                        )

    def test_create_custom_authorizer(self):
        gateway = _gateway.Gateway()
        self.verify_create(self.proxy.create_custom_authorizer,
                           _custom_auth.CustomAuthorizer,
                           method_args=[gateway],
                           expected_args=[],
                           method_kwargs={},
                           expected_kwargs={'gateway_id': None}
                           )

    def test_update_custom_authorizer(self):
        gateway = _gateway.Gateway()
        custom_auth = _custom_auth.CustomAuthorizer()
        self.verify_update(self.proxy.update_custom_authorizer,
                           _custom_auth.CustomAuthorizer,
                           method_args=[gateway, custom_auth],
                           expected_args=[custom_auth],
                           method_kwargs={},
                           expected_kwargs={'gateway_id': None}
                           )

    def test_delete_custom_authorizer(self):
        gateway = _gateway.Gateway()
        custom_auth = _custom_auth.CustomAuthorizer()
        self.verify_delete(self.proxy.delete_custom_authorizer,
                           _custom_auth.CustomAuthorizer,
                           method_args=[gateway, custom_auth],
                           expected_args=[custom_auth],
                           method_kwargs={},
                           expected_kwargs={'gateway_id': None}
                           )


class TestExportApi(TestApiGatewayProxy):
    def test_import_api(self):
        gateway = _gateway.Gateway()
        self._verify(
            'otcextensions.sdk.apig.v2.export_api.'
            'ImportApi._import_api',
            self.proxy.import_api,
            method_args=[gateway],
            expected_args=[self.proxy],
            expected_kwargs={'gateway_id': None}
        )

    def test_export_api(self):
        gateway = _gateway.Gateway()
        full_path = ''
        self._verify(
            'otcextensions.sdk.apig.v2.export_api.'
            'ExportApi._export_api',
            self.proxy.export_api,
            method_args=[gateway, full_path],
            expected_args=[self.proxy],
            expected_kwargs={'gateway_id': None,
                             'full_path': full_path}
        )


class TestVpc(TestApiGatewayProxy):
    def test_create_vpc_channel(self):
        gateway = _gateway.Gateway()
        self.verify_create(self.proxy.create_vpc_channel,
                           _vpc.VpcChannel,
                           method_args=[gateway],
                           expected_args=[],
                           method_kwargs={},
                           expected_kwargs={'gateway_id': None}
                           )

    def test_update_vpc_channel(self):
        gateway = _gateway.Gateway()
        vpc_channel = _vpc.VpcChannel()
        self.verify_update(self.proxy.update_vpc_channel,
                           _vpc.VpcChannel,
                           method_args=[gateway, vpc_channel],
                           expected_args=[vpc_channel],
                           method_kwargs={},
                           expected_kwargs={'gateway_id': None}
                           )

    def test_delete_vpc_channel(self):
        gateway = _gateway.Gateway()
        vpc_channel = _vpc.VpcChannel()
        self.verify_delete(self.proxy.delete_vpc_channel,
                           _vpc.VpcChannel,
                           method_args=[gateway, vpc_channel],
                           expected_args=[vpc_channel],
                           method_kwargs={},
                           expected_kwargs={'gateway_id': None}
                           )

    def test_get_vpc_channel(self):
        gateway = _gateway.Gateway()
        vpc_channel = _vpc.VpcChannel()
        self.verify_get(self.proxy.get_vpc_channel,
                        _vpc.VpcChannel,
                        method_args=[gateway, vpc_channel],
                        expected_args=[vpc_channel],
                        method_kwargs={},
                        expected_kwargs={'gateway_id': None}
                        )

    def test_list_vpc_channels(self):
        gateway = _gateway.Gateway()
        self.verify_list(self.proxy.vpc_channels,
                         _vpc.VpcChannel,
                         method_args=[gateway],
                         expected_args=[],
                         method_kwargs={},
                         expected_kwargs={'gateway_id': None}
                         )

    def test_modify_vpc_channel_healthcheck(self):
        gateway = _gateway.Gateway()
        vpc_channel = _vpc.VpcChannel()
        self._verify(
            'otcextensions.sdk.apig.v2.vpc_channel.'
            'VpcChannel.modify_healthcheck',
            self.proxy.modify_vpc_channel_healthcheck,
            method_args=[gateway, vpc_channel],
            expected_args=[self.proxy],
            expected_kwargs={'gateway_id': None,
                             'vpc_channel_id': None}
        )

    def test_add_or_update_backend_server_group(self):
        gateway = _gateway.Gateway()
        vpc_channel = _vpc.VpcChannel()
        self._verify(
            'otcextensions.sdk.apig.v2.backend_server_group.'
            'BackendServerGroup.create_group',
            self.proxy.add_or_update_backend_server_group,
            method_args=[gateway, vpc_channel],
            expected_args=[self.proxy],
            expected_kwargs={'gateway_id': None,
                             'vpc_channel_id': None}
        )

    def test_backend_server_groups(self):
        gateway = _gateway.Gateway()
        vpc_channel = _vpc.VpcChannel()
        self.verify_list(self.proxy.backend_server_groups,
                         _vpc_sg.BackendServerGroup,
                         method_args=[gateway, vpc_channel],
                         expected_args=[],
                         method_kwargs={},
                         expected_kwargs={'gateway_id': None,
                                          'vpc_channel_id': None}
                         )

    def test_get_backend_server_group(self):
        gateway = _gateway.Gateway()
        vpc_channel = _vpc.VpcChannel()
        backend_server_group = _vpc_sg.BackendServerGroup()
        self.verify_get(self.proxy.get_backend_server_group,
                        _vpc_sg.BackendServerGroup,
                        method_args=[gateway, vpc_channel,
                                     backend_server_group],
                        expected_args=[None],
                        method_kwargs={},
                        expected_kwargs={'gateway_id': None,
                                         'vpc_channel_id': None}
                        )

    def test_update_backend_server_group(self):
        gateway = _gateway.Gateway()
        vpc_channel = _vpc.VpcChannel()
        backend_server_group = _vpc_sg.BackendServerGroup()
        self.verify_update(self.proxy.update_backend_server_group,
                           _vpc_sg.BackendServerGroup,
                           method_args=[gateway, vpc_channel,
                                        backend_server_group],
                           expected_args=[None],
                           method_kwargs={},
                           expected_kwargs={'gateway_id': None,
                                            'vpc_channel_id': None}
                           )

    def test_delete_backend_server_group(self):
        gateway = _gateway.Gateway()
        vpc_channel = _vpc.VpcChannel()
        backend_server_group = _vpc_sg.BackendServerGroup()
        self.verify_delete(self.proxy.delete_backend_server_group,
                           _vpc_sg.BackendServerGroup,
                           method_args=[gateway, vpc_channel,
                                        backend_server_group],
                           expected_args=[None],
                           method_kwargs={},
                           expected_kwargs={'gateway_id': None,
                                            'vpc_channel_id': None}
                           )

    def test_add_or_update_backend_servers(self):
        gateway = _gateway.Gateway()
        vpc_channel = _vpc.VpcChannel()
        self._verify(
            'otcextensions.sdk.apig.v2.backend_server.'
            'BackendServer.create_members',
            self.proxy.add_or_update_backend_servers,
            method_args=[gateway, vpc_channel],
            expected_args=[self.proxy],
            expected_kwargs={'gateway_id': None,
                             'vpc_channel_id': None}
        )

    def test_list_backend_servers(self):
        gateway = _gateway.Gateway()
        vpc_channel = _vpc.VpcChannel()
        self.verify_list(self.proxy.list_backend_servers,
                         _vpc_s.BackendServer,
                         method_args=[gateway, vpc_channel],
                         expected_args=[],
                         method_kwargs={},
                         expected_kwargs={'gateway_id': None,
                                          'vpc_chan_id': None}
                         )

    def test_update_backend_servers(self):
        gateway = _gateway.Gateway()
        vpc_channel = _vpc.VpcChannel()
        self._verify(
            'otcextensions.sdk.apig.v2.backend_server.'
            'BackendServer.update_members',
            self.proxy.update_backend_server,
            method_args=[gateway, vpc_channel],
            expected_args=[self.proxy],
            expected_kwargs={'gateway_id': None,
                             'vpc_channel_id': None}
        )

    def test_delete_backend_servers(self):
        gateway = _gateway.Gateway()
        vpc_channel = _vpc.VpcChannel()
        backend_server = _vpc_s.BackendServer()
        self.verify_delete(self.proxy.remove_backend_server,
                           _vpc_s.BackendServer,
                           method_args=[gateway, vpc_channel, backend_server],
                           expected_args=[backend_server],
                           method_kwargs={},
                           expected_kwargs={'gateway_id': None,
                                            'vpc_chan_id': None}
                           )

    def test_enable_backend_server(self):
        gateway = _gateway.Gateway()
        vpc_channel = _vpc.VpcChannel()
        backend_server = _vpc_s.BackendServer()
        self._verify(
            'otcextensions.sdk.apig.v2.backend_server.'
            'BackendServer.enable_server',
            self.proxy.enable_backend_server,
            method_args=[gateway, vpc_channel, backend_server],
            expected_args=[self.proxy],
            expected_kwargs={'gateway_id': None,
                             'vpc_chan_id': None}
        )

    def test_disable_backend_server(self):
        gateway = _gateway.Gateway()
        vpc_channel = _vpc.VpcChannel()
        backend_server = _vpc_s.BackendServer()
        self._verify(
            'otcextensions.sdk.apig.v2.backend_server.'
            'BackendServer.disable_server',
            self.proxy.disable_backend_server,
            method_args=[gateway, vpc_channel, backend_server],
            expected_args=[self.proxy],
            expected_kwargs={'gateway_id': None,
                             'vpc_chan_id': None}
        )


class TestApiCall(TestApiGatewayProxy):
    def test_list_api_calls_for_period(self):
        gateway = _gateway.Gateway()
        self._verify(
            'otcextensions.sdk.apig.v2.api_call.'
            'ApiCallResult.get_api_calls_for_period',
            self.proxy.list_api_calls_for_period,
            method_args=[gateway],
            expected_args=[self.proxy],
            expected_kwargs={'gateway_id': None}
        )

    def test_list_api_calls_for_group(self):
        gateway = _gateway.Gateway()
        self._verify(
            'otcextensions.sdk.apig.v2.api_call.'
            'ApiCallResult.get_api_calls_for_group',
            self.proxy.list_api_calls_for_group,
            method_args=[gateway],
            expected_args=[self.proxy],
            expected_kwargs={'gateway_id': None}
        )

    def test_list_metric_data(self):
        gateway = _gateway.Gateway()
        self._verify(
            'otcextensions.sdk.apig.v2.metric_data.'
            'MetricData.get_metric_data',
            self.proxy.list_metric_data,
            method_args=[gateway],
            expected_args=[self.proxy],
            expected_kwargs={'gateway_id': None}
        )
