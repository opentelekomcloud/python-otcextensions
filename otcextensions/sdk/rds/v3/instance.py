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

from otcextensions.sdk.rds.v3 import _base


class Instance(_base.Resource):

    base_path = '/instances'
    resources_key = 'instances'

    # capabilities
    allow_create = True
    allow_delete = True
    allow_commit = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'id', 'name', 'type', 'datastore_type', 'router_id',
        'subnet_id', 'limit', 'offset',
        router_id='vpc_id')

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
    #: Async job id
    job_id = resource.Body('job_id')
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
    #: Default user of the DB
    user_name = resource.Body('db_user_name')
    #: Volume information
    #: *Type: dict*
    volume = resource.Body('volume', type=dict)

    def _translate_response(self, response, has_body=None, error_message=None):
        """Given a KSA response, inflate this instance with its data

        DELETE operations don't return a body, so only try to work
        with a body when has_body is True.

        This method updates attributes that correspond to headers
        and body on this instance and clears the dirty set.
        """
        if has_body is None:
            has_body = self.has_body
        exceptions.raise_from_response(response, error_message=error_message)
        if has_body:
            try:
                body = response.json()
                # Need to merge job_id on the root with other data inside of
                # 'instance' container
                job_id = body.get('job_id')
                if 'instance' in body:
                    body = body['instance']
                    if job_id:
                        body['job_id'] = job_id

                body_attrs = self._consume_body_attrs(body)

                if self._store_unknown_attrs_as_properties:
                    body_attrs = self._pack_attrs_under_properties(
                        body_attrs, body)

                self._body.attributes.update(body_attrs)
                self._body.clean()
                if self.commit_jsonpatch or self.allow_patch:
                    # We need the original body to compare against
                    self._original_body = body_attrs.copy()
            except ValueError:
                # Server returned not parse-able response (202, 204, etc)
                # Do simply nothing
                pass

        headers = self._consume_header_attrs(response.headers)
        self._header.attributes.update(headers)
        self._header.clean()
        self._update_location()
        dict.update(self, self.to_dict())

    @classmethod
    def find(cls, session, name_or_id, ignore_missing=True, **params):
        """Find a resource by its name or id.

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param name_or_id: This resource's identifier, if needed by
                           the request. The default is ``None``.
        :param bool ignore_missing: When set to ``False``
                    :class:`~openstack.exceptions.ResourceNotFound` will be
                    raised when the resource does not exist.
                    When set to ``True``, None will be returned when
                    attempting to find a nonexistent resource.
        :param dict params: Any additional parameters to be passed into
                            underlying methods, such as to
                            :meth:`~openstack.resource.Resource.existing`
                            in order to pass on URI parameters.

        :return: The :class:`Resource` object matching the given name or id
                 or None if nothing matches.
        :raises: :class:`openstack.exceptions.DuplicateResource` if more
                 than one resource is found for this request.
        :raises: :class:`openstack.exceptions.ResourceNotFound` if nothing
                 is found and ignore_missing is ``False``.
        """
        session = cls._get_session(session)

        result = cls._find(session, name_or_id, id=name_or_id, **params)

        if not result:
            result = cls._find(session, name_or_id, name=name_or_id, **params)

        if result:
            return result

        if ignore_missing:
            return None
        raise exceptions.ResourceNotFound(
            "No %s found for %s" % (cls.__name__, name_or_id))

    @classmethod
    def _find(cls, session, name_or_id, **params):
        data = cls.list(session, **params)

        result = cls._get_one_match(name_or_id, data)
        if result is not None:
            return result

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
        data = self.list(session, paginated=False, id=self.id)
        result = self._get_one_match(self.id, data)
        if not result:
            raise exceptions.ResourceNotFound(
                "No Instance found for %s" % (self.id))

        self._body.attributes.update(result._body.attributes)
        self._body.clean()

        return self

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

    def restore(self, session, backup=None, restore_time=None):
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

        body['source']['instance_id'] = self.id

        response = session.post(url, json=body)
        exceptions.raise_from_response(response)
        job_id = response.json().get('job_id')

        return job_id

    def get_backup_policy(self, session):
        """Get instance backup policy
        """
        url = utils.urljoin(self.base_path, self.id, 'backups', 'policy')
        response = session.get(url)
        exceptions.raise_from_response(response)

        return response.json().get('backup_policy')

    def set_backup_policy(self, session, keep_days, start_time=None,
                          period=None):
        """Set instance backup policy
        """
        url = utils.urljoin(self.base_path, self.id, 'backups', 'policy')
        body = {
            'keep_days': keep_days
        }
        if start_time:
            body['start_time'] = start_time
        if period:
            body['period'] = period
            response = session.put(url, json={'backup_policy': body})
        exceptions.raise_from_response(response)

        return None
