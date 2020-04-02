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

from otcextensions.tests.functional.osclient.nat.v2 import common


class TestDnatRule(common.NatTestCase):
    """Functional Tests for NAT Gateway"""

    @classmethod
    def setUpClass(cls):
        super(TestDnatRule, cls).setUpClass()

    def test_nat_dnat_rule_list(self):
        json_output = json.loads(self.openstack(
            'nat dnat rule list -f json '
        ))
        self.assertIsNotNone(json_output)

    def test_nat_dnat_rule_list_filters(self):
        json_output = json.loads(self.openstack(
            'nat dnat rule list -f json '
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
            '--created-at "{}"'.format(self.CURR_TIME)
        ))
        self.assertIsNotNone(json_output)

    def test_nat_dnat_rule_create(self):
        json_output = self.create_dnat_rule()
        self.addCleanup(self.delete_dnat_rule)
        dnat_rule_id = json_output['id']
        nat_id = json_output['nat_gateway_id']

        # List Dnat Rules by Id filter
        json_output = json.loads(self.openstack(
            'nat dnat rule list -f json '
            '--id ' + dnat_rule_id
        ))
        self.assertIsNotNone(json_output)
        self.assertEqual(next(iter(json_output))['Id'], dnat_rule_id)
        self.assertEqual(
            next(iter(json_output))['Nat Gateway Id'], nat_id)

        # List Dnat Rules by Nat Id filter
        json_output = json.loads(self.openstack(
            'nat dnat rule list -f json '
            '--nat-gateway-id ' + nat_id
        ))
        self.assertIsNotNone(json_output)
        self.assertEqual(
            next(iter(json_output))['Nat Gateway Id'], nat_id)

        # Show Dnat Rule details
        json_output = json.loads(self.openstack(
            'nat dnat rule show '
            ' -f json ' + dnat_rule_id
        ))
        self.assertIsNotNone(json_output)
        self.assertEqual(json_output['id'], dnat_rule_id)
