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

from otcextensions.sdk import sdk_resource

# Only a basic tests for extended functionality are implemented since
# the _list code is copied from sdk.resource to override headers
# TODO(agoncharov) make sense to implement (copy) existing base_resource
# tests from SDK

PROJECT_ID = '123'
IDENTIFIER = 'IDENTIFIER'
EXAMPLE = {
    'id': IDENTIFIER,
    'links': '1',
    'name': '2',
    'ram': 3,
}


class Res(sdk_resource.Resource):

    base_path = '/'
    allow_list = True


class TestBaseResource(base.TestCase):

    def setUp(self):
        super(TestBaseResource, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.get_project_id = mock.Mock(return_value=PROJECT_ID)

        self.sot = Res(**EXAMPLE)

        # inject some properties to enable methods
        # self.sot.allow_list = True
        # self.sot.base_path = '/'

        self.base_path = self.sot.base_path

        self.headers = {"Content-Type": "application/json"}

    def test_basic(self):
        sot = sdk_resource.Resource()
        self.assertFalse(sot.allow_list)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_get)
        self.assertFalse(sot.allow_update)
        self.assertFalse(sot.allow_delete)

    def test_list_defaults(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []

        self.sess.get.return_value = mock_response

        result = list(self.sot.list(self.sess))

        self.sess.get.assert_called_once_with(
            self.base_path,
            params={},
        )

        self.assertEqual([], result)

    def test_list_override_headers(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [EXAMPLE]

        self.sess.get.return_value = mock_response

        result = list(self.sot.list(self.sess, headers={'a': 'b'}))

        self.sess.get.assert_called_once_with(
            self.base_path,
            headers={"a": "b"},
            params={},
        )

        self.assertEqual([sdk_resource.Resource(**EXAMPLE)], result)

    def test_list_override_endpoint(self):
        # sot = _base.Resource()

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [EXAMPLE]

        self.sess.get.return_value = mock_response

        result = list(self.sot.list(
            self.sess,
            headers={'a': 'b'},
            endpoint_override='http:example.com'))

        self.sess.get.assert_called_once_with(
            self.base_path,
            headers={"a": "b"},
            endpoint_override='http:example.com',
            params={},
        )

        self.assertEqual([self.sot], result)
