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

from otcextensions.sdk.rds.v1 import datastore


PROJECT_ID = '123'
IDENTIFIER = 'IDENTIFIER'
EXAMPLE = {
    "id": IDENTIFIER,
    "name": "5.6.33",
    "datastore": "736270b9-27c7-4f03-823b-447d8245e1c2",
    "image": "36bdc308-0389-4830-8813-4a98d62b97de",
    "packages": "MySQL-server-5.6.33",
    "active": 1
}


class TestDatastore(base.TestCase):

    def setUp(self):
        super(TestDatastore, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.get = mock.Mock()
        self.sess.get_project_id = mock.Mock(return_value=PROJECT_ID)
        self.sot = datastore.Datastore(**EXAMPLE)
        # print(self.sot.to_dict())

    def test_basic(self):
        sot = datastore.Datastore()
        self.assertEqual('', sot.resource_key)
        self.assertEqual('dataStores', sot.resources_key)
        self.assertEqual('/%(project_id)s/datastores/%(datastore_name)s'
                         '/versions',
                         sot.base_path)
        self.assertEqual('rds', sot.service.service_type)
        self.assertTrue(sot.allow_list)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_get)
        self.assertFalse(sot.allow_update)
        self.assertFalse(sot.allow_delete)

    def test_make_it(self):
        sot = datastore.Datastore(**EXAMPLE)
        self.assertEqual(IDENTIFIER, sot.id)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['datastore'], sot.datastore)
        self.assertEqual(EXAMPLE['image'], sot.image)
        self.assertEqual(EXAMPLE['packages'], sot.packages)
        self.assertEqual(EXAMPLE['active'], sot.active)

    def test_list(self):

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'dataStores': [EXAMPLE]}

        self.sess.get.return_value = mock_response

        result = list(self.sot.list(
            self.sess,
            project_id=PROJECT_ID,
            datastore_name='datastore')
        )

        self.sess.get.assert_called_once_with(
            '/%s/datastores/%s/versions' % (PROJECT_ID, 'datastore'),
        )

        self.assertEqual([datastore.Datastore(**EXAMPLE)], result)
