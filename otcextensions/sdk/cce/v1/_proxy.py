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
from otcextensions.sdk.cce.v1 import cluster as _cluster
from otcextensions.sdk.cce.v1 import cluster_host as _cluster_host


class Proxy(sdk_proxy.Proxy):

    # ======== Cluster ========
    def clusters(self):
        """List all Clusters.

        :returns: a generator of
            (:class:`~otcextensions.sdk.cce.v1.cluster.Cluster`) instances
        """
        return self._list(_cluster.Cluster, paginated=False)

    def get_cluster(self, cluster):
        """Get the cluster by UUID

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.cce.v1.cluster.Cluster`

        :returns: instance of
            :class:`~otcextensions.sdk.cce.v1.cluster.Cluster`
        """
        return self._get(
            _cluster.Cluster, cluster,
        )

    def delete_cluster(self, cluster, ignore_missing=True):
        """Delete a cluster

        :param cluster: The value can be the ID of a cluster
             or a :class:`~otcextensions.sdk.cce.v1.cluster.Cluster`
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

    # ======== Cluster Nodes ========
    def cluster_nodes(self, cluster):
        """List all Cluster nodes.

        :param cluster: The value can be the ID of a cluster
             or a :class:`~otcextensions.sdk.cce.v1.cluster.Cluster`
             instance.

        :returns: a generator of
            (:class:`~otcextensions.sdk.cce.v1.cluster_host.ClusterHost`)
            instances
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        return self._list(
            _cluster_host.ClusterHost, cluster_uuid=cluster.id,
            paginated=False
        )

    def get_cluster_node(self, cluster, node_id):
        """Get the cluster node by it's UUID

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.cce.v1.cluster.Cluster`
        :param node_id: Cluster node id to be fetched

        :returns: instance of
            :class:`~otcextensions.sdk.cce.v1.cluster_node.ClusterNode`
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        return self._get(
            _cluster_host.ClusterHost,
            node_id,
            cluster_uuid=cluster.id,
        )

    def delete_cluster_nodes(self, cluster, node_names):
        """Delete nodes from the cluster

        :param cluster: The value can be the ID of a cluster
             or a :class:`~otcextensions.sdk.cce.v1.cluster.Cluster`
             instance.
        :param node_names: List of node names to be deleted.
            Can be also a single node name.
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        return cluster.delete_nodes(
            self,
            node_names,
        )

    def add_node(self, cluster, **attrs):
        """Add a new node to the cluster

        :param cluster: The value can be the ID of a cluster
             or a :class:`~otcextensions.sdk.cce.v1.cluster.Cluster`
             instance.
        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.cce.v1.cluster_host.ClusterHost`,
            comprised of the properties on the ClusterHost class.
        :returns: The results of config creation
        :rtype: :class:`~otcextensions.sdk.cce.v1.config.Config`
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        return self._create(
            _cluster_host.ClusterHost,
            cluster_uuid=cluster.id,
            **attrs
        )
