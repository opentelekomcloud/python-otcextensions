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


class TestSnat(base.BaseFunctionalTest):
    
    floating_ip = None
    snat_rule = None
    uuid_v4 = uuid.uuid4().hex[:8]
    network_info = None
    gateway = None
    gateway_name = uuid_v4 + 'test-snat-gateway'
    attrs = {
        "name": gateway_name,
        "spec": "1"
    }

    def _create_network(self):
        cidr = '192.168.0.0/16'
        ipv4 = 4
        uuid_v4 = uuid.uuid4().hex[:8]
        router_name = 'snat-test-router-' + uuid_v4
        net_name = 'snat-test-net-' + uuid_v4
        subnet_name = 'snat-test-subnet-' + uuid_v4

        if not TestSnat.network_info:
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

            TestSnat.network_info = {
                'router_id': router_id,
                'subnet_id': subnet_id,
                'network_id': net_id
            }
        if not TestSnat.gateway:
            self.attrs['router_id'] = TestSnat.network_info['router_id']
            self.attrs['internal_network_id'] = TestSnat.network_info['network_id']
            TestSnat.gateway = self.conn.nat.create_gateway(**self.attrs)
            self.conn.nat.wait_for_gateway(TestSnat.gateway)
            self.assertIsNotNone(TestSnat.gateway)
        if not TestSnat.floating_ip:
            TestSnat.floating_ip = self.conn.network.create_ip(
                floating_network_id="0a2228f2-7f8a-45f1-8e09-9039e1d09975")

    def _destroy_network(self):
        if TestSnat.gateway:
            self.conn.nat.delete_gateway(gateway=TestSnat.gateway)
            self.conn.nat.wait_for_delete_gateway(TestSnat.gateway)
            TestSnat.gateway = None
        if TestSnat.floating_ip:
            self.conn.network.delete_ip(TestSnat.floating_ip)
            TestSnat.floating_ip = None
        if TestSnat.network_info:
            router_id = TestSnat.network_info['router_id']
            subnet_id = TestSnat.network_info['subnet_id']
            network_id = TestSnat.network_info['network_id']
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

            TestSnat.network_info = None
            self.assertIsNone(sot)

    def setUp(self):
        super(TestSnat, self).setUp()

    def tearDown(self):
        super(TestSnat, self).tearDown()

    def _create_snat_rule(self):
        TestSnat.snat_rule = self.conn.nat.create_snat_rule(floating_ip_id=TestSnat.floating_ip.id,
                                                            nat_gateway_id=TestSnat.gateway.id,
                                                            network_id=TestSnat.network_info['network_id'])
        self.conn.nat.wait_for_snat(TestSnat.snat_rule)
        self.assertIsNotNone(TestSnat.snat_rule)

    def test_01_list_snat_rules(self):
        self._create_network()
        self._create_snat_rule()
        self.snat_rules = list(self.conn.nat.snat_rules())
        self.assertGreaterEqual(len(self.snat_rules), 0)

    def test_02_get_snat_rule(self):
        snat_rule = self.conn.nat.get_snat_rule(TestSnat.snat_rule.id)
        self.assertEqual(snat_rule.id, TestSnat.snat_rule.id)

    def test_03_delete_snat_rule(self):
        self.conn.nat.delete_snat_rule(snat=TestSnat.snat_rule)
        self.conn.nat.wait_for_delete_snat(TestSnat.snat_rule, interval=5, wait=250)
        self._destroy_network()
        try:
            snat_rule = self.conn.nat.get_snat_rule(TestSnat.snat_rule.id)
        except openstack.exceptions.ResourceNotFound:
            snat_rule = None
        self.assertIsNone(snat_rule)

