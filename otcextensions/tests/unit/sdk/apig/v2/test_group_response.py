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
from openstack.tests.unit import base
from otcextensions.sdk.apig.v2 import group_response

EXAMPLE_RESPONSE = {
    'gateway_id': 'gw-001',
    'group_id': 'grp-001',
    'name': 'not-found-handler',
    'responses': {
        'NOT_FOUND': {
            'status': 404,
            'body': '{"error":"not found"}',
            'headers': {
                'key': 'Content-Type',
                'value': 'application/json'
            }
        }
    }
}


class TestGroupResponse(base.TestCase):

    def test_basic(self):
        sot = group_response.GroupResponse()
        self.assertEqual(
            '/apigw/instances/%(gateway_id)s/api-groups/%(group_id)s/'
            'gateway-responses',
            sot.base_path
        )
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_commit)
        self.assertEqual('responses', sot.resources_key)

    def test_make_it(self):
        sot = group_response.GroupResponse(**EXAMPLE_RESPONSE)
        self.assertEqual('gw-001', sot.gateway_id)
        self.assertEqual('grp-001', sot.group_id)
        self.assertEqual('not-found-handler', sot.name)
        self.assertIn('NOT_FOUND', sot.responses)
