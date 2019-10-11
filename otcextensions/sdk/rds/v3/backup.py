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

from otcextensions.sdk.rds.v3 import _base


class Backup(_base.Resource):

    base_path = '/backups'
    resources_key = 'backups'
    resource_key = 'backup'

    # capabilities
    allow_create = True
    allow_delete = True
    allow_list = True
    allow_fetch = False

    _query_mapping = resource.QueryParameters(
        'offset', 'begin_time', 'instance_id', 'id',
        'type', 'begin_time', 'end_time', 'offset', 'limit',
        id='backup_id', type='backup_type')

    #: Backup id
    #: Type: uuid*
    id = resource.Body('id')
    #: Begin time
    begin_time = resource.Body('begin_time')
    #: Create back of specific dbs
    #: *Type:list*
    databases = resource.Body('databases', type=list)
    #: Datastore
    #: *Type:dict*
    datastore = resource.Body('datastore', type=dict)
    #: Data backup description
    description = resource.Body('description')
    #: Instance id
    instance_id = resource.Body('instance_id')
    #: Back file size in GB
    #: *Type:int*
    size = resource.Body('size', type=int)
    #: Backup status
    status = resource.Body('status')
    #: Finished time
    end_time = resource.Body('end_time')
    #: Backup type
    #:  `auto`: automated full backup
    #:  `manual`: manual full backup
    #:  `fragment`: differential full backup
    #:  `incremental`: automated incremental backup
    type = resource.Body('type')


class BackupFile(resource.Resource):

    base_path = '/backup-files'
    resources_key = 'files'

    # capabilities
    allow_list = True

    _query_mapping = resource.QueryParameters('backup_id')

    #:  Indicates the file name
    #:  *Type: string*
    name = resource.Body('name')
    #:  Indicates the file size in KB.
    #:  *Type: long*
    size = resource.Body('size', type=int)
    #:  Indicates the link for downloading the backup file.
    #:  *Type: string*
    download_link = resource.Body('download_link')
    #:  Indicates the link expiration time.
    #:  The format is "yyyy-mmddThh:mm:ssZ".
    #:  *Type: string*
    expires_at = resource.Body('link_expired_time')
