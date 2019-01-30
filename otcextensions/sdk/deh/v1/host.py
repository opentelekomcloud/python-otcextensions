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


class HostInstanceCapacity(resource.Resource):
    #: Specifies flavor ID
    flavor = resource.Body('flavor')


class HostProperties(resource.Resource):
    #: Specifies the VM flavors placed on the DeH
    available_instance_capacities = \
        resource.Body('available_instance_capacities',
                      type=list,
                      list_type=HostInstanceCapacity)
    #: Specifies the number of host physical cores
    cores = resource.Body('cores', type=int)
    #: Specifes the DeH type
    host_type = resource.Body('host_type')
    #: Specifes the DeH name of type
    host_type_name = resource.Body('host_type_name')
    #: Specifies the size of host physical memory (MB)
    memory = resource.Body('memory', type=int)
    #: Specifies the number of host physical sockets
    sockets = resource.Body('sockets', type=int)
    #: Specifies the number of host vCPUs
    vcpus = resource.Body('vcpus', type=int)


class Host(sdk_resource.Resource):
    resource_key = 'dedicated_host'
    resources_key = 'dedicated_hosts'
    base_path = '/dedicated-hosts'

    # capabilities
    allow_create = True
    allow_list = True
    allow_get = True
    allow_delete = True
    allow_update = True

    _query_mapping = resource.QueryParameters(
        'id', 'name', 'host_type', 'host_type_name',
        'flavor', 'state', 'tenant', 'availability_zone',
        'changes_since',
        changes_since='changes-since')

    #: Properties
    #: Specifies DeH ID
    id = resource.Body('dedicated_host_id', alternate_id=True)
    #: Time at which the DeH has been allocated
    allocated_at = resource.Body('allocated_at')
    #: Specifies whether to allow a VM to be placed on this available
    #: host if its DeH ID is not specified during its creation
    #: value: ['on', 'off']
    auto_placement = resource.Body('auto_placement')
    #: Specifies the number of available vCPUs for the DeH
    available_vcpus = resource.Body('available_vcpus', type=int)
    #: Specifies the number of available memory for the DeH
    available_memory = resource.Body('available_memory', type=int)
    #: Specifies the AZ to which the DeH belongs
    availability_zone = resource.Body('availability_zone')
    #: list of created DeH hosts (during create)
    dedicated_host_ids = resource.Body('dedicated_host_ids', type=list)
    #: Specifies the property of host
    host_properties = resource.Body('host_properties', type=HostProperties)
    #: Specifies the DeH type (for creation)
    host_type = resource.Body('host_type')
    #: Specifies the number of the placed VMs
    instance_total = resource.Body('instance_total', type=int)
    #: Specifies the VMs started on the DeH.
    #: The "Querying DeHs" intercace does not display this parameter.
    instance_uuids = resource.Body('instance_uuids', type=list)
    #: Specifies the tenant who owns the DeH
    project_id = resource.Body('project_id')
    #: Specifies the number of allocated DeHs (during creation).
    quantity = resource.Body('quantity', type=int)
    #: Time at which the DeH has been released
    released_at = resource.Body('released_at')
    #: Specifies the DeH status.
    #: The value can be available, fault or released
    state = resource.Body('state')
