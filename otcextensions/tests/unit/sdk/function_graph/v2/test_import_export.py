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

from otcextensions.sdk.function_graph.v2 import import_function
from otcextensions.sdk.function_graph.v2 import export_function

EXAMPLE_EXPORT = {
    'file_name': 'test',
    'code_url': 'url'
}
EXAMPLE_IMPORT = {
    "func_urn": "urn",
    "func_name": "test_v1_2",
    "domain_id": "14ee2e35****a7998b******aa24cabf",
    "project_name": "{region}",
    "package": "default",
    "runtime": "Node.js6.10",
    "timeout": 3,
    "handler": "index.handler",
    "memory_size": 128,
    "cpu": 300,
    "code_type": "zip",
    "code_filename": "index.zip",
    "code_size": 6709,
    "digest": "123",
    "version": "latest",
    "image_name": "latest-191025153727@zehht",
    "last_modified": "2019-10-25 15:37:27",
    "strategy_config": {
        "concurrency": -1
    },
    "enterprise_project_id": "123"
}


class TestFunctionExport(base.TestCase):

    def test_basic(self):
        sot = export_function.Export()
        path = '/fgs/functions/%(function_urn)s/export'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_fetch)

    def test_make_it(self):
        sot = export_function.Export(**EXAMPLE_EXPORT)
        self.assertEqual(EXAMPLE_EXPORT['file_name'], sot.file_name)
        self.assertEqual(EXAMPLE_EXPORT['code_url'], sot.code_url)


class TestFunctionImport(base.TestCase):

    def test_basic(self):
        sot = import_function.Import()
        path = '/fgs/functions/import'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_create)

    def test_make_it(self):
        sot = import_function.Import(**EXAMPLE_IMPORT)
        self.assertEqual(EXAMPLE_IMPORT['func_name'], sot.func_name)
        self.assertEqual(EXAMPLE_IMPORT['code_type'], sot.code_type)
