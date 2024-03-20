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
from openstack import exceptions
from openstack import resource
from openstack import utils
from otcextensions.common import format as otc_format


class Snapshot(resource.Resource):

    base_path = '/clusters/%(uri_cluster_id)s/index_snapshot'
    # base_path = '/clusters/%(cluster_id}s/index_snapshot'

    resource_key = 'backup'
    resources_key = 'backups'

    allow_create = True
    allow_delete = True
    allow_list = True
    allow_fetch = True

    #: ID of the cluster where index data is to be backed up.
    uri_cluster_id = resource.URI('uri_cluster_id')

    #: Snapshot retention period.
    backup_keep_days = resource.Body('backupKeepDay', type=int)
    #: Snapshot creation mode.
    backup_method = resource.Body('backupMethod')
    #: Time when a snapshot is executed every day.
    backup_period = resource.Body('backupPeriod')
    #: Time when the snapshot starts to be executed.
    backup_start_time = resource.Body('backupExpectedStartTime')
    #: Snapshot Type Automatic/Manual
    backup_type = resource.Body('backupType')
    #: Bucket for storing snapshot data.
    bucket_name = resource.Body('bucketName')
    #: Cluster name.
    cluster_name = resource.Body('clusterName')
    #: Cluster Id.
    cluster_id = resource.Body('clusterId')
    #: Time when a snapshot is created.
    created_at = resource.Body('created')
    #: Type of the data search engine.
    datastore = resource.Body('datastore', type=dict)
    #: Description of a snapshot.
    description = resource.Body('description')
    #: Timestamp when the snapshot execution ends.
    end_time = resource.Body('endTime')
    #: Number of shards that fail to be backed up.
    failed_shards = resource.Body('failedShards', type=int)
    #: Indices that need to be backed up.
    indices = resource.Body('indices')
    #: Rule for defining the indices to be restored.
    rename_pattern = resource.Body('renamePattern')
    #: Rule for renaming an index.
    rename_replacement = resource.Body('renameReplacement')
    #: Snapshot restoration status.
    restore_status = resource.Body('restoreStatus')
    #: Timestamp when the snapshot starts to be executed.
    start_time = resource.Body('startTime')
    #: Snapshot status.
    status = resource.Body('status')
    #: ID of the cluster, to which the snapshot is to be restored.
    target_cluster = resource.Body('targetCluster')
    #: Total number of shards of the indices to be backed up.
    total_shards = resource.Body('totalShards', type=int)
    #: Time when a snapshot status is updated.
    updated_at = resource.Body('updated')
    #: Version of the snapshot.
    version = resource.Body('version')

    def create(self, session, base_path=None):
        # This overrides the default behavior of resource creation because
        # backup create doesn't accept resource_key in its request.
        return super(Snapshot, self).create(
            session, prepend_key=False, base_path=base_path
        )

    def restore(self, session, cluster_id, **body):
        """Restoring a Snapshot."""
        uri = utils.urljoin(
            'clusters', cluster_id, 'index_snapshot', self.id, 'restore'
        )
        response = session.post(uri, json=body)
        exceptions.raise_from_response(response)


class SnapshotPolicy(resource.Resource):

    base_path = '/clusters/%(cluster_id)s/index_snapshot/policy'

    allow_create = True
    allow_fetch = True

    #: ID of the cluster where automatic snapshot creation is enabled.
    cluster_id = resource.URI('cluster_id')

    #: Agency used to access OBS buckets.
    agency = resource.Body('agency')
    #: Storage path of the snapshot in the OBS bucket.
    backup_path = resource.Body('basePath')
    #: Time when a snapshot is created every day.
    backup_period = resource.Body('period')
    #: Retention days for a snapshot.
    backup_keep_days = resource.Body('keepday', type=int)
    #: OBS bucket for storing snapshots.
    bucket_name = resource.Body('bucket')
    #: Snapshot encryption ID.
    cmk_id = resource.Body('snapshotCmkId')
    #: Whether to delete all automatically created snapshots when the
    #:  automatic snapshot creation policy is disabled.
    delete_auto = resource.Body('deleteAuto', type=otc_format.BoolStr_1)
    #: Snapshot name prefix.
    prefix = resource.Body('prefix')
    #: Name of the index to be backed up.
    indices = resource.Body('indices')
    #: Whether to enable the automatic snapshot creation policy.
    is_enabled = resource.Body('enable', type=otc_format.BoolStr_1)


class SnapshotConfiguration(resource.Resource):

    base_path = '/clusters/%(cluster_id)s/index_snapshot/%(setting)s'

    allow_create = True

    #: ID of the cluster where automatic snapshot creation is enabled.
    cluster_id = resource.URI('cluster_id')
    #: Setting -> auto_setting or custom setting
    setting = resource.URI('setting')

    #: OBS bucket used for index data backup.
    bucket_name = resource.Body('bucket')
    #: IAM agency used to access OBS.
    agency = resource.Body('agency')
    #: Key ID used for snapshot encryption.
    cmk_id = resource.Body('snapshotCmkId')

    def disable(self, session):
        """Disable Snapshot Function."""
        uri = utils.urljoin('clusters', self.cluster_id, 'index_snapshots')
        response = session.delete(uri)
        exceptions.raise_from_response(response)
