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


class TestThrottlingExcluded(TestApiG):
    environment = None

    def setUp(self):
        super(TestThrottlingExcluded, self).setUp()
        self.suffix = uuid.uuid4().hex[:4]
        self.create_gateway()
        self.gateway_id = TestThrottlingExcluded.gateway.id
        # self.gateway_id = "be76ca6de5fe4aa7af503c03b3b44dea"
        self.attrs = {
            "api_call_limits": 100,
            "app_call_limits": 60,
            "enable_adaptive_control": "FALSE",
            "ip_call_limits": 60,
            "name": f"throttle_{self.suffix}",
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
        self.ex_attrs = {
            "call_limits": 50,
            "object_id": self.conn.current_user_id,
            "object_type": "USER"
        }
        self.excluded = self.client.create_throttling_excluded_policy(
            gateway=self.gateway_id,
            policy=self.policy,
            **self.ex_attrs
        )

        self.addCleanup(
            self.client.delete_throttling_policy,
            gateway=self.gateway_id,
            policy=self.policy
        )
        self.addCleanup(
            self.client.delete_throttling_excluded_policy,
            gateway=self.gateway_id,
            policy=self.policy,
            exclude=self.excluded
        )
        self.addCleanup(self.delete_gateway())

    def test_list_throttling_excluded_policies(self):
        pol = list(self.client.throttling_excluded_policies(
            gateway=self.gateway_id, policy=self.policy))
        self.assertEqual(len(pol), 1)

    def test_update_throttling_excluded_policy(self):
        attrs = {
            "call_limits": 30
        }
        updated = self.client.update_throttling_excluded_policy(
            gateway=self.gateway_id,
            policy=self.policy.id,
            exclude=self.excluded,
            **attrs
        )
        self.assertEqual(updated.call_limits, attrs["call_limits"])
