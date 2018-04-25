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
from otcextensions.sdk.dms.v1 import group
from otcextensions.sdk.dms.v1 import message
from otcextensions.sdk.dms.v1 import message_consumer

EXAMPLE = {
    "id": "9bf46390-38a2-462d-b392-4d5b2d519c55",
    "name": "queue_001",
    "description": "test1",
    "redrive_policy": "enable",
    "max_consume_count": 1,
    "retention_hours": 7
}

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

MSG_CONSUME_EXAMPLE = {
    "message": {
        "body": {
            "foo": "123="
        },
        "attributes": {
            "attribute1": "value1",
            "attribute2": "value2"
        }
    },
    "handler": "eyJjZyI6Im15X2pzb25fZ3JvdXAiLCJjaSI6InJlc3QtY29uc3VtZXItYz",
}


class TestQueue(base.TestCase):

    example = EXAMPLE
    objcls = queue.Queue

    def test_basic(self):
        sot = self.objcls()

        self.assertEqual('/queues', sot.base_path)

        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_get)
        self.assertFalse(sot.allow_update)
        self.assertTrue(sot.allow_delete)

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


class TestGroup(base.TestCase):

    example = GROUP_EXAMPLE
    objcls = group.Group

    def test_basic(self):
        sot = self.objcls()

        self.assertEqual('queues/%(queue_id)s/groups', sot.base_path)

    def test_make_it(self):

        sot = self.objcls(**self.example)
        self.assertEqual(self.example['groups'], sot.groups)


class TestMessage(base.TestCase):

    objcls = message.Message

    def test_basic(self):
        sot = self.objcls()

        self.assertEqual('/queues/%(queue_id)s/messages', sot.base_path)

    def test_make_it(self):

        sot = self.objcls(**self.example)
        self.assertEqual(self.example['messages'], sot.messages)


class TestMessageConsumer(base.TestCase):

    example = MSG_CONSUME_EXAMPLE
    objcls = message_consumer.MessageConsumer

    def test_basic(self):
        sot = self.objcls()

        self.assertEqual(
            '/queues/%(queue_id)s/groups/%(consumer_group_id)s/messages',
            sot.base_path)

    def test_make_it(self):

        sot = self.objcls(**self.example)
        self.assertEqual(self.example['message'], sot.message)
        self.assertEqual(self.example['handler'], sot.handler)
