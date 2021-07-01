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
    network_info = None
    gateway = None
    server = None
    keypair = None
    server_name = uuid_v4 + 'test-dnat-server'
    gateway_name = uuid_v4 + 'test-dnat-gateway'
    flavor = "s3.medium.1"
    image = "Standard_Ubuntu_18.04_latest"
    kp_name = uuid_v4 + "test-dnat-kp"
    fixed_ip = "192.168.0.10"
    attrs = {
        "name": gateway_name,
        "spec": "1"
    }
    AZ = 'eu-de-01'

    def _create_network(self):
        cidr = '192.168.0.0/16'
        ipv4 = 4
        uuid_v4 = uuid.uuid4().hex[:8]
        router_name = 'dnat-test-router-' + uuid_v4
        net_name = 'dnat-test-net-' + uuid_v4
        subnet_name = 'dnat-test-subnet-' + uuid_v4

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
            self.attrs['internal_network_id'] = \
                TestDnat.network_info['network_id']
            TestDnat.gateway = self.conn.nat.create_gateway(**self.attrs)
            self.conn.nat.wait_for_gateway(TestDnat.gateway)
            self.assertIsNotNone(TestDnat.gateway)
        if not TestDnat.floating_ip:
            admin_external_net = self.conn.network.find_network(
                name_or_id='admin_external_net')
            self.assertIsNone(admin_external_net)
            TestDnat.floating_ip = self.conn.network.create_ip(
                floating_network_id=admin_external_net.id)
        image = self.conn.compute.find_image(self.image)
        flavor = self.conn.compute.find_flavor(self.flavor)
        if not TestDnat.keypair:
            TestDnat.keypair = self.conn.compute.create_keypair(
                name=self.kp_name)
        if not TestDnat.port:
            TestDnat.port = self.conn.network.create_port(
                network_id=TestDnat.network_info['network_id'])
        TestDnat.server = self.conn.compute.create_server(
            name=self.server_name, networks=[{"port": TestDnat.port.id}],
            key_name=self.kp_name, flavorRef=flavor.id, imageRef=image.id)
        self.conn.compute.wait_for_server(TestDnat.server)

    def _destroy_network(self):
        if TestDnat.floating_ip:
            self.conn.network.delete_ip(TestDnat.floating_ip)
            TestDnat.floating_ip = None
        if TestDnat.server:
            self.conn.compute.delete_server(TestDnat.server)
            self.conn.compute.wait_for_delete(
                TestDnat.server, interval=5, wait=300)
            TestDnat.server = None
        if TestDnat.keypair:
            self.conn.compute.delete_keypair(TestDnat.keypair)
            self.conn.compute.wait_for_delete(TestDnat.keypair)
            TestDnat.keypair = None
        if TestDnat.gateway:
            self.conn.nat.delete_gateway(gateway=TestDnat.gateway)
            self.conn.nat.wait_for_delete_gateway(TestDnat.gateway)
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

    def test_01_create_dnat_rule(self):
        self._create_network()
        TestDnat.dnat_rule = self.conn.nat.create_dnat_rule(
            nat_gateway_id=TestDnat.gateway.id,
            floating_ip_id=TestDnat.floating_ip.id,
            network_id=TestDnat.network_info['network_id'],
            private_ip=TestDnat.port.fixed_ips[0]["ip_address"],
            protocol='TCP', internal_service_port=22,
            external_service_port=22)
        self.conn.nat.wait_for_dnat(TestDnat.dnat_rule)
        self.assertIsNotNone(TestDnat.dnat_rule)

    def test_02_list_dnat_rules(self):
        self.dnat_rules = list(self.conn.nat.dnat_rules())
        self.assertGreaterEqual(len(self.dnat_rules), 0)

    def test_03_get_dnat_rule(self):
        dnat_rule = self.conn.nat.get_dnat_rule(TestDnat.dnat_rule.id)
        self.assertEqual(dnat_rule.id, TestDnat.dnat_rule.id)

    def test_04_delete_dnat_rule(self):
        self.conn.nat.delete_dnat_rule(dnat=TestDnat.dnat_rule)
        self.conn.nat.wait_for_delete_dnat(TestDnat.dnat_rule)
        self._destroy_network()
        try:
            dnat_rule = self.conn.nat.get_dnat_rule(TestDnat.dnat_rule.id)
        except openstack.exceptions.ResourceNotFound:
            dnat_rule = None
        self.assertIsNone(dnat_rule)
