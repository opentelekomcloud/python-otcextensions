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


class L7Rule(resource.Resource):
    resource_key = 'rule'
    resources_key = 'rules'
    base_path = '/elb/l7policies/%(l7policy_id)s/rules'

    # capabilities
    allow_create = True
    allow_fetch = True
    allow_commit = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'admin_state_up', 'compare_type', 'id',
        'invert', 'key', 'provisioning_status',
        'type', 'value', is_admin_state_up='admin_state_up'
    )

    # Properties
    #: Specifies the forwarding policy ID.
    l7policy_id = resource.URI('l7policy_id')

    #: Specifies how requests are matched and forwarded.
    compare_type = resource.Body('compare_type')
    #: Specifies the matching conditions of the forwarding rule.
    conditions = resource.Body('conditions', type=list)
    #: Specifies whether reverse matching is supported.
    invert = resource.Body('invert', type=bool)
    #: Specifies the administrative status of the forwarding rule.
    is_admin_state_up = resource.Body('admin_state_up', type=bool)
    #: Specifies the key of the match item.
    key = resource.Body('key')
    #: Specifies the project ID.
    project_id = resource.Body('project_id')
    #: Specifies the provisioning status of the forwarding rule.
    provisioning_status = resource.Body('provisioning_status')
    #: Specifies the match content.
    type = resource.Body('type')
    #: Specifies the value of the match item.
    value = resource.Body('value')
