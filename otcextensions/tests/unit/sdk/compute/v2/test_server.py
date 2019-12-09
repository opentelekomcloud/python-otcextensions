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
from openstack.tests.unit import base

from otcextensions.sdk.compute.v2 import server


IDENTIFIER = 'fake_id'


class TestServer(base.TestCase):

    def setUp(self):
        super(TestServer, self).setUp()
        self.sot = server.Server(id=IDENTIFIER)
        self.resp = mock.Mock()
        self.resp.body = None
        self.resp.json = mock.Mock(return_value=self.resp.body)
        self.resp.status_code = 200
        self.sess = mock.Mock()
        self.sess.post = mock.Mock(return_value=self.resp)
        self.ecs = mock.Mock()
        self.ecs.post = mock.Mock(return_value=self.resp)
        self.sot._connection = mock.Mock(ecs=self.ecs)

    def test__get_tag_struct(self):
        self.assertDictEqual(
            {'key': 'k1', 'value': 'v1'},
            self.sot._get_tag_struct('k1=v1')
        )
        self.assertDictEqual(
            {'key': 'k1', 'value': ''},
            self.sot._get_tag_struct('k1')
        )

    def test_add_tag(self):
        # Let the translate pass through, that portion is tested elsewhere
        self.sot._translate_response = lambda arg: arg

        result = self.sot.add_tag(self.sess, 'a=b')

        self.assertIsInstance(result, server.Server)

        url = 'servers/%s/tags/action' % (IDENTIFIER)
        body = {
            "action": "create",
            "tags": [{'key': 'a', 'value': 'b'}]
        }
        self.sot._connection.ecs.post.assert_called_with(
            url, json=body)

    def test_remove_tag(self):
        # Let the translate pass through, that portion is tested elsewhere
        self.sot._translate_response = lambda arg: arg

        result = self.sot.remove_tag(self.sess, 'a=b')

        self.assertIsInstance(result, server.Server)

        url = 'servers/%s/tags/action' % (IDENTIFIER)
        body = {
            "action": "delete",
            "tags": [{'key': 'a', 'value': 'b'}]
        }
        self.sot._connection.ecs.post.assert_called_with(
            url, json=body)
