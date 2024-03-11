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

# from pathlib import Path


# from PIL import Image


def get_directory_size(dir_path, file_type=None):
    total_size = 0
    # Add more file types as needed
    # file_types = {
    #     "image": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    #     "text": [".txt", ".doc", ".docx", ".pdf"],
    #     "speech": [".mp3", ".wav", ".ogg"],
    #     "table": [".csv", ".xls", ".xlsx"],
    #     "video": [".mp4", ".avi", ".mkv", ".mov"],
    # }
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
        raise exceptions.SDKException(f"The directory {dir_path} is empty.")
    for file_name in files:
        file_path = os.path.join(dir_path, file_name)
        # _, file_extension = os.path.splitext(file_path)
        # if file_extension.lower() in file_types[file_type]:
        #     total_size += os.path.getsize(file_path)
        total_size += os.path.getsize(file_path)
    if total_size == 0:
        raise exceptions.SDKException(
            "Directory is empty"
            # f"No files found of type {str(file_types[file_type])}"
        )
    return total_size, files


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

        :returns: a generator of
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
            comprised of the properties on the Datasets class.
        :returns: The results of dataset creation
        :rtype: :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Dataset`
        """
        return self._create(_dataset.Dataset, **attrs)

    def get_dataset(self, dataset):
        """Query details of a dataset.

        :param dataset: key id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Dataset`

        :returns: instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Dataset`
        """
        return self._get(_dataset.Dataset, dataset)

    def find_dataset(self, name_or_id, ignore_missing=False):
        """Find a dataset by name or id.

        :param name_or_id: The name or ID of a dataset
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the dataset does not exist.
            When set to ``True``, no exception will be set when attempting
            to find a nonexistent dataset.

        :returns:
            One :class:`~otcextensions.sdk.nat.v2.dataset.Dataset`
              or ``None``
        """
        return self._find(
            _dataset.Dataset,
            name_or_id,
            ignore_missing=ignore_missing,
        )

    def update_dataset(self, dataset, **attrs):
        """Get the dataset by id

        :param dataset: key id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Dataset`

        :returns: instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Dataset`
        """
        return self._update(_dataset.Dataset, dataset, **attrs)

    def delete_dataset(self, dataset, ignore_missing=False):
        """Delete a dataset.

        :param dataset: Thie value can be the name of a dataset
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the dataset does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent dataset.
        """
        return self._delete(
            _dataset.Dataset, dataset, ignore_missing=ignore_missing
        )

    # ======== Dataset Statistics ========

    def get_dataset_statistics(self, dataset_id):
        """Query Dataset statistics

        :param dataset_id: Dataset ID.

        :returns:
            (One :class:`~otcextensions.sdk.modelartsv2.v2.\
                dataset_statistics.DatasetStatistics`)
        """
        return self._get(
            _dataset_statistics.DatasetStatistics,
            datasetId=dataset_id,
            requires_id=False,
        )

    # ======== Dataset Label Management ========

    def dataset_labels(self, dataset_id, **params):
        """List all Labels in a dataset.

        :param dataset_id: Dataset ID.
        :param dict params: Optional query parameters to be sent to limit
            the instances being returned.
        :returns: a generator of
            (:class:`~otcextensions.sdk.modelartsv2.v2.dataset_label.DatasetLabel`)
            instances.
        """
        return self._list(
            _dataset_label.DatasetLabel, datasetId=dataset_id, **params
        )

    def create_dataset_label(self, dataset_id, **attrs):
        """Create a daraset label from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Label`,
            comprised of the properties on the Labels class.
        :returns: The results of label creation
        :rtype: :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Label`
        """
        return self._create(
            _dataset_label.DatasetLabel, datasetId=dataset_id, **attrs
        )

    def update_dataset_labels(self, dataset_id, **attrs):
        """Modify a dataset labels in batches.

        :param dataset_id: Dataset ID.

        :returns: instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Dataset`
        """
        obj = self._get_resource(
            _dataset_label.DatasetLabel, None, datasetId=dataset_id
        )
        return obj.update_labels(self, attrs.get("labels"))

    def delete_dataset_labels(self, dataset_id, delete_source=False, **labels):
        """Delete dataset labels.

        :param dataset_id: Dataset ID.
        :param labels: List of labels ID(s) to delete.

        :returns: ``None``
        """
        obj = _dataset_label.DatasetLabel(datasetId=dataset_id)
        return obj.delete_labels(
            self,
            **labels,
            delete_source=delete_source,
        )

    # ======== Dataset Version Management ========

    def dataset_versions(self, dataset_id):
        """List all dataset versions.

        :returns: a generator of
            (:class:`~otcextensions.sdk.modelartsv2.v2.\
                dataset_version.DatasetVersion`) instances
        """
        return self._list(
            _dataset_version.DatasetVersion, datasetId=dataset_id
        )

    def create_dataset_version(self, dataset_id, **attrs):
        """Create a dataset from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.modelartsv2.v2.datasets.Datasets`,
            comprised of the properties on the Datasets class.
        :returns: The results of dataset creation
        :rtype: :class:`~otcextensions.sdk.modelartsv2.v2.\
            dataset.DatasetVersion`
        """
        return self._create(
            _dataset_version.DatasetVersion,
            datasetId=dataset_id,
            **attrs,
        )

    def delete_dataset_version(self, dataset_id, version_id, **kwargs):
        """Delete a dataset version

        :param version_id: ID of a dataset version
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the group does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent dataset.
        """
        return self._delete(
            _dataset.Version,
            version_id,
            datasetId=dataset_id,
            **kwargs,
        )

    def get_dataset_version(self, dataset_id, version_id):
        """Get the dataset version by version id

        :param dataset_id: Dataset ID.
        :param version_id: key id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset.DatasetVersion`

        :returns: instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset.DatasetVersion`
        """
        return self._get(
            _dataset_version.DatasetVersion, version_id, datasetId=dataset_id
        )

    # ======== Dataset Sample Management ========

    def dataset_samples(self, dataset_id, **params):
        """List all Dataset Samples in a Dataset.

        :param dataset_id: Dataset ID.
        :param dict params: Optional query parameters to be sent to limit
            the instances being returned.
        :returns: a generator of
            (:class:`~otcextensions.sdk.modelartsv2.v2\
                    .dataset.DatasetSample`) instances
        """
        return self._list(
            _dataset_sample.DatasetSample,
            datasetId=dataset_id,
            **params,
            paginated=False,
        )

    def add_dataset_samples(
        self,
        dataset_id,
        directory_path=None,
        file_path=None,
        sample_type=None,
        labels=[],
        metadata={},
        data_source={},
    ):
        """Upload samples to a dataset.

        :param dataset_id: Dataset ID.
        :param dict attrs: Keyword arguments which will be used to create
            upload samples to a dataset and obtain instance of.
            a :class:`~otcextensions.sdk.modelartsv2.v2.\
                    dataset_sample.DatasetSample`,

        :returns: The result after uploading the dataset samples.

        :rtype: :class:`~otcextensions.sdk.modelartsv2.v2.\
                dataset.CreateSample`
        """
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
            # print("Files_Size after count: ", count, " ", files_size)
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
        return self._create(
            _dataset_sample.DatasetSample, datasetId=dataset_id, **attrs
        )

    def delete_dataset_samples(
        self, dataset_id, samples=[], delete_source=False
    ):
        """Delete dataset samples.

        :param dataset_id: Dataset ID.
        :param samples: List of sample ID(s) to delete.

        :returns: ``None``
        """
        dataset_sample = self._get_resource(
            _dataset_sample.DatasetSample, None
        )
        return dataset_sample.delete_samples(
            self, dataset_id, samples, delete_source
        )

    def get_dataset_sample(self, dataset_id, sample_id):
        """Get the Dataset Sample

        :param dataset_id: Dataset ID.
        :param sample_id: key id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset.sample.Sample`
        :returns: instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset.sample.Sample`
        """
        return self._get(
            _dataset_sample.DatasetSample, sample_id, datasetId=dataset_id
        )

    # ======== Dataset Import Task Management ========

    def dataset_import_tasks(self, dataset_id):
        """List all dataset export tasks.

        :returns: a generator of
            (:class:`~otcextensions.sdk.modelartsv2.v2.\
                    dataset.ImportTask`) instances.
        """
        return self._list(
            _dataset_import_task.DatasetImportTask, datasetId=dataset_id
        )

    def create_dataset_import_task(self, dataset_id, **attrs):
        """Create a data import task from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.modelartsv2.v2.dataset.ImportTask`,
            comprised of the properties on the ImportTask class.

        :returns: The results of dataset import task.

        :rtype: :class:`~otcextensions.sdk.modelartsv2.v2.dataset.ImportTask`
        """
        return self._create(
            _dataset_import_task.DatasetImportTask,
            datasetId=dataset_id,
            prepend_key=False,
            **attrs,
        )

    def get_dataset_import_task(self, dataset_id, task_id):
        """Get the data import task by dataset id

         :param dataset_id: key id or an instance of
             :class:`~otcextensions.sdk.modelartsv2.v2.dataset.ImportTask`

         :returns: instance of :class:`~otcextensions.sdk.modelartsv2.v2.\
                dataset.ImportTask`
         """
        return self._get(
            _dataset_import_task.DatasetImportTask,
            task_id,
            datasetId=dataset_id,
        )

    # ======== Dataset Export Task Management ========

    def get_dataset_export_task(self, dataset_id, task_id):
        """Get the dataset export task by dataset id

          :param dataset_id: key id or an instance of
              :class:`~otcextensions.sdk.modelartsv2.v2.dataset.ExportTask`

          :returns: instance of :class:`~otcextensions.sdk.modelartsv2.v2.\
                dataset.ExportTask`
          """
        return self._get(
            _dataset_export_task.DatasetExportTask,
            task_id,
            datasetId=dataset_id,
        )

    def dataset_export_tasks(self, dataset_id):
        """List all dataset export tasks.

        :returns: a generator of
            (:class:`~otcextensions.sdk.modelartsv2.v2.\
                    dataset.ExportTask`) instances
        """
        return self._list(
            _dataset_export_task.DatasetExportTask, datasetId=dataset_id
        )

    def create_dataset_export_task(self, dataset_id, **attrs):
        """Create a data import task from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.modelartsv2.v2.dataset.ExportTask`,
            comprised of the properties on the ExportTask class.

        :returns: The results of dataset export task.

        :rtype: :class:`~otcextensions.sdk.modelartsv2.v2.dataset.ExportTask`
        """
        return self._create(
            _dataset_export_task.DatasetExportTask,
            datasetId=dataset_id,
            **attrs,
        )

    # ======== Dataset Synchronization Task Management ========

    def dataset_sync(self, dataset_id):
        """Synchronize samples and labeling information
            from the input dataset path to the dataset.

        :param dataset_id: Dataset ID.
        :returns: None
        """
        return self._create(_dataset_sync.DatasetSync, datasetId=dataset_id)

    def get_dataset_sync_status(self, dataset_id):
        """Query Dataset sync task status

        :param dataset_id: Dataset ID.

        :returns:
            One :class:`~otcextensions.sdk.nat.v2.dataset.Sync`
        """
        return self._get(
            _dataset_sync.DatasetSync, "status", datasetId=dataset_id
        )
