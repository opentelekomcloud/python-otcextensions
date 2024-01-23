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
from openstack import proxy
# from otcextensions.sdk.modelartsv2.v2 import sample as _sample
from otcextensions.sdk.modelartsv2.v2 import dataset as _dataset
from otcextensions.sdk.modelartsv2.v2 import \
    dataset_export_task as _dataset_export_task
from otcextensions.sdk.modelartsv2.v2 import \
    dataset_import_task as _dataset_import_task
from otcextensions.sdk.modelartsv2.v2 import dataset_sample as _dataset_sample
from otcextensions.sdk.modelartsv2.v2 import \
    dataset_synchronization_task as _dataset_synchronization_task
from otcextensions.sdk.modelartsv2.v2 import \
    dataset_version as _dataset_version
from otcextensions.sdk.modelartsv2.v2 import label as _label


class Proxy(proxy.Proxy):
    skip_discovery = True

    def __init__(self, session, *args, **kwargs):
        super(Proxy, self).__init__(session=session, *args, **kwargs)
        self.additional_headers = {
            "Accept": "application/json",
            "Content-type": "application/json",
        }

    # ======== Dataset ========
    def datasets(self):
        """List all Datasets.

        :returns: a generator of
            (:class:`~otcextensions.sdk.modelartsv2.v2\
                    .dataset.Datasets`) instances
        """
        return self._list(_dataset.Dataset)

    def create_dataset(self, **attrs):
        """Create a dataset from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.modelartsv2.v2.datasets.Datasets`,
            comprised of the properties on the Datasets class.
        :returns: The results of dataset creation
        :rtype: :class:`~otcextensions.sdk.modelartsv2.v2.datasets.Datasets`
        """
        return self._create(_dataset.Dataset, prepend_key=False, **attrs)

    def delete_dataset(self, dataset, ignore_missing=False):
        """Delete a dataset

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

    def show_dataset(self, dataset):
        """Get the dataset by id

        :param dataset: key id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.datasets.Datasets`

        :returns: instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.datasets.Datasets`
        """
        return self._get(_dataset.Dataset, dataset)

    def find_dataset(self, name_or_id, ignore_missing=False):
        """Find a single gateway

        :param name_or_id: The name or ID of a gateway
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the gateway does not exist.
            When set to ``True``, no exception will be set when attempting
            to find a nonexistent gateway.

        :returns:
            One :class:`~otcextensions.sdk.nat.v2.gateway.Gateway` or ``None``
        """
        return self._find(
            _dataset.Dataset, name_or_id, ignore_missing=ignore_missing
        )

    def modify_dataset(self, dataset_id, **attrs):
        """Get the dataset by id

        :param dataset: key id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.datasets.Datasets`

        :returns: instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.datasets.Datasets`
        """
        return self._update(_dataset.Dataset, dataset_id, **attrs)

    def labels(self, **attrs):
        """List all Labels.

        :returns: a generator of
            (:class:`~otcextensions.sdk.modelartsv2.v2.label.Label`) instances
        """
        return self._list(_label.Label, **attrs)

    def label_stats(self, **attrs):
        """List all Labels.

        :returns: a generator of
            (:class:`~otcextensions.sdk.modelartsv2.v2.label.LabelStatistic`)
            instances
        """
        return self._list(_label.LabelStatistic, **attrs)

    def create_label(self, **attrs):
        """Create a cluster from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.modelartsv2.v2.labels.Labels`,
            comprised of the properties on the Labels class.
        :returns: The results of label creation
        :rtype: :class:`~otcextensions.sdk.modelartsv2.v2.label.Label`
        """
        return self._create(_label.Label, prepend_key=False, **attrs)

    def delete_label(self, label, ignore_missing=False):
        """Delete a dataset

        :param label: This value can be the name of a label
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the label does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent label.
        """
        return self._delete(
            _label.Label,
            label,
            ignore_missing=ignore_missing,
        )

    def show_label(self, label):
        """Get the label by id

        :param label: key id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.label.Label`

        :returns: instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.label.Label`
        """
        return self._get(_label.Label, label)

    def dataset_version(self, **attrs):
        """List all dataset versions.

        :returns: a generator of
            (:class:`~otcextensions.sdk.modelartsv2.v2.\
                    dataset_version.DatasetVersion`) instances
        """
        return self._list(_dataset_version.DatasetVersion, **attrs)

    def create_dataset_version(self, **attrs):
        """Create a dataset from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.modelartsv2.v2.datasets.Datasets`,
            comprised of the properties on the Datasets class.
        :returns: The results of dataset creation
        :rtype: :class:`~otcextensions.sdk.modelartsv2.v2.datasets.Datasets`
        """
        return self._create(
            _dataset_version.DatasetVersion, prepend_key=False, **attrs
        )

    def delete_dataset_version(self, version_id, **kwargs):
        """Delete a dataset version

        :param version_id: ID of a dataset version
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the group does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent dataset.
        """
        return self._delete(
            _dataset_version.DatasetVersion, version_id, **kwargs
        )

    def show_dataset_version(self, version_id, **attrs):
        """Get the dataset version by version id

        :param version_id: key id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.datasets.Datasets`

        :returns: instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset_version.DatasetVersion`
        """
        return self._get(_dataset_version.DatasetVersion, version_id, **attrs)

    def list_dataset_synchronization_task(self, **attrs):
        """List all Datasets.

        :returns: a generator of
            (:class:`~otcextensions.sdk.modelartsv2.v2.\
                    dataset_sync.DatasetSync`) instances
        """
        return self._list(
            _dataset_synchronization_task.DatasetSynchronizationTask, **attrs
        )

    def synchronize_dataset(self, **attrs):
        """Create a dataset from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.modelartsv2.v2.datasets.Datasets`,
            comprised of the properties on the Datasets class.
        :returns: The results of dataset creation
        :rtype: :class:`~otcextensions.sdk.modelartsv2.v2.datasets.Datasets`
        """
        return self._create(
            _dataset_synchronization_task.SynchronizeDataset,
            **attrs,
        )
    #         return self._create(_dataset_synchronization_task.SynchronizeDataset, prepend_key=False,   **attrs,        )

    def show_dataset_export_task(self, task_id, **attrs):
        """Get the dataset export task by dataset id

          :param dataset_id: key id or an instance of
              :class:`~otcextensions.sdk.modelartsv2.v2.datasets.Datasets`

          :returns: instance of :class:`~otcextensions.sdk.modelartsv2.v2.\
                dataset_export_task.DatasetExportTask`
          """
        return self._get(
            _dataset_export_task.DatasetExportTask, task_id, **attrs
        )

    def show_dataset_import_task(self, task_id, **attrs):
        """Get the data import task by dataset id

         :param dataset_id: key id or an instance of
             :class:`~otcextensions.sdk.modelartsv2.v2.datasets.Datasets`

         :returns: instance of :class:`~otcextensions.sdk.modelartsv2.v2.\
                data_import_task.DataImportTask`
         """
        return self._get(
            _dataset_import_task.DatasetImportTask, task_id, **attrs
        )

    # def samples(self, **attrs):
    #     """List all Samples.

    #     :returns: a generator of
    #         (:class:`~otcextensions.sdk.modelartsv2.v2\
    #                 .samples.Samples`) instances
    #     """
    #     return self.v2._list(_sample.Sample, **attrs)

    # def show_sample(self, sample_id, **attrs):
    #     """Get the sample by sample id

    #      :param sample_id: key id or an instance of
    #          :class:`~otcextensions.sdk.modelartsv2.v2.samples.Samples`

    #      :returns: instance of
    #          :class:`~otcextensions.sdk.modelartsv2.v2.samples.Samples`
    #      """
    #     return self.v2._get(
    #         _sample.Sample, sample_id, **attrs
    #     )

    def dataset_export_tasks(self, **attrs):
        """List all dataset export tasks.

        :returns: a generator of
            (:class:`~otcextensions.sdk.modelartsv2.v2.\
                    dataset_export_task.DatasetExportTask`) instances
        """
        return self._list(_dataset_export_task.DatasetExportTask, **attrs)

    def create_dataset_export_task(self, **attrs):
        """Create a data import task from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.modelartsv2.v2.datasets.Datasets`,
            comprised of the properties on the Datasets class.

        :returns: The results of dataset creation

        :rtype: :class:`~otcextensions.sdk.modelartsv2.v2.datasets.Datasets`
        """
        return self._create(
            _dataset_export_task.DatasetExportTask, prepend_key=False, **attrs
        )

    def create_dataset_import_task(self, **attrs):
        """Create a data import task from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.modelartsv2.v2.datasets.Datasets`,
            comprised of the properties on the Datasets class.

        :returns: The results of dataset creation

        :rtype: :class:`~otcextensions.sdk.modelartsv2.v2.datasets.Datasets`
        """
        return self._create(
            _dataset_import_task.DatasetImportTask, prepend_key=False, **attrs
        )

    def dataset_import_tasks(self, **attrs):
        """List all dataset export tasks.

        :returns: a generator of
            (:class:`~otcextensions.sdk.modelartsv2.v2.\
                    dataset_import_task.DatasetImportTask`) instances.
        """
        return self._list(_dataset_import_task.DatasetImportTask, **attrs)

    # Dataset Sample Management

    def dataset_samples(self, dataset_id, **params):
        """List all Dataset Samples in a Dataset.

        :param dataset_id: Dataset ID.
        :param dict params: Optional query parameters to be sent to limit
            the instances being returned.
        :returns: a generator of
            (:class:`~otcextensions.sdk.modelartsv2.v2\
                    .dataset_sample.DatasetSample`) instances
        """
        return self._list(
            _dataset_sample.DatasetSample, dataset_id=dataset_id, **params
        )

    def add_dataset_samples(self, dataset_id, **attrs):
        """Upload samples to a dataset.

        :param dataset_id: Dataset ID.
        :param dict attrs: Keyword arguments which will be used to create
            upload samples to a dataset and obtain instance of.
            a :class:`~otcextensions.sdk.modelartsv2.v2.\
                    dataset_sample.DatasetSample`,

        :returns: The result after uploading the dataset samples.

        :rtype: :class:`~otcextensions.sdk.modelartsv2.v2.\
                dataset_sample.DatasetSample`
        """

        return self._create(
            _dataset_sample.DatasetSample, dataset_id=dataset_id, **attrs
        )

    def delete_dataset_samples(
        self, dataset_id, *samples, delete_source=False
    ):
        """Delete an instance

        :param dataset_id: Dataset ID.
        :param samples: List of sample ID(s) to delete.

        :returns: ``None``
        """
        obj = _dataset_sample.DatasetSample(dataset_id=dataset_id)
        return obj.delete_samples(
            self,
            *samples,
            delete_source=delete_source,
        )

    def get_dataset_sample(self, dataset_id, sample_id):
        """Get the Dataset Sample

        :param dataset_id: Dataset ID.
        :param sample_id: key id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset_sample.DatasetSample`
        :returns: instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset_sample.DatasetSample`
        """
        return self._get(
            _dataset_sample.DatasetSample, sample_id, dataset_id=dataset_id
        )
