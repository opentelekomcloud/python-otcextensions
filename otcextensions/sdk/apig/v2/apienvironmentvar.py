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


class ApiEnvironmentVar(resource.Resource):
    base_path = f'/apigw/instances/%(gateway_id)s/env-variables'

    allow_list = True
    allow_fetch = True
    allow_create = True
    allow_commit = True
    allow_delete = True

    resources_key = 'variables'

    _query_mapping = resource.QueryParameters(
        'limit', 'offset', 'group_id',
        'env_id', 'variable_name', 'precise_search'
    )

    gateway_id = resource.URI('gateway_id')

    # The variable value can contain 1 to 255 characters.
    # Only letters, digits, and special characters (_-/.:) are allowed.
    variable_value = resource.Body('variable_value')
    # Environment ID.
    env_id = resource.Body('env_id')
    # API group ID.
    group_id = resource.Body('group_id')
    # Variable name, which can contain 3 to 32 characters,
    # starting with a letter.
    # Only letters, digits, hyphens (-), and underscores (_) are allowed.
    variable_name = resource.Body('variable_name')
    # Environment variable ID.
    id = resource.Body('id')
