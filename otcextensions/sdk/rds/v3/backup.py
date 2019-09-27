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
from otcextensions.sdk import sdk_resource

class Backup(sdk_resource.Resource):

    base_path = '/backups'
    resource_key = 'backup'
    resources_key = 'backups'
    service_expectes_json_type = True

    # capabilities
    allow_create = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'offset',
        'begin_time',
        'instance_id',
        'backup_id',
        'backup_type',
        'begin_time',
        'end_time'
    )

    #: Backup id
    #: Type: uuid*
    id = resource.Body('id')
    #: Instance id
    instance_id = resource.Body('instance_id')
    #: Data backup description
    description = resource.Body('description')
    #: Create back of specific dbs
    #: *Type:list*
    databases = resource.Body('databases', type=list)
    #: Data store information
    #: *Type: dict*
    datastore = resource.Body('datastore', type=dict)
    #: Back file name
    name = resource.Body('name')
    #: Back file size in GB
    #: *Type:int*
    size = resource.Body('size', type=int)
    #: Backup status
    status = resource.Body('status')
    #: Begin time
    begin_time = resource.Body('begin_time')
    #: Finished time
    end_time = resource.Body('end_time')
    #: Backup type
    type = resource.Body('type')


class BackupPolicy(sdk_resource.Resource):

    base_path = '/instances/%(instance_id)s/backups/policy'
    resource_key = 'backup_policy'

    # capabilities
    allow_update = True
    allow_get = True

    #: instaceId
    instance_id = resource.URI('instance_id')
    # project_id = resource.URI('project_id')

    # Properties
    #: Policy keep days
    #:  Indicates the number of days to retain the generated backup files.
    #:  Its value range is 0 to 35. If this parameter is 0,
    #:  the automated backup policy is not set.
    #: *Type: int*
    keep_days = resource.Body('keep_days', type=int)

    #: Start time
    #:  Indicates the backup start time that has been set.
    #:  The backup task will be triggered within one hour
    #:  after the backup start time.
    #:  The current time is the UTC time.
    #: *Type: string*
    start_time = resource.Body('start_time')

    #: Period
    #:  Indicates the backup cycle configuration
    #:  The backup task will be performed on
    #:  selected days every week
    #: *Type: string*
    period = resource.Body('period')

    # @classmethod
    # def new(cls, **attrs):
    #     return BackupPolicy(
    #         content_type='application/json',
    #         x_language='en-us', **attrs)

    # use put to create, but we don't require id
    def update(self, session, prepend_key=True,
               endpoint_override=None, headers=None):
        """Create a remote resource based on this instance.

        Method is overriden, because PUT without ID should be used

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param prepend_key: A boolean indicating whether the resource_key
                            should be prepended in a resource creation
                            request. Default to True.

        :return: None.
        :raises: :exc:`~openstack.exceptions.MethodNotSupported` if
                 :data:`Resource.allow_create` is not set to ``True``.
        """
        self.update_no_id(
            session, prepend_key,
            # endpoint_override=endpoint_override,
            headers=headers)

        return None


class BackupRestoreTime(sdk_resource.Resource):

    base_path = '/instances/%(instance_id)s/restore-time'
    resource_key = 'restore_time'

    # capabilities
    allow_get = True

    #: instaceId
    instance_id = resource.URI('instance_id')
    # project_id = resource.URI('project_id')

    #: Start time
    #:  Indicates the start time of the recovery time period in
    #:  the UNIX timestamp format. The unit is
    #:  millisecond and the time zone is UTC.
    #: *Type: string*
    start_time = resource.Body('start_time')

    #: End time
    #:  Indicates the end time of the recovery time period in
    #:  the UNIX timestamp format. The unit is
    #:  millisecond and the time zone is UTC.
    #: *Type: string*
    end_time = resource.Body('end_time')
