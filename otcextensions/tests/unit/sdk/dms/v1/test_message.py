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

from otcextensions.sdk.dms.v1 import message


MESSAGES_EXAMPLE = {
    "messages": [
        {
            "body": "TEST11",
            "attributes": {
                "attribute1": "value1",
                "attribute2": "value2"
            },
        }, {
            "body": {
                "foo": "test02"
            },
            "attributes": {
                "attribute1": "value1",
                "attribute2": "value2"
            },
        }
    ]
}


class TestMessage(base.TestCase):

    def test_basic(self):
        sot = message.Message()

        self.assertEqual(
            '/queues/%(queue_id)s/groups/%(group_id)s/messages',
            sot.base_path)
        self.assertEqual('message', sot.resource_key)
        self.assertTrue(sot.allow_list)

        self.assertDictEqual({
            'ack_wait': 'ack_wait',
            'limit': 'limit',
            'marker': 'marker',
            'max_msgs': 'max_msgs',
            'time_wait': 'time_wait'},
            sot._query_mapping._mapping
        )

    def test_make_it(self):

        sot = message.Message()
        self.assertIsNone(sot.queue_id)
        # TODO()

    def test__collect_attrs(self):
        # TODO()
        pass

    def test_list(self):
        # TODO()
        pass


class TestMessages(base.TestCase):

    def test_basic(self):
        sot = message.Messages()

        self.assertEqual('/queues/%(queue_id)s/messages', sot.base_path)
        self.assertEqual('messages', sot.resources_key)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)

        self.assertDictEqual(
            {
                'limit': 'limit',
                'marker': 'marker',
            },
            sot._query_mapping._mapping
        )

    def test_make_it(self):

        sot = message.Messages(**MESSAGES_EXAMPLE)
        self.assertEqual(2, len(sot.messages))
        # TODO()
