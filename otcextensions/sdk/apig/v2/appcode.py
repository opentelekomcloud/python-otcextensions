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


class AppCode(resource.Resource):
    base_path = f'/apigw/instances/%(gateway_id)s/apps/%(app_id)s/app-codes'
    resources_key = 'app_codes'

    gateway_id = resource.URI('gateway_id')
    app_id = resource.URI('app_id')

    app_code = resource.Body('app_code')
    id = resource.Body('id')
    create_time = resource.Body('create_time')
    allow_fetch = True
    allow_delete = True
    allow_create = True
    allow_list = True

    def _generate_app_code(self, session, gateway, app, **attrs):
        url = f'/apigw/instances/{gateway.id}/apps/{app.id}/app-codes'
        response = session.put(url, json=attrs)
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self
