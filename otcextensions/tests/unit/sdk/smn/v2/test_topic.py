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

from otcextensions.sdk.smn.v2 import topic


EXAMPLE = {
    "update_time": "2016-08-01T02:16:38Z",
    "push_policy": 0,
    "create_time": "2016-08-01T02:16:38Z",
    "name": "test_create_topic_v2",
    "topic_urn": "urn:smn:regionId:8bad8a40e0f7462f8c1676e3f",
    "display_name": "test create topic v2",
    "request_id": "6837531fd3f54550927b930180a706bf"
}


class TestTopic(base.TestCase):

    def test_basic(self):
        sot = topic.Topic()
        self.assertEqual('topics', sot.resources_key)
        path = '/notifications/topics'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = topic.Topic(**EXAMPLE)
        self.assertEqual(EXAMPLE['topic_urn'], sot.id)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['create_time'], sot.create_time)
        self.assertEqual(EXAMPLE['update_time'], sot.update_time)
        self.assertEqual(EXAMPLE['push_policy'], sot.push_policy)
        self.assertEqual(EXAMPLE['request_id'], sot.request_id)
