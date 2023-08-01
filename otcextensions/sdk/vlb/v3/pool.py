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


class Pool(resource.Resource):
    resource_key = 'pool'
    resources_key = 'pools'
    base_path = '/elb/pools'

    # capabilities
    allow_create = True
    allow_fetch = True
    allow_commit = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'admin_state_up', 'description', 'healthmonitor_id',
        'id', 'name', 'loadbalancer_id', 'protocol',
        'lb_algorithm', 'enterprise_project_id',
        'ip_version', 'member_address', 'member_device_id',
        is_admin_state_up='admin_state_up'
    )

    # Properties
    #: Description.
    description = resource.Body('description')
    #: Specifies the time when a backend server group was created.
    created_at = resource.Body('created_at')
    #: Specifies the ID of the health check configured
    #: for the backend server group.
    healthmonitor_id = resource.Body('healthmonitor_id')
    #: Specifies the administrative status of the backend server group.
    is_admin_state_up = resource.Body('admin_state_up', type=bool)
    #: Specifies the IP version supported by the backend server group.
    ip_version = resource.Body('ip_version')
    #: Specifies the load balancing algorithm used by the load balancer
    #: to route requests to backend servers.
    lb_algorithm = resource.Body('lb_algorithm')
    #: Specifies the ID of the listener associated with the
    #: backend server group.
    listener_id = resource.Body('listener_id')
    #: Lists the listeners associated with the backend server group.
    listeners = resource.Body('listeners', type=list, elements=dict)
    #: Specifies the ID of the associated load balancer.
    loadbalancer_id = resource.Body('loadbalancer_id')
    #: Lists the IDs of load balancers associated with the
    #: backend server group.
    loadbalancers = resource.Body('loadbalancers', type=list, elements=dict)
    #: Lists the backend servers in the backend server group.
    members = resource.Body('members', type=list, elements=dict)
    #: Specifies whether to enable removal protection.
    member_deletion_protection_enable = resource.Body(
        'member_deletion_protection_enable', type=bool)
    #: Specifies the backend server group name.
    name = resource.Body('name')
    #: Specifies the project ID.
    project_id = resource.Body('project_id')
    #: Specifies the protocol used by the backend server group
    #: to receive requests. TCP, UDP, and HTTP are supported.
    protocol = resource.Body('protocol')
    #: Specifies whether to enable sticky sessions.
    session_persistence = resource.Body('session_persistence', type=dict)
    #: Specifies whether to enable slow start.
    slow_start = resource.Body('slow_start', type=dict)
    #: Specifies the time when when a backend server group was updated.
    updated_at = resource.Body('updated_at')
    #: Specifies the ID of the VPC where the backend server group works.
    vpc_id = resource.Body('vpc_id')
    #: Specifies the type of the backend server group.
    type = resource.Body('type')
