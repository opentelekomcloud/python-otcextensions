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
import base64
import os

from openstack.tests.unit import test_proxy_base
from otcextensions.sdk.modelartsv2.v2 import _proxy
from otcextensions.sdk.modelartsv2.v2 import dataset
from otcextensions.sdk.modelartsv2.v2 import dataset_export_task
from otcextensions.sdk.modelartsv2.v2 import dataset_import_task
from otcextensions.sdk.modelartsv2.v2 import dataset_label
from otcextensions.sdk.modelartsv2.v2 import dataset_sample
from otcextensions.sdk.modelartsv2.v2 import dataset_statistics
from otcextensions.sdk.modelartsv2.v2 import dataset_sync
from otcextensions.sdk.modelartsv2.v2 import dataset_version


class TestModelartsV2Proxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestModelartsV2Proxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestDataset(TestModelartsV2Proxy):
    def test_datasets(self):
        self.verify_list(
            self.proxy.datasets,
            dataset.Dataset,
            method_kwargs={"limit": 10},
            expected_kwargs={"limit": 10},
        )

    def test_get_dataset(self):
        self.verify_get(
            self.proxy.get_dataset,
            dataset.Dataset,
            method_args=["dataset-uuid"],
            expected_args=["dataset-uuid"],
        )

    def test_find_dataset(self):
        self.verify_find(
            self.proxy.find_dataset,
            dataset.Dataset,
        )

    def test_create_dataset(self):
        self.verify_create(
            self.proxy.create_dataset,
            dataset.Dataset,
            method_kwargs={"arg1": "val1", "arg2": "val2"},
            expected_kwargs={"arg1": "val1", "arg2": "val2"},
        )

    def test_delete_dataset(self):
        self.verify_delete(
            self.proxy.delete_dataset,
            dataset.Dataset,
            False,
        )

    def test_delete_dataset_ignore(self):
        self.verify_delete(
            self.proxy.delete_dataset,
            dataset.Dataset,
            True,
        )


class TestDatasetSample(TestModelartsV2Proxy):
    def test_dataset_samples(self):
        self.verify_list(
            self.proxy.dataset_samples,
            dataset_sample.DatasetSample,
            method_args=["dataset-uuid"],
            expected_args=[],
            method_kwargs={"limit": 10},
            expected_kwargs={"datasetId": "dataset-uuid", "limit": 10},
        )

    def test_get_dataset_sample(self):
        self.verify_get(
            self.proxy.get_dataset_sample,
            dataset_sample.DatasetSample,
            method_args=["dataset-uuid", "sample-uuid"],
            expected_args=["sample-uuid"],
            expected_kwargs={"datasetId": "dataset-uuid"},
        )

    def test_add_dataset_samples(self):
        dirname = os.path.dirname(__file__)
        file_path = os.path.join(dirname, "8710109684_e2c5ef6aeb_n.jpg")
        with open(file_path, "rb") as file:
            sample = {
                "name": "8710109684_e2c5ef6aeb_n.jpg",
                "data": base64.b64encode(file.read()).decode(),
            }
        self.verify_create(
            self.proxy.add_dataset_samples,
            dataset_sample.DatasetSample,
            method_args=["dataset-uuid"],
            expected_args=[],
            method_kwargs={
                "file_path": file_path,
            },
            expected_kwargs={
                "datasetId": "dataset-uuid",
                "samples": [sample],
            },
        )

    def test_delete_dataset_samples(self):
        self._verify(
            "otcextensions.sdk.modelartsv2.v2.dataset_sample.DatasetSample.delete_samples",  # noqa
            self.proxy.delete_dataset_samples,
            method_args=["dataset-id"],
            method_kwargs={
                "samples": ["s1-uuid", "s2-uuid"],
                "delete_source": False,
            },
            expected_args=[
                self.proxy,
                "dataset-id",
                ["s1-uuid", "s2-uuid"],
                False,
            ],
        )


class TestDatasetLabel(TestModelartsV2Proxy):
    def test_dataset_labels(self):
        self.verify_list(
            self.proxy.dataset_labels,
            dataset_label.DatasetLabel,
            method_kwargs={"dataset": "dataset-id"},
            expected_kwargs={"datasetId": "dataset-id"},
        )

    def test_create_dataset_label(self):
        self.verify_create(
            self.proxy.create_dataset_label,
            dataset_label.DatasetLabel,
            method_kwargs={
                "dataset": "dataset-id",
                "arg1": "val1",
                "arg2": "val2",
            },
            expected_kwargs={
                "datasetId": "dataset-id",
                "arg1": "val1",
                "arg2": "val2",
            },
        )

    def test_update_dataset_labels(self):
        self._verify(
            "otcextensions.sdk.modelartsv2.v2.dataset_label.DatasetLabel.update_labels",  # noqa
            self.proxy.update_dataset_labels,
            method_args=["dataset-id"],
            method_kwargs={
                "labels": [{"name": "cat"}, {"name": "pussycat"}],
            },
            expected_args=[
                self.proxy,
                [{"name": "cat"}, {"name": "pussycat"}],
            ],
        )

    def test_delete_dataset_labels(self):
        self._verify(
            "otcextensions.sdk.modelartsv2.v2.dataset_label.DatasetLabel.delete_labels",  # noqa
            self.proxy.delete_dataset_labels,
            method_args=["dataset-id"],
            method_kwargs={
                "labels": [{"name": "cat"}, {"name": "pussycat"}],
                "delete_policy": 0,
            },
            expected_args=[
                self.proxy,
                [{"name": "cat"}, {"name": "pussycat"}],
                0,
            ],
        )


class TestDatasetExportTask(TestModelartsV2Proxy):
    def test_dataset_export_tasks(self):
        self.verify_list(
            self.proxy.dataset_export_tasks,
            dataset_export_task.DatasetExportTask,
            method_kwargs={"dataset": "dataset-id"},
            expected_kwargs={"datasetId": "dataset-id"},
        )

    def test_get_dataset_export_task(self):
        self.verify_get(
            self.proxy.get_dataset_export_task,
            dataset_export_task.DatasetExportTask,
            method_args=["dataset-id", "task-id"],
            expected_args=["task-id"],
            expected_kwargs={"datasetId": "dataset-id"},
        )

    def test_create_dataset_export_task(self):
        self.verify_create(
            self.proxy.create_dataset_export_task,
            dataset_export_task.DatasetExportTask,
            method_kwargs={"dataset": "dataset-id"},
            expected_kwargs={"datasetId": "dataset-id"},
        )


class TestDatasetImportTask(TestModelartsV2Proxy):
    def test_dataset_import_tasks(self):
        self.verify_list(
            self.proxy.dataset_import_tasks,
            dataset_import_task.DatasetImportTask,
            method_kwargs={"dataset": "dataset-id"},
            expected_kwargs={"datasetId": "dataset-id"},
        )

    def test_get_dataset_export_task(self):
        self.verify_get(
            self.proxy.get_dataset_import_task,
            dataset_import_task.DatasetImportTask,
            method_args=["dataset-id", "task-id"],
            expected_args=["task-id"],
            expected_kwargs={"datasetId": "dataset-id"},
        )

    def test_create_dataset_import_task(self):
        self.verify_create(
            self.proxy.create_dataset_import_task,
            dataset_import_task.DatasetImportTask,
            method_kwargs={"dataset": "dataset-id"},
            expected_kwargs={"datasetId": "dataset-id"},
        )


class TestDatasetVersion(TestModelartsV2Proxy):
    def test_dataset_versions(self):
        self.verify_list(
            self.proxy.dataset_versions,
            dataset_version.DatasetVersion,
            method_kwargs={"dataset": "dataset-id"},
            expected_kwargs={"datasetId": "dataset-id"},
        )

    def test_get_dataset_version(self):
        self.verify_get(
            self.proxy.get_dataset_version,
            dataset_version.DatasetVersion,
            method_args=["dataset-id", "version-id"],
            expected_args=["version-id"],
            expected_kwargs={"datasetId": "dataset-id"},
        )

    def test_create_dataset_version(self):
        self.verify_create(
            self.proxy.create_dataset_version,
            dataset_version.DatasetVersion,
            method_kwargs={"dataset": "dataset-id"},
            expected_kwargs={"datasetId": "dataset-id"},
        )

    def test_delete_dataset_version(self):
        self.verify_delete(
            self.proxy.delete_dataset_version,
            dataset_version.DatasetVersion,
            False,
            method_args=["dataset-id", "version-id"],
            expected_args=["version-id"],
            expected_kwargs={"datasetId": "dataset-id"},
        )


class TestDatasetStatistics(TestModelartsV2Proxy):
    def test_get_dataset_statistics(self):
        self.verify_get(
            self.proxy.get_dataset_statistics,
            dataset_statistics.DatasetStatistics,
            method_args=[],
            method_kwargs={"dataset": "dataset-id"},
            expected_kwargs={"datasetId": "dataset-id", "requires_id": False},
        )


class TestDatasetSync(TestModelartsV2Proxy):
    def test_get_dataset_sync_status(self):
        self.verify_get(
            self.proxy.get_dataset_sync_status,
            dataset_sync.DatasetSync,
            method_args=[],
            expected_args=["status"],
            method_kwargs={"dataset": "dataset-id"},
            expected_kwargs={"datasetId": "dataset-id"},
        )

    def test_dataset_sync(self):
        self.verify_create(
            self.proxy.dataset_sync,
            dataset_sync.DatasetSync,
            method_kwargs={"dataset": "dataset-id"},
            expected_kwargs={"datasetId": "dataset-id"},
        )
