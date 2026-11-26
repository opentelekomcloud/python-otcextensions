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
from otcextensions.tests.functional import base


class TestQuota(base.BaseFunctionalTest):
    def test_raw_quota_request(self):
        response = self.conn.ccn.get("/gcn/quotas")
        self.assertEqual(200, response.status_code)
        self.assertGreater(len(response.json()["quotas"]), 0)

    def test_list_central_network_quotas(self):
        quotas = list(self.conn.ccn.central_network_quotas())

        self.assertGreater(len(quotas), 0)
        for quota in quotas:
            self.assertIsNotNone(quota.quota_key)
            self.assertIsInstance(quota.quota_limit, int)
            if quota.used is not None:
                self.assertIsInstance(quota.used, int)
            self.assertIsNotNone(quota.unit)
        account_quota = next(
            q for q in quotas if q.quota_key == "central_networks_per_account"
        )
        self.assertIsInstance(account_quota.used, int)
