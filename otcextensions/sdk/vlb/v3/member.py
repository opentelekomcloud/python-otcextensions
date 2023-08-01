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


class Member(resource.Resource):
    resource_key = 'member'
    resources_key = 'members'
    base_path = '/elb/pools/%(pool_id)s/members'

    # capabilities
    allow_create = True
    allow_fetch = True
    allow_commit = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'address', 'admin_state_up', 'name',
        'id', 'ip_version', 'name', 'protocol_port',
        'operating_status', 'subnet_cidr_id', 'member_type',
        'weight', 'instance_id',
        is_admin_state_up='admin_state_up',
    )

    # Properties
    #: Specifies the ID of the backend server group.
    id = resource.URI('id')
    #: Specifies the IP address of the backend server.
    address = resource.Body('address')
    #: Specifies the time when a backend server was added.
    created_at = resource.Body('created_at')
    #: Specifies the IP version supported by the backend server.
    ip_version = resource.Body('ip_version')
    #: Specifies the ID of the instance associated with the backend server.
    instance_id = resource.Body('instance_id')
    #: Specifies the administrative status of the backend server.
    is_admin_state_up = resource.Body('admin_state_up', type=bool)
    #: Specifies the backend server name.
    name = resource.Body('name')
    #: Specifies the type of the backend server.
    member_type = resource.Body('member_type')
    #: Specifies the ID of the IPv4 or IPv6 subnet where the backend server
    # resides.
    subnet_id = resource.Body('subnet_cidr_id')
    #: Specifies the operating status of the backend server.
    operating_status = resource.Body('operating_status')
    #: Specifies the project ID.
    project_id = resource.Body('project_id')
    #: Specifies the port used by the backend server to receive requests.
    protocol_port = resource.Body('protocol_port', type=int)
    #: Specifies the health status of the backend server if listener_id is
    # specified.
    status = resource.Body('status', type=list, elements=dict)
    #: Specifies the weight of the backend server.
    weight = resource.Body('weight', type=int)
    #: Specifies the time when a backend server was updated.
    updated_at = resource.Body('updated_at')
