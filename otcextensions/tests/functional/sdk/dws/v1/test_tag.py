# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from openstack import _log
from otcextensions.tests.functional import base

_logger = _log.setup_logging('openstack')

class TestClusterTags(base.BaseFunctionalTest):
    """Functional tests for DWS cluster tags."""


    def setUp(self):
        """Prepare resources for testing."""
        super(TestClusterTags, self).setUp()
        self.client = self.conn.dws
        self.cluster_id = "670f868a-07ae-4fca-8bdc-665498333641"
        self.created_tags = []

    def tearDown(self):
        """Clean up resources after testing."""
        for tag_key in self.created_tags:
            self.client.delete_cluster_tag(self.cluster_id, tag_key)
        self.created_tags.clear()
        super(TestClusterTags, self).tearDown()

    def test_list_cluster_tags(self):
        """Test listing all tags of a cluster."""
        tags = list(self.client.list_cluster_tags(self.cluster_id))
        self.assertGreaterEqual(len(tags), 0)

    def test_create_cluster_tag(self):
        """Test creating a single tag for a cluster."""
        tag_key = "test_key"
        tag_value = "test_value"
        created_tag = self.client.create_cluster_tag(
            self.cluster_id, {"key": tag_key, "value": tag_value})
        self.assertIsNotNone(created_tag)
        self.assertEqual(created_tag.key, tag_key)
        self.assertEqual(created_tag.value, tag_value)
        self.created_tags.append(tag_key)

    def test_delete_cluster_tag(self):
        """Test deleting a single tag from a cluster."""
        tag_key = "delete_test_key"
        tag_value = "delete_test_value"
        self.client.create_cluster_tag(
            self.cluster_id, {"key": tag_key, "value": tag_value})
        self.client.delete_cluster_tag(self.cluster_id, tag_key)
        tags = list(self.client.list_cluster_tags(self.cluster_id))
        self.assertFalse(any(tag.key == tag_key for tag in tags))

    def test_batch_create_cluster_tags(self):
        """Test batch creation of multiple tags for a cluster."""
        tags_to_create = [
            {"key": "test_key1", "value": "test_value1"},
            {"key": "test_key2", "value": "test_value2"}]
        response_create = self.client.cluster_tags_batch_create(
            self.cluster_id, tags_to_create)
        self.assertEqual(response_create.status_code, 204)

    def test_batch_delete_cluster_tags(self):
        """Test batch deletion of multiple tags from a cluster."""
        tags_to_create = [
            {"key": "batch_delete_key1", "value": "value1"},
            {"key": "batch_delete_key2", "value": "value2"}]
        self.client.cluster_tags_batch_create(
            self.cluster_id, tags_to_create)
        tags_to_delete = [
            {"key": "batch_delete_key1"}, {"key": "batch_delete_key2"}]
        response_delete = self.client.cluster_tags_batch_delete(
            self.cluster_id, tags_to_delete)
        self.assertEqual(response_delete.status_code, 204)
        remaining_tags = list(self.client.list_cluster_tags(self.cluster_id))
        for tag in tags_to_delete:
            self.assertFalse(
                any(t.key == tag['key'] for t in remaining_tags),
                f"Tag {tag['key']} was not deleted")