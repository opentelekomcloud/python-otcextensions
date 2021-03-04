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


class DcsBool(object):
    val = False

    def __init__(self, value):
        if value.lower() == 'true':
            self.val = True
        else:
            self.val = False

    def __get__(self):
        return self.val

    def __set__(self, value):
        if value.lower() == 'true':
            self.val = True
        else:
            self.val = False

    def __eq__(self, other):
        return self.val == other


class Backup(resource.Resource):

    resources_key = 'backup_record_response'

    base_path = '/instances/%(instance_id)s/backups'

    # capabilities
    allow_create = True
    allow_list = True
    allow_fetch = True
    allow_delete = True

    _query_mapping = resource.QueryParameters(
        'limit', 'start', 'begin_time', 'end_time',
        begin_time='beginTime',
        end_time='endTime')

    # Properties
    instance_id = resource.URI('instance_id')
    #: Time at which the backup task is created.
    created_at = resource.Body('created_at')
    #:  Description of the DCS instance backup.
    description = resource.Body('remark')
    #: Error code returned if DCS instance backup fails.
    error_code = resource.Body('error_code')
    #: Backup ID
    id = resource.Body('backup_id', alternate_id=True)
    #: An indicator of whether restoration is supported. The
    #: value can be TRUE or FALSE.
    is_restorable = resource.Body('is_support_restore', type=DcsBool)
    #: Backup name
    name = resource.Body('backup_name')
    #: Time segment in which DCS instance backup was performed.
    period = resource.Body('period')
    #: Backup progress.
    progress = resource.Body('progress')
    #: Size of the backup file.
    #: Unit: byte.
    size = resource.Body('size', type=int)
    #: Backup status.
    #: * waiting: DCS instance backup is waiting to begin.
    #: * backuping: DCS instance backup is in progress.
    #: * succeed: DCS instance backup succeeded.
    #: * failed: DCS instance backup failed.
    #: * expired: The backup file has expired.
    #: * deleted: The backup file has been deleted manually.
    status = resource.Body('status')
    #: Backup type.
    #: * manual: manual backup.
    #: * auto: automatic backup.
    type = resource.Body('backup_type')
    #: Time at which DCS instance backup is completed.
    updated_at = resource.Body('updated_at')
