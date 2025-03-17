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


class App(resource.Resource):
    base_path = f'/apigw/instances/%(gateway_id)s/apps'
    resources_key = 'apps'

    allow_fetch = True
    allow_list = True
    allow_create = True
    allow_commit = True
    allow_delete = True

    _query_mapping = resource.QueryParameters(
        'limit', 'offset', 'id', 'creator',
        'name', 'status', 'app_key', 'precise_search'
    )

    gateway_id = resource.URI('gateway_id')

    name = resource.Body('name')
    remark = resource.Body('remark')
    app_key = resource.Body('app_key')
    app_secret = resource.Body('app_secret')

    id = resource.Body('id')
    creator = resource.Body('creator')
    update_time = resource.Body('update_time')
    register_time = resource.Body('register_time')
    status = resource.Body('status', type=int)
    app_type = resource.Body('app_type')
    roma_app_type = resource.Body('roma_app_type')
    bind_num = resource.Body('bind_num', type=int)

    def _verify_app(self, session, gateway):
        url = f'/apigw/instances/{gateway.id}/apps/validation/{self.id}'
        response = session.get(url)
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self

    def _reset_secret(self, session, gateway, **attrs):
        url = f'/apigw/instances/{gateway.id}/apps/secret/{self.id}'
        response = session.put(url, json=attrs)
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self
