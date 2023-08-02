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


class L7Policy(resource.Resource):
    resource_key = 'l7policy'
    resources_key = 'l7policies'
    base_path = '/elb/l7policies'

    # capabilities
    allow_create = True
    allow_fetch = True
    allow_commit = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'action', 'admin_state_up', 'description',
        'display_all_rules', 'id', 'listener_id',
        'name', 'position', 'provisioning_status',
        'priority', 'redirect_url', 'redirect_pool_id',
        'redirect_listener_id',
        is_admin_state_up='admin_state_up',
    )

    # Properties
    #: Specifies where requests will be forwarded.
    action = resource.Body('action')
    #: Specifies the time when the forwarding policy was added.
    created_at = resource.Body('created_at')
    #: Provides supplementary information about the forwarding policy.
    description = resource.Body('description')
    #: Specifies the administrative status of the forwarding policy.
    is_admin_state_up = resource.Body('admin_state_up', type=bool)
    #: Specifies the ID of the listener to which the forwarding policy is
    #: added.
    listener_id = resource.Body('listener_id')
    #: Specifies the forwarding policy name.
    name = resource.Body('name')
    #: Specifies the forwarding policy priority.
    priority = resource.Body('priority', type=int)
    #: Specifies the ID of the project where the forwarding policy is used.
    project_id = resource.Body('project_id')
    #: Specifies the provisioning status of the forwarding policy.
    provisioning_status = resource.Body('provisioning_status')
    #: Specifies the ID of the backend server group that requests are
    #: forwarded to.
    redirect_pool_id = resource.Body('redirect_pool_id')
    #: Specifies the forwarding policy priority.
    position = resource.Body('position', type=int)
    # #: Specifies the configuration of the backend server group that
    # # the requests are forwarded to.
    # redirect_pools_config = resource.Body('redirect_pools_config', tyr=list,
    #                                       elements=dict)
    #: Specifies the ID of the listener to which requests are redirected.
    redirect_listener_id = resource.Body('redirect_listener_id')
    #: Specifies the URL to which requests are forwarded.
    redirect_url = resource.Body('redirect_url')
    #: Lists the forwarding rules in the forwarding policy.
    rules = resource.Body('rules', type=list)
    #: Specifies the URL to which requests are forwarded.
    redirect_url_config = resource.Body('redirect_url_config', type=dict)
    #: Specifies the configuration of the page that will be returned.
    fixed_response_config = resource.Body('fixed_response_config', type=dict)
    #: Specifies the time when the forwarding policy was updated.
    updated_at = resource.Body('updated_at')
