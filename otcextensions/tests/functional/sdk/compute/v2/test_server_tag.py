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
from openstack import _log

from otcextensions.tests.functional import base

_logger = _log.setup_logging('openstack')


class TestServerTag(base.BaseFunctionalTest):
    cidr = '192.168.0.0/16'
    uuid_v4 = uuid.uuid4().hex[:8]
    vpc_name = 'server-test-vpc-' + uuid_v4
    subnet_name = 'server-test-subnet-' + uuid_v4
    server_name = 'server-test-' + uuid_v4
    kp_name = 'server-test-kp-' + uuid_v4
    image_name = 'Standard_Fedora_34_latest'
    flavor_name = 's3.medium.1'

    def setUp(self):
        super(TestServerTag, self).setUp()
        self.vpc = self.conn.vpc.create_vpc(
            name=self.vpc_name,
            cidr=self.cidr
        )
        self.assertEqual(self.vpc_name, self.vpc.name)
        gw, _ = self.cidr.split("/")
        self.subnet = self.conn.vpc.create_subnet(
            name=self.subnet_name,
            vpc_id=self.vpc.id,
            cidr=self.vpc.cidr,
            gateway_ip=gw[:-2] + ".1",
            dns_list=[
                "100.125.4.25",
                "100.125.129.199",
            ]
        )
        resource.wait_for_status(
            self.conn.vpc, self.subnet, "ACTIVE", None, 2, 20
        )
        self.assertEqual(self.subnet_name, self.subnet.name)

        image = self.conn.compute.find_image(self.image_name)
        flavor = self.conn.compute.find_flavor(self.flavor_name)
        self.keypair = self.conn.compute.create_keypair(name=self.kp_name)
        self.server = self.conn.compute.create_server(
            name=self.server_name,
            image_id=image.id,
            flavor_id=flavor.id,
            networks=[{"uuid": self.subnet.neutron_network_id}],
            key_name=self.keypair.name
        )
        self.server = self.conn.compute.wait_for_server(self.server)

    def tearDown(self):
        kp = self.conn.compute.find_keypair(self.kp_name)
        srv = self.conn.compute.find_server(self.server_name)
        self.conn.compute.delete_server(srv)
        self.conn.compute.wait_for_delete(
            srv, interval=5, wait=600)
        self.conn.compute.delete_keypair(kp)
        self.conn.compute.wait_for_delete(kp)

        resource.wait_for_status(
            self.conn.vpc, self.subnet, "ACTIVE", None, 2, 20
        )
        self.conn.vpc.delete_subnet(self.subnet, ignore_missing=False)
        resource.wait_for_delete(self.conn.vpc, self.subnet, 2, 60)

        sot = self.conn.vpc.delete_vpc(self.vpc)
        self.assertIsNotNone(sot)
        super(TestServerTag, self).tearDown()

    def test_tags_workflow(self):
        instance = self.conn.compute.get_server(self.server)
        self.assertEqual(len(instance.tags), 0)
        self.server.add_tag(self.conn.compute, 'pytest=test1')
        self.assertEqual(len(instance.tags), 1)
        self.server.remove_tag(self.conn.compute, 'pytest=test1')
        self.assertEqual(len(instance.tags), 0)
