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
import time
import uuid
from otcextensions.tests.functional.sdk.vpcep import TestVpcep


class TestEndpoint(TestVpcep):
    def setUp(self):
        super(TestEndpoint, self).setUp()
        self.network_data = self.create_network()
        self.addCleanup(self.destroy_network, self.network_data)
        self.port = self.create_port(self.network_data['network_id'])
        self.addCleanup(self.destroy_port, self.port.id)
        self.service = self.create_service_helper()
        self.endpoint_name = 'sdk-vpcep-test-endpoint-' + uuid.uuid4().hex[:8]

    def _create_endpoint(self, remove=True):
        attrs = {
            'router_id': self.network_data['router_id'],
            'network_id': self.network_data['network_id'],
            'endpoint_service_id': self.service.id,
            'enable_dns': False,
            'tags': [{'key': 'test-key', 'value': 'test-value'}]
        }
        endpoint = self.client.create_endpoint(**attrs)
        self.assertIsNotNone(endpoint)
        if remove:
            self.addCleanup(self.client.delete_endpoint, endpoint.id)
        return endpoint

    def test_create_endpoint(self):
        """Test creating an Endpoint and verifying its attributes."""
        ep = self._create_endpoint()
        self.assertEqual(self.service.id, ep.endpoint_service_id)
        self.assertEqual(self.network_data['router_id'], ep.router_id)
        self.assertTrue(len(ep.tags) > 0)
        self.assertEqual('test-key', ep.tags[0].key)

    def test_list_endpoints(self):
        """Test listing Endpoints."""
        ep = self._create_endpoint()
        eps = list(self.client.endpoints())
        self.assertGreater(len(eps), 0)
        found = any([e.id == ep.id for e in eps])
        self.assertTrue(found)

    def test_get_endpoint(self):
        """Test retrieving a single Endpoint."""
        ep = self._create_endpoint()
        got = self.client.get_endpoint(ep.id)
        self.assertEqual(ep.id, got.id)

    def test_delete_endpoint(self):
        """Test deleting an Endpoint."""
        ep = self._create_endpoint(remove=False)
        self.client.delete_endpoint(ep.id)
        time.sleep(5)
        eps = list(self.client.endpoints())
        self.assertFalse(any(e.id == ep.id for e in eps))
