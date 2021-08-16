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
from otcextensions.sdk.css.v1 import snapshot as _snapshot
from otcextensions.sdk.css.v1 import cert as _cert

from six.moves.urllib.parse import urlparse
from six.moves.urllib.parse import urlunparse


class Proxy(proxy.Proxy):

    skip_discovery = True

    def __init__(self, session, *args, **kwargs):
        super(Proxy, self).__init__(session=session, *args, **kwargs)
        self.additional_headers = {"Accept": "application/json",
                                   "Content-type": "application/json"}

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

    def restart_cluster(self, cluster):
        """Get the cluster by UUID

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.css.v1.cluster.Cluster`

        :returns: instance of
            :class:`~otcextensions.sdk.css.v1.cluster.Cluster`
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        return cluster.restart(self)

    def extend_cluster(self, cluster, new_size):
        """Scaling Out a Cluster with only Common Nodes

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.css.v1.cluster.Cluster`

        :returns: instance of
            :class:`~otcextensions.sdk.css.v1.cluster.Cluster`
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        return cluster.extend(self, new_size)

    def delete_cluster(self, cluster, ignore_missing=False):
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

    # ======== Snapshot ========
    def snapshots(self, cluster):
        """List all Snapshots of a cluster.

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.css.v1.cluster.Cluster`
        :returns: a generator of
            (:class:`~otcextensions.sdk.css.v1.snapshot.Snapshot`) instances
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        base_path = f'/clusters/{cluster.id}/index_snapshots'
        return self._list(_snapshot.Snapshot, base_path=base_path)

    def create_snapshot(self, cluster, **attrs):
        """Create a cluster Snapshot from attributes

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.css.v1.cluster.Cluster`
        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.css.v1.snapshot.Snapshot`,
            comprised of the properties on the Snapshot class.
        :returns: The results of cluster snapshot creation
        :rtype: :class:`~otcextensions.sdk.css.v1.snapshot.Snapshot`
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        return self._create(
            _snapshot.Snapshot,
            cluster_id=cluster.id,
            prepend_key=False,
            **attrs,
        )

    def delete_snapshot(self, cluster, snapshot,
                        ignore_missing=False):
        """Delete a snapshot

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.css.v1.cluster.Cluster`
        :param snapshot: key id or an instance of
            :class:`~otcextensions.sdk.css.v1.snapshot.Snapshot`
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the snapshot does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent snapshot.
        :returns: ``None``
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        return self._delete(
            _snapshot.Snapshot, snapshot,
            cluster_id=cluster.id,
            ignore_missing=ignore_missing,
        )

    def set_snapshot_configuration(self, cluster, auto_setting=False,
                                   **attrs):
        """Setting Basic Configurations of a Cluster Snapshot

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.css.v1.cluster.Cluster`
        :param bool auto: When set to ``True``
            Basic Configurations of a Cluster Snapshot will be set
            automatically.
        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.css.v1.snapshot.Snapshot`,
            comprised of the properties on the Snapshot class.
        :returns: ``None``
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        setting = 'setting'
        if auto_setting and isinstance(auto_setting, bool):
            setting = 'auto_setting'
            attrs['has_body'] = False
        return self._create(
            _snapshot.SnapshotConfiguration,
            cluster_id=cluster.id,
            setting=setting,
            **attrs
        )

    def set_snapshot_policy(self, cluster, **attrs):
        """Set parameters related to automatic snapshot creation

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.css.v1.cluster.Cluster`
        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.css.v1.snapshot.Snapshot`,
            comprised of the properties on the Snapshot class.
        :returns: ``None``
        """

        cluster = self._get_resource(_cluster.Cluster, cluster)
        return self._create(
            _snapshot.SnapshotPolicy,
            cluster_id=cluster.id,
            **attrs
        )

    def get_snapshot_policy(self, cluster):
        """Query the automatic snapshot creation policy for a cluster.

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.css.v1.cluster.Cluster`
        :returns: instance of
            :class:`~otcextensions.sdk.css.v1.snapshot.SnapshotPolicy`
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        return self._get(
            _snapshot.SnapshotPolicy,
            cluster_id=cluster.id,
            requires_id=False
        )

    def disable_snapshot_function(self, cluster, ignore_missing=False):
        """Disable the snapshot function of a cluster.

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.css.v1.cluster.Cluster`
        :returns: ``None``
        """

        cluster = self._get_resource(_cluster.Cluster, cluster)
        uri = f'{cluster.id}/index_snapshots'
        return self._delete(
            _snapshot.Snapshot,
            requires_id=False,
            custom_uri=uri,
            ignore_missing=ignore_missing
        )

    def restore_snapshot(self, cluster, snapshot, **attrs):
        """Restore a snapshot.

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.css.v1.cluster.Cluster`
        :param snapshot: key id or an instance of
            :class:`~otcextensions.sdk.css.v1.snapshot.Snapshot`
        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.css.v1.snapshot.Snapshot`,
            comprised of the properties on the Snapshot class.
        :returns: ``None``
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        uri = f'{cluster.id}/index_snapshot/{snapshot}/restore'
        return self._create(
            _snapshot.Snapshot,
            custom_uri=uri,
            prepend_key=False,
            **attrs
        )

    def get_certificate(self):
        urlcomp = list(urlparse(self.get_endpoint()))
        urlcomp[2] = ''
        baseurl = urlunparse(urlcomp)
        self.endpoint_override = baseurl + '/v1.0/'
        resp = self._get(
            _cert.Cert,
            requires_id=False,
        )
        self.endpoint_override = None
        return resp
