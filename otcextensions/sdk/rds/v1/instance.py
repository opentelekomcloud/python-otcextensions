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
from openstack import utils

from otcextensions.sdk.rds import rds_service

from otcextensions.sdk import sdk_resource

_logger = _log.setup_logging('openstack')


class Instance(sdk_resource.Resource):

    base_path = '/%(project_id)s/instances'
    resource_key = 'instance'
    resources_key = 'instances'
    service = rds_service.RdsService()

    # capabilities
    allow_create = True
    allow_delete = True
    allow_get = True
    allow_update = True
    allow_list = True

    project_id = resource.URI('project_id')
    # Properties
    #: Instance id
    id = resource.Body('id')
    #: Instance status
    status = resource.Body('status')
    #: Instance name
    name = resource.Body('name')
    #: Links
    #: *Type:list*
    links = resource.Body('links', type=list)
    #: Flavor information
    #: *Type: dict*
    flavor = resource.Body('flavor', type=dict)
    #: Data store information
    #: *Type: dict*
    datastore = resource.Body('datastore', type=dict)
    #: Region
    region = resource.Body('region')
    #: Tenant_id
    #: *Type: str*
    tenante_id = resource.Body('tenant_id')
    #: Volume information
    #: *Type: dict*
    volume = resource.Body('volume', type=dict)
    #: Host name of the instance
    #: *Type:str*
    hostname = resource.Body('hostname')
    #: Instance ip
    #: *Type:str*
    created = resource.Body('ip')
    #: Instance created time
    #: *Type:str*
    created = resource.Body('created')
    #: Instance updated time
    #: *Type:str*
    updated = resource.Body('updated')
    #: Fault, only validate if fault
    #: *Type:dict*
    fault = resource.Body('fault', type=dict)
    #: Replicas
    #: *Type:dict*
    replicas = resource.Body('replicas', type=list)
    #: Configuration
    #: *Type:dict*
    configuration = resource.Body('configuration', type=dict)
    #: Locality
    #: Not supported in RDS
    #: *Type:str*
    locality = resource.Body('locality')
    #: Used local Storage
    #: Not supported in RDS
    local_storage_used = resource.Body('local_storage_used')
    #: Password
    #: The password of the database root user(i.e. the administrative user).
    password = resource.Body('password')
    #: Cluster id
    cluster_id = resource.Body('cluster_id')
    #: Shard id
    shard_id = resource.Body('shard_id')
    #: Server id
    #: The ID of the underlying Nova instance for an instance.
    #: *Type:str*
    server_id = resource.Body('server_id')
    #: Volume id
    #: The ID of a volume.
    #: *Type:str*
    volume_id = resource.Body('volume_id')
    #: encrypted_rpc_messaging
    #: Whether the instance is using encrypted rpm messaging feature or not.
    #: *Type:bool*
    encrypted_rpc_messaging = resource.Body('encrypted_rpc_messaging')

    # Additional Creation properties
    #: Users
    #: *Type:list*
    users = resource.Body('users', type=list)
    #: Flavor ID
    #: *Type:uuid*
    flavorRef = resource.Body('flavorRef')
    #: Modules
    #: *Type:dict*
    modules = resource.Body('modules', type=dict)
    #: Restore point
    #: *Type:dict*
    restore_point = resource.Body('restore_point', type=dict)
    #: Availability Zone
    #: The availability zone of the instance.
    #: *Type:str*
    availability_zone = resource.Body('availability_zone', alias='azcode')
    #: Nics interface list
    #: *Type:dict*
    nics = resource.Body('nics', type=dict)
    #: Id of the master
    #: *Type:str*
    replica_of = resource.Body('replica_of')
    #: Replica of the instance
    #: *Type:int*
    replica_count = resource.Body('replica_count')
    #: region name
    #: *Type:str*
    region_name = resource.Body('region_name')
    #: Databases object
    #: *Type:list*
    databases = resource.Body('databases', type=list)

    # RDS additinal attributes
    #: Instance type readreplica/master/slave
    type = resource.Body('type')
    #: Private cloud id
    vpc = resource.Body('vpc')
    #: Security group
    #: *Type: dict*
    securityGroup = resource.Body('securityGroup', type=dict)
    #: Backup Strategy
    #: *Type: dict*
    backupStrategy = resource.Body('backupStrategy', type=dict)
    #: HA information
    #: *Type: dict*
    ha = resource.Body('ha', type=dict)
    #: Restore Point, create new instance from restore
    #: *Type: dict*
    restorePoint = resource.Body("restorePoint", type=dict)
    #: Root password
    dbRtPd = resource.Body("dbRtPd")
    #: Status of configuration
    configurationStatus = resource.Body("configurationStatus")
    #: Id of configuration
    paramsGroupId = resource.Body('paramsGroupId')
    #: Id of subnet
    subnetid = resource.Body('subnetid')
    #: Instance role
    role = resource.Body('role')
    #: Internal subnet id
    internalSubnetId = resource.Body('internalSubnetId')
    #: Group of instance
    group = resource.Body('group')
    #: Secure group id
    securegroup = resource.Body('securegroup')
    #: Az code
    azcode = resource.Body('azcode')
    #: DB user
    dbuser = resource.Body('dbuser')
    #: Storage Engine
    storeEngine = resource.Body('storeEngine')
    #: Pay model
    payModel = resource.Body('payModel')
    #: Slave of instance
    slave_of = resource.Body('slave_of')
    # Indicates the EIP for public access, including
    # the IP address and port number.
    # *Type:string*
    publicEndpoint = resource.Body('publicEndpoint')

    def _action(self, exec_method, json, endpoint_override=None):
        """Executes the action

        :returns: ``None``
        """
        if not endpoint_override:
            if getattr(self, 'endpoint_override', None):
                # If we have internal endpoint_override - use it
                endpoint_override = self.endpoint_override
        base_url = self.base_path % self._uri.attributes
        url = utils.urljoin(base_url, self.id, 'action')
        return exec_method(url, json=json, endpoint_override=endpoint_override)

    def restart(self, session, endpoint_override=None):
        """Restart the database instance

        :returns: ``None``
        """
        body = {'restart': {}}
        self._action(session.post, body, endpoint_override)

    def resize(self, session, flavor_reference, endpoint_override=None):
        """Resize the database instance flavor

        :returns: ``None``
        """
        body = {'resize': {'flavorRef': flavor_reference}}
        self._action(session.post, body, endpoint_override)

    def resize_volume(self, session, volume_size, endpoint_override=None):
        """Resize the volume attached to the instance

        :returns: ``None``
        """
        body = {'resize': {'volume': volume_size}}
        self._action(session.post, body, endpoint_override)

    def restore(self, session, backupRef, endpoint_override=None):
        """Restores database to the given backup rference

        :returns: ``None``
        """
        body = {"restore": {"backupRef": backupRef}}
        self._action(session.post, body, endpoint_override)

        # TODO(agoncharov) call returns jobId
        # return self._action(session, {"restore": {"backupRef": backupRef}})

    def create_from_backup(self, **attrs):
        """This interface is used to restore
        the specified DB instance data to a new DB instance.

        """
        raise NotImplementedError
        # TODO(agoncharov) call returns instance spec
