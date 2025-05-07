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


class ExportApi(resource.Resource):
    base_path = f'apigw/instances/%(gateway_id)s/openapi/export'

    _query_mapping = resource.QueryParameters('oas_version')

    gateway_id = resource.URI('gateway_id')
    env_id = resource.Body('env_id')
    group_id = resource.Body('group_id')
    define = resource.Body('define')
    type = resource.Body('type')
    version = resource.Body('version')
    apis = resource.Body('apis', type=list)

    def _export_api(self, session, gateway_id,
                    full_path, **attrs):
        uri = f'apigw/instances/{gateway_id}/openapi/export'
        response = session.post(uri, json=attrs)
        exceptions.raise_from_response(response)
        file_type = attrs['type'] if 'type' in attrs else 'json'
        with open(f'{full_path}.{file_type}', 'wb') as f:
            f.write(response.content)
        return None


class SuccessSpec(resource.Resource):
    id = resource.Body('id')
    method = resource.Body('method')
    path = resource.Body('path')
    action = resource.Body('action')


class FailureSpec(resource.Resource):
    method = resource.Body('method')
    path = resource.Body('path')
    error_code = resource.Body('error_code')
    error_msg = resource.Body('error_msg')


class SwaggerSpec(resource.Resource):
    id = resource.Body('id')
    result = resource.Body('result')


class IgnoreSpec(resource.Resource):
    method = resource.Body('method')
    path = resource.Body('path')


class ImportApi(resource.Resource):
    base_path = f'apigw/instances/%(gateway_id)s/openapi/import'

    gateway_id = resource.URI('gateway_id')
    is_create_group = resource.Body('is_create_group', type=bool)
    group_id = resource.Body('group_id')
    extend_mode = resource.Body('extend_mode')
    simple_mode = resource.Body('simple_mode', type=bool)
    mock_mode = resource.Body('mock_mode', type=bool)
    api_mode = resource.Body('api_mode')
    file_name = resource.Body('file_name')

    success = resource.Body('success', type=list, list_type=SuccessSpec)
    failure = resource.Body('failure', type=list, list_type=FailureSpec)
    swagger = resource.Body('swagger', type=SwaggerSpec)
    ignore = resource.Body('ignore', type=list, list_type=IgnoreSpec)

    def _import_api(self, session, gateway_id, **attrs):
        uri = f'apigw/instances/{gateway_id}/openapi/import'
        response = session.post(uri, json=attrs)
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self
