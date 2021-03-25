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

    resources_key = 'instances'

    base_path = '/instances'

    # capabilities
    allow_create = True
    allow_list = True
    allow_delete = True
    allow_fetch = True
    allow_commit = True

    _query_mapping = resource.QueryParameters(
        'limit', 'start', 'name', 'status',
        'includeFailure', 'exactMatchName')

    # Properties
    #: AZ where a cache node resides.
    #: The value of this parameter in the response contains an AZ ID.
    available_zones = resource.Body('available_zones', type=list)
    #: Backup policy.
    backup_policy = resource.Body('instance_backup_policy', type=dict)
    #:  Cache capacity in GB
    #: *Type: int*
    capacity = resource.Body('capacity', type=int)
    #: Billing mode.
    #: 0 indicates that users only pay for what they use.
    charging_mode = resource.Body('charging_mode')
    #: Time at which the DCS instance is created.
    #: For example, 2017-03-31T12:24:46.297Z.
    created_at = resource.Body('created_at')
    #: Instance description
    description = resource.Body('description')
    #: Domain name.
    domain_name = resource.Body('domainName')
    #: Instance engine
    engine = resource.Body('engine')
    #: Cache engine version.
    engine_version = resource.Body('engine_version')
    #: Error code returned when the DCS instance fails to be created
    #: or is in abnormal status.
    error_code = resource.Body('error_code')
    #: Instance Id
    id = resource.Body('instance_id', alternate_id=True)
    #: Internal DCS version.
    internal_version = resource.Body('internal_version')
    #: Cache node's IP address in tenant's VPC.
    ip = resource.Body('ip')
    #: Account lockout duration.
    lock_time = resource.Body('lock_time')
    #: Remaining time before the account is unlocked.
    lock_time_left = resource.Body('lock_time_left')
    #: Time at which the maintenance time window starts.
    #: Format: HH:mm:ss.
    maintain_begin = resource.Body('maintain_begin')
    #: Time at which the maintenance time window ends.
    #: Format: HH:mm:ss.
    maintain_end = resource.Body('maintain_end')
    #: Overall memory size.
    #: Unit: MB.
    max_memory = resource.Body('max_memory', type=int)
    #: Return message of the operation on the instance
    message = resource.Body('message')
    #: Instance name
    name = resource.Body('name')
    #: Order ID.
    #: An order ID is generated only in the monthly or yearly
    #: billing mode. In other billing modes, no value is returned
    #: for this parameter.
    order_id = resource.Body('order_id')
    #: Password.
    password = resource.Body('password')
    #: Port of the cache node.
    port = resource.Body('port')
    #: Product ID used to differentiate DCS instance types.
    #: * OTC_DCS_SINGLE: indicates a single-node DCS instance.
    #: * OTC_DCS_MS: indicates a master/standby DCS instance.
    #: * OTC_DCS_CL: indicates a DCS instance in cluster mode.
    product_id = resource.Body('product_id')
    #: Result of the operation on the instance
    result = resource.Body('result')
    #: Count of the change password retries
    #: *Type: str*
    retry_times_left = resource.Body('retry_times_left')
    security_group_id = resource.Body('security_group_id')
    security_group_name = resource.Body('security_group_name')
    #: Cache instance status. Instance Statuses.
    status = resource.Body('status')
    subnet_id = resource.Body('subnet_id')
    subnet_name = resource.Body('subnet_name')
    subnet_cidr = resource.Body('subnet_cidr')
    #: Resource specifications.
    #: * dcs.single_node: indicates a DCS instance in single-node mode.
    #: * dcs.master_standby: indicates a DCS instance in master/standby mode.
    #: * dcs.cluster: indicates a DCS instance in cluster mode.
    resource_spec_code = resource.Body('resource_spec_code')
    #: Size of the used memory.
    #: Unit: MB.
    used_memory = resource.Body('used_memory', type=int)
    user_id = resource.Body('user_id')
    user_name = resource.Body('user_name')
    vpc_id = resource.Body('vpc_id')
    vpc_name = resource.Body('vpc_name')

    '''
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
        # Try to short-circuit by looking directly for a matching ID.
        try:
            match = cls.existing(
                id=name_or_id,
                connection=session._get_connection(),
                **params)
            return match.fetch(session, **params)

        # Ecosystems:
        # Add additional Exceptions to avoid abort of find method
        except (exceptions.NotFoundException, exceptions.HttpException,
                exceptions.MethodNotSupported, exceptions.BadRequestException):
            session.log.warn('Please specify instance ID if known for '
                             'better performance')

        if ('name' in cls._query_mapping._mapping.keys()
                and 'name' not in params):
            params['name'] = name_or_id

        data = cls.list(session, **params)

        result = cls._get_one_match(name_or_id, data)
        if result is not None:
            return result

        if ignore_missing:
            return None
        raise exceptions.ResourceNotFound(
            "No %s found for %s" % (cls.__name__, name_or_id))
    '''

    def change_pwd(self, session, current_password, new_password):
        """Schange instance password
        """
        body = {
            'old_password': current_password,
            'new_password': new_password
        }
        url = utils.urljoin(self.base_path, self.id, 'password')
        response = session.put(
            url,
            json=body)
        return self._translate_response(response, False)

    def extend(self, session, capacity):
        """Extend instance capacity
        """
        body = {'new_capacity': capacity}
        url = utils.urljoin(self.base_path, self.id, 'extend')
        response = session.post(
            url,
            json=body)
        return self._translate_response(response, False)

    def stop(self, session):
        """Stop instance
        """
        return self._status_action(session, 'stop')

    def start(self, session):
        """Start instance
        """
        return self._status_action(session, 'start')

    def restart(self, session):
        """Retart instance
        """
        return self._status_action(session, 'restart')

    def _status_action(self, session, action):
        '''perform status action on instance'''
        body = {'action': action, 'instances': [self.id]}
        url = utils.urljoin(self.base_path, 'status')
        response = session.put(
            url,
            json=body)
        return self._translate_response(response, False)
