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

from otcextensions.sdk.dds.v3 import datastore

EXAMPLE = {"versions": "5.7"}


class TestDatastore(base.TestCase):
    def setUp(self):
        super(TestDatastore, self).setUp()

    def test_basic(self):
        sot = datastore.Datastore()
        self.assertEqual(
            '/datastores/%(datastore_name)s/versions',
            sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertFalse(sot.allow_fetch)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_delete)
        self.assertFalse(sot.allow_commit)
        self.assertDictEqual({
            'limit': 'limit',
            'marker': 'marker'
        }, sot._query_mapping._mapping)

    def test_make_it(self):
        sot = datastore.Datastore(**EXAMPLE)
        self.assertEqual(EXAMPLE['versions'], sot.versions)

    def test_list(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {[EXAMPLE]}

        self.sess.get.return_value = mock_response

        result = list(self.sot.list(
            self.sess,
            datastore_name='datastore')
        )

        self.sess.get.assert_called_once_with(
            '/datastores/%s/versions' % ('datastore'),
            params={},
        )

        self.assertEqual([datastore.Datastore(**EXAMPLE)], result)
