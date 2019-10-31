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
from openstack import proxy
from openstack import resource

from otcextensions.sdk.cce.v3 import cluster as _cluster
from otcextensions.sdk.cce.v3 import cluster_node as _cluster_node
from otcextensions.sdk.cce.v3 import cluster_cert as _cluster_cert
from otcextensions.sdk.cce.v3 import job as _job


class Proxy(proxy.Proxy):

    skip_discovery = True

    # ======== Cluster ========
    def clusters(self):
        """List all Clusters.

        :returns: a generator of
            (:class:`~otcextensions.sdk.cce.v3.cluster.Cluster`) instances
        """
        return self._list(_cluster.Cluster, paginated=False)

    def get_cluster(self, cluster):
        """Get the cluster by UUID.

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.cce.v3.cluster.Cluster`

        :returns: instance of
            :class:`~otcextensions.sdk.cce.v3.cluster.Cluster`
        """
        return self._get(
            _cluster.Cluster, cluster,
        )

    def create_cluster(self, **attrs):
        """Create a cluster from attributes.

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.cce.v3.cluster.Cluster`,
            comprised of the properties on the Cluster class.

        :returns: The results of cluster creation
        :rtype: :class:`~otcextensions.sdk.cce.v3.cluster.Cluster`
        """
        return self._create(
            _cluster.Cluster, prepend_key=False, **attrs
        )

    def find_cluster(self, name_or_id, ignore_missing=True):
        """Find a single cluster.

        :param name_or_id: The name or ID of a cluster
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the group does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent group.

        :returns: ``None``
        """
        return self._find(
            _cluster.Cluster, name_or_id,
            ignore_missing=ignore_missing,
        )

    def delete_cluster(self, cluster, ignore_missing=True):
        """Delete a cluster.

        :param cluster: The value can be the ID of a cluster
             or a :class:`~otcextensions.sdk.cce.v3.cluster.Cluster`
             instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the group does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent cluster.
        """
        return self._delete(
            _cluster.Cluster, cluster, ignore_missing=ignore_missing,
        )

    def get_cluster_certificates(self, cluster):
        """Get the certificates of a cluster.

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.cce.v3.cluster.Cluster`

        :returns: instance of
            :class:`~otcextensions.sdk.cce.v3.cluster_cert.ClusterCertificates`
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        return self._get(
            _cluster_cert.ClusterCertificate, cluster_id=cluster.id,
            requires_id=False
        )

    def wait_for_cluster(self, cluster, status='Available', failures=None,
                         interval=2, wait=960):
        """Wait for a server to be in a particular status.

        :param cluster:
            The :class:`~otcextensions.sdk.cce.v3.cluster.Cluster` to wait on
            to reach the specified status.
        :param status: Desired status.
        :param failures:
            Statuses that would be interpreted as failures.
        :type failures: :py:class:`list`
        :param int interval:
            Number of seconds to wait before to consecutive checks.
            Default to 2.
        :param int wait:
            Maximum number of seconds to wait before the change.
            Default to 960.
        :returns: The resource is returned on success.
        :raises: :class:`~openstack.exceptions.ResourceTimeout` if transition
                 to the desired status failed to occur in specified seconds.
        :raises: :class:`~openstack.exceptions.ResourceFailure` if the resource
                 has transited to one of the failure statuses.
        """
        failures = ['ERROR'] if failures is None else failures
        return resource.wait_for_status(
            self, cluster, status, failures, interval, wait,
            attribute='status.status')

    # ======== Cluster Nodes ========
    def cluster_nodes(self, cluster):
        """List all Cluster nodes.

        :param cluster: The value can be the ID of a cluster
             or a :class:`~otcextensions.sdk.cce.v3.cluster.Cluster`
             instance.

        :returns: a generator of
            (:class:`~otcextensions.sdk.cce.v3.cluster_node.ClusterNode`)
            instances
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        return self._list(
            _cluster_node.ClusterNode, cluster_id=cluster.id,
            paginated=False
        )

    def get_cluster_node(self, cluster, node_id):
        """Get the cluster node by it's UUID.

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.cce.v3.cluster.Cluster`
        :param node_id: Cluster node id to be fetched

        :returns: instance of
            :class:`~otcextensions.sdk.cce.v3.cluster_node.ClusterNode`
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        return self._get(
            _cluster_node.ClusterNode,
            node_id,
            cluster_id=cluster.id,
        )

    def find_cluster_node(self, cluster, node):
        """Find the cluster node by it's UUID or name.

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.cce.v3.cluster.Cluster`
        :param node: Cluster node id or name to be fetched

        :returns: instance of
            :class:`~otcextensions.sdk.cce.v3.cluster_node.ClusterNode`
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        return self._find(
            _cluster_node.ClusterNode,
            node,
            cluster_id=cluster.id,
        )

    def delete_cluster_node(self, cluster, node, ignore_missing=True):
        """Delete nodes from the cluster.

        :param cluster: The value can be the ID of a cluster
             or a :class:`~otcextensions.sdk.cce.v3.cluster.Cluster`
             instance.
        :param node: The value can be the ID of a cluster node
             or a :class:`~otcextensions.sdk.cce.v3.cluster_node.ClusterNode`
             instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the node does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent cluster node.
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        return self._delete(
            _cluster_node.ClusterNode,
            node,
            ignore_missing=ignore_missing,
            cluster_id=cluster.id,
        )

    def create_cluster_node(self, cluster, **attrs):
        """Add a new node to the cluster.

        :param cluster: The value can be the ID of a cluster
             or a :class:`~otcextensions.sdk.cce.v3.cluster.Cluster`
             instance.
        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.cce.v3.cluster_node.ClusterNode`,
            comprised of the properties on the ClusterNode class.
        :returns: The results of config creation
        :rtype: :class:`~otcextensions.sdk.cce.v3.cluster_node.ClusterNode`
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        return self._create(
            _cluster_node.ClusterNode,
            cluster_id=cluster.id,
            **attrs
        )

    def get_job(self, job):
        """Get the job by UUID.

        :param job: key id or an instance of
            :class:`~otcextensions.sdk.cce.v3.job.Job`

        :returns: instance of
            :class:`~otcextensions.sdk.cce.v3.job.Job`
        """
        return self._get(
            _job.Job, job,
        )

    def wait_for_job(self, job_id, status='success',
                     failures=None, interval=5, wait=3600,
                     attribute='status.status'):
        failures = ['FAILED'] if failures is None else failures
        job = self.get_job(job_id)
        return resource.wait_for_status(
            self, job, status, failures, interval, wait,
            attribute='status.status')
