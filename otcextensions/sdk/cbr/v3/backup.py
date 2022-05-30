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


class AppCSpec(resource.Resource):
    app_consistency = resource.Body('app_consistency')
    error_code = resource.Body('app_consistency_error_code')
    error_message = resource.Body('app_consistency_error_message')
    error_status = resource.Body('app_consistency_error_status')


class ExtendInfo(resource.Resource):
    app_consistency = resource.Body('app_consistency', type=AppCSpec)
    architecture = resource.Body('architecture')
    #: Whether the backup is automatically triggered
    auto_trigger = resource.Body('auto_trigger', type=bool)
    #: Whether the backup is a system disk backup
    bootable = resource.Body('bootable', type=bool)
    #: Whether the VM backup data contains system disk data
    contain_system_disk = resource.Body('contain_system_disk', type=bool)
    #: Whether the backup is encrypted
    encrypted = resource.Body('encrypted', type=bool)
    #: Whether the backup is an incremental backup
    incremental = resource.Body('incremental', type=bool)
    #: ID list of images created using backups
    os_images_data = resource.Body('os_images_data')
    progress = resource.Body('progress')
    #: Snapshot ID of the disk backup
    snapshot_id = resource.Body('snapshot_id')
    #: Whether to allow lazyloading for fast restoration
    support_lld = resource.Body('support_lld', type=bool)
    #: Restoration mode
    #: Choices: na, snapshot, backup
    #: Default: na
    #: na indicates the backup cannot be used for restoration
    supported_restore_mode = resource.Body('supported_restore_mode')
    #: Whether the disk is a system disk
    system_disk = resource.Body('system_disk', type=bool)


class Backup(resource.Resource):
    """CBR Backup Resource"""
    resource_key = 'backup'
    resources_key = 'backups'
    base_path = '/backups'

    # capabilities
    allow_create = False
    allow_list = True
    allow_fetch = True
    allow_delete = True
    allow_commit = False

    _query_mapping = resource.QueryParameters(
        'checkpoint_id', 'dec', 'end_time', 'image_type', 'limit',
        'marker', 'member_status', 'name', 'offset', 'own_type',
        'parent_id', 'resource_az', 'resource_id', 'resource_name',
        'resource_type', 'sort', 'start_time', 'status',
        'used_percent', 'vault_id')

    #: Properties
    #: Restore point ID
    checkpoint_id = resource.Body('checkpoint_id')
    children = resource.Body('children', type=list)
    #: Creation time
    created_at = resource.Body('created_at')
    #: Backup description
    description = resource.Body('description')
    #: Expiration time
    expired_at = resource.Body('expired_at')
    #: Extended Information
    extend_info = resource.Body('extend_info', type=ExtendInfo)
    #: Backup type
    #: Values: backup or replication
    image_type = resource.Body('image_type')
    #: Backup name
    name = resource.Body('name')
    #: Parent backup ID
    parent_id = resource.Body('parent_id')
    #: Project ID
    project_id = resource.Body('project_id')
    #: Backup time
    protected_at = resource.Body('protected_at')
    provider_id = resource.Body('provider_id')
    replication_records = resource.Body('replication_records', type=list)
    #: Resource availability zone
    resource_az = resource.Body('resource_az')
    #: Resource ID
    resource_id = resource.Body('resource_id')
    #: Resource name
    resource_name = resource.Body('resource_name')
    #: Resource type:
    #: OS::Nova::Server or OS::Cinder::Volume
    resource_type = resource.Body('resource_type')
    #: Resource size in GB
    resource_size = resource.Body('resource_size', type=int)
    #: Backup status
    status = resource.Body('status')
    #: Update time
    updated_at = resource.Body('updated_at')
    #: Vault ID
    vault_id = resource.Body('vault_id')

    def add_members(self, session, members):
        """Method to add several share members to a backup

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param list members: List of target project IDs to which the backup
            is shared
        """
        url = utils.urljoin(self.base_path, self.id, '/members')
        body = {
            'members': members
        }
        return session.post(url, json=body)
