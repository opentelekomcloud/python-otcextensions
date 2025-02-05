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


class Import(resource.Resource):
    base_path = '/fgs/functions/import'

    # Capabilities
    allow_create = True

    # Properties
    func_name = resource.URI('func_name', type=str)
    file_name = resource.Body('file_name', type=str)
    file_type = resource.Body('file_type', type=str)
    file_code = resource.Body('file_code', type=str)
    package = resource.Body('package', type=str)

    # Attributes
    func_urn = resource.Body('func_urn', type=str)
    domain_id = resource.Body('domain_id', type=str)
    project_id = resource.Body('namespace', type=str)
    project_name = resource.Body('project_name', type=str)
    runtime = resource.Body('runtime', type=str)
    timeout = resource.Body('timeout', type=int)
    handler = resource.Body('handler', type=str)
    memory_size = resource.Body('memory_size', type=int)
    gpu_memory = resource.Body('gpu_memory', type=int)
    cpu = resource.Body('cpu', type=int)
    code_type = resource.Body('code_type', type=str)
    code_url = resource.Body('code_url', type=str)
    code_filename = resource.Body('code_filename', type=str)
    code_size = resource.Body('code_size', type=int)
    user_data = resource.Body('user_data', type=str)
    digest = resource.Body('digest', type=str)
    version = resource.Body('version', type=str)
    image_name = resource.Body('image_name', type=str)
    xrole = resource.Body('xrole', type=str)
    app_xrole = resource.Body('app_xrole', type=str)
    description = resource.Body('description', type=str)
    version_description = resource.Body('version_description', type=str)
    last_modified = resource.Body('last_modified', type=str)
    func_vpc = resource.Body('func_vpc', type=dict)
    depend_version_list = resource.Body('depend_version_list', type=list)
    strategy_config = resource.Body('strategy_config', type=dict)
    extend_config = resource.Body('extend_config', type=str)
    initializer_handler = resource.Body('initializer_handler', type=str)
    initializer_timeout = resource.Body('initializer_timeout', type=int)
    pre_stop_handler = resource.Body('pre_stop_handler', type=str)
    pre_stop_timeout = resource.Body('pre_stop_timeout', type=int)
    enterprise_project_id = resource.Body('enterprise_project_id', type=str)
