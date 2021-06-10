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

from otcextensions.tests.functional import base


_logger = openstack._log.setup_logging('openstack')


class TestGateway(base.BaseFunctionalTest):

    CIDR = "192.168.0.0/24"
    IPV4 = 4
    VPC_ID = None
    NETWORK_ID = None
    SUBNET_ID = None
    GATEWAY_ID = None
    SPEC = 1
    ID = None

    def _initialize_network(self):
        network = self.conn.network.create_network(name=self.NETWORK_NAME)
        self.NETWORK_ID = network.id

        subnet = self.conn.network.create_subnet(
            name=self.SUBNET_NAME,
            ip_version=self.IPV4,
            network_id=self.NETWORK_ID,
            cidr=self.CIDR
        )
        self.SUBNET_ID = subnet.id

        vpc = self.conn.network.create_router(name=self.VPC_NAME)

        self.VPC_ID = vpc.id
        interface = vpc.add_interface(self.conn.network,
                                         subnet_id=self.SUBNET_ID)

    def setUp(self):
        super(TestGateway, self).setUp()
        self.GATEWAY_NAME = self.getUniqueString('gateway')
        self.UPDATE_NAME = self.getUniqueString('updated-gateway')
        self.NETWORK_NAME = self.getUniqueString('network')
        self.SUBNET_NAME = self.getUniqueString('subnet')
        self.VPC_NAME = self.getUniqueString('vpc')
        self._initialize_network()
        gateway = self.conn.nat.create_gateway(
            name=self.GATEWAY_NAME, internal_network_id=self.network['id'],
            router_id=self.vpc['id'], spec=self.spec)
        self.conn.nat.wait_for_gateway(gateway=gateway)
        self.ID = gateway['id']

    def test_find_gateway(self):
        gw = self.conn.nat.find_gateway(self.GATEWAY_NAME)
        self.assertEqual(self.ID, gw.id)

    def test_get(self):
        gw = self.conn.nat.get_gateway(self.ID)
        self.assertEqual(self.GATEWAY_NAME, gw.name)
        self.assertEqual(self.ID, gw.id)

    def test_update(self):
        gw = self.conn.network.update_gateway(self.ID, 
                                              name=self.UPDATE_NAME)
        self.assertEqual(self.UPDATE_NAME, gw.name)

    def test_list(self):
        gateways = list(self.conn.nat.gateways())
        self.assertGreaterEqual(len(gateways), 0)

    def test_list_filters(self):
        attrs = {
            'limit': 1,
            'id': '2',
            'name': '3',
            'spec': '4',
            'router_id': '5',
            'internal_network_id': '6',
            'project_id': '7',
            'status': 'active',
            'admin_state_up': True,
            'created_at': self.CURR_TIME
        }
        gateways = list(self.conn.nat.gateways(**attrs))
        self.assertGreaterEqual(len(gateways), 0)

    def tearDown(self):
        gw = self.conn.nat.delete_gateway(self.ID, ignore_missing=True)
        self.assertIsNone(gw)
        self._deinitialize_network()
        super(TestGateway, self).tearDown()

    def _deinitialize_network(self):
        router = self.conn.network.get_router(self.ROUTER_ID)
        router.remove_interface(self.conn.network,
                                subnet_id=self.SUBNET_ID)
        self.conn.network.delete_router(
            self.ROUTER_ID, ignore_missing=False)
        self.conn.network.delete_subnet(
            self.SUBNET_ID, ignore_missing=False)
        self.conn.network.delete_network(
            self.NET_ID, ignore_missing=False)
        self.conn.network.delete_security_group(
            self.SG_ID, ignore_missing=False)
