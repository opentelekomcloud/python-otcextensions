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
from openstack.tests.unit import base
from otcextensions.sdk.apig.v2 import throttling_policy_binding

EXAMPLE_BIND = {
    "throttle_id": "0b0e8f456b8742218af75f945307173c",
    "publish_ids": ["40e7162dc6b94bbbbb1a60d2a24b1b0c"]
}


class TestThrottlingPolicyBind(base.TestCase):

    def test_basic(self):
        sot = throttling_policy_binding.ThrottlingPolicyBind()
        self.assertEqual(
            '/apigw/instances/%(gateway_id)s/throttle-bindings',
            sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)
        self.assertEqual('apis', sot.resources_key)

    def test_make_it(self):
        sot = throttling_policy_binding.ThrottlingPolicyBind(**EXAMPLE_BIND)
        self.assertEqual(EXAMPLE_BIND['throttle_id'], sot.throttle_id)
        self.assertEqual(EXAMPLE_BIND['publish_ids'], sot.publish_ids)


EXAMPLE_NOTBOUND = {
    "run_env_name": "RELEASE",
    "group_name": "api_group_001",
    "publish_id": "40e7162dc6b94bbbbb1a60d2a24b1b0c",
    "group_id": "c77f5e81d9cb4424bf704ef2b0ac7600",
    "throttle_apply_id": "3e06ac135e18477e918060d3c59d6f6a",
    "name": "Api_http",
    "apply_time": "2020-08-03T12:25:52Z",
    "remark": "Web backend API",
    "run_env_id": "DEFAULT_ENVIRONMENT_RELEASE_ID",
    "id": "5f918d104dc84480a75166ba99efff21",
    "type": 1,
    "throttle_name": "throttle_demo",
    "auth_type": "APP",
    "req_uri": "/test/http"
}


class TestThrottlingPolicyNotBoundApi(base.TestCase):

    def test_basic(self):
        sot = throttling_policy_binding.NotBoundApi()
        self.assertEqual(
            '/apigw/instances/%(gateway_id)s/'
            'throttle-bindings/unbinded-apis',
            sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertEqual('apis', sot.resources_key)

    def test_make_it(self):
        sot = throttling_policy_binding.NotBoundApi(**EXAMPLE_NOTBOUND)
        self.assertEqual(
            EXAMPLE_NOTBOUND['throttle_apply_id'], sot.throttle_apply_id
        )


EXAMPLE_BOUND = {
    "id": "3437448ad06f4e0c91a224183116e965",
    "name": "throttle_demo",
    "api_call_limits": 800,
    "user_call_limits": 500,
    "app_call_limits": 300,
    "ip_call_limits": 600,
    "time_interval": 1,
    "time_unit": "SECOND",
    "create_time": "2020-07-31T08:44:02Z",
    "is_inclu_special_throttle": 2,
    "env_name": "RELEASE",
    "type": 1,
    "bind_id": "3e06ac135e18477e918060d3c59d6f6a",
    "bind_time": "2020-08-03T12:25:52Z",
    "bind_num": 0,
    "enable_adaptive_control": "FALSE"
}


class TestThrottlingPolicyBoundThrottles(base.TestCase):

    def test_basic(self):
        sot = throttling_policy_binding.BoundThrottles()
        self.assertEqual(
            '/apigw/instances/%(gateway_id)s/'
            'throttle-bindings/binded-throttles',
            sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertEqual('throttles', sot.resources_key)

    def test_make_it(self):
        sot = throttling_policy_binding.BoundThrottles(**EXAMPLE_BOUND)
        self.assertEqual(EXAMPLE_BOUND['id'], sot.id)
        self.assertEqual(EXAMPLE_BOUND['name'], sot.name)
        self.assertEqual(EXAMPLE_BOUND['api_call_limits'], sot.api_call_limits)
        self.assertEqual(
            EXAMPLE_BOUND['user_call_limits'], sot.user_call_limits
        )
        self.assertEqual(EXAMPLE_BOUND['ip_call_limits'], sot.ip_call_limits)
