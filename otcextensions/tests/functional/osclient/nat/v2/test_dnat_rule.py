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


class TestDnatRule(base.TestCase):
    """Functional Tests for NAT Gateway"""

    UUID = uuid.uuid4().hex[:8]
    ROUTER_NAME = 'sdk-test-router-' + UUID
    NETWORK_NAME = 'sdk-test-net-' + UUID
    SUBNET_NAME = 'sdk-test-subnet-' + UUID
    PORT_NAME = 'sdk-test-port-' + UUID
    ROUTER_ID = None
    NETWORK_ID = None
    FLOATING_IP_ID = None
    PORT_ID = None

    NAT_NAME = 'os-cli-test-' + UUID
    NAT_ID = None
    DNAT_RULE_ID = None

    def test_01_nat_dnat_rule_list(self):
        self.openstack(
            'nat dnat rule list -f json '
        )

    def test_02_nat_dnat_rule_list_filters(self):
        self.openstack(
            'nat dnat rule list '
            '--limit 1 --id 2 '
            '--project-id 3 '
            '--port-id 4 '
            '--private-ip 5 '
            '--internal-service-port 6 '
            '--floating-ip-id 7 '
            '--floating-ip-address 8 '
            '--external-service-port 9 '
            '--status 10 '
            '--nat-gateway-id 11 '
            '--protocol tcp '
            '--admin-state-up true '
        )

    def test_03_nat_dnat_rule_create(self):
        self._create_nat_gateway()
        self.assertIsNotNone(self.PORT_ID)
        self.assertIsNotNone(self.FLOATING_IP_ID)
        json_output = json.loads(self.openstack(
            'nat dnat rule create '
            '--nat-gateway-id {nat_gateway_id} '
            '--floating-ip-id {floating_ip_id} '
            '--protocol {protocol} '
            '--internal-service-port 80 '
            '--external-service-port 80 '
            '--private-ip {private_ip} '
            '-f json'.format(
                nat_gateway_id=self.NAT_ID,
                protocol='TCP',
                private_ip='192.168.0.3',
                floating_ip_id=self.FLOATING_IP_ID)
        ))
        self.assertIsNotNone(json_output)
        TestDnatRule.DNAT_RULE_ID = json_output['id']

    def test_04_nat_dnat_rule_list_by_id(self):
        self.assertIsNotNone(self.DNAT_RULE_ID)
        json_output = json.loads(self.openstack(
            'nat dnat rule list -f json '
            '--id ' + self.DNAT_RULE_ID
        ))
        self.assertIsNotNone(json_output)
        self.assertEqual(next(iter(json_output))['Id'], self.DNAT_RULE_ID)
        self.assertEqual(
            next(iter(json_output))['Nat Gateway Id'], self.NAT_ID)

    def test_05_nat_dnat_rule_list_by_nat_id(self):
        self.assertIsNotNone(self.DNAT_RULE_ID)
        json_output = json.loads(self.openstack(
            'nat dnat rule list -f json '
            '--nat-gateway-id ' + self.NAT_ID
        ))
        self.assertIsNotNone(json_output)
        self.assertEqual(
            next(iter(json_output))['Nat Gateway Id'], self.NAT_ID)

    def test_06_nat_dnat_rule_show(self):
        self.assertIsNotNone(self.DNAT_RULE_ID)
        json_output = json.loads(self.openstack(
            'nat dnat rule show '
            ' -f json ' + self.DNAT_RULE_ID
        ))
        self.assertIsNotNone(json_output)
        self.assertEqual(json_output['id'], self.DNAT_RULE_ID)

    def test_07_nat_dnat_rule_delete(self):
        self.addCleanup(self._delete_nat_gateway)
        self.assertIsNotNone(self.NAT_ID)
        self.assertIsNotNone(self.DNAT_RULE_ID)
        self.openstack(
            'nat dnat rule delete ' + self.DNAT_RULE_ID)

    def _create_nat_gateway(self):
        self._initialize_network()
        json_output = json.loads(self.openstack(
            'nat gateway create {name}'
            ' --router-id {router_id}'
            ' --internal-network-id {net_id}'
            ' --spec {spec} -f json'.format(
                name=self.NAT_NAME,
                router_id=self.ROUTER_ID,
                net_id=self.NETWORK_ID,
                description='OTCE Lib Test',
                spec=1)
        ))
        TestDnatRule.NAT_ID = json_output['id']

    def _delete_nat_gateway(self):
        self.addCleanup(self._denitialize_network)
        self.openstack('nat gateway delete ' + self.NAT_ID)

    def _initialize_network(self):
        router = json.loads(self.openstack(
            'router create -f json ' + self.ROUTER_NAME
        ))
        network = json.loads(self.openstack(
            'network create -f json ' + self.NETWORK_NAME
        ))
        self.openstack(
            'subnet create {subnet} -f json '
            '--network {net} '
            '--subnet-range 192.168.0.0/24 '.format(
                subnet=self.SUBNET_NAME,
                net=self.NETWORK_NAME
            ))

        self.openstack(
            'router add subnet {router} '
            '{subnet} '.format(
                router=self.ROUTER_NAME,
                subnet=self.SUBNET_NAME
            )
        )

        floating_ip = json.loads(self.openstack(
            'floating ip create -f json '
            '{network}'.format(
                network='admin_external_net')
        ))

        TestDnatRule.ROUTER_ID = router['id']
        TestDnatRule.NETWORK_ID = network['id']
        TestDnatRule.FLOATING_IP_ID = floating_ip['id']

        port = json.loads(self.openstack(
            'port create {name} '
            '--network {net_id} '
            '-f json'.format(
                name=self.PORT_NAME,
                net_id=self.NETWORK_ID)
        ))
        TestDnatRule.PORT_ID = port['id']

    def _denitialize_network(self):
        self.openstack(
            'port delete ' + self.PORT_NAME
        )
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
            'network delete ' + self.NETWORK_NAME
        )
        self.openstack(
            'router delete ' + self.ROUTER_NAME
        )
        self.openstack(
            'floating ip delete ' + self.FLOATING_IP_ID
        )
