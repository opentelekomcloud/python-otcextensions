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
import mock
from keystoneauth1 import adapter
from openstack.tests.unit import base

from otcextensions.sdk.elb.v2 import listener_tag

EXAMPLE = {
    "key": 'fake_key',
    "value": "fake_name",
}


class TestElbLoadBalancerTag(base.TestCase):

    def setUp(self):
        super(TestElbLoadBalancerTag, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.post = mock.Mock()

    def test_basic(self):
        sot = listener_tag.Tag()

        self.assertEqual('/listeners/%(listener_id)s/tags', sot.base_path)
        self.assertEqual('tags', sot.resources_key)
        self.assertIsNone(sot.resource_key)

        self.assertTrue(sot.allow_list)
        self.assertFalse(sot.allow_fetch)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)
        self.assertFalse(sot.allow_commit)

    def test_make(self):
        sot = listener_tag.Tag(**EXAMPLE)
        self.assertEqual(EXAMPLE['key'], sot.key)
        self.assertEqual(EXAMPLE['value'], sot.value)
