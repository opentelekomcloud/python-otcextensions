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
from otcextensions.sdk import sdk_proxy
from otcextensions.sdk.mrs.v1 import cluster as _cluster
from otcextensions.sdk.mrs.v1 import datasource as _datasource
from otcextensions.sdk.mrs.v1 import jobbinary as _jobbinary
from otcextensions.sdk.mrs.v1 import job as _job


class Proxy(sdk_proxy.Proxy):
    skip_discovery = True

    def __init__(self, session, *args, **kwargs):
        super(Proxy, self).__init__(session=session, *args, **kwargs)
        self.additional_headers = {
            'Content-Type': 'application/json',
        }

    # ======== clusters ========
    def clusters(self, **query):
        """Retrieve a generator of clusters

        :param dict query: Optional query parameters to be sent to limit the
            resources being returned.
        :returns: A generator of cluster
            :class:`~otcextensions.sdk.mrs.v1.cluster.ClusterInfo` instances
        """
        return self._list(_cluster.ClusterInfo, **query)

    def get_cluster(self, cluster):
        """Get a cluster

        :param cluster: The value can be the ID or an instance of
            :class:`~otcextensions.sdk.cbr.v3.cluster.ClusterInfo`
        :returns: Cluster instance
        :rtype: :class:`~otcextensions.sdk.mrs.v1.cluster.ClusterInfo`
        """
        return self._get(_cluster.ClusterInfo, cluster)

    def find_cluster(self, name_or_id, ignore_missing=True):
        """Find a single Cluster by name or id

        :param name_or_id: The name or ID of a Cluster
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the group does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent group.

        :returns: ``None``
        """
        return self._find(
            _cluster.ClusterInfo, name_or_id,
            ignore_missing=ignore_missing,
        )

    def update_cluster(self, cluster, **attrs):
        """Update Cluster attributes

        :param cluster: The id or an instance of
            :class:`~otcextensions.sdk.cbr.v1.cluster.ClusterInfo`
        :param dict attrs: attributes for update on
            :class:`~otcextensions.sdk.cbr.v1.cluster.ClusterInfo`

        :rtype: :class:`~otcextensions.sdk.cbr.v1.cluster.ClusterInfo`
        """
        return self._update(_cluster.ClusterInfo, cluster, **attrs)

    def delete_cluster(self, cluster, ignore_missing=True):
        """Delete (release) a cluster

        :param cluster: The value can be the ID of a cluster
             or a :class:`~otcextensions.sdk.mrs.v1.cluster.ClusterInfo` instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the host does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent host.

        :returns: Cluster been deleted
        :rtype: :class:`~otcextensions.sdk.mrs.v1.cluster.Cluster`
        """
        if isinstance(cluster, _cluster.ClusterInfo):
            cluster = cluster.id
        return self._delete(
            _cluster.Cluster,
            cluster,
            ignore_missing=ignore_missing,)

    def hosts(self, **query):
        """Retrieve a generator of hosts

        :param dict query: Optional query parameters to be sent to limit the
            resources being returned.
        :returns: A generator of host
            :class:`~otcextensions.sdk.mrs.v1.cluster.Host` instances
        """
        return self._list(_cluster.Host, **query)

    # ======== datasources ========
    def datasources(self, **query):
        """Retrieve a generator of hosts

        :param dict query: Optional query parameters to be sent to limit the
            resources being returned.

            * `marker`:  pagination marker
            * `limit`: pagination limit

        :returns: A generator of datasoruce
            :class:`~otcextensions.sdk.mrs.v1.datasoruce.Datasource` instances
        """
        return self._list(_datasource.Datasource, paginated=True, **query)

    def create_datasource(self, **attrs):
        """Create (allocate) a new ds from attributes

        :param dict attrs: Keyword arguments which will be used to create
               a :class:`~otcextensions.sdk.mrs.v1.datasource.Datasource`,
               comprised of the properties on the Datasource class.
        :returns: The results of datasoruce creation
        :rtype: :class:`~otcextensions.sdk.mrs.v1.datasource.Datasource`
        """
        return self._create(_datasource.Datasource, prepend_key=False, **attrs)

    def get_datasource(self, datasource):
        """Get a datasource

        :param host: The value can be the ID of a DS
        or a :class:`~otcextensions.sdk.mrs.v1.datasource.Datasource`
        :returns: Host instance
        :rtype: :class:`~otcextensions.sdk.mrs.v1.datasource.Datasource`
        """
        return self._get(_datasource.Datasource, datasource)

    def delete_datasource(self, datasource, ignore_missing=True):
        """Delete (release) a datasource

        :param host: The value can be the ID of a datasource
             or a :class:`~otcextensions.sdk.mrs.v1.datasource.Datasource` .
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the host does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent host.

        :returns: host been deleted
        :rtype: :class:`~otcextensions.sdk.mrs.v1.datasource.Datasource`
        """
        return self._delete(_datasource.Datasource, datasource,
                            ignore_missing=ignore_missing)

    def find_datasource(self, name_or_id, ignore_missing=True):
        """Find a single datasource

        :param name_or_id: The name or ID of a datasource
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the host does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent ds.

        :returns: ``None``
        """
        return self._find(_datasource.Datasource, name_or_id,
                          ignore_missing=ignore_missing)

    def update_datasource(self, datasource, **attrs):
        """Update ds attributes

        :param host: The id or an instance of
            :class:`~otcextensions.sdk.mrs.v1.datasource.Datasource`
        :param dict attrs: attributes for update on
            :class:`~otcextensions.sdk.mrs.v1.datasource.Datasource`

        :rtype: :class:`~otcextensions.sdk.mrs.v1.datasource.Datasource`
        """
        return self._update(_datasource.Datasource, datasource, **attrs)

    # ======== jobbinaries ========
    def jobbinaries(self, **query):
        """Retrieve a generator of jobbinaries

        :param dict query: Optional query parameters to be sent to limit the
            resources being returned.

            * `marker`:  pagination marker
            * `limit`: pagination limit

        :returns: A generator of jobbinary
            :class:`~otcextensions.sdk.mrs.v1.jobbinary.Jobbinary` instances
        """
        return self._list(_jobbinary.Jobbinary, paginated=True, **query)

    def create_jobbinary(self, **attrs):
        """Create a new jobbinary

        :param dict attrs: Keyword arguments which will be used to create
               a :class:`~otcextensions.sdk.mrs.v1.jobbinary.Jobbinary`,
               comprised of the properties on the Jobbinary class.
        :returns: The results of datasoruce creation
        :rtype: :class:`~otcextensions.sdk.mrs.v1.jobbinary.Jobbinary`
        """
        return self._create(_jobbinary.Jobbinary, prepend_key=False, **attrs)

    def get_jobbinary(self, jobbinary):
        """Get a jobbinary

        :param host: The value can be the ID of a jobbinary
        or a :class:`~otcextensions.sdk.mrs.v1.jobbinary.Jobbinary`
        :returns: Jobbinary instance
        :rtype: :class:`~otcextensions.sdk.mrs.v1.jobbinary.Jobbinary`
        """
        return self._get(_jobbinary.Jobbinary, jobbinary)

    def delete_jobbinary(self, jobbinary, ignore_missing=True):
        """Delete (release) a jobbinary

        :param host: The value can be the ID of a jobbinary
             or a :class:`~otcextensions.sdk.mrs.v1.jobbinary.Jobbinary` .
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the host does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent host.

        :rtype: :class:`~otcextensions.sdk.mrs.v1.jobbinary.Jobbinary`
        """
        return self._delete(_jobbinary.Jobbinary, jobbinary,
                            ignore_missing=ignore_missing)

    def find_jobbinary(self, name_or_id, ignore_missing=True):
        """Find a single jobbinary

        :param name_or_id: The name or ID of a jobbinary
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the host does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent ds.

        :returns: ``None``
        """
        return self._find(_jobbinary.Jobbinary, name_or_id,
                          ignore_missing=ignore_missing)

    def update_jobbinary(self, jobbinary, **attrs):
        """Update jobbinary attributes

        :param host: The id or an instance of
            :class:`~otcextensions.sdk.mrs.v1.jobbinary.Jobbinary`
        :param dict attrs: attributes for update on
            :class:`~otcextensions.sdk.mrs.v1.jobbinary.Jobbinary`

        :rtype: :class:`~otcextensions.sdk.mrs.v1.jobbinary.Jobbinary`
        """
        return self._update(_jobbinary.Jobbinary, jobbinary, **attrs)

    # ======== jobs ========
    def jobs(self, **query):
        """Retrieve a generator of jobs

        :param dict query: Optional query parameters to be sent to limit the
            resources being returned.

            * `marker`:  pagination marker
            * `limit`: pagination limit

        :returns: A generator of jobs
            :class:`~otcextensions.sdk.mrs.v1.job.Job` instances
        """
        return self._list(_job.Job, paginated=True, **query)

    def create_job(self, **attrs):
        """Create (allocate) a new job from attributes

        :param dict attrs: Keyword arguments which will be used to create
               a :class:`~otcextensions.sdk.mrs.v1.job.Job`,
               comprised of the properties on the Job class.
        :returns: The results of job creation
        :rtype: :class:`~otcextensions.sdk.mrs.v1.job.Job`
        """
        return self._create(_job.Job, prepend_key=False, **attrs)

    def get_job(self, job):
        """Get a job

        :param host: The value can be the ID of a job
        or a :class:`~otcextensions.sdk.mrs.v1.job.Job`
        :returns: Job instance
        :rtype: :class:`~otcextensions.sdk.mrs.v1.job.Job`
        """
        return self._get(_job.Job, job)

    def delete_job(self, job, ignore_missing=True):
        """Delete (release) a job

        :param host: The value can be the ID of a job
             or a :class:`~otcextensions.sdk.mrs.v1.job.Job` .
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the host does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent host.

        :returns: Job been deleted
        :rtype: :class:`~otcextensions.sdk.mrs.v1.job.Job`
        """
        return self._delete(_job.Job, job,
                            ignore_missing=ignore_missing)

    def find_job(self, name_or_id, ignore_missing=True):
        """Find a single job

        :param name_or_id: The name or ID of a job
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the host does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent job.

        :returns: ``None``
        """
        return self._find(_job.Job, name_or_id,
                          ignore_missing=ignore_missing)

    def update_job(self, job, **attrs):
        """Update job attributes

        :param host: The id or an instance of
            :class:`~otcextensions.sdk.mrs.v1.job.Job`
        :param dict attrs: attributes for update on
            :class:`~otcextensions.sdk.mrs.v1.job.Job`

        :rtype: :class:`~otcextensions.sdk.mrs.v1.job.Job`
        """
        return self._update(_job.Job, job, **attrs)

    def cancel(self, job):
        """Confirm consumed message

        :param job: An object of an instance of
          :class:`~otcextensions.sdk.mrs.v1.job.CancelJob
        :param status: The expeced status of the consumed message
        :returns: An object of an instance of
          :class:`~otcextensions.sdk.mrs.v1.job.CancelJob`
        """
        return job.cancel(self.session)
