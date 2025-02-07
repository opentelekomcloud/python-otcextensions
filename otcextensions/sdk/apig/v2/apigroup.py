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

class UrlDomainSpec(resource.Resource):
    id = resource.Body('id')
    domain = resource.Body('domain')
    cname_status = resource.Body('cname_status', type=int)
    ssl_id = resource.Body('ssl_id')
    ssl_name = resource.Body('ssl_name')
    min_ssl_version = resource.Body('min_ssl_version')
    verified_client_certificate_enabled = resource.Body(
        'verified_client_certificate_enabled',
        type=bool)
    is_has_trusted_root_ca = resource.Body('is_has_trusted_root_ca',
                                           type=bool)


class ApiGroup(resource.Resource):
    base_path = f'/apigw/instances/%(gateway_id)s/api-groups'

    allow_list = True
    allow_create = True
    allow_commit = True
    allow_delete = True
    allow_fetch = True

    _query_mapping = resource.QueryParameters('limit', 'offset', 'id',
                                              'name', 'precise_search')
    resources_key = 'groups'

    gateway_id = resource.URI('gateway_id')
    name = resource.Body('name')
    remark = resource.Body('remark')
    roma_app_id = resource.Body('roma_app_id')
    version = resource.Body('version')


    id = resource.Body('id')
    status = resource.Body('status')
    sl_domain = resource.Body('sl_domain')
    register_time = resource.Body('register_time')
    update_time = resource.Body('update_time')
    on_sell_status = resource.Body('on_sell_status', type=int)
    url_domains = resource.Body('url_domains',
                                type=list,
                                list_type=UrlDomainSpec)
    sl_domain_access_enabled = resource.Body('sl_domain_access_enabled',
                                             type=bool)
    sl_domains = resource.Body('sl_domains', type=list)
    call_limits = resource.Body('call_limits', type=int)
    time_interval = resource.Body('time_interval', type=int)
    time_unit = resource.Body('time_unit')
    is_default = resource.Body('is_default', type=bool)
    roma_app_name = resource.Body('roma_app_name')

    def _verify_name(self, session, gateway, **attrs):
        """Verify the name of an API group.
        """
        uri = f'/apigw/instances/{gateway.id}/api-groups/check'
        response = session.post(uri, json=attrs)
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self

    def _update_group(self, session, gateway, **attrs):
        """Update API group.
        """
        url = f'/apigw/instances/{gateway.id}/api-groups/{self.id}'
        response = session.put(url, json=attrs)
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self
