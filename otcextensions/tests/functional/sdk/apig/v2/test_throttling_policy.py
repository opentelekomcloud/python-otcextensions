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

from otcextensions.tests.functional.sdk.apig import TestApiG


class TestThrottlingPolicy(TestApiG):
    environment = None

    def setUp(self):
        super(TestThrottlingPolicy, self).setUp()
        self.create_gateway()
        self.gateway_id = TestThrottlingPolicy.gateway.id
        # self.gateway_id = "be76ca6de5fe4aa7af503c03b3b44dea"
        self.attrs = {
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
        self.policy = self.client.create_throttling_policy(
            gateway=self.gateway_id,
            **self.attrs
        )

        self.addCleanup(
            self.client.delete_throttling_policy,
            gateway=self.gateway_id,
            policy=self.policy
        )
        self.addCleanup(self.delete_gateway())

    def test_list_throttling_policies(self):
        pol = list(self.client.throttling_policies(
            gateway=self.gateway_id))
        self.assertEqual(len(pol), 1)

    def test_get_throttling_policy(self):
        pol = self.client.get_throttling_policy(
            gateway=self.gateway_id,
            policy=self.policy.id)
        self.assertEqual(pol.id, self.policy.id)

    def test_update_throttling_policy(self):
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
        updated = self.client.update_throttling_policy(
            gateway=self.gateway_id,
            policy=self.policy.id,
            **attrs
        )
        self.assertEqual(updated.remark, attrs["remark"])
