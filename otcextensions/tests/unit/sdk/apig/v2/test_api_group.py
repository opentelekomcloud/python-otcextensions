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
from otcextensions.sdk.apig.v2 import apigroup


EXAMPLE_API_GROUP = {
    'id': 'group-12345',
    'gateway_id': 'gateway-67890',
    'name': 'Test API Group',
    'remark': 'This is a test API group',
    'roma_app_id': 'app-54321',
    'version': 'v1',
    'status': 1,
    'sl_domain': 'api.example.com',
    'register_time': '2025-02-07T12:00:00Z',
    'update_time': '2025-02-07T12:30:00Z',
    'on_sell_status': 1,
    'url_domains': [
        {
            'id': 'domain-1',
            'domain': 'example.com',
            'cname_status': 1,
            'ssl_id': 'ssl-123',
            'ssl_name': 'SSL Cert',
            'min_ssl_version': 'TLSv1.2',
            'verified_client_certificate_enabled': True,
            'is_has_trusted_root_ca': False
        }
    ],
    'sl_domain_access_enabled': True,
    'sl_domains': ['sl1.example.com', 'sl2.example.com'],
    'call_limits': 1000,
    'time_interval': 60,
    'time_unit': 'second',
    'is_default': False,
    'roma_app_name': 'Test App'
}


class TestApiGroup(base.TestCase):

    def test_basic(self):
        sot = apigroup.ApiGroup()
        self.assertEqual('/apigw/instances/%(gateway_id)s/api-groups',
                         sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_fetch)
        self.assertEqual('groups', sot.resources_key)

    def test_make_it(self):
        sot = apigroup.ApiGroup(**EXAMPLE_API_GROUP)
        self.assertEqual(EXAMPLE_API_GROUP['id'], sot.id)
        self.assertEqual(EXAMPLE_API_GROUP['gateway_id'], sot.gateway_id)
        self.assertEqual(EXAMPLE_API_GROUP['name'], sot.name)
        self.assertEqual(EXAMPLE_API_GROUP['remark'], sot.remark)
        self.assertEqual(EXAMPLE_API_GROUP['roma_app_id'], sot.roma_app_id)
        self.assertEqual(EXAMPLE_API_GROUP['version'], sot.version)
        self.assertEqual(EXAMPLE_API_GROUP['status'], sot.status)
        self.assertEqual(EXAMPLE_API_GROUP['sl_domain'], sot.sl_domain)
        self.assertEqual(EXAMPLE_API_GROUP['register_time'], sot.register_time)
        self.assertEqual(EXAMPLE_API_GROUP['update_time'], sot.update_time)
        self.assertEqual(EXAMPLE_API_GROUP['on_sell_status'],
                         sot.on_sell_status)
        self.assertEqual(EXAMPLE_API_GROUP['sl_domain_access_enabled'],
                         sot.sl_domain_access_enabled)
        self.assertEqual(EXAMPLE_API_GROUP['sl_domains'], sot.sl_domains)
        self.assertEqual(EXAMPLE_API_GROUP['call_limits'], sot.call_limits)
        self.assertEqual(EXAMPLE_API_GROUP['time_interval'], sot.time_interval)
        self.assertEqual(EXAMPLE_API_GROUP['time_unit'], sot.time_unit)
        self.assertEqual(EXAMPLE_API_GROUP['is_default'], sot.is_default)
        self.assertEqual(EXAMPLE_API_GROUP['roma_app_name'], sot.roma_app_name)

        self.assertEqual(len(EXAMPLE_API_GROUP['url_domains']),
                         len(sot.url_domains))
        self.assertEqual(
            EXAMPLE_API_GROUP['url_domains'][0]['id'],
            sot.url_domains[0].id)
        self.assertEqual(
            EXAMPLE_API_GROUP['url_domains'][0]['domain'],
            sot.url_domains[0].domain)
        self.assertEqual(
            EXAMPLE_API_GROUP['url_domains'][0]['cname_status'],
            sot.url_domains[0].cname_status)
        self.assertEqual(
            EXAMPLE_API_GROUP['url_domains'][0]['ssl_id'],
            sot.url_domains[0].ssl_id)
        self.assertEqual(
            EXAMPLE_API_GROUP['url_domains'][0]['ssl_name'],
            sot.url_domains[0].ssl_name)
        self.assertEqual(
            EXAMPLE_API_GROUP['url_domains'][0]['min_ssl_version'],
            sot.url_domains[0].min_ssl_version)
        self.assertEqual(
            EXAMPLE_API_GROUP['url_domains'][0]
            ['verified_client_certificate_enabled'],
            sot.url_domains[0].verified_client_certificate_enabled)
        self.assertEqual(
            EXAMPLE_API_GROUP['url_domains'][0]['is_has_trusted_root_ca'],
            sot.url_domains[0].is_has_trusted_root_ca)
