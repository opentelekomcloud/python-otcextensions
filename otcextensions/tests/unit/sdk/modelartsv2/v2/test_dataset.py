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
    "dataset_id": "gfghHSokody6AJigS5A",
    "dataset_name": "dataset-f9e8",
    "dataset_type": 0,
    "data_format": "Default",
    "next_version_num": 4,
    "status": 1,
    "data_sources": [
        {"data_type": 0, "data_path": "/test-obs/input/catDog4/"}
    ],
    "create_time": 1605690595404,
    "update_time": 1605690595404,
    "description": "",
    "current_version_id": "54IXbeJhfttGpL46lbv",
    "current_version_name": "V003",
    "total_sample_count": 10,
    "annotated_sample_count": 10,
    "unconfirmed_sample_count": 0,
    "work_path": "/test-obs/output/",
    "inner_work_path": "/test-obs/output/dataset-f9e/",
    "inner_annotation_path": "/test-obs/output/dataset-f9e/annotation/",
    "inner_data_path": "/test-obs/output/dataset-f9e/data/",
    "inner_log_path": "/test-obs/output/dataset-f9e/logs/",
    "inner_temp_path": "/test-obs/output/dataset-f9e/temp/",
    "inner_task_path": "/test-obs/output/dataset-f9e/task/",
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
    "dataset_version_count": 3,
    "dataset_version": "v1",
    "content_labeling": True,
    "labels": [
        {
            "name": "Cat",
            "type": 0,
            "property": {"@modelarts:color": "#3399ff"},
        },
        {
            "name": "Dog",
            "type": 0,
            "property": {"@modelarts:color": "#3399ff"},
        },
    ],
}


class TestDataset(base.TestCase):
    def setUp(self):
        super(TestDataset, self).setUp()

    def test_basic(self):
        sot = dataset.Dataset()

        self.assertEqual("/datasets", sot.base_path)
        # self.assertEqual('', sot.resource_key)
        self.assertEqual("datasets", sot.resources_key)

        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_commit)

    def test_make_it(self):
        updated_sot_attrs = []
        sot = dataset.Dataset(**EXAMPLE)
        # self.assertEqual(EXAMPLE['create_time'], sot.created_at)

        for key, value in EXAMPLE.items():
            if key not in updated_sot_attrs:
                self.assertEqual(getattr(sot, key), value)
