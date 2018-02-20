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

from otcextensions.sdk.obs.v1 import object as _object


PROJECT_ID = '123'
IDENTIFIER = 'IDENTIFIER'
EXAMPLE = {
    'id': IDENTIFIER,
    'name': '2',
    'lastmodified': 'somedate',
    'bucket': 'somebucket',
}


class TestObject(base.TestCase):

    def setUp(self):
        super(TestObject, self).setUp()
        self.resp = mock.Mock()
        self.resp.body = None
        self.resp.json = mock.Mock(return_value=self.resp.body)
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.get = mock.Mock(return_value=self.resp)
        self.sess.get_project_id = mock.Mock(return_value=PROJECT_ID)

    def test_basic(self):
        sot = _object.Object()
        self.assertEqual('', sot.resource_key)
        self.assertEqual('', sot.resources_key)
        self.assertEqual('/', sot.base_path)
        self.assertEqual('obs', sot.service.service_type)
        self.assertTrue(sot.allow_list)
        self.assertFalse(sot.allow_create)
        self.assertTrue(sot.allow_get)
        self.assertFalse(sot.allow_update)
        self.assertFalse(sot.allow_delete)

    def test_make_it(self):
        sot = _object.Object(**EXAMPLE)
        self.assertEqual(IDENTIFIER, sot.id)
        # self.assertEqual(EXAMPLE['links'], sot.links)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['lastmodified'], sot.lastmodified)
