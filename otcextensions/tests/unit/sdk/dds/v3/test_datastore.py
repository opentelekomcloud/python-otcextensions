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
from unittest import mock

from keystoneauth1 import adapter

from openstack.tests.unit import base

from otcextensions.sdk.dds.v3 import datastore


EXAMPLE = {
    "storage_engine": "wiredTiger",
    "type": "DDS-Community",
    "version": "3.2"}


class TestDatastore(base.TestCase):
    def setUp(self):
        super(TestDatastore, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.get = mock.Mock()
        self.sess.default_microversion = None
        self.sess._get_connection = mock.Mock(return_value=self.cloud)

    def test_basic(self):
        sot = datastore.Datastore()
        self.assertEqual(
            '/datastores',
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
        self.assertEqual(EXAMPLE['storage_engine'], sot.storage_engine)
        self.assertEqual(EXAMPLE['type'], sot.type)
        self.assertEqual(EXAMPLE['version'], sot.version)

    def test_list(self):
        sot = datastore.Datastore()
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"versions": ["1", "2"]}
        self.sess.get.return_value = mock_response

        datastore_name = 'foo'
        res = list(sot.list(self.sess, datastore_name=datastore_name))
        self.sess.get.assert_called_with(
            f'datastores/{datastore_name}/versions',
            headers={'Accept': 'application/json'},
            microversion=None
        )
        self.assertEqual(2, len(res))
        self.assertEqual(
            datastore.Datastore(
                type=datastore_name,
                storage_engine='wiredTiger',
                version='1'
            ).to_dict(computed=False),
            res[0].to_dict(computed=False)
        )
