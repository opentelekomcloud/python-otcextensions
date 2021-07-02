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
    #: Specifies the node type.
    #: * mongos
    #: * shard
    #: * config
    #: * replica
    #: *Type:string*
    type = resource.Body('type')
    #: Specifies node quantity.
    #: *Type:int*
    num = resource.Body('num', type=int)
    #: Specifies the disk type.
    #: Valid values:
    #: mongos: The value ranges from 2 to 16.
    #: shard: The value ranges from 2 to 16.
    #: config: The value is 1.
    #: replica: The value is 1.
    #: *Type:string*
    storage = resource.Body('storage')
    #: Specifies the disk size.
    #: valid value: ``ULTRAHIGH``,
    #: *Type:int*
    size = resource.Body('size', type=int)
    #: Specifies the resource specification code.
    #: *Type:string*
    spec_code = resource.Body('spec_code')


class BackupStrategySpec(resource.Resource):
    #: Specifies the backup time window.
    #: valid value must be in the "hh:mm-HH:MM" format.
    #: Example value: 08:15-09:15
    #: *Type:string*
    start_time = resource.Body('start_time')
    #: Specifies the number of days to retain the generated backup files.
    #: valid value range is from 0 to 732.
    #: *Type:string*
    keep_days = resource.Body('keep_days')


class DatastoreSpec(resource.Resource):
    #: Specifies the database type.
    #: The value is ``DDS-Community``.
    #: *Type:string*
    type = resource.Body('type')
    #: Specifies the database version.
    #: valid value is 3.2 or 3.4.
    #: *Type:string*
    version = resource.Body('version')
    #: Specifies the storage engine.
    #: valid value is wiredTiger.
    #: *Type:string*
    storage_engine = resource.Body('storage_engine')


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

    #: DB instance ID.
    #: *Type:string*
    id = resource.Body('id')
    #: DB instance name.
    #: *Type:string*
    name = resource.Body('name')
    #: Specifies the instance type.
    #: * Sharding indicates the cluster instance.
    #: * ReplicaSet indicate the replica set instance.
    #: *Type:string*
    mode = resource.Body('mode')
    #: Specifies the database type.
    #: *Type:string*
    datastore_type = resource.Body('datastore_type')
    #: Specifies the VPC ID.
    #: *Type:string*
    vpc_id = resource.Body('vpc_id')
    #: Data store information.
    #: *Type:string*
    subnet_id = resource.Body('subnet_id')
    #: Specifies the ID of the security group
    #: where a specified DB instance belongs to.
    #: *Type:string*
    security_group_id = resource.Body('security_group_id')
    #: Specifies the database information.
    #: *Type:dict*
    datastore = resource.Body('datastore', type=DatastoreSpec)
    #: Specifies the region ID.
    #: *Type:string*
    region = resource.Body('region')
    #: Specifies the AZ ID.
    #: *Type:string*
    availability_zone = resource.Body('availability_zone')
    #: Specifies the database password.
    #: *Type:string*
    password = resource.Body('password')
    #: Specifies the key ID used for disk encryption.
    #: *Type:string*
    disk_encryption_id = resource.Body('disk_encryption_id')
    #: Specifies the instance specifications.
    #: *Type:list*
    flavor = resource.Body('flavor', type=list, list_type=FlavorSpec)
    #: Specifies the advanced backup policy.
    #: *Type:dict*
    backup_strategy = resource.Body('backup_strategy', type=BackupStrategySpec)
    #: Specifies whether to enable SSL.
    #: *Type:string*
    ssl_option = resource.Body('ssl_option')

    def fetch(self, session, requires_id=True,
              base_path=None, error_message=None, **params):
        """Get a remote resource based on this instance.

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param boolean requires_id: A boolean indicating whether resource ID
                                    should be part of the requested URI.
        :param str base_path: Base part of the URI for fetching resources, if
                              different from
                              :data:`~openstack.resource.Resource.base_path`.
        :param str error_message: An Error message to be returned if
                                  requested object does not exist.
        :param dict params: Additional parameters that can be consumed.
        :return: This :class:`Resource` instance.
        :raises: :exc:`~openstack.exceptions.MethodNotSupported` if
                 :data:`Resource.allow_fetch` is not set to ``True``.
        :raises: :exc:`~openstack.exceptions.ResourceNotFound` if
                 the resource was not found.
        """
        if not self.allow_fetch:
            raise exceptions.MethodNotSupported(self, "fetch")

        params = {
            'id': self.id,
            'name': self.name,
            'mode': self.mode,
            'datastore_type': self.datastore_type,
            'vpc_id': self.vpc_id,
            'subnet_id': self.subnet_id,
        }
        query_params = self._query_mapping._transpose(params, self)
        url = utils.urljoin(self.base_path) % params

        session = self._get_session(session)
        microversion = self._get_microversion_for(session, 'fetch')
        response = session.get(
            url, microversion=microversion,
            headers={"Accept": "application/json"},
            params=query_params.copy())

        exceptions.raise_from_response(response)

        try:
            body = response.json()
            if self.resources_key in body:
                body = body[self.resources_key]

            if not len(body) == 1:
                raise exceptions.SDKException('Not a single result returned')

            body = body[0]
            body_attrs = self._consume_body_attrs(body)
            self._body.attributes.update(body_attrs)
            self._body.clean()

        except ValueError:
            # Server returned not parse-able response (202, 204, etc)
            # Do simply nothing
            pass

        dict.update(self, self.to_dict())

        return self

    def create(self, session, prepend_key=False, base_path=None):
        return super(Instance, self).create(
            session,
            prepend_key=prepend_key,
            base_path=base_path)
