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


class Version(resource.Resource):
    base_path = '/fgs/functions/%(function_urn)s/versions'
    resources_key = 'versions'
    # Capabilities
    allow_create = True
    allow_fetch = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'maxitems', 'marker'
    )

    # Properties
    function_urn = resource.URI('function_urn', type=str)
    digest = resource.Body('digest', type=str)
    version = resource.Body('version', type=str)
    description = resource.Body('description', type=str)

    # Attributes
    next_marker = resource.Body('next_marker', type=int)
    count = resource.Body('count', type=int)
    func_urn = resource.Body('func_urn', type=str)
    func_name = resource.Body('func_name', type=str)
    domain_id = resource.Body('domain_id', type=str)
    project_id = resource.Body('namespace', type=str)
    project_name = resource.Body('project_name', type=str)
    package = resource.Body('package', type=str)
    runtime = resource.Body('runtime', type=str)
    timeout = resource.Body('timeout', type=int)
    handler = resource.Body('handler', type=str)
    memory_size = resource.Body('memory_size', type=int)
    cpu = resource.Body('cpu', type=int)
    code_type = resource.Body('code_type', type=str)
    code_url = resource.Body('code_url', type=str)
    code_filename = resource.Body('code_filename', type=str)
    code_size = resource.Body('code_size', type=int)
    user_data = resource.Body('user_data', type=str)
    encrypted_user_data = resource.Body('encrypted_user_data', type=str)
    image_name = resource.Body('image_name', type=str)
    xrole = resource.Body('xrole', type=str)
    app_xrole = resource.Body('app_xrole', type=str)
    version_description = resource.Body('version_description', type=str)
    last_modified = resource.Body('last_modified', type=str)
    func_vpc = resource.Body('func_vpc', type=dict)
    mount_config = resource.Body('mount_config', type=dict)
    strategy_config = resource.Body('strategy_config', type=dict)
    dependencies = resource.Body('dependencies', type=dict)
    initializer_handler = resource.Body('initializer_handler', type=str)
    initializer_timeout = resource.Body('initializer_timeout', type=int)
    pre_stop_handler = resource.Body('pre_stop_handler', type=str)
    pre_stop_timeout = resource.Body('pre_stop_timeout', type=int)
    enterprise_project_id = resource.Body('enterprise_project_id', type=str)
    long_time = resource.Body('long_time', type=bool)
    log_group_id = resource.Body('log_group_id', type=str)
    log_stream_id = resource.Body('log_stream_id', type=str)
    type = resource.Body('type', type=str)
    enable_dynamic_memory = resource.Body('enable_dynamic_memory', type=bool)
    function_async_config = resource.Body('function_async_config', type=dict)
