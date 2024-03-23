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
#
from openstack.tests.unit import base
from otcextensions.sdk.modelartsv1.v1 import model
from otcextensions.tests.unit.sdk.modelartsv1.v1 import examples
from otcextensions.tests.unit.sdk.utils import assert_attributes_equal

EXAMPLE = examples.MODEL


class TestModel(base.TestCase):
    def setUp(self):
        super(TestModel, self).setUp()

    def test_basic(self):
        sot = model.Model()

        self.assertEqual("/models", sot.base_path)
        self.assertEqual("models", sot.resources_key)

        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)
        self.assertFalse(sot.allow_commit)
        self.assertFalse(sot.allow_patch)

        self.assertDictEqual(
            {
                "description": "description",
                "limit": "limit",
                "marker": "marker",
                "model_type": "model_type",
                "model_version": "model_version",
                "name": "model_name",
                "not_model_type": "not_model_type",
                "offset": "offset",
                "model_version": "model_version",
                "order": "order",
                "sort_by": "sort_by",
                "status": "model_status",
                "workspace_id": "workspace_id",
            },
            sot._query_mapping._mapping,
        )

    def test_make_it(self):
        updated_sot_attrs = {
            "create_at": "created_at",
            "model_name": "name",
            "model_id": "id",
            "model_status": "status",
            "model_version": "version",
            "owner": "owner_id",
            "project": "project_id",
            "tenant": "tenant_id",
            "tunable": "is_tunable",
            "market_flag": "is_subscribed",
            "publishable_flag": "is_publishable",
        }
        sot = model.Model(**EXAMPLE)

        for key, value in EXAMPLE.items():
            if key in updated_sot_attrs.keys():
                self.assertEqual(
                    getattr(sot, updated_sot_attrs[key]), EXAMPLE[key]
                )
            else:
                assert_attributes_equal(self, getattr(sot, key), value)
