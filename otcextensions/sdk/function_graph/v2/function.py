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
from openstack import exceptions


class TagSpec(resource.Resource):
    #: Key
    key = resource.Body('key')
    #: Value.
    values = resource.Body('values', type=list)


class Function(resource.Resource):
    resources_key = 'functions'
    base_path = '/fgs/functions'

    # Capabilities
    allow_create = True
    allow_fetch = True
    allow_commit = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'package_name', 'maxitems', 'marker'
    )

    # Properties
    func_name = resource.Body('func_name', type=str)
    package = resource.Body('package', type=str)
    runtime = resource.Body('runtime', type=str)
    timeout = resource.Body('timeout', type=int)
    handler = resource.Body('handler', type=str)
    depend_version_list = resource.Body('depend_version_list', type=list)
    func_vpc = resource.Body('func_vpc', type=dict)
    memory_size = resource.Body('memory_size', type=int)
    code_type = resource.Body('code_type', type=str)
    code_url = resource.Body('code_url', type=str)
    code_filename = resource.Body('code_filename', type=str)
    custom_image = resource.Body('custom_image', type=dict)
    user_data = resource.Body('user_data', type=str)
    encrypted_user_data = resource.Body('encrypted_user_data', type=str)
    xrole = resource.Body('xrole', type=str)
    app_xrole = resource.Body('app_xrole', type=str)
    description = resource.Body('description', type=str)
    func_code = resource.Body('func_code', type=dict)
    mount_config = resource.Body('mount_config', type=dict)
    initializer_handler = resource.Body('initializer_handler', type=str)
    initializer_timeout = resource.Body('initializer_timeout', type=int)
    pre_stop_handler = resource.Body('pre_stop_handler', type=str)
    pre_stop_timeout = resource.Body('pre_stop_timeout', type=int)
    enterprise_project_id = resource.Body('enterprise_project_id', type=str)
    type = resource.Body('type', type=str)
    log_config = resource.Body('log_config', type=dict)
    network_controller = resource.Body('network_controller', type=dict)
    is_stateful_function = resource.Body('is_stateful_function', type=bool)
    enable_dynamic_memory = resource.Body('enable_dynamic_memory', type=bool)

    # Attributes
    func_id = resource.Body('func_id', type=str)
    func_urn = resource.Body('func_urn', type=str)
    domain_id = resource.Body('domain_id', type=str)
    namespace = resource.Body('namespace', type=str)
    project_name = resource.Body('project_name', type=str)
    cpu = resource.Body('cpu', type=int)
    code_size = resource.Body('code_size', type=int)
    domain_names = resource.Body('domain_names', type=str)
    digest = resource.Body('digest', type=str)
    version = resource.Body('version', type=str)
    image_name = resource.Body('image_name', type=str)
    last_modified = resource.Body('last_modified', type=str)
    reserved_instance_count = resource.Body(
        'reserved_instance_count', type=int)
    strategy_config = resource.Body('strategy_config', type=dict)
    extend_config = resource.Body('extend_config', type=str)
    dependencies = resource.Body('dependencies', type=list)
    long_time = resource.Body('long_time', type=bool)
    log_group_id = resource.Body('log_group_id', type=str)
    log_stream_id = resource.Body('log_stream_id', type=str)
    enable_cloud_debug = resource.Body('enable_cloud_debug', type=str)
    is_bridge_function = resource.Body('is_bridge_function', type=bool)
    apig_route_enable = resource.Body('apig_route_enable', type=bool)
    heartbeat_handler = resource.Body('heartbeat_handler', type=str)
    enable_class_isolation = resource.Body('enable_class_isolation', type=bool)
    allow_ephemeral_storage = resource.Body(
        'allow_ephemeral_storage', type=bool)
    ephemeral_storage = resource.Body('ephemeral_storage', type=int)
    resource_id = resource.Body('resource_id', type=str)
    is_return_stream = resource.Body('is_return_stream', type=bool)
    enable_auth_in_header = resource.Body('enable_auth_in_header', type=bool)
    gpu_memory = resource.Body('gpu_memory', type=int)
    func_vpc_id = resource.Body('func_vpc_id', type=str)
    bind_bridge_func_urns = resource.Body('bind_bridge_funcUrns', type=list)
    reserved_instance_idle_mode = resource.Body(
        'reserved_instance_idle_mode', type=bool)
    gpu_type = resource.Body('gpu_type', type=str)
    tags = resource.Body('tags', type=list, list_type=TagSpec)

    def _delete_function(self, session, function):
        """Delete Function
        """
        url = self.base_path + f'/{function.func_urn.rpartition(":")[0]}'
        response = session.delete(url)
        exceptions.raise_from_response(response)
        return None

    def _get_function_code(self, session, function):
        """Get Function Code
        """
        url = self.base_path + f'/{function.func_urn.rpartition(":")[0]}/code'
        response = session.get(url)
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self

    def _get_function_metadata(self, session, function):
        """Get Function Metadata
        """
        urn = function.func_urn.rpartition(":")[0]
        url = self.base_path + f'/{urn}/config'
        response = session.get(url)
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self

    def _get_resource_tags(self, session, function):
        """Get Resource Tags
        """
        url = f'/functions/tags'
        response = session.get(url)
        exceptions.raise_from_response(response)
        self.tags = response.json()["tags"]
        return self

    def _create_resource_tags(self, session, function, tags):
        """Create Resource Tags
        """
        data = {"tags": tags}
        url = f'/functions/{function.func_urn.rpartition(":")[0]}/tags/create'
        response = session.post(url, json=data)
        exceptions.raise_from_response(response)
        return None

    def _delete_resource_tags(self, session, function, tags):
        """Delete Resource Tags
        """
        data = {"tags": tags}
        url = f'/functions/{function.func_urn.rpartition(":")[0]}/tags/delete'
        response = session.delete(url, json=data)
        exceptions.raise_from_response(response)
        return None

    def _update_pin_status(self, session, function):
        """Update Pin Status
        """
        urn = function.func_urn.rpartition(":")[0]
        url = self.base_path + f'/{urn}/collect/true'
        response = session.put(url)
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self

    def _update_function_code(self, session, function, **attrs):
        """Update Function Code
        """
        url = self.base_path + f'/{function.func_urn.rpartition(":")[0]}/code'
        response = session.put(url, json=attrs)
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self

    def _update_function_metadata(self, session, function, **attrs):
        """Update Function Metadata
        """
        urn = function.func_urn.rpartition(":")[0]
        url = self.base_path + f'/{urn}/config'
        response = session.put(url, json=attrs)
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self

    def _update_max_instances(self, session, function, number):
        """Update Function Instances Number
        """
        urn = function.func_urn.rpartition(":")[0]
        url = self.base_path + f'/{urn}/config-max-instance'
        response = session.put(url, json={'max_instance_num': number})
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self
