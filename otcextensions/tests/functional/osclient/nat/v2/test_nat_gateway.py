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


class TestNatGateway(common.NatTestCase):
    """Functional Tests for NAT Gateway"""

    @classmethod
    def setUpClass(cls):
        super(TestNatGateway, cls).setUpClass()

    def test_nat_gateway_list(self):
        json_output = json.loads(self.openstack(
            'nat gateway list -f json '
        ))
        self.assertIsNotNone(json_output)

    def test_nat_gateway_list_filters(self):
        json_output = json.loads(self.openstack(
            'nat gateway list -f json '
            '--limit 1 --id 2 '
            '--name 3 --spec 4 '
            '--router-id 5 '
            '--internal-network-id 6 '
            '--project-id 7 '
            '--status active '
            '--admin-state-up True '
            '--created-at "{}"'.format(self.CURR_TIME)
        ))
        self.assertIsNotNone(json_output)

    def test_nat_gateway(self):
        nat_gateway = self.create_nat_gateway()
        nat_id = nat_gateway['id']
        nat_name = nat_gateway['name']
        router_id = nat_gateway['router_id']

        self.addCleanup(self.delete_nat_gateway)

        # List Nat Gateway By Id
        json_output = json.loads(self.openstack(
            'nat gateway list -f json'
            ' --id {}'.format(nat_id)
        ))
        self.assertEqual(json_output[0]['Name'], nat_name)
        self.assertEqual(json_output[0]['Id'], nat_id)

        # List Nat Gateway By Name
        json_output = json.loads(self.openstack(
            'nat gateway list -f json'
            ' --name {}'.format(nat_name)
        ))
        self.assertEqual(json_output[0]['Name'], nat_name)
        self.assertEqual(json_output[0]['Id'], nat_id)

        # List Nat Gateway by Router ID
        json_output = json.loads(self.openstack(
            'nat gateway list -f json'
            ' --router-id {}'.format(router_id)
        ))
        for nat_gw in json_output:
            self.assertEqual(nat_gw['Router Id'], router_id)

        # Show Nat Gateway by Name
        json_output = json.loads(self.openstack(
            'nat gateway show -f json ' + nat_name
        ))
        self.assertEqual(json_output['name'], nat_name)
        self.assertEqual(json_output['id'], nat_id)

        # Show Nat Gateway by Id
        json_output = json.loads(self.openstack(
            'nat gateway show -f json ' + nat_id
        ))
        self.assertEqual(json_output['name'], nat_name)
        self.assertEqual(json_output['id'], nat_id)

        # Update Nat Gateway
        nat_name = nat_name + "-updated"
        description = "otce cli test nat updated"
        json_output = json.loads(self.openstack(
            'nat gateway update {nat_id} '
            '--name {name} '
            '--description "{desc}" '
            '-f json'.format(
                nat_id=nat_id,
                name=nat_name,
                desc=description)
        ))
        self.assertEqual(json_output['name'], nat_name)
        self.assertEqual(json_output['description'], description)
