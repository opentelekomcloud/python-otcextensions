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


class Instance(_base.Resource):

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
    #: Instance created time
    created = resource.Body('created')
    #: Host name of the instance
    hostname = resource.Body('hostname')
    #: Instance type readreplica/master/slave
    type = resource.Body('type')
    #: Region
    region = resource.Body('region')
    #: Instance updated time
    updated = resource.Body('updated')
    #: Availability Zone
    availability_zone = resource.Body('availability_zone')
    #: Private cloud id
    vpc = resource.Body('vpc')
    #: Nics interface list
    #: *Type:dict*
    nics = resource.Body('nics', type=dict)
    #: Security group
    #: *Type: dict*
    securityGroup = resource.Body('securityGroup', type=dict)
    #: Flavor information
    #: *Type: dict*
    flavor = resource.Body('flavor', type=dict)
    #: Volume information
    #: *Type: dict*
    volume = resource.Body('volume', type=dict)
    #: Data store information
    #: *Type: dict*
    datastore = resource.Body('datastore', type=dict)
    #: Backup Strategy
    #: *Type: dict*
    backupStrategy = resource.Body('backupStrategy', type=dict)
    #: Id of the master
    replica_of = resource.Body('replica_of')
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
    #: Links
    #: *Type:list*
    links = resource.Body('links', type=list)
    #: Fault, only validate if fault
    #: *Type:dict*
    fault = resource.Body('fault', type=dict)
    #: Configuration
    #: *Type:dict*
    configuration = resource.Body('configuration', type=dict)
    #: Replicas
    #: *Type:dict*
    replicas = resource.Body('replicas', type=dict)
    #: DB user
    dbuser = resource.Body('dbuser')
    #: Storage Engine
    storeEngine = resource.Body('storeEngine')
    #: Pay model
    payModel = resource.Body('payModel')
    #: Cluster ID
    cluster_id = resource.Body('cluster_id')
    #: Slave of instance
    slave_of = resource.Body('slave_of')
    #: Replica of the instance
    replica_count = resource.Body('replica_count')

    # Indicates the EIP for public access, including
    # the IP address and port number.
    # *Type:string*
    publicEndpoint = resource.Body('publicEndpoint')

    # def _action(self, session, body):
    #     """Perform instance action"""
    #     url = utils.urljoin(self.base_path, self._get_id(self), 'action')
    #     endpoint_override = self.service.get_endpoint_override()
    #     resp = session.post(url, endpoint_filter=self.service,
    #                         endpoint_override=endpoint_override,
    #                         json=body,
    #                         headers={"Accept": "application/json",
    #                                  "Content-type": "application/json",
    #                                  "X-Language": "en-us"})
    #
    #     return resp.json()
    #
    # def resize(self, session, flavorRef):
    #     return self._action(session, {"resize": {"flavorRef": flavorRef}})
    #
    # def resize_volume(self, session, size):
    #     return self._action(session, {"resize": {"volume": {"size": size}}})
    #
    # def restart(self, session):
    #     return self._action(session, {"restart": {}})
    #
    # def restore(self, session, backupRef):
    #     return self._action(session, {"restore": {"backupRef": backupRef}})
