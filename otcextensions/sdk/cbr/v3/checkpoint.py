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


class ExtraInfo(resource.Resource):
    #: Properties
    #: Backup name
    name = resource.Body('name')
    #: Backup description
    description = resource.Body('description')
    #: Number of days that backups can be retained
    retention_duration = resource.Body('retention_duration', type=int)


class CheckpointResource(resource.Resource):
    #: Properties
    #: Number of backups
    backup_count = resource.Body('backup_count')
    #: Backup size
    backup_size = resource.Body('backup_size')
    #: Extra information of the resource
    extra_info = resource.Body('extra_info')
    #: ID of the resource to be backed up
    id = resource.Body('id')
    #: Name of the resource to be backed up
    #: max 255 characters
    name = resource.Body('name')
    #: Protection status, choices:
    #: available, error, protecting, restoring, removing
    protect_status = resource.Body('protect_status')
    #: Allocated capacity for the associated resource in GB
    resource_size = resource.Body('resource_size')
    #: type of the resource to be backed up.
    type = resource.Body('type')


class SkippedResource(resource.Resource):
    #: Properties
    #: Error Codes
    code = resource.Body('code')
    #: Resource ID
    id = resource.Body('id')
    #: Resource name
    name = resource.Body('name')
    #: Reason for skipping
    reason = resource.Body('reason')
    #: type of the resource to be backed up.
    type = resource.Body('type')


class Vault(resource.Resource):
    #: Properties
    #: Vault ID
    id = resource.Body('id')
    #: Vault name
    name = resource.Body('name')
    #: Backup objects
    resources = resource.Body('resource', type=list,
                              list_type=CheckpointResource)
    #: Resources skipped during backup
    skipped_resources = resource.Body('skipped_resources', type=list,
                                      list_type=SkippedResource)


class IncludeVolumes(resource.Resource):
    #: Properties
    #: EVS disk UUID
    id = resource.Body('id')
    #: OS type
    os_version = resource.Body('os_version')


class ResourceExtraInfo(resource.Resource):
    #: Properties
    #: List of IDs that is excluded from backup.
    exclude_volumes = resource.Body('exclude_volumes', type=list)
    #: Disk to be backed up
    include_volumes = resource.Body('include_volumes', type=list,
                                    list_type=IncludeVolumes)


class ResourceDetails(resource.Resource):
    #: Checkpoint resource creation Properties
    #: Extra information of the resource
    extra_info = resource.Body('extra_info', type=ResourceExtraInfo)
    #: ID of the resource to be backed up
    id = resource.Body('id')
    #: Name of the resource to be backed up
    name = resource.Body('name')
    #: Type of the resource to be backed up
    resource_type = resource.Body('type')


class Parameters(resource.Resource):
    #: Properties
    #: Whether automatic triggering is enabled
    auto_trigger = resource.Body('auto_trigger', type=bool)
    #: Backup description
    description = resource.Body('description')
    #: Whether the backup is an incremental backup
    incremental = resource.Body('incremental')
    #: Backup name
    name = resource.Body('name')
    #: UUID list of resources to be backed up
    resources = resource.Body('resources', type=list)
    resource_details = resource.Body('resource_details',
                                     type=ResourceDetails)


class Checkpoint(resource.Resource):
    """CBR Checkpoint Resource"""
    resource_key = 'checkpoint'
    resources_key = ''
    base_path = '/checkpoints'

    # capabilities
    allow_create = True
    allow_list = False
    allow_fetch = True
    allow_delete = False
    allow_commit = False

    _query_mapping = resource.QueryParameters(
        'checkpoint_id')

    #: Properties
    #: Creation time
    #: Example: 2020-02-05T10:38:34.209782
    created_at = resource.Body('created_at')
    #: Extra info
    extra_info = resource.Body('extra_info', type=ExtraInfo)
    #: Resoure point ID
    id = resource.Body('id')
    #: Checkpoint creation parameters
    parameters = resource.Body('parameters', type=Parameters)
    #: Project ID
    project_id = resource.Body('project_id')
    #: Status
    status = resource.Body('status')
    #: Vault information
    vault = resource.Body('vault', type=Vault)
    #: Vault ID for checkpoint creation
    vault_id = resource.Body('vault_id')
