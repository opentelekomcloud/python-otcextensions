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


class Instance(sdk_resource.Resource):

    base_path = '/instances'
    resources_key = 'instances'
    resource_key = 'instance'
    # service_expectes_json_type = True

    # capabilities
    allow_create = True
    allow_delete = True
    allow_update = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'id', 'name', 'type', 'datastore_type',
        'vpc_id', 'subnet_id', 'offset', 'limit'
    )
    #: Instance id
    id = resource.Body('id')
    #: Instance name
    name = resource.Body('name')
    #: Instance status
    status = resource.Body('status')
    #: Private IP address List
    #: *Type:list*
    private_ips = resource.Body('private_ips', type=list)
    #: Public IP address List
    #: *Type:list*
    public_ips = resource.Body('public_ips', type=list)
    #: Database port number
    #: *Type:int*
    port = resource.Body('port', type=int)
    #: Instance type readreplica/master/slave
    #: *Type:str*
    type = resource.Body('type')
    #: HA information
    #: *Type: dict*
    ha = resource.Body('ha', type=dict)
    #: Region
    #: *Type:str*
    region = resource.Body('region')
    #: Data store information
    #: *Type: dict*
    datastore = resource.Body('datastore', type=dict)
    #: Instance created time
    #: *Type:str*
    created = resource.Body('created')
    # datastore: Instance updated time
    #: *Type:str*
    updated = resource.Body('updated')
    #: DB default username
    #: *Type:str*
    db_user_name = resource.Body('db_user_name')
    #: Private cloud id
    vpc_id = resource.Body('vpc_id')
    #: Id of subnet
    subnet_id = resource.Body('subnet_id')
    #: Security Group Id
    security_group_id = resource.Body('security_group_id')
    #: Flavor ID
    #: *Type:uuid*
    flavor_ref = resource.Body('flavor_ref')
    #: Availability Zone
    #: *Type:str*
    availability_zone = resource.Body('availability_zone')
    #: Volume information
    #: *Type: dict*
    volume = resource.Body('volume', type=dict)
    #: Switch Strategy
    #: *Type:str*
    switch_strategy = resource.Body('switch_strategy')
    #: Backup Strategy
    #: *Type: dict*
    backup_strategy = resource.Body('backup_strategy', type=dict)
    #: maintenance time window
    #: *Type:str*
    maintenance_window = resource.Body('maintenance_window')
    #: Node information
    #:  Indicates the primary/standby DB
    #:  instance information
    #: *Type:list*
    nodes = resource.Body('nodes', type=list)
    #: list of associated DB instances
    #: *Type:list*
    related_instance = resource.Body('related_instance', type=list)
    #: Disk Encryption Key Id
    #: *Type:str*
    disk_encryption_id = resource.Body('disk_encryption_id')
    #: Database Password
    #: *Type:str*
    password = resource.Body('password')
    #: Time Zone
    #: *Type:str*
    time_zone = resource.Body('time_zone')
    #: replication mode for the standby
    #:   DB instance.
    #: *Type:str*
    replication_mode = resource.Body('replication_mode')
    #: Charge Info
    #: *Type: dict*
    backup_strategy = resource.Body('charge_info', type=dict)


class InstanceRecovery(sdk_resource.Resource):

    # capabilities
    allow_create = True

    #: Specifies the restoration information
    #:  *Type: dict*
    source = resource.Body('source', type=dict)
    #: Specifies the restoration target
    #:  *Type: dict*
    target = resource.Body('target', type=dict)


class InstanceConfiguration(sdk_resource.Resource):

    base_path = '/instances/%(instance_id)s/configurations'

    # capabilities
    allow_get = True
    allow_update = True

    #: instaceId
    instance_id = resource.URI('instance_id')

    #: database version name
    #:  *Type: string*
    datastore_version_name = resource.Body('datastore_version_name')
    #: database name
    #:  *Type: string*
    datastore_name = resource.Body('datastore_name')
    #: Indicates the creation time in the following
    #:  format: yyyy-MM-ddTHH:mm:ssZ.
    #:  *Type: string*
    created = resource.Body('created')
    #: Indicates the update time in the following
    #:  format: yyyy-MM-ddTHH:mm:ssZ.
    #:  *Type: string*
    updated = resource.Body('updated')
    #: Indicates the parameter configuration
    #:  defined by users based on the default
    #:  parameter groups.
    #:  *Type: list*
    configuration_parameters = resource.Body('configuration_parameters')

    def update(self, session, prepend_key=False):
        """
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
        return self.update_no_id(session, prepend_key)


class InstanceRestoreTime(resource.Resource):

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
