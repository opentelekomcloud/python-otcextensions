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

from openstack.tests.unit import base
from otcextensions.sdk.apig.v2 import ssl_domain

EXAMPLE_DOMAIN = {
    'id': 'domain-001',
    'certificate_id': 'cert-abc123',
    'url_domain': 'api.example.com',
    'status': 1,
    'min_ssl_version': 'TLSv1.2',
    'is_http_redirect_to_https': True,
    'verified_client_certificate_enabled': False,
    'ssl_id': 'ssl-xyz',
    'ssl_name': 'MySSL',
    'api_group_id': 'group-001',
    'api_group_name': 'MyAPIGroup',
    'instance_id': 'instance-789'
}


class TestSslDomain(base.TestCase):

    def test_basic(self):
        sot = ssl_domain.SslDomain()
        self.assertEqual(
            '/apigw/certificates/%(certificate_id)s/attached-domains',
            sot.base_path
        )
        self.assertTrue(sot.allow_list)
        self.assertEqual('bound_domains', sot.resources_key)

    def test_make_it(self):
        sot = ssl_domain.SslDomain(**EXAMPLE_DOMAIN)
        self.assertEqual('domain-001', sot.id)
        self.assertEqual('cert-abc123', sot.certificate_id)
        self.assertEqual('api.example.com', sot.url_domain)
        self.assertEqual(1, sot.status)
        self.assertEqual('TLSv1.2', sot.min_ssl_version)
        self.assertTrue(sot.is_http_redirect_to_https)
        self.assertFalse(sot.verified_client_certificate_enabled)
        self.assertEqual('ssl-xyz', sot.ssl_id)
        self.assertEqual('MySSL', sot.ssl_name)
        self.assertEqual('group-001', sot.api_group_id)
        self.assertEqual('MyAPIGroup', sot.api_group_name)
        self.assertEqual('instance-789', sot.instance_id)
