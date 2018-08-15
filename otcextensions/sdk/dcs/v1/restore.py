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
from openstack import _log

from otcextensions.sdk import sdk_resource

_logger = _log.setup_logging('openstack')


class Restore(sdk_resource.Resource):

    resources_key = 'restore_record_response'

    base_path = '/instances/%(instance_id)s/restores'

    # capabilities
    allow_list = True
    allow_create = True

    _query_mapping = resource.QueryParameters(
        'limit', 'start', 'begin_time', 'end_time',
        begin_time='beginTime',
        end_time='endTime')

    # Properties
    #: Instance ID
    instance_id = resource.URI('instance_id')
    #: Backup description
    backup_description = resource.Body('backup_remark')
    #: Backup ID
    backup_id = resource.Body('backup_id')
    #: Backup name
    backup_name = resource.Body('backup_name')
    #: Time at which the backup task is created.
    created_at = resource.Body('created_at')
    #: Restore description
    description = resource.Body('remark')
    #: Error code returned if DCS instance restore fails.
    error_code = resource.Body('error_code')
    #: Restore ID
    id = resource.Body('restore_id', alternate_id=True)
    #: Restore description
    restore_description = resource.Body('restore_remark', alias='description')
    #: Restore name
    restore_name = resource.Body('restore_name')
    #: Restore progress.
    progress = resource.Body('progress')
    #: Restore status.
    #: * waiting: DCS instance restore is waiting to begin.
    #: * restoring: DCS instance restore is in progress.
    #: * succeed: DCS instance restore succeeded.
    #: * failed: DCS instance restore failed.
    status = resource.Body('status')
    #: Time at which DCS instance restore is completed.
    updated_at = resource.Body('updated_at')
