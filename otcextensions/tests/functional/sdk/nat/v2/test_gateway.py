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

from otcextensions.tests.functional import base

_logger = openstack._log.setup_logging('openstack')


class TestGateway(base.BaseFunctionalTest):
    uuid_v4 = uuid.uuid4().hex[:8]
    update_gateway_name = uuid_v4 + 'update-test-gateway'
    network_info = None
    gateway = None
    gateway_name = uuid_v4 + 'test-gateway-gateway'
    attrs = {
        "name": gateway_name,
        "spec": "1"
    }

    def create_network(self):
        cidr = '192.168.0.0/16'
        ipv4 = 4
        uuid_v4 = uuid.uuid4().hex[:8]
        router_name = 'gw-test-router-' + uuid_v4
        net_name = 'gw-test-net-' + uuid_v4
        subnet_name = 'gw-test-subnet-' + uuid_v4

        if not TestGateway.network_info:
            network = self.conn.network.create_network(name=net_name)
            self.assertEqual(net_name, network.name)
            net_id = network.id
            subnet = self.conn.network.create_subnet(
                name=subnet_name,
                ip_version=ipv4,
                network_id=net_id,
                cidr=cidr
            )
            self.assertEqual(subnet_name, subnet.name)
            subnet_id = subnet.id

            router = self.conn.network.create_router(name=router_name)
            self.assertEqual(router_name, router.name)
            router_id = router.id
            interface = router.add_interface(
                self.conn.network,
                subnet_id=subnet_id
            )
            self.assertEqual(interface['subnet_id'], subnet_id)
            self.assertIn('port_id', interface)

            TestGateway.network_info = {
                'router_id': router_id,
                'subnet_id': subnet_id,
                'network_id': net_id
            }
        if not TestGateway.gateway:
            self.attrs['router_id'] = TestGateway.network_info['router_id']
            self.attrs['internal_network_id'] = \
                TestGateway.network_info['network_id']
            TestGateway.gateway = self.conn.nat.create_gateway(**self.attrs)
            self.conn.nat.wait_for_gateway(TestGateway.gateway)
            self.assertIsNotNone(TestGateway.gateway)

    def destroy_network(self):
        if TestGateway.network_info:
            router_id = TestGateway.network_info['router_id']
            subnet_id = TestGateway.network_info['subnet_id']
            network_id = TestGateway.network_info['network_id']
            router = self.conn.network.get_router(router_id)

            interface = router.remove_interface(
                self.conn.network,
                subnet_id=subnet_id
            )
            self.assertEqual(interface['subnet_id'], subnet_id)
            self.assertIn('port_id', interface)
            sot = self.conn.network.delete_router(
                router_id,
                ignore_missing=False
            )
            self.assertIsNone(sot)
            sot = self.conn.network.delete_subnet(
                subnet_id,
                ignore_missing=False
            )
            self.assertIsNone(sot)
            sot = self.conn.network.delete_network(
                network_id,
                ignore_missing=False
            )

            TestGateway.network_info = None
            self.assertIsNone(sot)

    def setUp(self):
        super(TestGateway, self).setUp()

    def tearDown(self):
        super(TestGateway, self).tearDown()

    def test_01_list_gateways(self):
        self.create_network()
        self.gateways = list(self.conn.nat.gateways())
        self.assertGreaterEqual(len(self.gateways), 0)

    def test_02_get_gateway(self):
        gateway = self.conn.nat.get_gateway(TestGateway.gateway.id)
        self.assertEqual(gateway.name, self.gateway_name)

    def test_03_find_gateway(self):
        gateway = self.conn.nat.find_gateway(TestGateway.gateway.name)
        self.assertEqual(gateway.name, self.gateway_name)

    def test_04_update_gateway(self):
        update_gw = self.conn.nat.update_gateway(
            gateway=TestGateway.gateway.id,
            name=self.update_gateway_name)
        update_gw = self.conn.nat.get_gateway(update_gw.id)
        self.assertEqual(update_gw.name, self.update_gateway_name)

    def test_05_delete_gateway(self):
        self.conn.nat.delete_gateway(gateway=TestGateway.gateway)
        self.conn.nat.wait_for_delete_gateway(TestGateway.gateway)
        TestGateway.gateway = None
        self.destroy_network()
        gateway = self.conn.nat.find_gateway(
            self.update_gateway_name, ignore_missing=True)
        self.assertIsNone(gateway)
