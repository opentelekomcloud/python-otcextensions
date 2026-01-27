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
from otcextensions.tests.functional.sdk.vpcep import TestVpcepBase


class TestQuota(TestVpcepBase):
    def test_list_endpoint_service_quota(self):
        """Test listing Endpoint Service quotas."""
        quotas = list(self.client.resource_quota(type='endpoint_service'))
        self.assertGreater(len(quotas), 0)
        q = quotas[0]
        self.assertTrue(hasattr(q, 'type'))
        self.assertTrue(hasattr(q, 'quota'))
        self.assertTrue(hasattr(q, 'used'))
        self.assertEqual('endpoint_service', q.type)

    def test_list_endpoint_quota(self):
        """Test listing Endpoint quotas."""
        quotas_ep = list(self.client.resource_quota(type='endpoint'))
        self.assertGreater(len(quotas_ep), 0)
        self.assertEqual('endpoint', quotas_ep[0].type)

    def test_list_quota(self):
        """Test listing all quotas without type filter."""
        quotas = list(self.client.resource_quota())
        self.assertEqual(2, len(quotas))
        types = {q.type for q in quotas}
        self.assertEqual({'endpoint', 'endpoint_service'}, types)
