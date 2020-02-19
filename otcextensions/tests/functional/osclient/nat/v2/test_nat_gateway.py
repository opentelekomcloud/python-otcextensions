#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import json
import uuid

from openstackclient.tests.functional import base


class TestNatGateway(base.TestCase):
    """Functional Tests for NAT Gateway"""

    UUID = uuid.uuid4().hex[:8]
    ROUTER_NAME = 'sdk-test-router-' + UUID
    NET_NAME = 'sdk-test-net-' + UUID
    SUBNET_NAME = 'sdk-test-subnet-' + UUID
    ROUTER_ID = None
    NET_ID = None

    NAT_NAME = 'os-cli-test-' + UUID
    NAT_ID = None

    def test_01_nat_gateway_list(self):
        self.openstack(
            'nat gateway list -f json '
        )

    def test_02_gat_gateway_list_filters(self):
        self.openstack(
            'nat gateway list '
            '--limit 1 --id 2 '
            '--name 3 --spec 1 '
            '--router-id 123asd '
            '--internal-network-id 123qwe '
            '--status Active '
            '--admin-state-up True '
        )

    def test_03_nat_gateway_create(self):
        self._initialize_network()
        json_output = json.loads(self.openstack(
            'nat gateway create {name}'
            ' --router-id {router_id}'
            ' --internal-network-id {net_id}'
            ' --spec {spec} -f json'.format(
                name=self.NAT_NAME,
                router_id=self.ROUTER_ID,
                net_id=self.NET_ID,
                description='OTCE Lib Test',
                spec=1)
        ))
        self.assertIsNotNone(json_output)
        TestNatGateway.NAT_ID = json_output['id']

    def test_04_nat_gateway_list_by_id(self):
        json_output = json.loads(self.openstack(
            'nat gateway list -f json'
            ' --id {}'.format(self.NAT_ID)
        ))
        self.assertEqual(json_output[0]['Name'], self.NAT_NAME)
        self.assertEqual(json_output[0]['Id'], self.NAT_ID)

    def test_05_nat_gateway_list_by_name(self):
        json_output = json.loads(self.openstack(
            'nat gateway list -f json'
            ' --name {}'.format(self.NAT_NAME)
        ))
        self.assertEqual(json_output[0]['Name'], self.NAT_NAME)
        self.assertEqual(json_output[0]['Id'], self.NAT_ID)

    def test_06_nat_gateway_list_by_router_id(self):
        json_output = json.loads(self.openstack(
            'nat gateway list -f json'
            ' --router-id {}'.format(self.ROUTER_ID)
        ))
        for nat_gw in json_output:
            self.assertEqual(nat_gw['Router Id'], self.ROUTER_ID)

    def test_07_nat_gateway_show_by_name(self):
        json_output = json.loads(self.openstack(
            'nat gateway show -f json ' + self.NAT_NAME
        ))
        self.assertEqual(json_output['name'], self.NAT_NAME)
        self.assertEqual(json_output['id'], self.NAT_ID)

    def test_08_nat_gateway_show_by_id(self):
        json_output = json.loads(self.openstack(
            'nat gateway show -f json ' + self.NAT_ID
        ))
        self.assertEqual(json_output['name'], self.NAT_NAME)
        self.assertEqual(json_output['id'], self.NAT_ID)

    def test_09_nat_gateway_update_by_id(self):
        name = self.NAT_NAME + "-updated"
        description = "otce cli test nat updated"
        json_output = json.loads(self.openstack(
            'nat gateway update {nat_id} '
            '--name {name} '
            '--description "{desc}" '
            '-f json'.format(
                nat_id=self.NAT_ID,
                name=name,
                desc=description)
        ))
        self.assertEqual(json_output['name'], name)
        self.assertEqual(json_output['description'], description)
        TestNatGateway.NAT_NAME = json_output['name']

    def test_10_nat_gateway_update_by_name(self):
        name = 'os-cli-test-' + self.UUID
        description = "otce cli test nat"
        json_output = json.loads(self.openstack(
            'nat gateway update {nat_name} '
            '--name {name} '
            '--description "{desc}" '
            '--spec {spec} '
            '-f json'.format(
                nat_name=self.NAT_NAME,
                name=name,
                spec=2,
                desc=description)
        ))
        self.assertEqual(json_output['name'], name)
        self.assertEqual(json_output['description'], description)
        TestNatGateway.NAT_NAME = json_output['name']

    def test_11_nat_gateway_delete(self):
        self.addCleanup(self._denitialize_network)
        self.openstack('nat gateway delete ' + self.NAT_ID)

    def _initialize_network(self):
        router = json.loads(self.openstack(
            'router create -f json ' + self.ROUTER_NAME
        ))
        net = json.loads(self.openstack(
            'network create -f json ' + self.NET_NAME
        ))
        self.openstack(
            'subnet create {subnet} -f json '
            '--network {net} '
            '--subnet-range 192.168.0.0/24 '.format(
                subnet=self.SUBNET_NAME,
                net=self.NET_NAME
            ))

        self.openstack(
            'router add subnet {router} '
            '{subnet} '.format(
                router=self.ROUTER_NAME,
                subnet=self.SUBNET_NAME
            )
        )

        TestNatGateway.ROUTER_ID = router['id']
        TestNatGateway.NET_ID = net['id']

    def _denitialize_network(self):
        self.openstack(
            'router remove subnet {router} '
            '{subnet} '.format(
                router=self.ROUTER_NAME,
                subnet=self.SUBNET_NAME
            )
        )
        self.openstack(
            'subnet delete ' + self.SUBNET_NAME
        )
        self.openstack(
            'network delete ' + self.NET_NAME
        )
        self.openstack(
            'router delete ' + self.ROUTER_NAME
        )
