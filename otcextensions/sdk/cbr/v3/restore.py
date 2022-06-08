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


class Mapping(resource.Resource):
    #: Properties
    #: Disk backup ID
    backup_id = resource.Body('backup_id')
    #: ID of the to which data is restored
    volume_id = resource.Body('volume_id')


class Restore(resource.Resource):
    """CBR Backup Resource"""
    resource_key = 'restore'
    resources_key = ''
    base_path = '/backups/%(backup_id)s/restore'

    # capabilities
    allow_create = True
    allow_list = False
    allow_fetch = False
    allow_delete = False
    allow_commit = False

    _query_mapping = resource.QueryParameters()

    #: Properties
    #: URI backup reference
    backup_id = resource.URI('backup_id')
    #: Restores mapping relationship.
    #: Mandatory for VM restoreation and optional for disk restoration
    mappings = resource.Body('mappings', type=list, list_type=Mapping)
    #: Whether the server is powered on after restoration.
    #: Default: True
    power_on = resource.Body('power_on', type=bool)
    #: ID of the resource to be restored
    resource_id = resource.Body('resource_id')
    #: ID of the target VM to be restored.
    #: Mandatory for VM restoration.
    server_id = resource.Body('server_id')
    #: ID of the target disk to be restored
    #: This parameter is mandatory for disk restoration
    volume_id = resource.Body('volume_id')
