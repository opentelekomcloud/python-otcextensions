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
from tempest.lib.exceptions import CommandFailed


class TestSnatRule(base.TestCase):
    """Functional Tests for NAT Gateway"""

    UUID = uuid.uuid4().hex[:8]
    ROUTER_NAME = 'sdk-test-router-' + UUID
    NET_NAME = 'sdk-test-net-' + UUID
    SUBNET_NAME = 'sdk-test-subnet-' + UUID
    ROUTER_ID = None
    NET_ID = None
    FLOATING_IP_ID = None

    NAT_NAME = 'os-cli-test-' + UUID
    NAT_ID = None
    SNAT_RULE_ID = None

    def test_01_snat_rule_list(self):
        self.openstack(
            'nat snat rule list -f json '
        )

    def test_02_snat_rule_list_filters(self):
        self.openstack(
            'nat snat rule list '
            '--limit 1 --id 2 '
            '--project-id 3 '
            '--nat-gateway-id 4 '
            '--network-id 5 '
            '--cidr 6 '
            '--source-type 7 '
            '--floating-ip-id 8 '
            '--floating-ip-address 9 '
            '--status 10 '
            '--admin-state-up true '
        )

    def test_03_nat_snat_rule_create(self):
        self._create_nat_gateway()
        self.assertIsNotNone(self.NAT_ID)
        self.assertIsNotNone(self.FLOATING_IP_ID)
        json_output = json.loads(self.openstack(
            'nat snat rule create {nat_gateway_id} '
            '--floating-ip-id {floating_ip_id} '
            '--net-id {net_id} -f json'.format(
                nat_gateway_id=self.NAT_ID,
                floating_ip_id=self.FLOATING_IP_ID,
                net_id=self.NET_ID)
        ))
        self.assertIsNotNone(json_output)
        TestSnatRule.SNAT_RULE_ID = json_output['id']

    def test_04_nat_snat_rule_list_by_id(self):
        self.assertIsNotNone(self.SNAT_RULE_ID)
        json_output = json.loads(self.openstack(
            'nat snat rule list -f json '
            '--id ' + self.SNAT_RULE_ID
        ))
        self.assertIsNotNone(json_output)
        self.assertEqual(next(iter(json_output))['Id'], self.SNAT_RULE_ID)
        self.assertEqual(
            next(iter(json_output))['Nat Gateway Id'], self.NAT_ID)

    def test_05_nat_snat_rule_list_by_nat_id(self):
        self.assertIsNotNone(self.SNAT_RULE_ID)
        json_output = json.loads(self.openstack(
            'nat snat rule list -f json '
            '--nat-gateway-id ' + self.NAT_ID
        ))
        self.assertIsNotNone(json_output)
        self.assertEqual(
            next(iter(json_output))['Nat Gateway Id'], self.NAT_ID)

    def test_06_nat_snat_rule_show(self):
        self.assertIsNotNone(self.SNAT_RULE_ID)
        json_output = json.loads(self.openstack(
            'nat snat rule show '
            ' -f json ' + self.SNAT_RULE_ID
        ))
        self.assertIsNotNone(json_output)
        self.assertEqual(json_output['id'], self.SNAT_RULE_ID)

    def test_07_nat_snat_rule_create_for_existing_network(self):
        self.assertIsNotNone(self.NAT_ID)
        self.assertIsNotNone(self.FLOATING_IP_ID)
        self.assertRaises(
            CommandFailed,
            self.openstack,
            'nat snat rule create '
            '{nat_id} {floating_ip_id} '
            '--net-id {net_id} -f json'.format(
                nat_id=self.NAT_ID,
                floating_ip_id=self.FLOATING_IP_ID,
                net_id=self.NET_ID)
        )

    def test_08_nat_snat_rule_create_cidr_source_type(self):
        self.assertIsNotNone(self.NAT_ID)
        self.assertIsNotNone(self.FLOATING_IP_ID)
        json_output = json.loads(self.openstack(
            'nat snat rule create {nat_gateway_id} '
            '--floating-ip-id {floating_ip_id} '
            '--source-type {source_type} '
            '--cidr {cidr} -f json'.format(
                nat_gateway_id=self.NAT_ID,
                floating_ip_id=self.FLOATING_IP_ID,
                source_type=1,
                cidr='192.168.5.0/24')
        ))
        self.assertEqual(json_output['source_type'], 1)
        self.openstack(
            'nat snat rule delete ' + json_output['id'])

    def test_09_nat_snat_rule_delete(self):
        self.addCleanup(self._delete_nat_gateway)
        self.assertIsNotNone(self.NAT_ID)
        self.assertIsNotNone(self.SNAT_RULE_ID)
        self.openstack(
            'nat snat rule delete ' + self.SNAT_RULE_ID)

    def _create_nat_gateway(self):
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
        TestSnatRule.NAT_ID = json_output['id']

    def _delete_nat_gateway(self):
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

        floating_ip = json.loads(self.openstack(
            'floating ip create -f json '
            '{network}'.format(
                network='admin_external_net')
        ))

        TestSnatRule.ROUTER_ID = router['id']
        TestSnatRule.NET_ID = net['id']
        TestSnatRule.FLOATING_IP_ID = floating_ip['id']

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
        self.openstack(
            'floating ip delete ' + self.FLOATING_IP_ID
        )
