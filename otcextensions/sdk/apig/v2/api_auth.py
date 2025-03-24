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


class ApiAuthResult(resource.Resource):
    status = resource.Body('status')
    error_msg = resource.Body('error_msg')
    error_code = resource.Body('error_code')
    api_name = resource.Body('api_name')
    app_name = resource.Body('app_name')


class ApiAuthInfo(resource.Resource):
    base_path = f'apigw/instances/%(gateway_id)s/app-auths'
    resources_key = 'auths'

    _query_mapping = resource.QueryParameters('limit', 'offset', 'app_id',
                                              'api_id', 'api_name', 'group_id',
                                              'group_name', 'env_id', 'app_name')

    allow_list = True
    allow_create = True
    gateway_id = resource.URI('gateway_id')
    env_id = resource.Body('env_id')
    app_ids = resource.Body('app_ids', type=list)
    api_ids = resource.Body('api_ids', type=list)

    api_id = resource.Body('api_id')
    api_name = resource.Body('api_name')
    group_name = resource.Body('group_name')
    api_type = resource.Body('api_type', type=int)
    api_remark = resource.Body('api_remark')
    app_name = resource.Body('app_name')
    app_remark = resource.Body('app_remark')
    app_type = resource.Body('app_type')
    app_creator = resource.Body('app_creator')
    publish_id = resource.Body('publish_id')
    group_id = resource.Body('group_id')
    auth_result = resource.Body('auth_result', type=ApiAuthResult)
    auth_time = resource.Body('auth_time')
    id = resource.Body('id')
    app_id = resource.Body('app_id')
    auth_role = resource.Body('auth_role')
    auth_tunnel = resource.Body('auth_tunnel')
    auth_whitelist = resource.Body('auth_whitelist', type=list)
    auth_blacklist = resource.Body('auth_blacklist', type=list)
    visit_params = resource.Body('visit_params')
    visit_param = resource.Body('visit_param')
    roma_app_type = resource.Body('roma_app_type')
    env_name = resource.Body('env_name')
    run_env_name = resource.Body('run_env_name')

    def _authorize_apps(self, session, gateway_id, **attrs):
        uri = f'apigw/instances/{gateway_id}/app-auths'
        response = session.post(uri, json=attrs)
        exceptions.raise_from_response(response)
        data = response.json()
        resources = data[self.resources_key]
        for raw_resource in resources:
            value = self.existing(
                connection=session._get_connection(),
                **raw_resource)
            yield value

    def _cancel_auth(self, session, gateway_id, app_auth_id):
        uri = f'apigw/instances/{gateway_id}/app-auths/{app_auth_id}'
        response = session.delete(uri)
        exceptions.raise_from_response(response)
        return None