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


class Member(resource.Resource):
    """CBR Member Resource"""
    resource_key = 'member'
    resources_key = 'members'
    base_path = '/backups/%(backup_id)s/members'

    # capabilities
    allow_create = True
    allow_list = True
    allow_fetch = True
    allow_delete = True
    allow_commit = True

    _query_mapping = resource.QueryParameters(
        'backup_id', 'created_at', 'dest_project_id', 'id', 'image_id',
        'status', 'updated_at', 'vault_id')

    #: Properties
    #: Backup ID
    backup_id = resource.Body('backup_id')
    #: Backup sharing time
    #: Example: 2020-02-05T10:38:34.209782
    created_at = resource.Body('created_at')
    #: Destination project ID which the backup is shared
    dest_project_id = resource.Body('dest_project_id')
    #: ID of the image created by using the accepted shared backup_id
    image_id = resource.Body('image_id')
    #: Backup sharing values
    #: values: pending, accepted, rejected
    status = resource.Body('status')
    #: Update time
    #: Example: 2020-02-05T10:38:34.209782
    update_at = resource.Body('update_at')
    #: ID of the vault where the shared backup is stored
    vault_id = resource.Body('vault_id')
    