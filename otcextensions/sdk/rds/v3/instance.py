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
from openstack import exceptions
from openstack import resource
from openstack import utils


class Instance(resource.Resource):

    base_path = '/instances'
    resources_key = 'instances'

    # capabilities
    allow_create = True
    allow_delete = True
    allow_commit = True
    allow_list = True

    _query_mapping = resource.QueryParameters('id', 'name', 'type',
                                              'datastore_type', 'router_id',
                                              'subnet_id', 'limit', 'offset')

    #: Availability Zone.
    #: *Type:str*
    availability_zone = resource.Body('availability_zone')
    # TODO(not_gtema): extract backup strategy into separate type
    #: Backup Strategy.
    #: *Type: dict*
    backup_strategy = resource.Body('backup_strategy', type=dict)
    #: Specifies the billing information, which is pay-per-use.
    #: *Type: dict*
    charge_info = resource.Body('charge_info', type=dict)
    #: Parameter configuration ID.
    #: *Type:uuid*
    configuration_id = resource.Body('configuration_id')
    #: Instance created time.
    #: *Type:str*
    created_at = resource.Body('created')
    #: Data store information.
    #: *Type: dict*
    datastore = resource.Body('datastore', type=dict)
    #: Datastore type information (for querying).
    datastore_type = resource.Body('datastore_type')
    #: Disk Encryption Key Id.
    #: *Type:str*
    disk_encryption_id = resource.Body('disk_encryption_id')
    #: Flavor ID
    #: *Type:uuid*
    flavor_ref = resource.Body('flavor_ref')
    #: HighAvailability configuration parameters.
    #: *Type: dict*
    ha = resource.Body('ha', type=dict)
    #: Maintenance time window.
    #: *Type:str*
    maintenance_window = resource.Body('maintenance_window')
    #: Node information
    #:  Indicates the primary/standby DB instance information.
    #: *Type:list*
    nodes = resource.Body('nodes', type=list)
    #: Password of the default user.
    #: *Type:str*
    password = resource.Body('password')
    #: Database listen port number.
    #: *Type:int*
    port = resource.Body('port', type=int)
    #: Private IP address List.
    #: *Type:list*
    private_ips = resource.Body('private_ips', type=list)
    #: Public IP address List,
    #: *Type:list*
    public_ips = resource.Body('public_ips', type=list)
    #: Region where DB is deployed.
    #: *Type:str*
    region = resource.Body('region')
    #: list of associated DB instances.
    #: *Type:list*
    related_instances = resource.Body('related_instance', type=list)
    #: Specifies the DB instance ID, which is used to create a read replica.
    replica_of_id = resource.Body('replica_of_id')
    #: Specifies the restoration point for instance recovery.
    #: *Type: dict*
    restore_point = resource.Body('restore_point', type=dict)
    #: Recovery time period for instance.
    restore_time = resource.Body('restore_time', type=list)
    #: Neutron router ID.
    router_id = resource.Body('vpc_id')
    #: Security Group Id.
    security_group_id = resource.Body('security_group_id')
    #: Id of subnet.
    subnet_id = resource.Body('subnet_id')
    #: Instance status.
    status = resource.Body('status')
    #: Switch Strategy. The value can be reliability or availability,
    #: indicating the reliability first and availability first, respectively.
    #: *Type:str*
    switch_strategy = resource.Body('switch_strategy')
    #: Time Zone.
    #: *Type:str*
    time_zone = resource.Body('time_zone')
    #: Instance type Single/Ha/Replica.,
    #: *Type:str*
    type = resource.Body('type')
    # datastore: Instance updated time.
    #: *Type:str*
    updated_at = resource.Body('updated')
    #: Volume information
    #: *Type: dict*
    volume = resource.Body('volume', type=dict)

    def fetch_restore_times(self, session):
        """List possible restore times for the instance.
        """
        url = utils.urljoin(self.base_path, self.id, 'restore-time')
        response = session.get(url)
        self._translate_response(response)
        return self.restore_time

    def get_instance_configuration(self, session):
        pass

    def update_instance_configuration(self, session):
        pass

    def restore(self, session, source_instance,
                backup=None, restore_time=None):
        """Restore instance from the backup of PIR.
        """
        url = utils.urljoin(self.base_path, 'recovery')

        body = {
            'source': None,
            'target': {'instance_id': self.id}
        }

        if backup:
            body['source'] = {'type': 'backup', 'backup_id': backup.id}
        elif restore_time:
            body['source'] = {
                'type': 'timestamp',
                'restore_time': restore_time
            }
        if not source_instance:
            source_instance = self
        body['source']['instance_id'] = source_instance.id

        response = session.post(url, json=body)
        exceptions.raise_from_response(response)
        job_id = response.json().get('job_id')

        return job_id

#
# class InstanceConfiguration(sdk_resource.Resource):
#
#     base_path = '/instances/%(instance_id)s/configurations'
#
#     # capabilities
#     allow_get = True
#     allow_update = True
#
#     #: instaceId
#     instance_id = resource.URI('instance_id')
#
#     #: Indicates the parameter configuration
#     #:  defined by users based on the default parameter groups.
#     #:  *Type: list*
#     configuration_parameters = resource.Body('configuration_parameters')
#     #: Indicates the creation time in the following
#     #:  format: yyyy-MM-ddTHH:mm:ssZ.
#     #:  *Type: string*
#     created_at = resource.Body('created')
#     #: database version name.
#     #:  *Type: string*
#     datastore_version_name = resource.Body('datastore_version_name')
#     #: database name.
#     #:  *Type: string*
#     datastore_name = resource.Body('datastore_name')
#     #: Indicates the update time in the following
#     #:  format: yyyy-MM-ddTHH:mm:ssZ.
#     #:  *Type: string*
#     updated_at = resource.Body('updated')
#
#
#     def update(self, session, prepend_key=False):
#         """
#         Method is overriden, because PUT without ID should be used
#
#         :param session: The session to use for making this request.
#         :type session: :class:`~keystoneauth1.adapter.Adapter`
#         :param prepend_key: A boolean indicating whether the resource_key
#                             should be prepended in a resource creation
#                             request. Default to True.
#
#         :return: None.
#         :raises: :exc:`~openstack.exceptions.MethodNotSupported` if
#                  :data:`Resource.allow_create` is not set to ``True``.
#         """
#         return self.update_no_id(session, prepend_key)
#
