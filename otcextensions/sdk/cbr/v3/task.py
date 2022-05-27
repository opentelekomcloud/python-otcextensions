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


class ErrorInfoSpec(resource.Resource):
    #: Properties
    #: Error code
    code = resource.Body('code')
    #: Error message
    message = resource.Body('message')


class ExtendInfoBackup(resource.Resource):
    #: Properties
    #: Error code returned if application-consistent backup fails
    app_consistency_error_code = resource.Body('app_consistency_error_code')
    #: Error message returned if application-consistent backup fails
    app_consistency_error_mess = resource.Body('app_consistency_error_message')
    #: Application-consistent backup status
    app_consistency_status = resource.Body('app_consistency_status')
    #: Backup ID
    backup_id = resource.Body('backup_id')
    #: Backup name
    backup_name = resource.Body('backup_name')
    #: Whether incremental backup is used
    incremental = resource.Body('incremental')


class ExtendInfoCommon(resource.Resource):
    #: Properties
    #: Progress of the query task
    progress = resource.Body('progress')
    #: Request ID
    request_id = resource.Body('request_id')
    #: Backup task ID
    task_id = resource.Body('task_id')


class ExtendInfoDelete(resource.Resource):
    #: Properties
    #: Backup ID
    backup_id = resource.Body('backup_id')
    #: Backup name
    backup_name = resource.Body('backup_name')


class ExtendInfoSync(resource.Resource):
    #: Properties
    #: Number of synchronized backups
    sync_backup_num = resource.Body('sync_backup_num')
    #: Number of deleted backups
    delete_backup_num = resource.Body('delete_backup_num')
    #: Number of backups that fail to be synchronized
    err_sync_backup_num = resource.Body('err_sync_backup_num')


class ExtendInfoRestore(resource.Resource):
    #: Properties
    #: Backup ID
    backup_id = resource.Body('backup_id')
    #: Backup name
    backup_name = resource.Body('backup_name')
    #: ID of the resource to be restored
    target_resource_id = resource.Body('target_resource_id')
    #: Name of the resource to be restored
    target_resource_name = resource.Body('target_resource_name')


class ExtendInfoVaultDelete(resource.Resource):
    #: Properties
    #: Number of resources that fail to be deleted
    fail_count = resource.Body('fail_count')
    #: Number of deleted backups
    total_count = resource.Body('total_count')


class ResourceSpec(resource.Resource):
    #: Properties
    #: Additional information of the resource
    extra_info = resource.Body('extra_info', type=dict)
    #: ID of the resource to be backed up
    id = resource.Body('id')
    #: Name of the resource to be backed up
    name = resource.Body('name')
    #: Type of the resource to be backed up
    type = resource.Body('type')


class ExtendInfoRemoveResources(resource.Resource):
    #: Properties
    #: Number of resources that fail to be deleted
    fail_count = resource.Body('fail_count')
    #: Number of deleted backups
    total_count = resource.Body('total_count')
    #: Resources
    resources = resource.Body('resources', type=list, list_type=ResourceSpec)


class ExtraInfoSpec(resource.Resource):
    #: Properties
    #: Extended parameters of backup
    backup = resource.Body('backup', type=ExtendInfoBackup)
    #: Common parameters
    common = resource.Body('common', type=ExtendInfoCommon)
    #: Extended parameters of deletion
    delete = resource.Body('delete', type=ExtendInfoDelete)
    #: Extended parameters of synchronization
    sync = resource.Body('sync', type=ExtendInfoSync)
    #: Extended parameters of removing resources from a vault
    remove_resources = resource.Body('remove_resources',
                                     type=ExtendInfoRemoveResources)
    #: Resource information
    resource_info = resource.Body('resource', type=ResourceSpec)
    #: Extended parameters of restoration
    restore = resource.Body('restore', type=ExtendInfoRestore)
    #: Extended parameters of deleting a vault
    vault_delete = resource.Body('vault_delete', type=ExtendInfoVaultDelete)


class Task(resource.Resource):
    """CBR Task Resource"""
    resource_key = 'operation_log'
    resources_key = 'operation_logs'
    base_path = '/operation-logs'

    # capabilities
    allow_list = True
    allow_fetch = True

    _query_mapping = resource.QueryParameters('operation_log_id', 'project_id')

    #: Properties
    #: Backup record ID
    checkpoint_id = resource.Body('checkpoint_id')
    #: Creation time
    created_at = resource.Body('created_at')
    #: Task end time
    ended_at = resource.Body('ended_at')
    #: Task error message
    error_info = resource.Body('error_info', type=ErrorInfoSpec)
    #: Task extension information
    extra_info = resource.Body('extra_info', type=ExtraInfoSpec)
    #: Task ID
    id = resource.Body('id')
    #: Task type
    operation_type = resource.Body('operation_type')
    #: Policy ID
    policy_id = resource.Body('policy_id')
    #: Project ID
    project_id = resource.Body('project_id')
    #: Backup provider ID
    provider_id = resource.Body('provider_id')
    #: Task start time
    started_at = resource.Body('started_at')
    #: Task status
    status = resource.Body('status')
    #: Modification time
    updated_at = resource.Body('updated_at')
    #: ID of the vault with which the target resource is associated
    vault_id = resource.Body('vault_id')
    #: Name of the vault with which the target resource is associated
    vault_name = resource.Body('vault_name')
