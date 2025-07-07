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
from otcextensions.sdk.apig.v2 import export_api

EXAMPLE_EXPORT = {
    'env_id': 'env-123',
    'group_id': 'group-456',
    'define': 'full',
    'type': 'json',
    'version': '1.0.0',
    'apis': ['api-1', 'api-2'],
}

EXAMPLE_IMPORT = {
    'is_create_group': True,
    'group_id': 'group-789',
    'extend_mode': 'merge',
    'simple_mode': False,
    'mock_mode': True,
    'api_mode': 'overwrite',
    'file_name': 'spec_file.json',
    'success': [{'id': 'api-1', 'method': 'GET', 'path': '/success',
                 'action': 'import'}],
    'failure': [{'method': 'POST', 'path': '/fail', 'error_code': '500',
                 'error_msg': 'Internal Error'}],
    'swagger': {'id': 'swag-1', 'result': 'valid'},
    'ignore': [{'method': 'DELETE', 'path': '/ignore'}],
}


class TestExportApi(base.TestCase):

    def test_basic(self):
        sot = export_api.ExportApi()
        self.assertEqual('apigw/instances/%(gateway_id)s/openapi/export',
                         sot.base_path)

    def test_make_it(self):
        sot = export_api.ExportApi(**EXAMPLE_EXPORT)
        self.assertEqual(EXAMPLE_EXPORT['env_id'], sot.env_id)
        self.assertEqual(EXAMPLE_EXPORT['group_id'], sot.group_id)
        self.assertEqual(EXAMPLE_EXPORT['define'], sot.define)
        self.assertEqual(EXAMPLE_EXPORT['type'], sot.type)
        self.assertEqual(EXAMPLE_EXPORT['version'], sot.version)
        self.assertEqual(EXAMPLE_EXPORT['apis'], sot.apis)


class TestImportApi(base.TestCase):

    def test_basic(self):
        sot = export_api.ImportApi()
        self.assertEqual('apigw/instances/%(gateway_id)s/openapi/import',
                         sot.base_path)

    def test_make_it(self):
        sot = export_api.ImportApi(**EXAMPLE_IMPORT)
        self.assertTrue(sot.is_create_group)
        self.assertEqual(EXAMPLE_IMPORT['group_id'], sot.group_id)
        self.assertEqual(EXAMPLE_IMPORT['extend_mode'], sot.extend_mode)
        self.assertEqual(EXAMPLE_IMPORT['simple_mode'], sot.simple_mode)
        self.assertEqual(EXAMPLE_IMPORT['mock_mode'], sot.mock_mode)
        self.assertEqual(EXAMPLE_IMPORT['api_mode'], sot.api_mode)
        self.assertEqual(EXAMPLE_IMPORT['file_name'], sot.file_name)
        self.assertIsInstance(sot.success[0], export_api.SuccessSpec)
        self.assertEqual('api-1', sot.success[0].id)
        self.assertIsInstance(sot.failure[0], export_api.FailureSpec)
        self.assertEqual('/fail', sot.failure[0].path)
        self.assertIsInstance(sot.swagger, export_api.SwaggerSpec)
        self.assertEqual('swag-1', sot.swagger.id)
        self.assertIsInstance(sot.ignore[0], export_api.IgnoreSpec)
        self.assertEqual('DELETE', sot.ignore[0].method)
