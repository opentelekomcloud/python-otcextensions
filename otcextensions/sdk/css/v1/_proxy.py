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
import time
from urllib.parse import urlsplit

from openstack import exceptions
from openstack import proxy
from otcextensions.sdk.css.v1 import cert as _cert
from otcextensions.sdk.css.v1 import cluster as _cluster
from otcextensions.sdk.css.v1 import flavor as _flavor
from otcextensions.sdk.css.v1 import snapshot as _snapshot


class Proxy(proxy.Proxy):

    skip_discovery = True

    def __init__(self, session, *args, **kwargs):
        super(Proxy, self).__init__(session=session, *args, **kwargs)
        self.additional_headers = {
            "Accept": "application/json",
            "Content-type": "application/json",
        }

    # ======== Cluster ========
    def clusters(self, **query):
        """List all Clusters.

        :returns: a generator of
            (:class:`~otcextensions.sdk.css.v1.cluster.Cluster`) instances
        """
        if query.get('limit'):
            query.update(paginated=False)
        return self._list(_cluster.Cluster, **query)

    def get_cluster(self, cluster):
        """Get the cluster by UUID

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.css.v1.cluster.Cluster`

        :returns: instance of
            :class:`~otcextensions.sdk.css.v1.cluster.Cluster`
        """
        return self._get(_cluster.Cluster, cluster)

    def find_cluster(self, name_or_id, ignore_missing=True):
        """Find a single cluster

        :param name_or_id: The name or ID of a CSS cluster
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            if the cluster does not exist.
            When set to ``True``, no exception will be set when attempting
            to find a nonexistent cluster.

        :returns:
            One :class:`~otcextensions.sdk.css.v1.cluster.Cluster` or ``None``
        """
        return self._find(
            _cluster.Cluster, name_or_id, ignore_missing=ignore_missing
        )

    def create_cluster(self, **attrs):
        """Create a cluster from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.css.v1.cluster.Cluster`,
            comprised of the properties on the Cluster class.
        :returns: The results of cluster creation
        :rtype: :class:`~otcextensions.sdk.css.v1.cluster.Cluster`
        """
        return self._create(_cluster.Cluster, **attrs)

    def restart_cluster(self, cluster):
        """Restart a cluster.

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.css.v1.cluster.Cluster`
        :returns: ``None``
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        return cluster.restart(self)

    def extend_cluster(self, cluster, add_nodes):
        """Scaling Out a Cluster with only Common Nodes

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.css.v1.cluster.Cluster`
        :param add_nodes: Number of common nodes to be scaled out.
        :returns: ``None``
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        return cluster.extend(self, add_nodes)

    def extend_cluster_nodes(self, cluster, **attrs):
        """Scaling Out a Cluster with Special Nodes

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.css.v1.cluster.Cluster`
        :param data: Cluster scale-out request data.
        :returns: ``None``
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        return self._create(
            _cluster.ExtendClusterNodes, cluster_id=cluster.id, **attrs
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
        :returns: ``None``
        """
        return self._delete(
            _cluster.Cluster, cluster, ignore_missing=ignore_missing
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
            _snapshot.Snapshot, uri_cluster_id=cluster.id, **attrs
        )

    def find_snapshot(self, cluster, name_or_id, ignore_missing=True):
        """Find a single snapshot

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.css.v1.cluster.Cluster`
        :param name_or_id: The name or ID of a snapshot
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            if the snapshot does not exist.
            When set to ``True``, no exception will be set when attempting
            to find a nonexistent snapshot.

        :returns:
            One :class:`~otcextensions.sdk.dws.v1.snapshot.Snapshot` or
            ``None``
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        return self._find(
            _snapshot.Snapshot,
            name_or_id,
            base_path=f'/clusters/{cluster.id}/index_snapshots',
            ignore_missing=ignore_missing,
        )

    def delete_snapshot(self, cluster, snapshot, ignore_missing=True):
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
            _snapshot.Snapshot,
            snapshot,
            uri_cluster_id=cluster.id,
            ignore_missing=ignore_missing,
        )

    def set_snapshot_configuration(
        self, cluster, auto_configure=False, **attrs
    ):
        """Setting Basic Configurations of a Cluster Snapshot

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.css.v1.cluster.Cluster`
        :param bool auto_configure: When set to ``True``
            Basic Configurations of a Cluster Snapshot will be set
            automatically.
        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.css.v1.snapshot.Snapshot`,
            comprised of the properties on the Snapshot class.
        :returns: ``None``
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        setting = 'setting'
        if auto_configure and isinstance(auto_configure, bool):
            setting = 'auto_setting'
            attrs = {'has_body': False}
        return self._create(
            _snapshot.SnapshotConfiguration,
            cluster_id=cluster.id,
            setting=setting,
            **attrs,
        )

    def disable_snapshot_function(self, cluster):
        """Disable the snapshot function of a cluster.

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.css.v1.cluster.Cluster`
        :returns: ``None``
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        snapshot_config = self._get_resource(
            _snapshot.SnapshotConfiguration, '', cluster_id=cluster.id
        )
        snapshot_config.disable(self)

    def set_snapshot_policy(self, cluster, **attrs):
        """Set parameters related to automatic snapshot creation.

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.css.v1.cluster.Cluster`
        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.css.v1.snapshot.Snapshot`,
            comprised of the properties on the Snapshot class.
        :returns: ``None``
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        return self._create(
            _snapshot.SnapshotPolicy, cluster_id=cluster.id, **attrs
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
            _snapshot.SnapshotPolicy, cluster_id=cluster.id, requires_id=False
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
        snapshot = self._get_resource(_snapshot.Snapshot, snapshot)
        return snapshot.restore(self, cluster.id, **attrs)

    def get_certificate(self):
        """Download the HTTPS certificate file of the server."""
        split_url = urlsplit(self.get_endpoint())
        self.endpoint_override = (
            f'{split_url.scheme}://{split_url.netloc}/v1.0/'
        )
        resp = self._get(
            _cert.Cert,
            requires_id=False,
        )
        self.endpoint_override = None
        return resp

    def wait_for_cluster(
        self, cluster, timeout=1200, wait=5, print_status=False
    ):
        org_timeout = timeout
        while timeout > 0:
            obj = self.get_cluster(cluster)
            if getattr(obj, 'error'):
                raise exceptions.SDKException(obj.error)
            if obj.status_code == 100:
                pass
            elif obj.actions == [] and obj.action_progress == {}:
                return True
            self.log.debug(
                'Still waiting for resource %s to reach state %s, '
                'current state is %s'
                '\nWait Time Out remaining: %s seconds.',
                obj.name,
                'AVAILABLE',
                str(obj.action_progress or obj.status),
                str(timeout),
            )
            if print_status:
                dots = '.' * round(100 - ((timeout / org_timeout) * 100))
                print(
                    'CSS Cluster progress: '
                    + str(obj.action_progress or obj.status)
                    + ' '
                    + dots,
                    end='\r',
                )
            time.sleep(wait)
            timeout = timeout - wait
        raise exceptions.SDKException(
            'Wait Timed Out. Cluster action still in progress.'
        )
