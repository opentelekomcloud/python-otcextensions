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


class FlavorSpec(resource.Resource):
    #: Specifies node quantity.
    #: *Type:int*
    num = resource.Body('num', type=int)
    #: Specifies the disk size.
    #: valid value: ``ULTRAHIGH``,
    #: *Type:int*
    size = resource.Body('size', type=int)
    #: Specifies the resource specification code.
    #: *Type:string*
    spec_code = resource.Body('spec_code')
    #: Specifies the disk type.
    #: Valid values:
    #: mongos: The value ranges from 2 to 16.
    #: shard: The value ranges from 2 to 16.
    #: config: The value is 1.
    #: replica: The value is 1.
    #: *Type:string*
    storage = resource.Body('storage')
    #: Specifies the node type.
    #: * mongos
    #: * shard
    #: * config
    #: * replica
    #: *Type:string*
    type = resource.Body('type')


class BackupStrategySpec(resource.Resource):
    #: Specifies the number of days to retain the generated backup files.
    #: valid value range is from 0 to 732.
    #: *Type:string*
    keep_days = resource.Body('keep_days')
    #: Specifies the backup time window.
    #: valid value must be in the "hh:mm-HH:MM" format.
    #: Example value: 08:15-09:15
    #: *Type:string*
    start_time = resource.Body('start_time')


class VolumeSpec(resource.Resource):
    #: Disk size.
    #: *Type:string*
    size = resource.Body('size')
    #: Disk usage.
    #: *Type:string*
    used = resource.Body('used')


class NodeSpec(resource.Resource):
    #: The AZ.
    #: *Type:string*
    availability_zone = resource.Body('availability_zone')
    #: Node ID.
    #: *Type:string*
    id = resource.Body('id')
    #: Node name.
    #: *Type:string*
    name = resource.Body('name')
    #: Private IP address of a node.
    #: *Type:string*
    private_ip = resource.Body('private_ip')
    #: The EIP that has been bound.
    #: *Type:string*
    public_ip = resource.Body('public_ip')
    #: Node role.
    #: *Type:string*
    role = resource.Body('role')
    #: Resource specifications code.
    #: *Type:string*
    spec_code = resource.Body('spec_code')
    #: Node status.
    #: *Type:string*
    status = resource.Body('status')


class GroupSpec(resource.Resource):
    #: Group ID.
    #: *Type:string*
    id = resource.Body('id')
    #: Group name.
    #: *Type:string*
    name = resource.Body('name')
    #: Node information.
    #: *Type:list*
    nodes = resource.Body('nodes', type=list, list_type=NodeSpec)
    #: Group status.
    #: *Type:string*
    status = resource.Body('status')
    #: Node type.
    #: *Type:string*
    type = resource.Body('type')
    #: Volume information.
    #: *Type:dict*
    volume = resource.Body('volume', type=VolumeSpec)


class DatastoreSpec(resource.Resource):
    #: Specifies the storage engine.
    #: *Type:string*
    storage_engine = resource.Body('storage_engine')
    #: Specifies the database type.
    #: The value is ``DDS-Community``.
    #: *Type:string*
    type = resource.Body('type')
    #: Specifies the database version.
    #: valid value is 3.2 or 3.4.
    #: *Type:string*
    version = resource.Body('version')


class Instance(resource.Resource):
    base_path = '/instances'

    resources_key = 'instances'
    resource_key = 'instance'

    # capabilities
    allow_create = True
    allow_delete = True
    allow_commit = True
    allow_list = True
    allow_fetch = True

    _query_mapping = resource.QueryParameters(
        'id', 'name', 'mode', 'datastore_type',
        'vpc_id', 'subnet_id', 'limit', 'offset')

    #: Operations that is executed on the DB instance.
    #: *Type:string*
    actions = resource.Body('actions', type=list)
    #: Specifies the AZ ID.
    #: *Type:string*
    availability_zone = resource.Body('availability_zone')
    #: Specifies the advanced backup policy.
    #: *Type:dict*
    backup_strategy = resource.Body('backup_strategy', type=BackupStrategySpec)
    #: Time when a DB instance is created.
    #: *Type:string*
    created = resource.Body('created')
    #: Specifies the database information.
    #: *Type:dict*
    datastore = resource.Body('datastore', type=DatastoreSpec)
    #: Specifies the database type.
    #: *Type:string*
    datastore_type = resource.Body('datastore_type')
    #: Specifies the key ID used for disk encryption.
    #: *Type:string*
    disk_encryption_id = resource.Body('disk_encryption_id')
    #: Specifies the storage engine.
    #: *Type:string*
    engine = resource.Body('engine')
    #: Specifies the instance specifications.
    #: *Type:list*
    flavor = resource.Body('flavor', type=list, list_type=FlavorSpec)
    #: Group information
    #: *Type:dict*
    groups = resource.Body('groups', type=list, list_type=GroupSpec)
    #: DB instance ID.
    #: *Type:string*
    id = resource.Body('id')
    #: Async job id
    #: *Type:uuid*
    job_id = resource.Body('job_id')
    #: Maintenance time window.
    #: *Type:string*
    maintenance_window = resource.Body('maintenance_window')
    #: Specifies the instance type.
    #: * Sharding indicates the cluster instance.
    #: * ReplicaSet indicate the replica set instance.
    #: *Type:string*
    mode = resource.Body('mode')
    #: DB instance name.
    #: *Type:string*
    name = resource.Body('name')
    #: Specifies the database password.
    #: *Type:string*
    password = resource.Body('password')
    #: Billing mode.
    #: *Type:string*
    pay_mode = resource.Body('pay_mode')
    #: Database port number.
    #: *Type:int*
    port = resource.Body('port')
    #: Specifies the region ID.
    #: *Type:string*
    region = resource.Body('region')
    #: Specifies the ID of the security group
    #: where a specified DB instance belongs to.
    #: *Type:string*
    security_group_id = resource.Body('security_group_id')
    #: Instance status.
    #: *Type:string*
    status = resource.Body('status')
    #: Specifies whether to enable SSL.
    #: *Type:string*
    ssl = resource.Body('ssl')
    #: Data store information.
    #: *Type:string*
    subnet_id = resource.Body('subnet_id')
    #: Time zone.
    #: *Type:string*
    time_zone = resource.Body('time_zone')
    #: Specifies the VPC ID.
    #: *Type:string*
    vpc_id = resource.Body('vpc_id')
    #: Time when a DB instance is updated.
    #: *Type:string*
    updated = resource.Body('updated')

    def fetch(self, session, requires_id=True,
              base_path=None, error_message=None, **params):
        """Get a remote resource based on this instance.
        :param session: The session to use for making this request.
            :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param boolean requires_id: A boolean indicating whether resource ID
            should be part of the requested URI.
        :param str base_path: Base part of the URI for fetching resources, if
            different from :data:`~openstack.resource.Resource.base_path`.
        :param str error_message: An Error message to be returned if
            requested object does not exist.
        :param dict params: Additional parameters that can be consumed.

        :return: This :class:`Resource` instance.
        :raises: :exc:`~openstack.exceptions.MethodNotSupported` if
            :data:`Resource.allow_fetch` is not set to ``True``.
        :raises: :exc:`~openstack.exceptions.ResourceNotFound` if
            the resource was not found.
        """
        data = self.list(session, paginated=False, id=self.id)
        result = self._get_one_match(self.id, data)
        if not result:
            raise exceptions.ResourceNotFound(
                "No Instance found for %s" % (self.id))

        self._body.attributes.update(result._body.attributes)
        self._body.clean()
        return self

    def create(self, session, prepend_key=False, base_path=None):
        return super(Instance, self).create(
            session,
            prepend_key=prepend_key,
            base_path=base_path)

    def restart(self, session):
        '''Restart Instance'''
        body = {
            "target_type": self.datastore_type,
            "target_id": self.id
        }
        response = self._action(session, body, 'restart')
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self

    def enlarge(self, session, size, group_id):
        '''Enlarge Instance Storage Space'''
        body = {
            "volume":
                {
                    "size": size
                }
        }
        if group_id is not None:
            body["volume"]["group_id"] = group_id
        response = self._action(session, body, 'enlarge-volume')
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self

    def add_nodes(self, session, node_type, spec_code, num, volume=None):
        '''Add Nodes to Instance'''
        body = {
            "type": node_type,
            "spec_code": spec_code,
            "num": num
        }
        if volume is not None:
            body['volume'] = volume
        response = self._action(session, body, 'enlarge')
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self

    def resize(self, session, target_id, spec_code, target_type=None):
        body = {
            "resize": {
                "target_id": target_id,
                "target_spec_code": spec_code
            }
        }
        if target_type is not None:
            body['resize']['target_type'] = target_type
        response = self._action(session, body, 'resize')
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self

    def switchover(self, session):
        response = self._action(session, {}, 'switchover')
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self

    def switch_ssl(self, session, enable):
        body = {'ssl_option': "1" if enable else "0"}
        response = self._action(session, body, 'switch-ssl')
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self

    def modify_name(self, session, name):
        body = {
            "new_instance_name": name
        }
        response = self._action(session, body, 'modify-name', 'PUT')
        exceptions.raise_from_response(response)

    def change_port(self, session, port):
        body = {
            "port": port
        }
        response = self._action(session, body, 'modify-port')
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self

    def change_security_group(self, session, security_group_id):
        body = {
            "security_group_id": security_group_id
        }
        response = self._action(session, body, 'modify-security-group')
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self

    def change_private_ip(self, session, node_id, new_ip):
        body = {
            "node_id": node_id,
            "new_ip": new_ip
        }
        response = self._action(session, body, 'modify-internal-ip')
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self

    def create_ip(self, session, dds_type, password):
        body = {
            "type": dds_type,
            "password": password
        }
        response = self._action(session, body, 'create-ip')
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self

    def configure_client_network(self, session, network_ranges):
        body = {
            "client_network_ranges": network_ranges
        }
        response = self._action(session, body, 'client-network')
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self

    def set_recycle_bin_policy(self, session, *attrs):
        body = {
            "recycle_policy": attrs
        }
        response = self._action(session, body, 'recycle-policy')
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self

    def _action(self, session, body, action_type, api_type='POST'):
        """Preform actions given the message body.
        """
        url = utils.urljoin(self.base_path, self.id, action_type)
        if api_type == 'POST':
            return session.post(
                url,
                json=body)
        if api_type == 'PUT':
            return session.put(url, json=body)
