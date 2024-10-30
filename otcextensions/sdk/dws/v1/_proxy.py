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

from openstack import resource
from openstack import _log
from openstack import exceptions
from openstack import proxy
from otcextensions.sdk.dws.v1 import cluster as _cluster
from otcextensions.sdk.dws.v1 import flavor as _flavor
from otcextensions.sdk.dws.v1 import snapshot as _snapshot
from otcextensions.sdk.dws.v1 import tag as _tag

LOG = _log.setup_logging(__name__)


def _format_cluster_response(obj):
    if hasattr(obj, 'endpoints'):
        private_domain = []
        for endpoint in obj.endpoints:
            private_domain.append(endpoint['connect_info'])
        setattr(obj, 'private_domain', private_domain)
    if hasattr(obj, 'public_endpoints'):
        public_domain = []
        for public_endpoint in obj.public_endpoints:
            public_domain.append(public_endpoint['public_connect_info'])
        setattr(obj, 'public_domain', public_domain)
    return obj


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
            (:class:`~otcextensions.sdk.dws.v1.cluster.Cluster`) instances
        """
        if query.get('limit'):
            query.update(paginated=False)
        return self._list(_cluster.Cluster, **query)

    def get_cluster(self, cluster):
        """Get the cluster by UUID

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.dws.v1.cluster.Cluster`

        :returns: instance of
            :class:`~otcextensions.sdk.dws.v1.cluster.Cluster`
        """
        obj = self._get(_cluster.Cluster, cluster)
        return _format_cluster_response(obj)

    def find_cluster(self, name_or_id, ignore_missing=True):
        """Find a single cluster

        :param name_or_id: The name or ID of a DWS cluster
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            if the cluster does not exist.
            When set to ``True``, no exception will be set when attempting
            to find a nonexistent cluster.

        :returns:
            One :class:`~otcextensions.sdk.dws.v1.cluster.Cluster` or ``None``
        """
        obj = self._find(
            _cluster.Cluster, name_or_id, ignore_missing=ignore_missing
        )
        return _format_cluster_response(obj)

    def create_cluster(self, **attrs):
        """Create a cluster from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.dws.v1.cluster.Cluster`,
            comprised of the properties on the Cluster class.
        :returns: The results of cluster creation
        :rtype: :class:`~otcextensions.sdk.dws.v1.cluster.Cluster`
        """
        return self._create(_cluster.Cluster, **attrs)

    def restart_cluster(self, cluster):
        """Get the cluster by UUID

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.dws.v1.cluster.Cluster`

        :returns: instance of
            :class:`~otcextensions.sdk.dws.v1.cluster.Cluster`
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        return cluster.restart(self)

    def scale_out_cluster(self, cluster, node_count):
        """Scaling Out a Cluster Nodes

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.dws.v1.cluster.Cluster`
        :param count: Number of nodes to be scaled out.

        :returns: instance of
            :class:`~otcextensions.sdk.dws.v1.cluster.Cluster`
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        return cluster.scale_out(self, node_count)

    def reset_password(self, cluster, new_password):
        """Reset the password of cluster administrator.

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.dws.v1.cluster.Cluster`
        :param new_password: New password of the GaussDB(DWS)
            cluster administrator.

        :returns: instance of
            :class:`~otcextensions.sdk.dws.v1.cluster.Cluster`
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        return cluster.reset_password(self, new_password)

    def delete_cluster(
        self, cluster, keep_last_manual_snapshot=0, ignore_missing=True
    ):
        """Delete a DWS Cluster

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.dws.v1.cluster.Cluster`
        :param int keep_last_manual_snapshot: The number of latest manual
            snapshots that need to be retained for a cluster.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the cluster does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent cluster.
        :returns: None
        """
        return self._delete(
            _cluster.Cluster,
            cluster,
            keep_last_manual_snapshot=keep_last_manual_snapshot,
            ignore_missing=ignore_missing,
        )

    # ======== Flavors ========
    def flavors(self):
        """List all Flavors.

        :returns: a generator of
            (:class:`~otcextensions.sdk.dws.v1.flavor.Flavor`) instances
        """

        split_url = urlsplit(self.get_endpoint())
        url = '{}://{}/v2/{}/node-types'.format(
            split_url.scheme, split_url.netloc, self.get_project_id()
        )
        return self._list(_flavor.Flavor, base_path=url)

    # ======== Snapshot ========
    def snapshots(self):
        """List all Snapshots of a cluster.

        :returns: a generator of
            (:class:`~otcextensions.sdk.dws.v1.snapshot.Snapshot`) instances
        """
        return self._list(_snapshot.Snapshot)

    def get_snapshot(self, snapshot):
        """Get a Snapshot details

        :param snapshot: key id or an instance of
            :class:`~otcextensions.sdk.dws.v1.snapshot.Snapshot`

        :returns: instance of
            :class:`~otcextensions.sdk.dws.v1.snapshot.Snapshot`
        """
        return self._get(_snapshot.Snapshot, snapshot)

    def find_snapshot(self, name_or_id, ignore_missing=True):
        """Find a single snapshot

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
        return self._find(
            _snapshot.Snapshot, name_or_id, ignore_missing=ignore_missing
        )

    def create_snapshot(self, **attrs):
        """Create a cluster Snapshot from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.dws.v1.snapshot.Snapshot`,
            comprised of the properties on the Snapshot class.
        :returns: The results of cluster snapshot creation
        :rtype: :class:`~otcextensions.sdk.dws.v1.snapshot.Snapshot`
        """
        return self._create(
            _snapshot.Snapshot,
            **attrs,
        )

    def delete_snapshot(self, snapshot, ignore_missing=True):
        """Delete a snapshot

        :param snapshot: key id or an instance of
            :class:`~otcextensions.sdk.dws.v1.snapshot.Snapshot`
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the snapshot does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent snapshot.
        :returns: ``None``
        """
        return self._delete(
            _snapshot.Snapshot,
            snapshot,
            ignore_missing=ignore_missing,
        )

    def restore_snapshot(self, snapshot, **attrs):
        """Restore a snapshot.

        :param snapshot: key id or an instance of
            :class:`~otcextensions.sdk.dws.v1.snapshot.Snapshot`
        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.dws.v1.snapshot.Restore`,
            comprised of the properties on the Restore class.
        :returns: instance of
            :class:`~otcextensions.sdk.dws.v1.cluster.Cluster`
        """
        snapshot = self._get_resource(_snapshot.Snapshot, snapshot)
        obj = self._create(_snapshot.Restore, snapshot_id=snapshot.id, **attrs)
        if hasattr(obj, 'cluster'):
            return obj.cluster
        return obj

    def wait_for_cluster(self, cluster, interval=5, wait=1800):
        """Wait for a Cluster status to be `AVAILABLE`.

        :param cluster: The value can be the ID of a cluster
            or a :class:`~otcextensions.sdk.dws.v1.cluster.Cluster`
            instance.
        :param int interval:
            Number of seconds to wait before two consecutive checks.
            Default is 5.
        :param int wait:
            Maximum number of seconds to wait for the status change.
            Default is 1800.
        :return: ``True`` on success.
        :raises: :class:`~openstack.exceptions.ResourceFailure` if the resource
            transitions to a failure status.
        :raises: :class:`~openstack.exceptions.ResourceTimeout` if the
            transition to the desired status does not occur within
            the specified time.
        """
        end_time = time.time() + wait

        task_status_list = (
            'CONFIGURING_EXT_DATASOURCE',
            'DELETING_EXT_DATASOURCE',
            'GROWING',
            'REBOOTING',
            'REDISTRIBUTING',
            'RESTORING',
            'SETTING_CONFIGURATION',
            'SNAPSHOTTING',
        )

        while time.time() < end_time:
            obj = self._get(_cluster.Cluster, cluster)
            status = obj.status
            task_status = obj.task_status
            action_progress = obj.action_progress
            sub_status = obj.sub_status

            if status == 'CREATING':
                LOG.debug(
                    'Still waiting for resource %s to reach state %s, '
                    'current state is %s',
                    obj.name,
                    'AVAILABLE',
                    status,
                )
                time.sleep(interval)
            elif task_status in task_status_list or action_progress:
                LOG.debug(
                    'Still waiting for resource %s task_status to complete, '
                    'current task_status is %s',
                    obj.name,
                    task_status,
                )
                time.sleep(interval)
            elif sub_status == 'NORMAL' and status == 'AVAILABLE':
                return True
            else:
                raise exceptions.ResourceFailure(
                    f'Failed! Cluster status: {status} '
                    f'task_status: {task_status} '
                    f'sub_status: {sub_status} '
                    f'action_progress: {action_progress}'
                )
        raise exceptions.ResourceTimeout(
            'Wait Timed Out. Cluster action still in progress.'
        )

    def wait_for_cluster_scale_out(self, cluster, interval=5, wait=1800):
        """Wait for a Cluster Scale Out Task to Complete.

        :param cluster: The value can be the ID of a cluster
            or a :class:`~otcextensions.sdk.dws.v1.cluster.Cluster`
            instance.
        :param int interval:
            Number of seconds to wait before to consecutive checks.
            Default to 5.
        :param int wait:
            Maximum number of seconds to wait before the change.
            Default to 1800
        """
        obj = self._get(_cluster.Cluster, cluster)
        is_snapshotting = obj.task_status == 'SNAPSHOTTING'
        self.wait_for_cluster(cluster, interval, wait)
        if is_snapshotting:
            time.sleep(60)
            self.wait_for_cluster(cluster, interval, wait)

    def cluster_tags(self, cluster):
        """
        List tags for a DWS cluster.

        :param cluster: Cluster ID or an instance of
            `otcextensions.sdk.dws.v1.cluster.Cluster`.
        :returns: List of `otcextensions.sdk.dws.v1.tag.Tag` instances.
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        return self._list(_tag.Tag, cluster_id=cluster.id)

    def create_cluster_tag(self, cluster, tag):
        """
        Create a new tag for a DWS cluster.

        :param cluster: Cluster ID or an instance of
            `otcextensions.sdk.dws.v1.cluster.Cluster`.
        :param tag: Dictionary with 'key' and 'value' for the tag.
        :returns: Created tag instance.
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        return self._create(_tag.Tag, cluster_id=cluster.id, **tag)

    def delete_cluster_tag(self, cluster, tag_key, ignore_missing=True):
        """
        Delete a single tag from a DWS cluster.

        :param cluster: Cluster ID or an instance of
            `otcextensions.sdk.dws.v1.cluster.Cluster`.
        :param tag_key: The key of the tag to be deleted.
        :param ignore_missing: When False,
            `openstack.exceptions.ResourceNotFound`
            will be raised when the tag does not exist.
            When True, no exception will be set when attempting
            to delete a nonexistent tag.
        :returns: None
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        tag_obj = _tag.Tag.existing(key=tag_key, cluster_id=cluster.id)
        return self._delete(
            _tag.Tag,
            tag_obj.key,
            cluster_id=cluster.id,
            ignore_missing=ignore_missing,
        )

    def batch_create_cluster_tags(self, cluster, tags):
        """
        Batch addition of tags for a cluster.

        :param cluster: Cluster ID or an instance of
            `otcextensions.sdk.dws.v1.cluster.Cluster`.
        :param tags: List of dictionaries of tags to add.
        :return: A list of created
            `otcextensions.sdk.dws.v1.tag.Tag` instances.
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        return _tag.Tag().manage_tags_batch(self, cluster.id, tags, 'create')

    def batch_delete_cluster_tags(self, cluster, tags):
        """
        Batch deletion of tags from a cluster.

        :param cluster: Cluster ID or an instance of
            `otcextensions.sdk.dws.v1.cluster.Cluster`.
        :param tags: List of dictionaries of tags to delete.
        :return: A list of deleted
            `otcextensions.sdk.dws.v1.tag.Tag` instances.
        """
        cluster = self._get_resource(_cluster.Cluster, cluster)
        return _tag.Tag().manage_tags_batch(self, cluster.id, tags, 'delete')

    def wait_for_delete(self, cluster, interval=20, wait=12000, callback=None):
        """Wait for a resource to be deleted.

        :param cluster: The resource to wait on to be deleted.
        :param interval: Number of seconds to wait before to consecutive
            checks. Default to 2.
        :param wait: Maximum number of seconds to wait before the change.
            Default to 120.
        :param callback: A callback function. This will be called with a single
            value, progress, which is a percentage value from 0-100.

        :returns: The resource is returned on success.
        :raises: :class:`~openstack.exceptions.ResourceTimeout` if transition
            to delete failed to occur in the specified seconds.
        """
        return resource.wait_for_delete(self,
                                        cluster,
                                        interval,
                                        wait,
                                        callback)

    def _get_cleanup_dependencies(self):
        return {
            'dws': {
                'before': ['network']
            }
        }

    def _service_cleanup(
        self,
        dry_run=True,
        client_status_queue=None,
        identified_resources=None,
        filters=None,
        resource_evaluation_fn=None,
        skip_resources=None,
    ):
        if self.should_skip_resource_cleanup("cluster", skip_resources):
            return

        clusters = []
        for cluster in self.clusters():
            if not dry_run and cluster.status == 'AVAILABLE':
                tags = list(self.cluster_tags(cluster))
                for tag in tags:
                    self._service_cleanup_del_res(
                        self.delete_cluster_tag,
                        tag['key'],
                        dry_run=dry_run,
                        client_status_queue=client_status_queue,
                        identified_resources=identified_resources,
                        filters=filters,
                        resource_evaluation_fn=resource_evaluation_fn,
                    )
            need_delete = self._service_cleanup_del_res(
                self.delete_cluster,
                cluster,
                dry_run=dry_run,
                client_status_queue=client_status_queue,
                identified_resources=identified_resources,
                filters=filters,
                resource_evaluation_fn=resource_evaluation_fn,
            )
            if not dry_run and need_delete:
                clusters.append(cluster)

        for cluster in clusters:
            self.wait_for_delete(cluster)

        for snapshot in self.snapshots():
            self._service_cleanup_del_res(
                self.delete_snapshot,
                snapshot,
                dry_run=dry_run,
                client_status_queue=client_status_queue,
                identified_resources=identified_resources,
                filters=filters,
                resource_evaluation_fn=resource_evaluation_fn,
            )
