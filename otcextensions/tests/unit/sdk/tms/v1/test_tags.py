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

import mock
from openstack.tests.unit import base
from otcextensions.sdk.tms.v1 import tag


EXAMPLE = {
    "key": "test",
    "value": "test",
    "limit": "10",
    "order_field": "key",
    "order_method": "asc"
}


class TestTags(base.TestCase):
    def setUp(self):
        super(TestTags, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.put = mock.Mock()

    def test_basic(self):
        sot = tag.Tag()
        self.assertEqual('tag', sot.resource_key)
        self.assertEqual('tags', sot.resources_key)
        path = '/predefine_tags'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertFalse(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = tag.Tag(**EXAMPLE)
        self.assertEqual(EXAMPLE['key'], sot.key)
        self.assertEqual(EXAMPLE['value'], sot.value)
        self.assertEqual(EXAMPLE['limit'], sot.limit)
        self.assertEqual(EXAMPLE['order_field'], sot.order_field)
        self.assertEqual(EXAMPLE['order_method'], sot.order_method)
