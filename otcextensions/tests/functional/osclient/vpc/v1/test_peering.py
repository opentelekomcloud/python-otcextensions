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

from otcextensions.tests.functional.osclient.vpc.v1 import common


class TestPeering(common.VpcTestCase):
    """Functional Tests for NAT Gateway"""

    def setUp(self):
        super(TestPeering, self).setUp()

    def test_vpc_peering_list(self):
        json_output = json.loads(self.openstack(
            'vpc peering list -f json '
        ))
        self.assertIsNotNone(json_output)

    def test_vpc_peering_list_filters(self):
        json_output = json.loads(self.openstack(
            'vpc peering list -f json '
            '--limit 1 '
            '--id 2 '
            '--name 3 '
            '--project-id 4 '
            '--router-id 5 '
            '--status ACTIVE '
        ))
        self.assertIsNotNone(json_output)

    def test_vpc_peering(self):
        self.addCleanup(self.delete_vpc_peering)
        peering = self.create_vpc_peering()
        peering_id = peering['id']
        peering_name = peering['name']
        local_router_id = peering['local_vpc_info']['router_id']
        peer_router_id = peering['peer_vpc_info']['router_id']

        # List Vpc Peering By Id
        json_output = json.loads(self.openstack(
            'vpc peering list -f json '
            '--id {}'.format(peering_id)
        ))
        self.assertEqual(json_output[0]['Name'], peering_name)
        self.assertEqual(json_output[0]['Id'], peering_id)

        # List Vpc Peering By Name
        json_output = json.loads(self.openstack(
            'vpc peering list -f json '
            '--name {}'.format(peering_name)
        ))
        self.assertEqual(json_output[0]['Name'], peering_name)
        self.assertEqual(json_output[0]['Id'], peering_id)

        # List Vpc Peering by Requester Router ID
        json_output = json.loads(self.openstack(
            'vpc peering list -f json '
            '--router-id {}'.format(local_router_id)
        ))
        self.assertIsNotNone(json_output)

        # List Vpc Peering by Accepter Router ID
        json_output = json.loads(self.openstack(
            'vpc peering list -f json '
            '--router-id {}'.format(peer_router_id)
        ))
        for peering in json_output:
            self.assertEqual(
                peering['Peer Router Id'],
                peer_router_id
            )

        # Show Vpc Peering by Name
        json_output = json.loads(self.openstack(
            'vpc peering show -f json ' + peering_name
        ))
        self.assertEqual(json_output['name'], peering_name)
        self.assertEqual(json_output['id'], peering_id)

        # Show Vpc Peering by Id
        json_output = json.loads(self.openstack(
            'vpc peering show -f json ' + peering_id
        ))
        self.assertEqual(json_output['name'], peering_name)
        self.assertEqual(json_output['id'], peering_id)

        # Update Vpc Peering
        peering_name = peering_name + "-updated"
        description = "test vpc peering updated by otce cli"
        json_output = json.loads(self.openstack(
            'vpc peering update {peering_id} '
            '--name {name} '
            '--description "{desc}" '
            '-f json'.format(
                peering_id=peering_id,
                name=peering_name,
                desc=description)
        ))
        self.assertEqual(json_output['name'], peering_name)
        self.assertEqual(json_output['description'], description)
