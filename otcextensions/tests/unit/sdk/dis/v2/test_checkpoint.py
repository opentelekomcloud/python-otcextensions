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
from otcextensions.sdk.dis.v2 import checkpoint

EXAMPLE = {
    "sequence_number": "newstram",
    "metadata": ""
}


class TestCheckpoint(base.TestCase):
    def setUp(self):
        super(TestCheckpoint, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)

    def test_basic(self):
        sot = checkpoint.Checkpoint()
        self.assertEqual(None, sot.resource_key)
        self.assertEqual(None, sot.resources_key)
        path = '/checkpoints'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_delete)
        self.assertFalse(sot.allow_list)
        self.assertFalse(sot.allow_commit)
        self.assertFalse(sot.allow_patch)

    def test_make_it(self):
        sot = checkpoint.Checkpoint(**EXAMPLE)
        updated_sot_attrs = ()
        for key, value in EXAMPLE.items():
            if key not in updated_sot_attrs:
                self.assertEqual(getattr(sot, key), value)

    def test_checkpoint_get(self):
        sot = checkpoint.Checkpoint()
        params = {
            'stream_name': 'test-stream',
            'partition_id': 'test-partition-id',
        }
        response = mock.Mock()
        response.status_code = 200
        response.headers = {}
        response.json.return_value = {
            "sequence_number": "newstram",
            "metadata": ""
        }
        self.sess.get.return_value = response

        rt = sot.get_checkpoint(self.sess, **params)
        self.sess.get.assert_called_with(sot.base_path, params=params)
        self.assertIsNotNone(rt)

    def test_checkpoint_delete(self):
        sot = checkpoint.Checkpoint()
        params = {
            'stream_name': 'test-stream',
            'partition_id': 'test-partition-id',
        }
        response = mock.Mock()
        response.status_code = 204
        response.headers = {}
        response.text.return_value = None
        response.json.return_value = None
        self.sess.delete.return_value = response

        rt = sot.delete_checkpoint(self.sess, **params)
        self.sess.delete.assert_called_with(sot.base_path, params=params)
        self.assertIsNotNone(rt)
