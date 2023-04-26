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


class SecurityPolicy(resource.Resource):
    resource_key = 'security_policy'
    resources_key = 'security_policies'
    base_path = '/elb/security-policies'

    # capabilities
    allow_create = True
    allow_fetch = True
    allow_commit = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'project_id', 'id'
    )

    # Properties
    #: Specifies the security policy id.
    id = resource.Body('id', type=str)
    #: Specifies the security policy name.
    name = resource.Body('name', type=str)
    #: Lists the cipher suites supported by the custom security policy.
    ciphers = resource.Body('ciphers', type=list, list_type=str)
    #: Provides supplementary information about the security policy.
    description = resource.Body('description', type=str)
    #: Specifies the project ID of the custom security policy.
    project_id = resource.Body('project_id', type=str)
    #: Lists the TLS protocols supported by the custom security policy.
    protocols = resource.Body('protocols', type=list, list_type=str)
    #: The ID of the project this security policy is associated with.
    enterprise_project_id = resource.Body('enterprise_project_id', type=str)
    #: Specifies the listeners that use the custom security policies.
    listeners = resource.Body('listeners', type=list, list_type=dict)
    #: Specifies the time when the custom security policy was created.
    created_at = resource.Body('created_at', type=str)
    #: Specifies the time when the custom security policy was updated..
    updated_at = resource.Body('updated_at', type=str)
