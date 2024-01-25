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

EXAMPLE = {
    "dataset_id": "dataset-id",
    "dataset_name": "dataset-name",
    "dataset_type": 0,
    "data_format": "Default",
    "next_version_num": 1,
    "status": 1,
    "data_sources": [
        {
            "data_type": 0,
            "data_path": "/test-bucket/dataset/flowers/",
        }
    ],
    "create_time": 1704447736382,
    "update_time": 1704447736382,
    "description": "",
    "total_sample_count": 500,
    "annotated_sample_count": 0,
    "unconfirmed_sample_count": 0,
    "work_path": "/test-bucket/output/",
    "inner_work_path": "/test-bucket/output/tmp-path/",
    "inner_annotation_path": "/test-bucket/output/tmp-path/annotation/",
    "inner_data_path": "/test-bucket//output/tmp-path/data/",
    "inner_log_path": "/test-bucket/output/tmp-path/logs/",
    "inner_temp_path": "/test-bucket/output/tmp-path/temp/",
    "inner_task_path": "/test-bucket//output/tmp-path/task/",
    "work_path_type": 0,
    "workspace_id": "0",
    "enterprise_project_id": "0",
    "workforce_task_count": 0,
    "feature_supports": ["0"],
    "managed": False,
    "import_data": False,
    "ai_project": "default-ai-project",
    "label_task_count": 1,
    "dataset_format": 0,
    "dataset_version_count": 0,
    "dataset_version": "v1",
    "content_labeling": True,
    "data_update_time": 1704447743855,
    "labels": [
        {
            "name": "daisy",
            "type": 0,
            "property": {"@modelarts:color": "#266b5e"},
        },
        {
            "name": "dandelion",
            "type": 0,
            "property": {"@modelarts:color": "#1a0135"},
        },
    ],
}


class TestDataset(base.TestCase):
    def setUp(self):
        super(TestDataset, self).setUp()

    def test_basic(self):
        sot = dataset.Dataset()

        self.assertEqual("/datasets", sot.base_path)
        self.assertEqual(None, sot.resource_key)
        self.assertEqual("datasets", sot.resources_key)

        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)
        self.assertFalse(sot.allow_commit)

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
        updated_sot_attrs = []
        sot = dataset.Dataset(**EXAMPLE)

        for key, value in EXAMPLE.items():
            if key not in updated_sot_attrs:
                self.assertEqual(getattr(sot, key), value)
