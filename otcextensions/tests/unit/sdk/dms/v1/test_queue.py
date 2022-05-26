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

from otcextensions.sdk.dms.v1 import queue

EXAMPLE = {
    "id": "9bf46390-38a2-462d-b392-4d5b2d519c55",
    "name": "queue_001",
    "description": "test1",
    "redrive_policy": "enable",
    "max_consume_count": 1,
    "retention_hours": 7
}


class TestQueue(base.TestCase):

    example = EXAMPLE
    objcls = queue.Queue

    def test_basic(self):
        sot = self.objcls()

        self.assertEqual('/queues', sot.base_path)

        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertFalse(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

        self.assertDictEqual({
            'include_deadletter': 'include_deadletter',
            'include_messages_num': 'include_messages_num',
            'limit': 'limit',
            'marker': 'marker'},
            sot._query_mapping._mapping
        )

    def test_make_it(self):

        sot = self.objcls(**self.example)
        self.assertEqual(self.example['id'], sot.id)
        self.assertEqual(self.example['name'], sot.name)
        self.assertEqual(self.example['description'], sot.description)
        self.assertEqual(self.example['max_consume_count'],
                         sot.max_consume_count)
        self.assertEqual(self.example['redrive_policy'],
                         sot.redrive_policy)
        self.assertEqual(self.example['retention_hours'], sot.retention_hours)
