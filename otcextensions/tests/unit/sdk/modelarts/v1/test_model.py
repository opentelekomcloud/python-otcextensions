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

from otcextensions.sdk.modelarts.v1 import model
from otcextensions.tests.unit.sdk.modelarts.v1.examples import EXAMPLE_MODEL
from unittest.mock import MagicMock
import json
import copy


def _translate_response(body):
    for key in ('model_metrics', 'config', 'apis',
                'output_params', 'input_params'):
        if key in body:
            if isinstance(body[key], str):
                body[key] = json.loads(body[key])
            elif key in ('output_params', 'input_params') and \
                    isinstance(body[key], list):
                for param in body[key]:
                    if isinstance(param.get('param_desc'), str):
                        param['param_desc'] = json.loads(param['param_desc'])
    return body


class TestModel(base.TestCase):

    def setUp(self):
        super(TestModel, self).setUp()

    def test_basic(self):
        sot = model.Model()

        self.assertEqual('/models', sot.base_path)
        # self.assertEqual('model', sot.resource_key)
        self.assertEqual('models', sot.resources_key)

        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)
        self.assertFalse(sot.allow_commit)
        self.assertDictEqual({'description': 'description',
                              'limit': 'limit',
                              'marker': 'marker',
                              'model_type': 'model_type',
                              'model_version': 'model_version',
                              'name': 'model_name',
                              'not_model_type': 'not_model_type',
                              'offset': 'offset',
                              'model_version': 'model_version',
                              'order': 'order',
                              'sort_by': 'sort_by',
                              'status': 'model_status',
                              'workspace_id': 'workspace_id'},
                             sot._query_mapping._mapping)

    def test_make_it(self):
        EXAMPLE2 = copy.deepcopy(EXAMPLE_MODEL)
        EXAMPLE = copy.deepcopy(EXAMPLE_MODEL)
        sot = model.Model()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = EXAMPLE2
        sot._translate_response(mock_response)

        updated_sot_attrs = (
            'create_at',
            'model_name',
            'model_status',
            'model_version',
            'owner',
            'project',
            'tenant',
        )

        EXAMPLE = _translate_response(EXAMPLE)
        self.assertEqual(EXAMPLE['create_at'], sot.created_at)
        self.assertEqual(EXAMPLE['model_name'], sot.name)
        self.assertEqual(EXAMPLE['model_status'], sot.status)
        self.assertEqual(EXAMPLE['model_version'], sot.version)
        self.assertEqual(EXAMPLE['owner'], sot.owner_id)
        self.assertEqual(EXAMPLE['project'], sot.project_id)
        self.assertEqual(EXAMPLE['tenant'], sot.tenant_id)

        for key, value in EXAMPLE.items():
            if key not in updated_sot_attrs:
                self.assertEqual(getattr(sot, key), value)
