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
from otcextensions.sdk.modelartsv2.v2 import dataset_import_task

EXAMPLE = {
    "status": "COMPLETED",
    "task_id": "gfghHSokody6AJigS5A_RHJ1zOkIoI3Nzwxj8nh",
    "dataset_id": "gfghHSokody6AJigS5A",
    "import_path": "obs://test-obs/daoLu_images/cat-rabbit/",
    "import_type": 0,
    "total_sample_count": 20,
    "imported_sample_count": 20,
    "annotated_sample_count": 20,
    "total_sub_sample_count": 0,
    "imported_sub_sample_count": 0,
    "total_file_size": 0,
    "finished_file_count": 0,
    "finished_file_size": 0,
    "total_file_count": 0,
    "update_ms": 1606114833955,
    "create_time": 1606114833874,
    "elapsed_time": 2,
}


class TestDatasetImportTask(base.TestCase):
    def setUp(self):
        super(TestDatasetImportTask, self).setUp()

    def test_basic(self):
        sot = dataset_import_task.DatasetImportTask()

        self.assertEqual("/datasets/%(datasetId)s/import-tasks", sot.base_path)
        self.assertEqual(None, sot.resource_key)
        self.assertEqual("import_tasks", sot.resources_key)

        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_create)
        self.assertFalse(sot.allow_delete)
        self.assertFalse(sot.allow_commit)

    def test_make_it(self):
        updated_sot_attrs = []
        sot = dataset_import_task.DatasetImportTask(**EXAMPLE)

        for key, value in EXAMPLE.items():
            if key not in updated_sot_attrs:
                self.assertEqual(getattr(sot, key), value)
