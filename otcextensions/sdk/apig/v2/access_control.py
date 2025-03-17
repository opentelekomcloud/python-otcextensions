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


class AccessControl(resource.Resource):
    base_path = f'/apigw/instances/%(gateway_id)s/apps/%(app_url_id)s/app-acl'
    gateway_id = resource.URI('gateway_id')
    app_url_id = resource.URI('app_url_id')

    app_id = resource.Body('app_id')
    app_acl_type = resource.Body('app_acl_type')
    app_acl_values = resource.Body('app_acl_values', type=list)

    allow_fetch = True
    allow_delete = True
    allow_update = True

    def _configure(self, session, gateway, app, **attrs):
        url = f'/apigw/instances/{gateway.id}/apps/{app.id}/app-acl'
        response = session.put(url, json=attrs)
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self

    def _delete(self, session, gateway, app, **attrs):
        url = f'/apigw/instances/{gateway.id}/apps/{app.id}/app-acl'
        response = session.delete(url, json=attrs)
        exceptions.raise_from_response(response)
        return None
