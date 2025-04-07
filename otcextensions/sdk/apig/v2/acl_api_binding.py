#!/usr/bin/env python3
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


class AclApiBinding(resource.Resource):
    base_path = f'apigw/instances/%(gateway_id)s/acl-bindings'
    gateway_id = resource.URI('gateway_id', type=str)
    resources_key = 'acl_bindings'
    id = resource.Body('id')
    api_id = resource.Body('api_id')
    env_id = resource.Body('env_id')
    acl_id = resource.Body('acl_id')
    create_time = resource.Body('create_time')
    allow_delete = True

    def _bind_to_api(self, session, gateway_id, **attrs):
        uri = f'apigw/instances/{gateway_id}/acl-bindings'
        response = session.post(uri, json=attrs)
        exceptions.raise_from_response(response)
        data = response.json()
        resources = data[self.resources_key]
        for raw_resource in resources:
            value = self.existing(
                connection=session._get_connection(),
                **raw_resource)
            yield value


class AclBindingFailure(resource.Resource):
    resources_key = 'failure'
    bind_id = resource.Body('bind_id')
    error_code = resource.Body('error_code')
    error_msg = resource.Body('error_msg')
    api_id = resource.Body('api_id')
    api_name = resource.Body('api_name')

    def _unbind_multiple_acls(self, session, gateway_id, **attrs):
        uri = f'apigw/instances/{gateway_id}/acl-bindings?action=DELETE'
        response = session.put(uri, json=attrs)
        exceptions.raise_from_response(response)
        data = response.json()
        resources = data[self.resources_key]
        for raw_resource in resources:
            value = self.existing(
                connection=session._get_connection(),
                **raw_resource)
            yield value


class ApiForAcl(resource.Resource):
    base_path = f'apigw/instances/%(gateway_id)s/acl-bindings/binded-apis'
    gateway_id = resource.URI('gateway_id', type=str)
    _query_mapping = resource.QueryParameters(
        'limit', 'offset', 'acl_id', 'api_id', 'api_name',
        'env_id', 'group_id'
    )
    allow_list = True
    resources_key = 'apis'
    api_id = resource.Body('api_id')
    api_name = resource.Body('api_name')
    api_type = resource.Body('api_type')
    api_remark = resource.Body('api_remark')
    env_id = resource.Body('env_id')
    env_name = resource.Body('env_name')
    bind_id = resource.Body('bind_id')
    group_name = resource.Body('group_name')
    bind_time = resource.Body('bind_time')
    publish_id = resource.Body('publish_id')
    req_method = resource.Body('req_method')


class UnbindApiForAcl(resource.Resource):
    base_path = f'apigw/instances/%(gateway_id)s/acl-bindings/unbinded-apis'
    gateway_id = resource.URI('gateway_id', type=str)
    _query_mapping = resource.QueryParameters(
        'limit', 'offset', 'acl_id', 'api_id', 'api_name',
        'env_id', 'group_id'
    )
    allow_list = True
    resources_key = 'apis'
    id = resource.Body('id')
    name = resource.Body('name')
    group_id = resource.Body('group_id')
    group_name = resource.Body('group_name')
    type = resource.Body('type', type=int)
    remark = resource.Body('remark')
    run_env_name = resource.Body('run_env_name')
    run_env_id = resource.Body('run_env_id')
    publish_id = resource.Body('publish_id')
    acl_name = resource.Body('acl_name')
    req_uri = resource.Body('req_uri')
    auth_type = resource.Body('auth_type')
    req_method = resource.Body('req_method')


class AclForApi(resource.Resource):
    base_path = f'apigw/instances/%(gateway_id)s/acl-bindings/binded-acls'
    gateway_id = resource.URI('gateway_id', type=str)
    _query_mapping = resource.QueryParameters(
        'limit', 'offset', 'acl_id', 'api_id', 'env_name',
        'env_id', 'group_id'
    )
    allow_list = True

    resources_key = 'acls'
    acl_id = resource.Body('acl_id')
    acl_name = resource.Body('acl_name')
    entity_type = resource.Body('entity_type')
    acl_type = resource.Body('acl_type')
    acl_value = resource.Body('acl_value')
    env_id = resource.Body('env_id')
    env_name = resource.Body('env_name')
    bind_id = resource.Body('bind_id')
    bind_time = resource.Body('bind_time')
