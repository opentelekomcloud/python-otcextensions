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
from openstack import resource

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
    image = "Standard_Ubuntu_20.04_latest"
    kp_name = uuid_v4 + "test-dnat-kp"
    fixed_ip = "192.168.0.10"
    attrs = {
        "name": gateway_name,
        "spec": "1"
    }
    AZ = 'eu-de-01'

    def _create_network(self):
        cidr = '192.168.0.0/16'
        uuid_v4 = uuid.uuid4().hex[:8]
        vpc_name = 'dnat-test-vpc-' + uuid_v4
        subnet_name = 'dnat-test-subnet-' + uuid_v4

        if not TestDnat.network_info:
            vpc = self.conn.vpc.create_vpc(
                name=vpc_name,
                cidr=cidr
            )
            self.assertEqual(vpc_name, vpc.name)
            vpc_id = vpc.id
            gw, _ = cidr.split("/")
            subnet = self.conn.vpc.create_subnet(
                name=subnet_name,
                vpc_id=vpc.id,
                cidr=vpc.cidr,
                gateway_ip=gw[:-2] + ".1",
                dns_list=[
                    "100.125.4.25",
                    "100.125.129.199",
                ]
            )
            resource.wait_for_status(self.conn.vpc, subnet, "ACTIVE", None, 2, 20)
            self.assertEqual(subnet_name, subnet.name)
            subnet_id = subnet.id
            network_id = subnet.neutron_network_id

            TestDnat.network_info = {
                'vpc_id': vpc_id,
                'subnet_id': subnet_id,
                'network_id': network_id,
                'subnet': subnet,
                'vpc': vpc
            }
        if not TestDnat.gateway:
            self.attrs['router_id'] = TestDnat.network_info['vpc_id']
            self.attrs['internal_network_id'] = \
                TestDnat.network_info['network_id']
            TestDnat.gateway = self.conn.nat.create_gateway(**self.attrs)
            self.conn.nat.wait_for_gateway(TestDnat.gateway)
            self.assertIsNotNone(TestDnat.gateway)
        if not TestDnat.floating_ip:
            admin_external_net = self.conn.network.find_network(
                name_or_id='admin_external_net')
            self.assertIsNotNone(admin_external_net)
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
            # TODO: blacklisted now, because OTC had lack of nova apis
            # for releasing fixed_ip
            self.conn.compute.delete_server(TestDnat.server)
            self.conn.compute.wait_for_delete(
                TestDnat.server, interval=5, wait=600)
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
            vpc = TestDnat.network_info['vpc']
            subnet = TestDnat.network_info['subnet']

            resource.wait_for_status(self.conn.vpc, subnet, "ACTIVE", None, 2, 20)
            self.conn.vpc.delete_subnet(subnet, ignore_missing=False)
            resource.wait_for_delete(self.conn.vpc, subnet, 2, 60)

            sot = self.conn.vpc.delete_vpc(vpc)
            self.assertIsNotNone(sot)

            TestDnat.network_info = None

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
        try:
            self.conn.nat.delete_dnat_rule(dnat=TestDnat.dnat_rule)
            self.conn.nat.wait_for_delete_dnat(TestDnat.dnat_rule)
        except openstack.exceptions.InvalidRequest:
            self._destroy_network()
            raise
        self._destroy_network()
        try:
            dnat_rule = self.conn.nat.get_dnat_rule(TestDnat.dnat_rule.id)
        except openstack.exceptions.ResourceNotFound:
            dnat_rule = None
        self.assertIsNone(dnat_rule)
