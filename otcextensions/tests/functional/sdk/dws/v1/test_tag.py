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

from openstack import _log
from otcextensions.tests.functional import base

_logger = _log.setup_logging('openstack')


class TestClusterTags(base.BaseFunctionalTest):

    def setUp(self):
        super(TestClusterTags, self).setUp()
        self.client = self.conn.dws
        self.cluster_id = "670f868a-07ae-4fca-8bdc-665498333641"

    def test_list_cluster_tags(self):
        tags = list(self.client.list_cluster_tags(self.cluster_id))
        self.assertGreaterEqual(len(tags), 0)

    def test_create_cluster_tag(self):
        tag_key = "test_key"
        tag_value = "test_value"
        created_tag = self.client.create_cluster_tag(
            self.cluster_id, {"key": tag_key, "value": tag_value}
        )

        self.assertIsNotNone(created_tag)
        self.assertEqual(created_tag.key, tag_key)
        self.assertEqual(created_tag.value, tag_value)

    def test_create_cluster_tags(self):
        tags_to_add = [
            {"key": "test_env", "value": "test_env_value"},
            {"key": "test_owner", "value": "test_owner_value"}
        ]

        self.client.create_cluster_tags(self.cluster_id, tags_to_add)

        tags = list(self.client.list_cluster_tags(self.cluster_id))
        added_tags = [
            (tag.key, tag.value) for tag in tags
            if tag.key in ['test_env', 'test_owner']
        ]

        self.assertIn(('test_env', 'test_env_value'), added_tags)
        self.assertIn(('test_owner', 'test_owner_value'), added_tags)

    def test_delete_cluster_tag(self):
        tag_key_to_delete = "test_key"
        tag_value = "test_value"
        self.client.create_cluster_tag(
            self.cluster_id, {"key": tag_key_to_delete, "value": tag_value}
        )

        self.client.delete_cluster_tag(self.cluster_id, tag_key_to_delete)

        tags = list(self.client.list_cluster_tags(self.cluster_id))
        deleted_tag = [
            (tag.key, tag.value) for tag in tags
            if tag.key == tag_key_to_delete
        ]
        self.assertEqual(len(deleted_tag), 0)

    def test_delete_cluster_tags(self):
        tags_to_create = [
            {"key": "test_tag1", "value": "test_value1"},
            {"key": "test_tag2", "value": "test_value2"}
        ]
        for tag in tags_to_create:
            self.client.create_cluster_tag(self.cluster_id, tag)

        self.client.delete_cluster_tags(self.cluster_id, ["test_tag1", "test_tag2"])

        tags = list(self.client.list_cluster_tags(self.cluster_id))
        for tag_key in ["test_tag1", "test_tag2"]:
            self.assertNotIn(tag_key, [tag.key for tag in tags])
