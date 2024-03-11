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
from otcextensions.sdk.modelartsv2.v2 import dataset
from otcextensions.tests.unit.sdk.modelartsv2.v2 import examples
from otcextensions.tests.unit.utils import assert_attributes_equal

EXAMPLE = examples.DATASET

EXAMPLE_CREATE = {
    "workspace_id": "0",
    "dataset_name": "dataset-de83",
    "dataset_type": 400,
    "data_sources": [
        {
            "data_type": 0,
            "data_path": "/test-obs/table/input/",
            "with_column_header": True,
        }
    ],
    "description": "",
    "work_path": "/test-obs/table/output/",
    "work_path_type": 0,
    "schema": [
        {"schema_id": 1, "name": "150", "type": "STRING"},
        {"schema_id": 2, "name": "4", "type": "STRING"},
        {"schema_id": 3, "name": "setosa", "type": "STRING"},
        {"schema_id": 4, "name": "versicolor", "type": "STRING"},
        {"schema_id": 5, "name": "virginica", "type": "STRING"},
    ],
    "import_data": True,
}


class TestDataset(base.TestCase):
    def setUp(self):
        super(TestDataset, self).setUp()

    def test_basic(self):
        sot = dataset.Dataset()

        self.assertEqual("/datasets", sot.base_path)
        self.assertEqual("datasets", sot.resources_key)
        self.assertEqual(None, sot.resource_key)

        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_commit)

        self.assertDictEqual(
            {
                "check_running_task": "check_running_task",
                "contain_versions": "contain_versions",
                "dataset_type": "dataset_type",
                "file_preview": "file_preview",
                "limit": "limit",
                "marker": "marker",
                "offset": "offset",
                "order": "order",
                "running_task_type": "running_task_type",
                "search_content": "search_content",
                "sort_by": "sort_by",
                "support_export": "support_export",
                "train_evaluate_ratio": "train_evaluate_ratio",
                "version_format": "version_format",
                "with_labels": "with_labels",
                "workspace_id": "workspace_id",
            },
            sot._query_mapping._mapping,
        )

    def test_make_it(self):
        sot = dataset.Dataset(**EXAMPLE)
        self.assertEqual(sot.id, EXAMPLE["dataset_id"])
        for key, value in EXAMPLE.items():
            if key == "labels":
                for ix, data in enumerate(value):
                    self.assertEqual(sot.labels[ix].name, data["name"])
                    self.assertEqual(sot.labels[ix].type, data["type"])
                    self.assertEqual(
                        sot.labels[ix].attributes, data["attributes"]
                    )
                    self.assertEqual(
                        sot.labels[ix].property.color,
                        data["property"]["@modelarts:color"],
                    )
                    self.assertEqual(
                        sot.labels[ix].property.shortcut,
                        data["property"]["@modelarts:shortcut"],
                    )
            else:
                assert_attributes_equal(self, getattr(sot, key), value)

    def test_create_sot(self):
        sot = dataset.Dataset(**EXAMPLE_CREATE)
        assert_attributes_equal(self, sot, EXAMPLE_CREATE)
