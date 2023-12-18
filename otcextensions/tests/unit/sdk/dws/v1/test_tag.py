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
from otcextensions.sdk.dws.v1 import tag
from unittest import mock


class TestTag(base.TestCase):

    def setUp(self):
        super(TestTag, self).setUp()
        self.cluster_id = "example_cluster_id"
        self.proxy = mock.Mock()
        self.mock_response = mock.Mock()
        self.mock_response.status_code = 204

    def test_basic(self):
        sot = tag.Tag()
        self.assertEqual('/clusters/%(cluster_id)s/tags', sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        example = {
            "key": "example_key",
            "value": "example_value",
            "cluster_id": "example_cluster_id"
        }
        sot = tag.Tag(**example)
        self.assertEqual(example['key'], sot.key)
        self.assertEqual(example['value'], sot.value)
        self.assertEqual(example['cluster_id'], sot.cluster_id)

    def test_batch_create_cluster_tags(self):
        tags = [
            {"key": "key1", "value": "value1"},
            {"key": "key2", "value": "value2"}
        ]
        tag_instance = tag.Tag()
        self.proxy.post.return_value = self.mock_response
        tag_instance.manage_tags_batch(
            self.proxy, self.cluster_id, tags, 'create'
        )
        self.proxy.post.assert_called_once_with(
            'clusters/example_cluster_id/tags/action',
            json={'action': 'create', 'tags': tags}
        )

    def test_batch_delete_cluster_tags(self):
        tags = [{"key": "key1"}, {"key": "key2"}]
        tag_instance = tag.Tag()
        self.proxy.post.return_value = self.mock_response
        tag_instance.manage_tags_batch(
            self.proxy, self.cluster_id, tags, 'delete'
        )
        self.proxy.post.assert_called_once_with(
            'clusters/example_cluster_id/tags/action',
            json={'action': 'delete', 'tags': tags}
        )
