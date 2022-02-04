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

from otcextensions.sdk.dws.v1 import cluster as _cluster


class Proxy(proxy.Proxy):

    skip_discovery = True

    # ======= Clusters =======
    def clusters(self, **query):
        """Retrieve a generator of clusters

        :returns: A generator of clusters
          :class `~otcextensions.sdk.dws.v1.cluster.Cluster`.
        """
        return self._list(_cluster.Cluster, **query)

    def create_cluster(self, **attrs):
        """Create a new cluster from attributes

        :param dict attrs: Keyword arguments which will be used to create a
                           :class `~otcextensions.sdk.dws.v1.cluster.Cluster`,
                           comprised of the properties on the Cluster class.
        :returns: The results of Cluster creation
        :rtype: :class `~otcextensions.sdk.dws.v1.cluster.Cluster`.
        """
        return self._create(_cluster.Cluster, **attrs)

    def get_cluster(self, cluster):
        """Get a cluster

        :param cluster: The value can be the ID of a cluster
            or a :class `~otcextensions.sdk.dws.v1.cluster.Cluster` cluster.

        :returns: Cluster
        :rtype: :class `~otcextensions.sdk.dws.v1.cluster.Cluster`
        """
        return self._get(_cluster.Cluster, cluster)

    def delete_cluster(self, cluster, ignore_missing=True):
        """Delete a cluster
        :param cluster: The value can be the ID of a cluster
            or a :class `~otcextensions.sdk.dws.v1.cluster.Cluster` cluster.

        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the virtual gateway does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent zone.

        :returns: `None`
        """
        return self._delete(_cluster.Cluster, cluster,
                            ignore_missing=ignore_missing)

    def update_cluster(self, cluster, **attrs):
        """Update cluster attributes

        :param cluster: The value can be the ID of a cluster
            or a :class `~otcextensions.sdk.dws.v1.cluster.Cluster` cluster.
        :param dict attrs: attributes for update on
            :class `~otcextensions.sdk.dws.v1.cluster.Cluster` cluster.

        :rtype: :class `~otcextensions.sdk.dws.v1.cluster.Cluster`
        """
        return self._update(_cluster.Cluster, cluster, **attrs)

    def find_cluster(self, name_or_id, ignore_missing=True, **attrs):
        """Find a single virtual gateway

        :param name_or_id: The name or ID of a cluster
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the zone does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent zone.

        :returns: ``None``
        """
        return self._find(_cluster.Cluster, name_or_id,
                          ignore_missing=ignore_missing,
                          **attrs)
