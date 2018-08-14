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
from openstack import _log

from otcextensions.sdk import sdk_resource

_logger = _log.setup_logging('openstack')


class Instance(sdk_resource.Resource):

    resources_key = 'instances'

    base_path = '/instances'

    # capabilities
    allow_create = True
    allow_list = True
    allow_get = True
    allow_delete = True
    allow_update = True
    allow_fetch = True
    allow_commit = True

    _query_mapping = resource.QueryParameters(
        'limit', 'start', 'name', 'status',
        'includeFailure', 'exactMatchName')

    # Properties
    #: Instance Id
    id = resource.Body('instance_id', alternate_id=True)
    #: Instance name
    name = resource.Body('name')
    #: Instance description
    description = resource.Body('description')
    #: Instance engine
    engine = resource.Body('engine')

    #:  Cache capacity in GB
    #: *Type: int*
    capacity = resource.Body('capacity', type=int)

    #: Cache node's IP address in tenant's VPC.
    ip = resource.Body('ip')

    #: Domain name.
    domain_name = resource.Body('domainName')

    #: Port of the cache node.
    port = resource.Body('port')

    #: Cache instance status. Instance Statuses.
    status = resource.Body('status')

    #: Overall memory size.
    #: Unit: MB.
    max_memory = resource.Body('max_memory', type=int)

    #: Size of the used memory.
    #: Unit: MB.
    used_memory = resource.Body('used_memory', type=int)

    #: Resource specifications.
    #: * dcs.single_node: indicates a DCS instance in single-node mode.
    #: * dcs.master_standby: indicates a DCS instance in master/standby mode.
    #: * dcs.cluster: indicates a DCS instance in cluster mode.
    resource_spec_code = resource.Body('resource_spec_code')

    #: Cache engine version.
    engine_version = resource.Body('engine_version')

    #: Internal DCS version.
    internal_version = resource.Body('internal_version')

    #: Billing mode.
    #: 0 indicates that users only pay for what they use.
    charging_mode = resource.Body('charging_mode')
    security_group_id = resource.Body('security_group_id')
    security_group_name = resource.Body('security_group_name')
    subnet_id = resource.Body('subnet_id')
    subnet_name = resource.Body('subnet_name')
    subnet_cidr = resource.Body('subnet_cidr')
    vpc_id = resource.Body('vpc_id')
    vpc_name = resource.Body('vpc_name')

    #: Time at which the DCS instance is created.
    #: For example, 2017-03-31T12:24:46.297Z.
    created_at = resource.Body('created_at')

    #: Error code returned when the DCS instance fails to be created
    #: or is in abnormal status.
    error_code = resource.Body('error_code')

    user_id = resource.Body('user_id')
    user_name = resource.Body('user_name')

    #: Order ID.
    #: An order ID is generated only in the monthly or yearly
    #: billing mode. In other billing modes, no value is returned
    #: for this parameter.
    order_id = resource.Body('order_id')

    #: Time at which the maintenance time window starts.
    #: Format: HH:mm:ss.
    maintain_begin = resource.Body('maintain_begin')

    #: Time at which the maintenance time window ends.
    #: Format: HH:mm:ss.
    maintain_end = resource.Body('maintain_end')

    #: Product ID used to differentiate DCS instance types.
    #: * OTC_DCS_SINGLE: indicates a single-node DCS instance.
    #: * OTC_DCS_MS: indicates a master/standby DCS instance.
    #: * OTC_DCS_CL: indicates a DCS instance in cluster mode.
    product_id = resource.Body('product_id')

    #: AZ where a cache node resides.
    #: The value of this parameter in the response contains an AZ ID.
    available_zones = resource.Body('available_zones')

    #: Backup policy.
    backup_policy = resource.Body('instance_backup_policy', type=dict)

    @classmethod
    def find(cls, session, name_or_id, ignore_missing=True, **params):
        try:
            match = cls.existing(
                id=name_or_id,
                **params)
            return match.get(session)
        except (exceptions.NotFoundException, exceptions.HttpException,
                exceptions.MethodNotSupported, exceptions.BadRequestException):
            _logger.warn('Please specify instance ID if known for '
                         'better performance')

        data = cls.list(session, **params)

        result = cls._get_one_match(name_or_id, data)
        # Update result with URL parameters
        if result is not None:
            result._update(**params)
            return result

        if ignore_missing:
            return None
        raise exceptions.ResourceNotFound(
            "No %s found for %s" % (cls.__name__, name_or_id))

    def extend(self, session, capacity):
        '''extend instance capacity'''
        body = {'new_capacity': capacity}
        url = utils.urljoin(self.base_path, self.id, 'extend')
        response = session.post(
            url,
            json=body)
        return self._translate_response(response, False)
