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
from keystoneauth1 import adapter

from unittest import mock

from openstack.tests.unit import base

from otcextensions.sdk.dms.v1 import group

GROUP_EXAMPLE = {
    "queue_name": "queue_001",
    "groups": [{
               "id": "g-5ec247fd-d4a2-4d4f-9876-e4ff3280c461",
               "name": "abcDffD",
               "produced_messages": 0,
               "consumed_messages": 0,
               "available_messages": 0
               }],
    "redrive_policy": "enable",
    "queue_id": "9bf46390-38a2-462d-b392-4d5b2d519c55"
}


class TestGroup(base.TestCase):

    example = GROUP_EXAMPLE['groups'][0]
    objcls = group.Group

    def setUp(self):
        super(TestGroup, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.default_microversion = None

    def test_basic(self):
        sot = self.objcls()

        self.assertEqual('queues/%(queue_id)s/groups', sot.base_path)

        self.assertDictEqual({
            'current_page': 'current_page',
            'include_deadletter': 'include_deadletter',
            'limit': 'limit',
            'marker': 'marker',
            'page_size': 'page_size'},
            sot._query_mapping._mapping
        )

    def test_make_it(self):

        sot = self.objcls(**self.example)
        self.assertEqual(self.example['id'], sot.id)
        self.assertEqual(self.example['name'], sot.name)
        self.assertEqual(
            self.example['produced_messages'],
            sot.produced_messages)
        self.assertEqual(
            self.example['consumed_messages'],
            sot.consumed_messages)
        self.assertEqual(
            self.example['available_messages'],
            sot.available_messages)

    def test_create(self):
        sot = group.Group(queue_id='qid', name='grp')

        response = mock.Mock()
        response.body = {'groups': [{'id': '1', 'name': 'grp'}]}
        response.json = mock.Mock(return_value=response.body)
        self.sess.post = mock.Mock(return_value=response)

        obj = sot.create(self.sess)
        self.sess.post.assert_called_with(
            'queues/qid/groups',
            json={'groups': [{'name': 'grp'}]}
        )
        self.assertEqual('grp', obj.name)
        self.assertEqual('1', obj.id)

    def test_ack(self):
        sot = group.Group(queue_id='qid', id='gid')

        response = mock.Mock()
        response.json = mock.Mock(return_value={})
        response.status_code = 200
        self.sess.post = mock.Mock(return_value=response)

        sot.ack(self.sess, mock.Mock(id='qid'), ['1', '2'], 'failure')

        self.sess.post.assert_called_with(
            'queues/qid/groups/gid/ack',
            json={'message': [
                {'handler': '1', 'status': 'failure'},
                {'handler': '2', 'status': 'failure'}
            ]}
        )
