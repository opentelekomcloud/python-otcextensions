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
import openstack

from otcextensions.tests.functional.sdk.dds import TestDds

_logger = openstack._log.setup_logging('openstack')


class TestDatastores(TestDds):
    datastore_name = 'DDS-Community'

    def setUp(self):
        super(TestDatastores, self).setUp()

    def test_list_datastores(self):
        datastores = self.client.datastores(datastore_name=self.datastore_name)
        self.assertIsNotNone(next(datastores))

    def test_list_datastore_types(self):
        types = []
        datastore_types = self.client.datastore_types()
        for ds in datastore_types:
            types.append(ds.copy())
        self.assertIsNotNone(types)
        self.assertEqual(len(types), 2)
