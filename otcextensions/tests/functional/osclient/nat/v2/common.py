#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

import json
import uuid

from datetime import datetime

from openstackclient.tests.functional import base


class NatTestCase(base.TestCase):
    """Common functional test bits for NAT commands"""

    CURR_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    def setUp(self):
        super(NatTestCase, self).setUp()
        UUID = uuid.uuid4().hex[:8]
        self.ROUTER_NAME = 'otce-nat-test-router-' + UUID
        self.NETWORK_NAME = 'otce-nat-test-net-' + UUID
        self.SUBNET_NAME = 'otce-nat-test-subnet-' + UUID
        self.NAT_NAME = 'otce-nat-test-' + UUID

        self.ROUTER_ID = None
        self.NETWORK_ID = None
        self.FLOATING_IP_ID = None
        self.NAT_ID = None
        self.SNAT_RULE_ID = None
        self.DNAT_RULE_ID = None

    def create_nat_gateway(self, name=None):
        self._initialize_network()
        name = name or self.SUBNET_NAME
        json_output = json.loads(self.openstack(
            'nat gateway create {name}'
            ' --router-id {router_id}'
            ' --internal-network-id {net_id}'
            ' --spec {spec} -f json'.format(
                name=name,
                router_id=self.ROUTER_ID,
                net_id=self.NETWORK_ID,
                description='OTCE Lib Test',
                spec=1)
        ))
        self.assertIsNotNone(json_output)
        self.NAT_ID = json_output['id']
        return json_output

    def delete_nat_gateway(self):
        self.addCleanup(self._denitialize_network)
        self.openstack('nat gateway delete ' + self.NAT_ID)

    def create_snat_rule(self):
        nat_gateway = self.create_nat_gateway()
        self.assertIsNotNone(nat_gateway)
        self.assertIsNotNone(self.FLOATING_IP_ID)
        json_output = json.loads(self.openstack(
            'nat snat rule create '
            '--nat-gateway-id {nat_gateway_id} '
            '--floating-ip-id {floating_ip_id} '
            '--network-id {net_id} -f json'.format(
                nat_gateway_id=nat_gateway['id'],
                floating_ip_id=self.FLOATING_IP_ID,
                net_id=self.NETWORK_ID)
        ))
        self.assertIsNotNone(json_output)
        self.SNAT_RULE_ID = json_output['id']
        return json_output

    def delete_snat_rule(self):
        self.addCleanup(self.delete_nat_gateway)
        self.openstack(
            'nat snat rule delete ' + self.SNAT_RULE_ID)

    def create_dnat_rule(self):
        nat_gateway = self.create_nat_gateway()
        self.assertIsNotNone(nat_gateway)
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
                nat_gateway_id=nat_gateway['id'],
                protocol='TCP',
                private_ip='192.168.0.3',
                floating_ip_id=self.FLOATING_IP_ID)
        ))
        self.assertIsNotNone(json_output)
        self.DNAT_RULE_ID = json_output['id']
        return json_output

    def delete_dnat_rule(self):
        self.addCleanup(self.delete_nat_gateway)
        self.openstack(
            'nat dnat rule delete ' + self.DNAT_RULE_ID)

    def _initialize_network(self):
        router = json.loads(self.openstack(
            'router create -f json ' + self.ROUTER_NAME
        ))
        net = json.loads(self.openstack(
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

        self.ROUTER_ID = router['id']
        self.NETWORK_ID = net['id']
        self.FLOATING_IP_ID = floating_ip['id']

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
            'network delete ' + self.NETWORK_NAME
        )
        self.openstack(
            'router delete ' + self.ROUTER_NAME
        )
        self.openstack(
            'floating ip delete ' + self.FLOATING_IP_ID
        )
