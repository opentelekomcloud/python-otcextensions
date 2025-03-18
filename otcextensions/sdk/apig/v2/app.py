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


class Quota(resource.Resource):
    base_path = f'/apigw/instances/%(gateway_id)s/apps/%(app_id)s/bound-quota'

    gateway_id = resource.URI('gateway_id')
    app_id = resource.URI('app_id')

    allow_fetch = True

    app_quota_id = resource.Body('app_quota_id')
    name = resource.Body('name')
    call_limits = resource.Body('call_limits', type=int)
    time_unit = resource.Body('time_unit')
    time_interval = resource.Body('time_interval')
    remark = resource.Body('remark')
    reset_time = resource.Body('reset_time')
    create_time = resource.Body('create_time')
    bound_app_num = resource.Body('bound_app_num')


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
