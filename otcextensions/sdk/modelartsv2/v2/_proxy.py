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
from otcextensions.sdk.modelartsv2.v2 import dataset as _dataset


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

    # def find_dataset(self, name_or_id, ignore_missing=False):
    #     """Find a dataset by name or id.

    #     :param name_or_id: The name or ID of a dataset
    #     :param bool ignore_missing: When set to ``False``
    #         :class:`~openstack.exceptions.ResourceNotFound` will be raised
    #         when the dataset does not exist.
    #         When set to ``True``, no exception will be set when attempting
    #         to find a nonexistent dataset.

    #     :returns:
    #         One :class:`~otcextensions.sdk.nat.v2.dataset.Dataset`
    #           or ``None``
    #     """
    #     return self._find(
    #         _dataset.Dataset,
    #         name_or_id,
    #         ignore_missing=ignore_missing,
    #     )

    def modify_dataset(self, dataset, **attrs):
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
            One :class:`~otcextensions.sdk.nat.v2.dataset.Statistics`
        """
        return self._get(
            _dataset.Statistics,
            dataset_id=dataset_id,
            requires_id=False,
        )

    # ======== Dataset Label Management ========

    def dataset_labels(self, dataset_id, **params):
        """List all Labels in a dataset.

        :param dataset_id: Dataset ID.
        :param dict params: Optional query parameters to be sent to limit
            the instances being returned.
        :returns: a generator of
            (:class:`~otcextensions.sdk.modelartsv2.v2.dataset.Label`)
            instances.
        """
        return self._list(_dataset.Label, dataset_id=dataset_id, **params)

    def create_dataset_label(self, dataset_id, **attrs):
        """Create a daraset label from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Label`,
            comprised of the properties on the Labels class.
        :returns: The results of label creation
        :rtype: :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Label`
        """
        return self._create(_dataset.Label, dataset_id=dataset_id, **attrs)

    def update_dataset_labels(self, dataset_id, **attrs):
        """Modify a dataset labels in batches.

        :param dataset_id: Dataset ID.

        :returns: instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset.Dataset`
        """
        return self._update(_dataset.Dataset, dataset_id, **attrs)

    def delete_dataset_labels(self, dataset_id, *labels, delete_source=False):
        """Delete dataset labels.

        :param dataset_id: Dataset ID.
        :param labels: List of labels ID(s) to delete.

        :returns: ``None``
        """
        obj = _dataset.Label(dataset_id=dataset_id)
        return obj.delete_labels(
            self,
            *labels,
            delete_source=delete_source,
        )

    # ======== Dataset Version Management ========

    def dataset_version(self, **attrs):
        """List all dataset versions.

        :returns: a generator of
            (:class:`~otcextensions.sdk.modelartsv2.v2.\
                dataset_version.DatasetVersion`) instances
        """
        return self._list(_dataset.DatasetVersion, **attrs)

    def create_dataset_version(self, **attrs):
        """Create a dataset from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.modelartsv2.v2.datasets.Datasets`,
            comprised of the properties on the Datasets class.
        :returns: The results of dataset creation
        :rtype: :class:`~otcextensions.sdk.modelartsv2.v2.\
            dataset.DatasetVersion`
        """
        return self._create(
            _dataset.DatasetVersion, prepend_key=False, **attrs
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
        return self._delete(_dataset.DatasetVersion, version_id, **kwargs)

    def show_dataset_version(self, version_id, **attrs):
        """Get the dataset version by version id

        :param version_id: key id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset.DatasetVersion`

        :returns: instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset.DatasetVersion`
        """
        return self._get(_dataset.DatasetVersion, version_id, **attrs)

    # ======== Dataset Sample Management ========

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
            _dataset.Sample, dataset_id=dataset_id, **params, paginated=False
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

        return self._create(_dataset.Sample, dataset_id=dataset_id, **attrs)

    def delete_dataset_samples(
        self, dataset_id, samples=[], delete_source=False
    ):
        """Delete dataset samples.

        :param dataset_id: Dataset ID.
        :param samples: List of sample ID(s) to delete.

        :returns: ``None``
        """
        attrs = {
            "samples": samples,
            "delete_source": delete_source,
        }
        return self._create(
            _dataset.DeleteSample, dataset_id=dataset_id, **attrs
        )

    def get_dataset_sample(self, dataset_id, sample_id):
        """Get the Dataset Sample

        :param dataset_id: Dataset ID.
        :param sample_id: key id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset_sample.DatasetSample`
        :returns: instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.dataset_sample.DatasetSample`
        """
        return self._get(_dataset.Sample, sample_id, dataset_id=dataset_id)

    # ======== Dataset Import Task Management ========

    def dataset_import_tasks(self, **attrs):
        """List all dataset export tasks.

        :returns: a generator of
            (:class:`~otcextensions.sdk.modelartsv2.v2.\
                    dataset.ImportTask`) instances.
        """
        return self._list(_dataset.ImportTask, **attrs)

    def create_dataset_import_task(self, **attrs):
        """Create a data import task from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.modelartsv2.v2.dataset.ImportTask`,
            comprised of the properties on the ImportTask class.

        :returns: The results of dataset import task.

        :rtype: :class:`~otcextensions.sdk.modelartsv2.v2.dataset.ImportTask`
        """
        return self._create(_dataset.ImportTask, prepend_key=False, **attrs)

    def get_dataset_import_task(self, task_id, **attrs):
        """Get the data import task by dataset id

         :param dataset_id: key id or an instance of
             :class:`~otcextensions.sdk.modelartsv2.v2.dataset.ImportTask`

         :returns: instance of :class:`~otcextensions.sdk.modelartsv2.v2.\
                dataset.ImportTask`
         """
        return self._get(_dataset.ImportTask, task_id, **attrs)

    # ======== Dataset Export Task Management ========

    def show_dataset_export_task(self, task_id, **attrs):
        """Get the dataset export task by dataset id

          :param dataset_id: key id or an instance of
              :class:`~otcextensions.sdk.modelartsv2.v2.dataset.ExportTask`

          :returns: instance of :class:`~otcextensions.sdk.modelartsv2.v2.\
                dataset.ExportTask`
          """
        return self._get(_dataset.ExportTask, task_id, **attrs)

    def dataset_export_tasks(self, **attrs):
        """List all dataset export tasks.

        :returns: a generator of
            (:class:`~otcextensions.sdk.modelartsv2.v2.\
                    dataset.ExportTask`) instances
        """
        return self._list(_dataset.ExportTask, **attrs)

    def create_dataset_export_task(self, **attrs):
        """Create a data import task from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.modelartsv2.v2.dataset.ExportTask`,
            comprised of the properties on the ExportTask class.

        :returns: The results of dataset export task.

        :rtype: :class:`~otcextensions.sdk.modelartsv2.v2.dataset.ExportTask`
        """
        return self._create(_dataset.ExportTask, prepend_key=False, **attrs)

    # ======== Dataset Synchronization Task Management ========

    def sync_dataset(self, dataset_id):
        """Synchronize samples and labeling information
            from the input dataset path to the dataset.

        :param dataset_id: Dataset ID.
        :returns: None
        """
        return self._create(_dataset.Sync, datasetId=dataset_id)

    def get_dataset_sync_status(self, dataset_id):
        """Query Dataset sync task status

        :param dataset_id: Dataset ID.

        :returns:
            One :class:`~otcextensions.sdk.nat.v2.dataset.Sync`
        """
        return self._get(_dataset.Sync, "status", datasetId=dataset_id)
