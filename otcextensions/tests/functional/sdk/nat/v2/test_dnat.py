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


class TestDnat(base.BaseFunctionalTest):
    
    floating_ip = None
    dnat_rule = None
    port = None
    uuid_v4 = uuid.uuid4().hex[:8]
    port_name = uuid_v4 + 'test-dnat-port'
    admin_external_net_id = "0a2228f2-7f8a-45f1-8e09-9039e1d09975"
    network_info = None
    gateway = None
    gateway_name = uuid_v4 + 'test-dnat-gateway'
    attrs = {
        "name": gateway_name,
        "spec": "1"
    }

    def create_network(self):
        cidr = '192.168.0.0/16'
        ipv4 = 4
        uuid_v4 = uuid.uuid4().hex[:8]
        router_name = 'sdk-dnat-test-router-' + uuid_v4
        net_name = 'sdk-dnat-test-net-' + uuid_v4
        subnet_name = 'sdk-dnat-test-subnet-' + uuid_v4

        if not TestDnat.network_info:
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

            TestDnat.network_info = {
                'router_id': router_id,
                'subnet_id': subnet_id,
                'network_id': net_id
            }
        if not TestDnat.gateway:
            self.attrs['router_id'] = TestDnat.network_info['router_id']
            self.attrs['internal_network_id'] = TestDnat.network_info['network_id']
            TestDnat.gateway = self.conn.nat.create_gateway(**self.attrs)
            self.conn.nat.wait_for_gateway(TestDnat.gateway)
            self.assertIsNotNone(TestDnat.gateway)

    def destroy_network(self):
        if TestDnat.gateway:
            self.conn.nat.delete_gateway(gateway=TestDnat.gateway)
            self.conn.nat.wait_for_delete_gateway(TestDnat.gateway)
            gateway = self.conn.nat.find_gateway(TestDnat.gateway.name, ignore_missing=True)
            self.assertIsNone(gateway)
            TestDnat.gateway = None
        if TestDnat.network_info:
            router_id = TestDnat.network_info['router_id']
            subnet_id = TestDnat.network_info['subnet_id']
            network_id = TestDnat.network_info['network_id']
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

            TestDnat.network_info = None
            self.assertIsNone(sot)

    def setUp(self):
        super(TestDnat, self).setUp()

    def tearDown(self):
        super(TestDnat, self).tearDown()

    def _create_network(self):
        self.create_network()
        if not TestDnat.floating_ip:
            TestDnat.floating_ip = self.conn.network.create_ip(
                floating_network_id=self.admin_external_net_id)
        if not TestDnat.port:
            TestDnat.port = self.conn.network.create_port(network_id=TestDnat.network_info['network_id'])

    def _create_dnat_rule(self):
        self._create_network()
        TestDnat.dnat_rule = self.conn.nat.create_dnat_rule(nat_gateway_id=TestDnat.gateway.id,
                                                            floating_ip_id=TestDnat.floating_ip.id,
                                                            network_id=TestDnat.network_info['network_id'],
                                                            port_id=TestDnat.port.id,
                                                            protocol='TCP', internal_service_port=80,
                                                            external_service_port=80)
        self.assertIsNotNone(TestDnat.dnat_rule)

    def test_01_list_dnat_rules(self):
        self._create_dnat_rule()
        self.assertIsNotNone(TestDnat.dnat_rule)
