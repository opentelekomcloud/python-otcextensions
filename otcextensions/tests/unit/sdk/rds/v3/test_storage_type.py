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
from openstack.tests.unit import base

from otcextensions.sdk.rds.v3 import storage_type

EXAMPLE = {
    "name": "COMMON",
    "compute_group_type": [
        "normal",
        "normal2"
    ],
    "az_status": {
        "eu-de-02": "normal",
        "eu-de-01": "normal",
        "eu-de-03": "normal"
    }
}


class TestFlavor(base.TestCase):

    def test_basic(self):
        sot = storage_type.StorageType()

        self.assertEqual('/storage-type/%(datastore_name)s', sot.base_path)
        self.assertEqual('storage_type', sot.resources_key)
        self.assertIsNone(sot.resource_key)

        self.assertTrue(sot.allow_list)
        self.assertFalse(sot.allow_fetch)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_delete)
        self.assertFalse(sot.allow_commit)
        self.assertDictEqual({'limit': 'limit',
                              'marker': 'marker',
                              'version_name': 'version_name'},
                             sot._query_mapping._mapping)

    def test_make_it(self):

        sot = storage_type.StorageType(**EXAMPLE)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['compute_group_type'], sot.compute_group_type)
        self.assertEqual(EXAMPLE['az_status'], sot.az_status)
