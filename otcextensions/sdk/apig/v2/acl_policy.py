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


class AclPolicy(resource.Resource):
    base_path = f'apigw/instances/%(gateway_id)s/acls'
    resources_key = 'acls'

    allow_create = True
    allow_commit = True
    allow_delete = True
    allow_list = True
    allow_fetch = True

    _query_mapping = resource.QueryParameters(
        'limit', 'offset', 'name', 'id', 'precise_search',
        'acl_type', 'entity_type'
    )

    gateway_id = resource.URI('gateway_id', type=str)
    id = resource.Body('id')
    acl_name = resource.Body('acl_name')
    acl_type = resource.Body('acl_type')
    acl_value = resource.Body('acl_value')
    entity_type = resource.Body('entity_type')
    update_time = resource.Body('update_time')
    bind_num = resource.Body('bind_num')
    error_code = resource.Body('error_code')
    error_msg = resource.Body('error_msg')

    def _delete_multiple_acls(self, session, gateway_id, **attrs):
        uri = f'apigw/instances/{gateway_id}/acls?action=DELETE'
        response = session.put(uri, json=attrs)
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self
