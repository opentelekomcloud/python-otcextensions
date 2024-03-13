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

from openstack import exceptions
from openstack import proxy
from otcextensions.sdk.modelartsv2.v2 import dataset as _dataset
from otcextensions.sdk.modelartsv2.v2 import \
    dataset_export_task as _dataset_export_task
from otcextensions.sdk.modelartsv2.v2 import \
    dataset_import_task as _dataset_import_task
from otcextensions.sdk.modelartsv2.v2 import dataset_label as _dataset_label
from otcextensions.sdk.modelartsv2.v2 import dataset_sample as _dataset_sample
from otcextensions.sdk.modelartsv2.v2 import \
    dataset_statistics as _dataset_statistics
from otcextensions.sdk.modelartsv2.v2 import dataset_sync as _dataset_sync
from otcextensions.sdk.modelartsv2.v2 import \
    dataset_version as _dataset_version


class Proxy(proxy.Proxy):
    skip_discovery = True

    def __init__(self, session, *args, **kwargs):
        super(Proxy, self).__init__(session=session, *args, **kwargs)
        self.additional_headers = {
            "Accept": "application/json",
            "Content-type": "application/json",
        }

    # ======== Dataset Management ========
    def datasets(self, **params):
        """List all Datasets.

        :param dict params: Optional query parameters to be sent to limit
            the datasets being returned.

        :returns: A generator of
            (:class:`~otcextensions.sdk.modelartsv2.v2.dataset.Dataset`)
            instances.
        """
        if params.get("limit"):
            params.update(paginated=False)
        return self._list(_dataset.Dataset, **params)

    def create_dataset(self, **attrs):
        """Create a dataset from attributes.

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Dataset`,
            comprised of the properties on the Dataset class.
        :returns: The result of dataset creation.
        :rtype: Instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Dataset`.
        """
        return self._create(_dataset.Dataset, **attrs)

    def get_dataset(self, dataset):
        """Query details of a dataset.

        :param dataset: Dataset id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Dataset`.

        :returns: Instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Dataset`.
        """
        return self._get(_dataset.Dataset, dataset)

    def find_dataset(self, name_or_id, ignore_missing=False):
        """Find a dataset by name or id.

        :param name_or_id: The name or ID of a dataset.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the dataset does not exist.
            When set to ``True``, no exception will be set when attempting
            to find a nonexistent dataset.

        :returns: Instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Dataset`.
        """
        return self._find(
            _dataset.Dataset,
            name_or_id,
            ignore_missing=ignore_missing,
        )

    def update_dataset(self, dataset, **attrs):
        """Get details of a dataset.

        :param dataset: Dataset id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Dataset`
        :param dict attrs: Keyword arguments which will be used to update
            a :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Dataset`,
            comprised of the properties on the Dataset class.

        :returns: Instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Dataset`.
        """
        return self._update(_dataset.Dataset, dataset, **attrs)

    def delete_dataset(self, dataset, ignore_missing=False):
        """Delete a dataset.

        :param dataset: Dataset id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Dataset`.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the dataset does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent dataset.

        returns: ``None``
        """
        return self._delete(
            _dataset.Dataset, dataset, ignore_missing=ignore_missing
        )

    # ======== Dataset Statistics ========

    def get_dataset_statistics(self, dataset):
        """Query Dataset statistics.

        :param dataset: Dataset id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Dataset`

        :returns: Instance of :class:`~otcextensions.sdk.modelartsv2.v2.
            dataset_statistics.DatasetStatistics`.
        """
        dataset = self._get_resource(_dataset.Dataset, dataset)
        return self._get(
            _dataset_statistics.DatasetStatistics,
            datasetId=dataset.id,
            requires_id=False,
        )

    # ======== Dataset Label Management ========

    def dataset_labels(self, dataset, **params):
        """List all Labels in a dataset.

        :param dataset: Dataset id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Dataset`
        :param dict params: Optional query parameters to be sent to limit
            the instances being returned.

        :returns: A generator of (:class:`~otcextensions.sdk.modelartsv2.v2.
            dataset_label.DatasetLabel`) instances.
        """
        dataset = self._get_resource(_dataset.Dataset, dataset)
        return self._list(
            _dataset_label.DatasetLabel, datasetId=dataset.id, **params
        )

    def create_dataset_label(self, dataset, **attrs):
        """Create a dataset label from attributes.

        :param dataset: Dataset id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Dataset`.
        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.modelartsv2.v2.
            dataset_label.DatasetLabel`,
            comprised of the properties on the DatasetLabel class.

        :returns: The results of label creation.
        :rtype: Instance of :class:`~otcextensions.sdk.modelartsv2.v2.
            dataset_label.DatasetLabel`.
        """
        dataset = self._get_resource(_dataset.Dataset, dataset)
        return self._create(
            _dataset_label.DatasetLabel, datasetId=dataset.id, **attrs
        )

    def update_dataset_labels(self, dataset, labels=[], **attrs):
        """Modify dataset labels in batches.

        :param dataset: Dataset id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Dataset`.
        :param labels: List of Labels to update.
        :param dict attrs: Keyword arguments which will be used to update
            a :class:`~otcextensions.sdk.modelartsv2.v2.
            dataset_label.DatasetLabel`,
            comprised of the properties on the DatasetLabel class.

        :returns: Instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset_label.DatasetLabel`
        """
        dataset = self._get_resource(_dataset.Dataset, dataset)
        obj = self._get_resource(
            _dataset_label.DatasetLabel, None, datasetId=dataset.id
        )
        labels = labels or attrs.get("labels")
        return obj.update_labels(self, labels)

    def delete_dataset_labels(
        self, dataset, labels=[], delete_policy=None, **attrs
    ):
        """Delete dataset labels in batches.

        :param dataset: Dataset id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Dataset`.
        :param labels: List of labels dict to delete.
        :param dict attrs: Keyword arguments which will be used to delete a
            :class:`~otcextensions.sdk.modelartsv2.v2.
            dataset_label.DatasetLabel`,
            comprised of the properties on the DatasetLabel class.

        :returns: ``None``
        """
        dataset = self._get_resource(_dataset.Dataset, dataset)
        obj = self._get_resource(
            _dataset_label.DatasetLabel, None, datasetId=dataset.id
        )
        labels = labels or attrs.get("labels")
        return obj.delete_labels(self, labels, delete_policy)

    # ======== Dataset Version Management ========

    def dataset_versions(self, dataset, **params):
        """List all versions of a dataset.

        :param dataset: Dataset id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Dataset`.

        :returns: a generator of (:class:`~otcextensions.sdk.modelartsv2.v2.
            dataset_version.DatasetVersion`) instances.
        """
        dataset = self._get_resource(_dataset.Dataset, dataset)
        return self._list(
            _dataset_version.DatasetVersion, datasetId=dataset.id
        )

    def create_dataset_version(self, dataset, **attrs):
        """Create a dataset version from attributes.

        :param dataset: Dataset id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Dataset`
        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.modelartsv2.v2.
            dataset_version.DatasetVersion`,
            comprised of the properties on the DatasetVersion class.

        :returns: The results of dataset creation.
        :rtype: Instance of :class:`~otcextensions.sdk.modelartsv2.v2.
            dataset_version.DatasetVersion`.
        """
        dataset = self._get_resource(_dataset.Dataset, dataset)
        return self._create(
            _dataset_version.DatasetVersion,
            datasetId=dataset.id,
            **attrs,
        )

    def get_dataset_version(self, dataset, dataset_version):
        """Get details of a dataset version.

        :param dataset: Dataset id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Dataset`.
        :param dataset_version: Dataset version id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset_version.DatasetVersion`.

        :returns: Instance of :class:`~otcextensions.sdk.modelartsv2.v2.
            dataset_version.DatasetVersion`.
        """
        dataset = self._get_resource(_dataset.Dataset, dataset)
        return self._get(
            _dataset_version.DatasetVersion,
            dataset_version,
            datasetId=dataset.id,
        )

    def delete_dataset_version(
        self, dataset, dataset_version, ignore_missing=False
    ):
        """Delete a dataset version

        :param dataset: Dataset id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Dataset`
        :param dataset_version: Dataset version id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset_version.DatasetVersion`
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the group does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent dataset.

        :returns: ``None``
        """
        dataset = self._get_resource(_dataset.Dataset, dataset)
        return self._delete(
            _dataset_version.DatasetVersion,
            dataset_version,
            datasetId=dataset.id,
            ignore_missing=ignore_missing,
        )

    # ======== Dataset Sample Management ========

    def dataset_samples(self, dataset, **params):
        """List all samples in a Dataset.

        :param dataset: Dataset id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Dataset`
        :param dict params: Optional query parameters to be sent to limit
            the dataset samples being returned.
        :returns: a generator of (:class:`~otcextensions.sdk.modelartsv2.v2.
            dataset_sample.DatasetSample`) instances.
        """
        dataset = self._get_resource(_dataset.Dataset, dataset)
        return self._list(
            _dataset_sample.DatasetSample,
            datasetId=dataset.id,
            **params,
            paginated=False,
        )

    def add_dataset_samples(
        self,
        dataset,
        directory_path=None,
        file_path=None,
        sample_type=None,
        labels=[],
        metadata={},
        data_source={},
    ):
        """Upload samples to a dataset.

        :param dataset: Dataset id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Dataset`.
        :param dict attrs: Keyword arguments which will be used to create
            upload samples to a dataset and obtain instance of a
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset_sample.DatasetSample` # noqa: E501

        :returns: The result after uploading the dataset samples.
        :rtype: Instance of :class:`~otcextensions.sdk.modelartsv2.v2.
            dataset_sample.DatasetSample`.
        """

        def get_directory_size(dir_path, file_type=None):
            total_size = 0
            if not os.path.isdir(dir_path):
                raise exceptions.SDKException(
                    f"Error: {dir_path} is not a valid directory."
                )
            files = [
                os.path.join(dir_path, f)
                for f in os.listdir(dir_path)
                if os.path.isfile(os.path.join(dir_path, f))
            ]
            if not files:
                raise exceptions.SDKException(
                    f"The directory {dir_path} is empty."
                )
            for file_name in files:
                file_path = os.path.join(dir_path, file_name)
                total_size += os.path.getsize(file_path)
            if total_size == 0:
                raise exceptions.SDKException("Directory is empty")
            return total_size, files

        if file_path:
            file_size = os.path.getsize(file_path) / (1024 * 1024)
            if file_size > 7.5:
                raise exceptions.SDKException("File size is > 7.5 Mb")
            files = [file_path]
            # with Image.open(file_path) as image:
            #     with io.BytesIO() as byte_stream:
            #         image.save(byte_stream, format="JPEG")
            #         image_bytes = byte_stream.getvalue()
            # sample = {
            #     "name": os.path.split(file_path)[1],
            #     "data": base64.b64encode(image_bytes).decode("utf-8"),
            # }

        if not file_path and directory_path:
            _, files = get_directory_size(directory_path)
            # size, files = get_directory_size(directory_path)
            # if size / (1024 * 1024) > 7.5:
            #     raise exceptions.SDKException("Files size is > 7.5 Mb")

        count = 0
        samples = []
        files_size = 0
        for file_path in files:
            sample = {}
            count = count + 1
            files_size = files_size + os.path.getsize(file_path) / (
                1024 * 1024
            )
            if files_size > 7.5:
                break
            with open(file_path, "rb") as file:
                sample = {
                    "name": os.path.split(file_path)[1],
                    "data": base64.b64encode(file.read()).decode(),
                }
            if labels:
                sample.update(labels=labels)
            if data_source:
                sample.update(data_source=data_source)
            if sample_type:
                sample.update(sample_type=sample_type)
            if metadata:
                sample.update(metadata=metadata)
            samples.append(sample)
        attrs = {}
        if samples:
            attrs.update(samples=samples)
        dataset = self._get_resource(_dataset.Dataset, dataset)
        return self._create(
            _dataset_sample.DatasetSample, datasetId=dataset.id, **attrs
        )

    def delete_dataset_samples(self, dataset, samples=[], delete_source=False):
        """Delete dataset samples in batches.

        :param dataset: Dataset id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Dataset`
        :param samples: List of sample ID(s) to delete.
        :param bool delete_source: When set to ``True``
            sample source files will be also deleted.

        :returns: ``None``
        """
        dataset = self._get_resource(_dataset.Dataset, dataset)
        dataset_sample = self._get_resource(
            _dataset_sample.DatasetSample, None
        )
        return dataset_sample.delete_samples(
            self, dataset.id, samples, delete_source
        )

    def get_dataset_sample(self, dataset, dataset_sample):
        """Get details of the dataset sample.

        :param dataset: Dataset id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Dataset`
        :param dataset_sample: Dataset sample id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset_sample.DatasetSample`

        :returns: Instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset_sample.DatasetSample`
        """
        dataset = self._get_resource(_dataset.Dataset, dataset)
        return self._get(
            _dataset_sample.DatasetSample, dataset_sample, datasetId=dataset.id
        )

    # ======== Dataset Import Task Management ========

    def dataset_import_tasks(self, dataset, **params):
        """List all dataset import tasks.

        :param dataset: Dataset id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Dataset`
        :param dict params: Optional query parameters to be sent to limit
            the dataset import tasks being returned.

        :returns: A generator of (:class:`~otcextensions.sdk.modelartsv2.v2.
            dataset_import_task.DatasetImportTask`).
        """
        dataset = self._get_resource(_dataset.Dataset, dataset)
        return self._list(
            _dataset_import_task.DatasetImportTask,
            datasetId=dataset.id,
            **params,
        )

    def create_dataset_import_task(self, dataset, **attrs):
        """Create a data import task from attributes.

        :param dataset: Dataset id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Dataset`
        :param dict attrs: Keyword arguments which will be used to create a
            :class:`~otcextensions.sdk.modelartsv2.v2.
            dataset_import_task.DatasetImportTask`,
            comprised of the properties on the DatasetImportTask class.

        :returns: The results of dataset import task.
        :rtype: Instance of :class:`~otcextensions.sdk.modelartsv2.v2.
            dataset_import_task.DatasetImportTask`.
        """
        dataset = self._get_resource(_dataset.Dataset, dataset)
        return self._create(
            _dataset_import_task.DatasetImportTask,
            datasetId=dataset.id,
            **attrs,
        )

    def get_dataset_import_task(self, dataset, import_task):
        """Get details of a dataset import task.

        :param dataset: Dataset id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Dataset`
        :param import_task: Import task id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.
            dataset_import_task.DatasetImportTask`.

        :returns: Instance of :class:`~otcextensions.sdk.modelartsv2.v2.
            dataset_import_task.DatasetImportTask`.
        """
        dataset = self._get_resource(_dataset.Dataset, dataset)
        return self._get(
            _dataset_import_task.DatasetImportTask,
            import_task,
            datasetId=dataset.id,
        )

    # ======== Dataset Export Task Management ========

    def dataset_export_tasks(self, dataset, **params):
        """List all dataset export tasks.

        :param dataset: Dataset id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Dataset`
        :param dict params: Optional query parameters to be sent to limit
            the dataset export tasks being returned.

        :returns: A generator of
            (:class:`~otcextensions.sdk.modelartsv2.v2.
            dataset_export_task.DatasetExportTask`) instances.
        """
        dataset = self._get_resource(_dataset.Dataset, dataset)
        return self._list(
            _dataset_export_task.DatasetExportTask,
            datasetId=dataset.id,
            **params,
        )

    def create_dataset_export_task(self, dataset, **attrs):
        """Create a data import task from attributes.

        :param dataset: Dataset id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Dataset`
        :param dict attrs: Keyword arguments which will be used to create a
            :class:`~otcextensions.sdk.modelartsv2.v2.
            dataset_export_task.DatasetExportTask`,
            comprised of the properties on the DatasetExportTask class.

        :returns: The results of dataset export task.
        :rtype: Instance of :class:`~otcextensions.sdk.modelartsv2.v2.
            dataset_export_task.DatasetExportTask`.
        """
        dataset = self._get_resource(_dataset.Dataset, dataset)
        return self._create(
            _dataset_export_task.DatasetExportTask,
            datasetId=dataset.id,
            **attrs,
        )

    def get_dataset_export_task(self, dataset, export_task):
        """Get details of a dataset export task.

        :param dataset: Dataset id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Dataset`
        :param export_task: Export Task id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.
            dataset_export_task.DatasetExportTask`.

        :returns: Instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.
            dataset_export_task.DatasetExportTask`.
        """
        dataset = self._get_resource(_dataset.Dataset, dataset)
        return self._get(
            _dataset_export_task.DatasetExportTask,
            export_task,
            datasetId=dataset.id,
        )

    # ======== Dataset Synchronization Task Management ========

    def dataset_sync(self, dataset):
        """Synchronize samples and labeling information
            from the input dataset path to the dataset.

        :param dataset: Dataset id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Dataset`.

        :returns: Instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset_sync.DatasetSync`.
        """
        dataset = self._get_resource(_dataset.Dataset, dataset)
        return self._create(_dataset_sync.DatasetSync, datasetId=dataset.id)

    def get_dataset_sync_status(self, dataset):
        """Query Dataset sync task status.

        :param dataset: Dataset id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Dataset`.

        :returns: Instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset_sync.DatasetSync`.
        """
        dataset = self._get_resource(_dataset.Dataset, dataset)
        return self._get(
            _dataset_sync.DatasetSync, "status", datasetId=dataset.id
        )
