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


class TestSnatRule(common.NatTestCase):
    """Functional Tests for NAT Gateway"""

    @classmethod
    def setUpClass(cls):
        super(TestSnatRule, cls).setUpClass()

    def test_snat_rule_list(self):
        json_output = json.loads(self.openstack(
            'nat snat rule list -f json '
        ))
        self.assertIsNotNone(json_output)

    def test_snat_rule_list_filters(self):
        json_output = json.loads(self.openstack(
            'nat snat rule list -f json '
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
        ))
        self.assertIsNotNone(json_output)

    def test_nat_snat_rule_create(self):
        json_output = self.create_snat_rule()
        self.addCleanup(self.delete_snat_rule)
        snat_rule_id = json_output['id']
        nat_id = json_output['nat_gateway_id']

        # List Snat Rule by Snat Id filter
        json_output = json.loads(self.openstack(
            'nat snat rule list -f json '
            '--id ' + snat_rule_id
        ))
        self.assertIsNotNone(json_output)
        self.assertEqual(next(iter(json_output))['Id'], snat_rule_id)
        self.assertEqual(
            next(iter(json_output))['Nat Gateway Id'], nat_id)

        # List Snat Rule by nat-gateway-id filter
        json_output = json.loads(self.openstack(
            'nat snat rule list -f json '
            '--nat-gateway-id ' + nat_id
        ))
        self.assertIsNotNone(json_output)
        self.assertEqual(
            next(iter(json_output))['Nat Gateway Id'], nat_id)

        # Show Snat Rule by Id
        self.assertIsNotNone(self.SNAT_RULE_ID)
        json_output = json.loads(self.openstack(
            'nat snat rule show '
            ' -f json ' + self.SNAT_RULE_ID
        ))
        self.assertIsNotNone(json_output)
        self.assertEqual(json_output['id'], self.SNAT_RULE_ID)
