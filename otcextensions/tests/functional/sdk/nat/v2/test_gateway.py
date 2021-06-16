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
import openstack
import uuid

from otcextensions.tests.functional.sdk.nat import TestNat

_logger = openstack._log.setup_logging('openstack')


class TestGateway(TestNat):
    uuid_v4 = uuid.uuid4().hex[:8]
    gateway_name = uuid_v4 + 'test-gateway'
    update_gateway_name = uuid_v4 + 'update-test-gateway'
    attrs = {
        "name": gateway_name,
        "description": "my nat gateway 01",
        "router_id": "d84f345c-80a1-4fa2-a39c-d0d397c3f09a",
        "internal_network_id": "89d66639-aacb-4929-969d-07080b0f9fd9",
        "spec": "1"
    }
    gateway = None
    
    def setUp(self):
        super(TestGateway, self).setUp()

    def tearDown(self):
        super(TestGateway, self).tearDown()

    def _create_gateway(self):
        self.create_network()
        self.attrs['router_id'] = TestGateway.network_info['router_id']
        self.attrs['internal_network_id'] = TestGateway.network_info['network_id']
        TestGateway.gateway = self.conn.nat.create_gateway(**self.attrs)
        self.conn.nat.wait_for_gateway(TestGateway.gateway)
        self.assertIsNotNone(self.gateway)

    def test_01_list_gateways(self):
        self._create_gateway()
        self.gateways = list(self.conn.nat.gateways())
        self.assertGreaterEqual(len(self.gateways), 0)
        gateway = self.conn.nat.get_gateway(TestGateway.gateway.id)
        self.assertNotIn(gateway, self.gateways)

    def test_02_get_gateway(self):
        gateway = self.conn.nat.get_gateway(TestGateway.gateway.id)
        self.assertEqual(gateway.name, self.gateway_name)

    def test_03_find_gateway(self):
        gateway = self.conn.nat.find_gateway(TestGateway.gateway.name)
        self.assertEqual(gateway.name, self.gateway_name)

    def test_04_update_gateway(self):
        update_gw = self.conn.nat.update_gateway(gateway=TestGateway.gateway.id,
                                               name=self.update_gateway_name)
        update_gw = self.conn.nat.get_gateway(update_gw.id)
        self.assertEqual(update_gw.name, self.update_gateway_name)

    def test_05_delete_gateway(self):
        self.conn.nat.delete_gateway(gateway=TestGateway.gateway)
        self.conn.nat.wait_for_delete_gateway(TestGateway.gateway)
        gateway = self.conn.nat.find_gateway(self.update_gateway_name, ignore_missing=True)
        self.assertIsNone(gateway)
        self.destroy_network()
