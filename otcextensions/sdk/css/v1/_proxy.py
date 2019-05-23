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
from otcextensions.sdk.css.v1 import cluster as _cluster
from otcextensions.sdk.css.v1 import flavor as _flavor


class Proxy(proxy.Proxy):

    skip_discovery = True

    # ======== Cluster ========
    def clusters(self):
        """List all Clusters.

        :returns: a generator of
            (:class:`~otcextensions.sdk.css.v1.cluster.Cluster`) instances
        """
        return self._list(_cluster.Cluster)

    def get_cluster(self, cluster):
        """Get the cluster by UUID

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.css.v1.cluster.Cluster`

        :returns: instance of
            :class:`~otcextensions.sdk.css.v1.cluster.Cluster`
        """
        return self._get(
            _cluster.Cluster, cluster,
        )

    def create_cluster(self, **attrs):
        """Create a cluster from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.css.v1.cluster.Cluster`,
            comprised of the properties on the Cluster class.
        :returns: The results of cluster creation
        :rtype: :class:`~otcextensions.sdk.css.v1.cluster.Cluster`
        """
        return self._create(
            _cluster.Cluster, prepend_key=False, **attrs
        )

    def delete_cluster(self, cluster, ignore_missing=True):
        """Delete a cluster

        :param cluster: The value can be the ID of a cluster
             or a :class:`~otcextensions.sdk.css.v1.cluster.Cluster`
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

    # ======== Flavors ========
    def flavors(self):
        """List all Flavors.

        :returns: a generator of
            (:class:`~otcextensions.sdk.css.v1.flavor.Flavor`) instances
        """
        return self._list(_flavor.Flavor, paginated=False)
