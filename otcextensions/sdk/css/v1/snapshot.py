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
from openstack import resource
from openstack import utils

from otcextensions.common import format as otc_format


class DatastoreSpec(resource.Resource):
    #: Supported type: elasticsearch
    type = resource.Body('type')
    #: Elastic Search Engine version number.
    version = resource.Body('version')


class Snapshot(resource.Resource):

    base_path = '/clusters/%(cluster_id)s/index_snapshot'
    # base_path = '/clusters/%(cluster_id}s/index_snapshot'

    resource_key = 'backup'
    resources_key = 'backups'

    allow_create = True
    allow_delete = True
    allow_list = True
    allow_get = True

    #: ID of the cluster where index data is to be backed up.
    cluster_id = resource.URI('cluster_id')

    #: ID of the snapshot.
    id = resource.Body('id')
    #: Snapshot name.
    name = resource.Body('name')
    #: Description of a snapshot.
    description = resource.Body('description')
    #: Name of the index to be backed up.
    indices = resource.Body('indices')

    #: Time when a snapshot is created.
    created_at = resource.Body('created')
    #: Type of the data search engine.
    datastore = resource.Body('datastore', type=DatastoreSpec)
    #: Cluster name.
    cluster_name = resource.Body('clusterName')
    #: Snapshot status.
    status = resource.Body('status')
    #: Time when a snapshot status is updated.
    updated_at = resource.Body('updated')
    #: Snapshot Type Automatic/Manual
    backup_type = resource.Body('backupType')
    #: Snapshot creation mode.
    backup_method = resource.Body('backupMethod')
    #: Time when the snapshot starts to be executed.
    backup_start_time = resource.Body('backupExpectedStartTime')
    #: Snapshot retention period.
    backup_keep_days = resource.Body('backupKeepDay', type=int)
    #: Time when a snapshot is executed every day.
    backup_period = resource.Body('backupPeriod')
    #: Indices that need to be backed up.
    indices = resource.Body('indices')
    #: Total number of shards of the indices to be backed up.
    total_shards = resource.Body('totalShards', type=int)
    #: Number of shards that fail to be backed up.
    failed_shards = resource.Body('failedShards', type=int)
    #: Version of the snapshot.
    version = resource.Body('version')
    #: Snapshot restoration status.
    restore_status = resource.Body('restoreStatus')
    #: Timestamp when the snapshot starts to be executed.
    start_time = resource.Body('startTime')
    #: Timestamp when the snapshot execution ends.
    end_time = resource.Body('endTime')
    #: Bucket for storing snapshot data.
    bucket_name = resource.Body('bucketName')

    #: ID of the cluster, to which the snapshot is to be restored.
    target_cluster = resource.Body('targetCluster')
    #: Name of the index to be restored.
    indices = resource.Body('indices')
    #: Rule for defining the indices to be restored.
    rename_pattern = resource.Body('renamePattern')
    #: Rule for renaming an index.
    rename_replacement = resource.Body('renameReplacement')

    def restore(self, session, **body):
        """Preform actions given the message body.
        """
        url = utils.urljoin(self.base_path, self.id, 'restore')
        return session.post(url, json=body)


class SnapshotPolicy(resource.Resource):

    base_path = '/clusters/%(cluster_id)s/index_snapshot/policy'

    allow_create = True
    allow_fetch = True

    #: ID of the cluster where automatic snapshot creation is enabled.
    cluster_id = resource.URI('cluster_id')

    #: Retention days for a snapshot.
    backup_keep_days = resource.Body('keepday', type=int)
    #: Time when a snapshot is created every day.
    backup_period = resource.Body('period')
    #: Snapshot name prefix.
    backup_prefix = resource.Body('prefix')
    #: OBS bucket for storing snapshots.
    bucket_name = resource.Body('bucket')
    #: Storage path of the snapshot in the OBS bucket.
    backup_path = resource.Body('basePath')
    #: Agency used to access OBS buckets.
    agency = resource.Body('agency')
    #: Whether to enable the automatic snapshot creation policy.
    enable = resource.Body('enable', type=otc_format.BoolStr_1)
    #: Name of the index to be backed up.
    indices = resource.Body('indices')
    #: Snapshot encryption ID.
    cmk_id = resource.Body('snapshotCmkId')
    #: Whether to delete all automatically created snapshots when the
    #:  automatic snapshot creation policy is disabled.
    delete_auto = resource.Body('deleteAuto')


class SnapshotConfiguration(resource.Resource):

    base_path = '/clusters/%(cluster_id)s/index_snapshot/%(setting)s'

    allow_create = True

    #: ID of the cluster where automatic snapshot creation is enabled.
    clusterId = resource.URI('cluster_id')
    #: Setting -> auto_setting or custom setting
    setting = resource.URI('setting')

    #: OBS bucket used for index data backup.
    bucket_name = resource.Body('bucket')
    #: IAM agency used to access OBS.
    agency = resource.Body('agency')
    #: Key ID used for snapshot encryption.
    cmk_id = resource.Body('snapshotCmkId')
