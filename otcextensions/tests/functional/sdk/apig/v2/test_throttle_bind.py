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
import uuid

from otcextensions.tests.functional.sdk.apig import TestApiG


class TestThrottleBind(TestApiG):
    def setUp(self):
        super(TestThrottleBind, self).setUp()
        self.suffix = uuid.uuid4().hex[:4]

        self.create_gateway()
        self.gateway_id = TestThrottleBind.gateway.id
        # self.gateway_id = "be76ca6de5fe4aa7af503c03b3b44dea"

        self.attrs = {
            "api_call_limits": 100,
            "app_call_limits": 60,
            "enable_adaptive_control": "FALSE",
            "ip_call_limits": 60,
            "name": f"throttle_{self.suffix}",
            "time_interval": 1,
            "time_unit": "SECOND",
            "type": 1,
            "user_call_limits": 60
        }
        self.policy = self.client.create_throttling_policy(
            gateway=self.gateway_id,
            **self.attrs
        )

        group_attrs = {
            "name": f"api_group_{self.suffix}",
            "remark": "API group 1"
        }
        self.group = self.client.create_api_group(
            gateway=self.gateway_id,
            **group_attrs
        )
        self.assertIsNotNone(self.group.id)

        api_attrs = {
            "group_id": self.group.id,
            "name": f"test_api_{self.suffix}",
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
        self.api = self.client.create_api(
            gateway=self.gateway_id,
            **api_attrs
        )
        self.environment = self.client.create_environment(
            gateway=self.gateway_id,
            name=f"testPub{self.suffix}",
            remark="test publish"
        )
        self.publish = self.client.publish_api(
            gateway=self.gateway_id,
            api=self.api.id,
            env=self.environment,
            remark="publish"
        )

        self.attrs = {
            "throttle_id": self.policy.id,
            "publish_ids": [self.publish.publish_id]
        }
        self.bind = self.client.bind_throttling_policy(
            gateway=self.gateway_id,
            **self.attrs
        )

        self.addCleanup(
            self.client.delete_api_group,
            gateway=self.gateway_id,
            api_group=self.group.id,
        )
        self.addCleanup(
            self.client.delete_environment,
            gateway=self.gateway_id,
            environment=self.environment,
        )
        self.addCleanup(
            self.client.delete_throttling_policy,
            gateway=self.gateway_id,
            policy=self.policy
        )
        self.addCleanup(
            self.client.delete_api,
            gateway=self.gateway_id,
            api=self.api
        )
        self.addCleanup(
            self.client.offline_api,
            gateway=self.gateway_id,
            api=self.api.id,
            env=self.environment,
            remark="offline"
        )
        self.addCleanup(
            self.client.unbind_throttling_policies,
            gateway=self.gateway_id,
            throttle_bindings=[self.bind.policies[0].id]
        )

        self.addCleanup(self.delete_gateway())

    def test_list_bound_throttling_policies(self):
        sign = list(self.client.bound_throttling_policies(
            gateway=self.gateway_id,
            api_id=self.api.id
        ))
        self.assertEqual(len(sign), 1)

    def test_list_bound_throttling_policy_apis(self):
        sign = list(self.client.bound_throttling_policy_apis(
            gateway=self.gateway_id,
            throttle_id=self.policy.id
        ))
        self.assertEqual(len(sign), 1)

    def test_list_not_bound_throttling_policy_apis(self):
        sign = list(self.client.not_bound_throttling_policy_apis(
            gateway=self.gateway_id,
            throttle_id=self.policy.id
        ))
        self.assertEqual(len(sign), 0)
