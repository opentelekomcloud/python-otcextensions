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


class SslDomain(resource.Resource):
    base_path = '/apigw/certificates/%(certificate_id)s/attached-domains'
    allow_list = True
    resources_key = 'bound_domains'

    _query_mapping = resource.QueryParameters(
        'limit', 'offset', 'url_domain'
    )

    certificate_id = resource.URI('certificate_id')
    url_domain = resource.Body('url_domain')
    id = resource.Body('id')
    status = resource.Body('status', type=int)
    min_ssl_version = resource.Body('min_ssl_version')
    is_http_redirect_to_https = resource.Body(
        'is_http_redirect_to_https', type=bool)
    verified_client_certificate_enabled = resource.Body(
        'verified_client_certificate_enabled', type=bool)
    ssl_id = resource.Body('ssl_id')
    ssl_name = resource.Body('ssl_name')
    api_group_id = resource.Body('api_group_id')
    api_group_name = resource.Body('api_group_name')
    instance_id = resource.Body('instance_id')

    def _bind_certificate(self, session, certificate_id, **attrs):
        """Bind SSL certificate to a domain."""
        url = f'/apigw/certificates/{certificate_id}/domains/detach'
        response = session.post(url, json=attrs)
        exceptions.raise_from_response(response)
        return None

    def _unbind_certificate(self, session, certificate_id, **attrs):
        """Unbind SSL certificate from a domain."""
        url = f'/apigw/certificates/{certificate_id}/domains/attach'
        response = session.post(url, json=attrs)
        exceptions.raise_from_response(response)
        return None
