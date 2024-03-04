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

EXAMPLE = {
    "source_location": "swr.eu-de.otc.t-systems.com/.../mnist2:latest",
    "image_address": "swr.eu-de.otc.t-systems.com/...",
    "input_params": [
        {
            "url": "/",
            "method": "post",
            "protocol": "http",
            "param_name": "images",
            "param_type": "file",
            "param_desc": '{\n    "type": "file"\n}',
        }
    ],
    "output_params": [
        {
            "url": "/",
            "method": "post",
            "protocol": "http",
            "param_name": "predicted_label",
            "param_type": "string",
            "param_desc": '{\n    "type": "string"\n}',
        }
    ],
    "source_job_id": "5338",
    "source_job_version": "6420",
    "model_metrics": '{"f1":0.0,"recall":0.0,"precision":0.0,"accuracy":0.0}',
    "model_algorithm": "image_classification",
    "apis": [
        {
            "protocol": "http",
            "method": "post",
            "url": "/",
            "input_params": {
                "type": "object",
                "properties": {"images": {"type": "file"}},
            },
            "output_params": {
                "required": ["predicted_label", "scores"],
                "type": "object",
                "properties": {
                    "predicted_label": {"type": "string"},
                    "scores": {
                        "items": {
                            "minItems": 2.0,
                            "items": [{"type": "string"}, {"type": "number"}],
                            "type": "array",
                            "maxItems": 2.0,
                        },
                        "type": "array",
                    },
                },
            },
            "id": 0.0,
            "content_type": "multipart/form-data",
        }
    ],
    "model_labels": [],
    "labels_map": {"labels": []},
    "model_docs": [],
    "config": "{....config....}",
    "model_id": "model-id",
    "model_name": "model-43db",
    "model_version": "0.0.1",
    "model_type": "Image",
    "model_size": 2128636885,
    "model_status": "published",
    "tenant": "tenant-id",
    "project": "project-id",
    "owner": "owner-id",
    "create_at": 1658754813936,
    "workspace_id": "0",
    "ai_project": "default-ai-project",
    "install_type": ["real-time", "batch"],
    "model_source": "custom",
    "tunable": False,
    "market_flag": False,
    "publishable_flag": True,
    "specification": {},
    "runtime": "python2.7",
}


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
        sot = model.Model(**EXAMPLE)

        updated_sot_attrs = {
            "create_at": "created_at",
            "model_name": "name",
            "model_status": "status",
            "model_version": "version",
            "owner": "owner_id",
            "project": "project_id",
            "tenant": "tenant_id",
            "tunable": "is_tunable",
            "market_flag": "is_subscribed",
            "publishable_flag": "is_publishable",
        }

        for key, value in EXAMPLE.items():
            if key in updated_sot_attrs.keys():
                for k1, v1 in updated_sot_attrs.items():
                    self.assertEqual(getattr(sot, v1), EXAMPLE[k1])
            elif key in ("input_params", "output_params"):
                for param in value:
                    sot_param = model.ParamsSpec(**param)
                    for k2, v2 in param.items():
                        self.assertEqual(getattr(sot_param, k2), v2)

            elif key == "specification":
                sot_specification = model.SpecificationSpec(**value)
                for k3, v3 in value.items():
                    self.assertEqual(getattr(sot_specification, k3), v3)
            elif key == "apis":
                pass
            else:
                self.assertEqual(getattr(sot, key), value)
