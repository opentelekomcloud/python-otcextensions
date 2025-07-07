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


class IdentitySpec(resource.Resource):
    name = resource.Body('name')
    location = resource.Body('location')
    validation = resource.Body('validation')


class CustomAuthorizer(resource.Resource):
    base_path = f'/apigw/instances/%(gateway_id)s/authorizers'
    resources_key = 'authorizer_list'
    allow_list = True
    allow_fetch = True
    allow_create = True
    allow_patch = True
    allow_delete = True
    allow_commit = True

    _query_mapping = resource.QueryParameters(
        'limit', 'offset', 'id', 'type', 'name')
    gateway_id = resource.URI('gateway_id')
    name = resource.Body('name')
    type = resource.Body('type')
    authorizer_type = resource.Body('authorizer_type')
    authorizer_uri = resource.Body('authorizer_uri')
    network_type = resource.Body('network_type')
    authorizer_version = resource.Body('authorizer_version')
    authorizer_alias_uri = resource.Body('authorizer_alias_uri')
    identities = resource.Body('identities',
                               type=list,
                               list_type=IdentitySpec)
    ttl = resource.Body('ttl')
    user_data = resource.Body('user_data')
    ld_api_id = resource.Body('ld_api_id')
    need_body = resource.Body('need_body', type=bool)
    id = resource.Body('id')
    create_time = resource.Body('create_time')
    roma_app_id = resource.Body('roma_app_id')
    roma_app_name = resource.Body('roma_app_name')
