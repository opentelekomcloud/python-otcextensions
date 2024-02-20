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
import mock
from openstackclient.tests.unit import utils
from osc_lib import utils as _osc_lib_utils
from otcextensions.sdk.modelartsv2.v2 import dataset
from otcextensions.tests.unit.osclient import test_base


def gen_data(obj, columns, formatters=None):
    """Fill expected data tuple based on columns list"""
    return _osc_lib_utils.get_item_properties(
        obj, columns, formatters=formatters
    )


class TestModelartsv2(utils.TestCommand):
    def setUp(self):
        super(TestModelartsv2, self).setUp()

        self.app.client_manager.modelartsv2 = mock.Mock()

        self.client = self.app.client_manager.modelartsv2


class FakeDataset(test_base.Fake):
    """Fake one or more Modelarts dataset."""

    @classmethod
    def generate(cls):
        """Create a fake dataset sample.

        :return:
            A FakeResource object, with id, name and so on
        """
        object_info = {
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
            "inner_annotation_path": "/test-bucket/output/tmp-path/anotation/",
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
        return dataset.Dataset(**object_info)


class FakeStatistics(test_base.Fake):
    """Fake one or more Modelarts dataset Sample."""

    @classmethod
    def generate(cls):
        """Create a fake dataset statistics.

        :return:
            A FakeResource object, with id, name and so on
        """
        object_info = {
            "label_stats": [
                {
                    "name": "daisy",
                    "type": 0,
                    "property": {"@modelarts:color": "#266b5e"},
                    "count": 0,
                    "sample_count": 0,
                },
                {
                    "name": "dandelion",
                    "type": 0,
                    "property": {"@modelarts:color": "#1a0135"},
                    "count": 0,
                    "sample_count": 0,
                },
            ],
            "sample_stats": {
                "un_annotation": 500,
                "all": 500,
                "total": 500,
                "deleted": 0,
                "manual_annotation": 0,
                "auto_annotation": 0,
                "lefted": 500,
            },
            "key_sample_stats": {
                "total": 500,
                "non_key_sample": 500,
                "key_sample": 0,
            },
            "deletion_stats": {},
            "metadata_stats": {},
            "data_spliting_enable": False,
        }
        return dataset.Statistics(**object_info)


class FakeSample(test_base.Fake):
    """Fake one or more Modelarts dataset Sample."""

    @classmethod
    def generate(cls):
        """Create a fake dataset sample.

        :return:
            A FakeResource object, with id, name and so on
        """
        object_info = {
            "annotated_by": "human/OTC-EU-DE-000000000010000XXXXXX/dummy",
            "labels": [
                {
                    "name": "Tomato_healthy",
                    "property": {},
                    "type": 0,
                },
            ],
            "metadata": {
                "@modelarts:import_origin": 0,
                "@modelarts:size": [256, 256, 3],
                "@modelarts:source_image_info": "https://dummydummy/test",
            },
            "preview": "https://dummydummy/test",
            "sample_id": "000500f237d4c078ca64f2fd99da9828",
            "sample_status": "MANUAL_ANNOTATION",
            "sample_time": 1694457754000,
            "sample_type": 0,
            "source": "https://dummydummy/testdata",
        }
        return dataset.Sample(**object_info)


class FakeDeleteSample(test_base.Fake):
    """Fake dataset sample delete response."""

    @classmethod
    def generate(cls):
        object_info = {
            "success": False,
            "results": [
                {
                    "success": False,
                    "error_code": "ModelArts.4420",
                    "error_msg": "Sample not found. [sample-id]",
                },
                {
                    "success": True,
                },
            ],
        }
        return dataset.DeleteSample(**object_info)


class FakeDatasetSync(test_base.Fake):
    """Fake dataset sample delete response."""

    @classmethod
    def generate(cls):
        object_info = {
            "status": "COMPLETED",
            "dataset_id": "gfghHSokody6AJigS5A",
        }

        return dataset.Sync(**object_info)


class FakeDatasetImportTask(test_base.Fake):
    """Fake dataset export task response."""

    @classmethod
    def generate(cls):
        object_info = {
  "status" : "COMPLETED",
  "task_id" : "gfghHSokody6AJigS5A_RHJ1zOkIoI3Nzwxj8nh",
  "dataset_id" : "gfghHSokody6AJigS5A",
  "import_path" : "obs://test-obs/daoLu_images/cat-rabbit/",
  "import_type" : 0,
  "total_sample_count" : 20,
  "imported_sample_count" : 20,
  "annotated_sample_count" : 20,
  "total_sub_sample_count" : 0,
  "imported_sub_sample_count" : 0,
  "total_file_size" : 0,
  "finished_file_count" : 0,
  "finished_file_size" : 0,
  "total_file_count" : 0,
  "update_ms" : 1606114833955,
  "create_time" : 1606114833874,
  "elapsed_time" : 2
                }
        return dataset.ImportTask(**object_info)


class FakeDatasetExportTask(test_base.Fake):
    """Fake dataset export task response."""

    @classmethod
    def generate(cls):
        object_info = {
  "task_id" : "TZMuy7OKbClkGCAc3gb",
  "path" : "/test-obs/daoChu/",
  "export_type" : 3,
  "version_format" : "Default",
  "export_format" : 2,
  "export_params" : {
    "sample_state" : "",
    "export_dest" : "DIR",
    "clear_hard_property" : True,
    "clear_difficult" : False,
    "train_sample_ratio" : 1.0,
    "ratio_sample_usage" : False
  },
  "status" : "RUNNING",
  "progress" : 0.0,
  "create_time" : 1606103424662,
  "update_time" : 1606103494124
        }
        return dataset.ExportTask(**object_info)

