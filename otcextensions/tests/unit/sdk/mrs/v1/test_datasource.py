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

from otcextensions.sdk.mrs.v1 import datasource

EXAMPLE = {
    "name": "my-data-source",
    "url": "/simple/mapreduce/input",
    "is_protected": False,
    "is_public": False,
    "type": "hdfs",
    "description": "this is the data source template"
}


class TestDatasource(base.TestCase):

    def test_basic(self):
        sot = datasource.Datasource()
        self.assertEqual('data_source', sot.resource_key)
        self.assertEqual('data_sources', sot.resources_key)
        path = '/data-sources'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_get)
        self.assertFalse(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = datasource.Datasource(**EXAMPLE)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['url'], sot.url)
        self.assertEqual(EXAMPLE['type'], sot.type)
        self.assertEqual(EXAMPLE['description'], sot.description)
        self.assertEqual(EXAMPLE['is_public'], sot.is_public)
        self.assertEqual(EXAMPLE['is_protected'], sot.is_protected)
