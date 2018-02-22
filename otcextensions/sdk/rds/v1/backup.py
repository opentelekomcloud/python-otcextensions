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

from openstack import _log
from openstack import resource

from otcextensions.sdk.rds import rds_service

from otcextensions.sdk.rds.v1 import _base

_logger = _log.setup_logging('openstack')


class Backup(_base.Resource):

    base_path = '/%(project_id)s/backups'
    resource_key = 'backup'
    resources_key = 'backups'
    service = rds_service.RdsService()

    # capabilities
    allow_create = True
    allow_delete = True
    allow_list = True

    # Properties
    project_id = resource.URI('project_id')
    #: Backup id
    #: Type: uuid*
    id = resource.Body('id')
    #: Instance id
    instance_id = resource.Body('instance_id')
    #: Instance id alt
    instance = resource.Body('instance')
    #: Backup created time
    created = resource.Body('created')
    #: Data store information
    #: *Type: dict*
    dataStore = resource.Body('dataStore', type=dict)
    #: Data backup description
    description = resource.Body('description')
    #: Back file name
    name = resource.Body('name')
    #: Back file size in GB
    #: *Type:int*
    size = resource.Body('size', type=int)
    #: Backup status
    status = resource.Body('status')
    #: Finished time
    updated = resource.Body('updated')
    #: Backup type
    backuptype = resource.Body('backuptype')


class BackupPolicy(_base.Resource):

    base_path = '/%(project_id)s/instances/%(instance_id)s/backups/policy'
    resource_key = 'policy'
    service = rds_service.RdsService()

    # capabilities
    allow_update = True
    allow_get = True

    #: instaceId
    instance_id = resource.URI('instance_id')
    project_id = resource.URI('project_id')
    # Properties
    #: Policy keep days
    #:  Indicates the number of days to retain the generated backup files.
    #:  Its value range is 0 to 35. If this parameter is 0,
    #:  the automated backup policy is not set.
    #: *Type: int*
    keepday = resource.Body('keepday', type=int)
    #: Start time
    #:  Indicates the backup start time that has been set.
    #:  The backup task will be triggered within one hour
    #:  after the backup start time.
    #:  The current time is the UTC time.
    #: *Type: string*
    starttime = resource.Body('starttime')

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
            endpoint_override=endpoint_override,
            headers={
                'X-Language': 'en-us',
                'Content-Type': 'application/json'
            } if not headers else headers)

        return None
