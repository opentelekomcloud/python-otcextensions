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
        # Test listing tags of a cluster
        tags = list(self.client.list_cluster_tags(self.cluster_id))
        self.assertGreaterEqual(len(tags), 0)

    def test_create_cluster_tag(self):
        # Test creating a single cluster tag
        tag_key = "test_key"
        tag_value = "test_value"
        created_tag = self.client.create_cluster_tag(
            self.cluster_id, {"key": tag_key, "value": tag_value}
        )

        self.assertIsNotNone(created_tag)
        self.assertEqual(created_tag.key, tag_key)
        self.assertEqual(created_tag.value, tag_value)

    def test_manage_cluster_tags_batch_create(self):
        # Test deleting a single cluster tag
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

    def test_batch_create_cluster_tags(self):
        # Test batch creation of cluster tags
        tags_to_create = [{"key": "test_key1", "value": "test_value1"},
                          {"key": "test_key2", "value": "test_value2"}]

        # Create tags
        response_create = self.client.manage_cluster_tags_batch_create(
            self.cluster_id, tags_to_create)
        self.assertEqual(response_create.status_code, 204)

    def test_batch_delete_cluster_tags(self):
        # Test batch deletion of cluster tags
        tags_to_delete = [{"key": "test_key1", "value": "test_value1"},
                          {"key": "test_key2", "value": "test_value2"}]

        # Ensure tags are created first
        self.client.manage_cluster_tags_batch_create(
            self.cluster_id, tags_to_delete)

        # Delete tags
        response_delete = self.client.manage_cluster_tags_batch_delete(
            self.cluster_id, tags_to_delete)
        self.assertEqual(response_delete.status_code, 204)
