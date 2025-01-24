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
import os
import time

from openstack import exceptions
from openstack import proxy
from otcextensions.sdk.css.v1 import cluster as _cluster
from otcextensions.sdk.css.v1 import cluster_image as _cluster_image
from otcextensions.sdk.css.v1 import (
    cluster_upgrade_status as _cluster_upgrade_status
)
from otcextensions.sdk.css.v1 import flavor as _flavor
from otcextensions.sdk.css.v1 import snapshot as _snapshot


class Proxy(proxy.Proxy):
    skip_discovery = True

    def __init__(self, session, *args, **kwargs):
        super(Proxy, self).__init__(session=session, *args, **kwargs)
        self.additional_headers = {
            'Accept': 'application/json',
            'Content-type': 'application/json',
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

    def update_cluster_name(self, cluster, new_name):
        """Update cluster name

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.css.v1.cluster.Cluster`
        :param new_name: new name for the CSS cluster
        :returns: ``None``
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        return cluster.update_name(self, new_name)

    def update_cluster_password(self, cluster, new_password):
        """Update cluster password

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.css.v1.cluster.Cluster`
        :param new_password: new password for the CSS cluster
        :returns: ``None``
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        return cluster.update_password(self, new_password)

    def update_cluster_flavor(
        self, cluster, new_flavor, node_type=None, check_replica=True
    ):
        """Update cluster flavor

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.css.v1.cluster.Cluster`
        :param check_replica: indicates whether to verify replicas
        :param new_flavor: ID of the new flavor
        :param node_type: the type of node
        :returns: ``None``
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        return cluster.update_flavor(
            self, new_flavor, node_type, check_replica
        )

    def update_cluster_security_mode(
        self,
        cluster,
        https_enable=None,
        authority_enable=None,
        admin_pwd=None,
    ):
        """Update cluster security mode

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.css.v1.cluster.Cluster`
        :param authority_enable: indicates whether to enable the security mode
        :param admin_pwd: cluster password in security mode
        :param https_enable: indicates whether to enable HTTPS
        :returns: ``None``
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        return cluster.update_security_mode(
            self, https_enable, authority_enable, admin_pwd
        )

    def update_cluster_security_group(self, cluster, security_group_id):
        """Update cluster security group

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.css.v1.cluster.Cluster`
        :param security_group_id: new security group id for the CSS cluster
        :returns: ``None``
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        return cluster.update_security_group(self, security_group_id)

    def update_cluster_kernel(
        self,
        cluster,
        target_image_id,
        upgrade_type,
        indices_backup_check,
        agency,
        cluster_load_check=False,
    ):
        """Update cluster kernel

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.css.v1.cluster.Cluster`
        :param target_image_id: ID of the target image version.
        :param upgrade_type: upgrade type
        :param indices_backup_check: indicates whether to perform backup
            verification
        :param agency: agency name
        :param cluster_load_check: indicates whether to verify the load
        :returns: ``None``
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        return cluster.update_kernel(
            self,
            target_image_id,
            upgrade_type,
            indices_backup_check,
            agency,
            cluster_load_check,
        )

    def get_cluster_version_upgrades(self, cluster, upgrade_type):
        """Get cluster version upgrade info

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.css.v1.cluster.Cluster`
        :param upgrade_type: version type
        :returns: image info list
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        return self._get(
            _cluster_image.ClusterImage,
            cluster_id=cluster.id,
            upgrade_type=upgrade_type,
            requires_id=False,
        )

    def scale_in_cluster(self, cluster, nodes):
        """Scale in a cluster by removing specified nodes

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.css.v1.cluster.Cluster`
        :param nodes: list of node id
        :returns: ``None``
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        return cluster.scale_in(self, nodes)

    def scale_in_cluster_by_node_type(self, cluster, nodes):
        """Remove instances of specific types and reduce instance
            storage capacity in a cluster

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.css.v1.cluster.Cluster`
        :param nodes: type and quantity of nodes Type
            and quantity of nodes to remove
        :returns: ``None``
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        resp = cluster.scale_in_by_node_type(self, nodes)
        return resp

    def replace_cluster_node(self, cluster, node_id):
        """Replace a failed node

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.css.v1.cluster.Cluster`
        :param node_id: ID of the node to be replaced
        :returns: ``None``
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        return cluster.replace_node(self, node_id)

    def add_cluster_nodes(
        self, cluster, node_type, flavor, node_size, volume_type
    ):
        """Add master and client nodes to a cluster

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.css.v1.cluster.Cluster`
        :param node_type: node type
        :param flavor: flavor ID
        :param node_size: number of nodes
        :param volume_type: node storage type
        :returns: ``None``
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        return cluster.add_nodes(
            self, node_type, flavor, node_size, volume_type
        )

    def get_cluster_upgrade_status(self, cluster, **params):
        """Obtain the cluster updgrade details

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.css.v1.cluster.Cluster`
            return: ``None``
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        return self._list(
            _cluster_upgrade_status.ClusterUpgradeStatus,
            cluster_id=cluster.id,
            **params,
        )

    def retry_cluster_upgrade_job(self, cluster, job_id, retry_mode=None):
        """Retry a task or terminate the impact of a task

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.css.v1.cluster.Cluster`
        :param job_id: ID of the task to be retried
        :param retry_mode: if this parameter is not left blank, the impact
            of the task is terminated
        :returns: ``None``
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        return cluster.retry_upgrade_job(self, job_id, retry_mode)

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

    def download_certificate(self, filename=None):
        """
        Downloads a security certificate for ssl connectivity.
        The certificate is downloaded and saved to the specified file.

        :param filename: The name of the file to save the certificate as.
            If not provided, the default filename 'CloudSearchService.cer'
            is used.

        :returns: ``None``
        """
        headers = {'Accept': '*/*'}
        response = self.get('/cer/download', headers=headers, stream=True)
        exceptions.raise_from_response(response)

        # Extract the filename from Content-Disposition header if available
        content_disposition = response.headers.get('Content-Disposition', '')

        override_filename = filename
        filename = override_filename or 'CloudSearchService.cer'
        if not override_filename and 'filename=' in content_disposition:
            filename = content_disposition.split('filename=')[1].strip('"')

        if os.path.exists(filename):
            raise FileExistsError(
                f"The file '{filename}' already exists. Aborting download."
            )

        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

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
