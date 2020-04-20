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

from otcextensions.sdk.dms.v1 import topic


JSON_DATA = {
    "id": "haha",
    "partition": 3,
    "replication": 3,
    "sync_replication": True,
    "retention_time": 10,
    "sync_message_flush": True
}


class TestTopic(base.TestCase):

    def setUp(self):
        super(TestTopic, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.post = mock.Mock()

    def test_basic(self):
        sot = topic.Topic()

        self.assertEqual('/instances/%(instance_id)s/topics', sot.base_path)
        self.assertEqual('topics', sot.resources_key)

        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):

        sot = topic.Topic(**JSON_DATA)
        self.assertEqual(JSON_DATA['id'], sot.id)
        self.assertEqual(JSON_DATA['partition'], sot.partition)
        self.assertEqual(JSON_DATA['replication'], sot.replication)
        self.assertEqual(JSON_DATA['retention_time'], sot.retention_time)
        self.assertEqual(JSON_DATA['sync_message_flush'], sot.is_sync_flush)
        self.assertEqual(JSON_DATA['sync_replication'],
                         sot.is_sync_replication)
