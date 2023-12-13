from openstack.tests.unit import base
from otcextensions.sdk.dws.v1 import tag
from unittest import mock

class TestTag(base.TestCase):

    def setUp(self):
        super(TestTag, self).setUp()
        self.cluster_id = "example_cluster_id"
        self.proxy = mock.Mock()

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

    def test_cluster_tags_batch_create(self):
        tags = [{"key": "key1", "value": "value1"}, {"key": "key2", "value": "value2"}]
        self.proxy.manage_tags_batch(self.cluster_id, tags, 'create')
        self.proxy.manage_tags_batch.assert_called_once_with(self.cluster_id, tags, 'create')

    def test_cluster_tags_batch_delete(self):
        tags = [{"key": "key1"}, {"key": "key2"}]
        self.proxy.manage_tags_batch(self.cluster_id, tags, 'delete')
        self.proxy.manage_tags_batch.assert_called_once_with(self.cluster_id, tags, 'delete')