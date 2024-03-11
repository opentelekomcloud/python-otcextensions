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
from otcextensions.sdk.modelartsv2.v2 import dataset_export_task
from otcextensions.sdk.modelartsv2.v2 import dataset_import_task
from otcextensions.sdk.modelartsv2.v2 import dataset_sample
from otcextensions.sdk.modelartsv2.v2 import dataset_statistics
from otcextensions.sdk.modelartsv2.v2 import dataset_sync
from otcextensions.sdk.modelartsv2.v2 import dataset_version
from otcextensions.tests.unit.osclient import test_base
from otcextensions.tests.unit.sdk.modelartsv2.v2 import examples


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
        return dataset.Dataset(**examples.DATASET)


class FakeDatasetVersion(test_base.Fake):
    """Fake one or more Modelarts dataset."""

    @classmethod
    def generate(cls):
        """Create a fake dataset sample.

        :return:
            A FakeResource object, with id, name and so on
        """
        return dataset_version.DatasetVersion(**examples.DATASET_VERSION)


class FakeDatasetStatistics(test_base.Fake):
    """Fake one or more Modelarts dataset Sample."""

    @classmethod
    def generate(cls):
        """Create a fake dataset statistics.

        :return:
            A FakeResource object, with id, name and so on
        """
        return dataset_statistics.DatasetStatistics(
            **examples.DATASET_STATISTICS
        )


class FakeDatasetSample(test_base.Fake):
    """Fake one or more Modelarts dataset Sample."""

    @classmethod
    def generate(cls):
        """Create a fake dataset sample.

        :return:
            A FakeResource object, with id, name and so on
        """
        return dataset_sample.DatasetSample(**examples.DATASET_SAMPLE)


class FakeDatasetSampleResp(test_base.Fake):
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
        return dataset_sample.DatasetSample(**object_info)


class FakeDatasetSync(test_base.Fake):
    """Fake dataset sample delete response."""

    @classmethod
    def generate(cls):
        object_info = {
            "status": "COMPLETED",
            "dataset_id": "gfghHSokody6AJigS5A",
        }

        return dataset_sync.DatasetSync(**object_info)


class FakeDatasetImportTask(test_base.Fake):
    """Fake dataset export task response."""

    @classmethod
    def generate(cls):
        return dataset_import_task.DatasetImportTask(
            **examples.DATASET_IMPORT_TASK
        )


class FakeDatasetExportTask(test_base.Fake):
    """Fake dataset export task response."""

    @classmethod
    def generate(cls):
        return dataset_export_task.DatasetExportTask(
            **examples.DATASET_EXPORT_TASK
        )
