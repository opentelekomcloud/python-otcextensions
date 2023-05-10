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

from otcextensions.tests.functional.osclient.dcaas.v2 import common


class TestEndpointGroup(common.DcaasTestCase):

    def setUp(self):
        super(TestEndpointGroup, self).setUp()

    def test_list_endpoint_groups(self):
        json_output = json.loads(self.openstack(
            'dcaas endpoint group list -f json '
        ))
        self.assertIsNotNone(json_output)

    def test_find_endpoint_group(self):
        json_output = json.loads(self.openstack(
            'dcaas endpoint group show {id} -f json'.format(
                id=self.EP_GROUP_ID
            )
        ))
        self.assertIsNotNone(json_output)
        self.assertEqual(json_output['name'], self.EP_GROUP_NAME)

    def test_update_endpoint_group(self):
        ep_group_name = self.EP_GROUP_NAME + '-updated'
        json_output = json.loads(self.openstack(
            'dcaas endpoint group update {id} --name {name} -f json'.format(
                id=self.EP_GROUP_ID,
                name=ep_group_name
            )
        ))
        self.assertEqual(json_output['id'], self.EP_GROUP_ID)
        self.assertEqual(json_output['name'], ep_group_name)
