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
        'address', 'admin_state_up', 'enterprise_project_id',
        'id', 'ip_version', 'name', 'protocol_port',
        'operating_status', 'subnet_cidr_id', 'weight',
        is_admin_state_up='admin_state_up'
    )

    # Properties
    #: Specifies the ID of the backend server group.
    pool_id = resource.URI('pool_id')

    #: Specifies the IP address of the backend server.
    address = resource.Body('address')
    #: Address parameter
    ip_version = resource.Body('ip_version')
    #: Specifies the administrative status of the backend server.
    is_admin_state_up = resource.Body('admin_state_up', type=bool)
    #: Specifies the operating status of the backend server.
    operating_status = resource.Body('operating_status')
    #: Specifies the project ID.
    project_id = resource.Body('project_id')
    #: Specifies the port used by the backend server to receive requests.
    protocol_port = resource.Body('protocol_port', type=int)
    #: Specifies the ID of the subnet where the backend server works.
    subnet_cidr_id = resource.Body('subnet_cidr_id')
    #: Specifies the weight of the backend server.
    weight = resource.Body('weight', type=int)
