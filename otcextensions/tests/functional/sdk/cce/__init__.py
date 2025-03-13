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
import uuid

from openstack import resource

from otcextensions.tests.functional import base


class TestCce(base.BaseFunctionalTest):
    uuid_v4 = uuid.uuid4().hex[:8]
    network = None
    cluster = None

    def setUp(self):
        super(TestCce, self).setUp()
        self.client = self.conn.cce
        self.vpc = self.conn.vpc

    def create_cluster(
            self,
            name='sdk-cce-test-' + uuid_v4,
            description='test',
            flavor='cce.s1.small',
            container_network_mode='overlay_l2',
            cluster_type='VirtualMachine',
            **kwargs
    ):
        attrs = {
            'name': name,
            'description': description,
            'flavor': flavor,
            'container_network_mode': container_network_mode,
            'type': cluster_type,
            'router': TestCce.network['router'].id,
            'network': TestCce.network['network_id'],
            'wait_interval': 10,
            'wait': True,
            **kwargs
        }
        if TestCce.network and not TestCce.cluster:
            TestCce.cluster = self.conn.create_cce_cluster(**attrs)

    def create_network(
            self,
            cidr='192.168.0.0/16',
            router_name='sdk-cce-test-router-',
            subnet_name='sdk-cce-test-subnet-'
    ):
        uuid_v4 = uuid.uuid4().hex[:8]
        router_name += uuid_v4
        subnet_name += uuid_v4
        if not TestCce.network:
            vpc = self.conn.vpc.create_vpc(
                name=router_name,
                cidr=cidr
            )
            self.assertEqual(router_name, vpc.name)
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
            resource.wait_for_status(
                self.conn.vpc, subnet, "ACTIVE", None, 2, 20
            )
            self.assertEqual(subnet_name, subnet.name)
            network_id = subnet.neutron_network_id

            TestCce.network = {
                'router': vpc,
                'subnet': subnet,
                'network_id': network_id
            }
        return

    def _destroy_network(self):
        if TestCce.network:
            vpc = TestCce.network['router']
            subnet = TestCce.network['subnet']

            self.conn.vpc.delete_subnet(subnet, ignore_missing=False)
            resource.wait_for_delete(self.conn.vpc, subnet, 2, 60)

            sot = self.conn.vpc.delete_vpc(vpc)
            self.assertIsNotNone(sot)

            TestCce.network_info = None
