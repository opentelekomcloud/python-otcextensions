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
        uuid_v4 = uuid.uuid4().hex[:8]
        vpc_name = 'snat-test-vpc-' + uuid_v4
        subnet_name = 'snat-test-subnet-' + uuid_v4

        if not TestSnat.network_info:
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

            TestSnat.network_info = {
                'vpc_id': vpc_id,
                'subnet_id': subnet_id,
                'network_id': network_id,
                'subnet': subnet,
                'vpc': vpc
            }
        if not TestSnat.gateway:
            self.attrs['router_id'] = TestSnat.network_info['vpc_id']
            self.attrs['internal_network_id'] =\
                TestSnat.network_info['network_id']
            TestSnat.gateway = self.conn.nat.create_gateway(**self.attrs)
            self.conn.nat.wait_for_gateway(TestSnat.gateway)
            self.assertIsNotNone(TestSnat.gateway)
        if not TestSnat.floating_ip:
            admin_external_net = self.conn.network.find_network(
                name_or_id='admin_external_net')
            self.assertIsNotNone(admin_external_net)
            TestSnat.floating_ip = self.conn.network.create_ip(
                floating_network_id=admin_external_net.id)

    def _destroy_network(self):
        if TestSnat.gateway:
            self.conn.nat.delete_gateway(gateway=TestSnat.gateway)
            self.conn.nat.wait_for_delete_gateway(TestSnat.gateway,
                                                  interval=4, wait=500)
            TestSnat.gateway = None
        if TestSnat.floating_ip:
            self.conn.network.delete_ip(TestSnat.floating_ip)
            TestSnat.floating_ip = None

        if TestSnat.network_info:
            vpc = TestSnat.network_info['vpc']
            subnet = TestSnat.network_info['subnet']

            resource.wait_for_status(self.conn.vpc, subnet, "ACTIVE", None, 2, 20)
            self.conn.vpc.delete_subnet(subnet, ignore_missing=False)
            resource.wait_for_delete(self.conn.vpc, subnet, 2, 60)

            sot = self.conn.vpc.delete_vpc(vpc)
            self.assertIsNotNone(sot)

            TestSnat.network_info = None

    def _create_snat_rule(self):
        TestSnat.snat_rule = self.conn.nat.create_snat_rule(
            floating_ip_id=TestSnat.floating_ip.id,
            nat_gateway_id=TestSnat.gateway.id,
            cidr='192.168.0.0/16')
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
        try:
            self.conn.nat.delete_snat_rule(snat=TestSnat.snat_rule)
            self.conn.nat.wait_for_delete_snat(TestSnat.snat_rule,
                                               interval=5, wait=250)
        except openstack.exceptions.InvalidRequest:
            self._destroy_network()
            raise
        self._destroy_network()
        try:
            snat_rule = self.conn.nat.get_snat_rule(TestSnat.snat_rule.id)
        except openstack.exceptions.ResourceNotFound:
            snat_rule = None
        self.assertIsNone(snat_rule)
