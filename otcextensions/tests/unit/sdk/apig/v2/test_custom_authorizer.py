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
from otcextensions.sdk.apig.v2 import custom_authorizer

EXAMPLE_CUSTOM_AUTHORIZER = {
    'gateway_id': 'gateway-67890',
    'id': 'auth-001',
    'name': 'My Custom Authorizer',
    'type': 'JWT',
    'authorizer_type': 'FUNC',
    'authorizer_uri': 'https://example.com/auth',
    'network_type': 'VPC',
    'authorizer_version': 'v1',
    'authorizer_alias_uri': 'https://alias.example.com/auth',
    'identities': [
        {'name': 'Authorization', 'location': 'HEADER', 'validation': '.*'}
    ],
    'ttl': 300,
    'user_data': 'custom user data',
    'ld_api_id': 'api-12345',
    'need_body': True,
    'create_time': '2025-04-01T10:30:00Z',
    'roma_app_id': 'roma-999',
    'roma_app_name': 'My ROMA App'
}


class TestCustomAuthorizer(base.TestCase):

    def test_basic(self):
        sot = custom_authorizer.CustomAuthorizer()
        self.assertEqual('/apigw/instances/%(gateway_id)s/authorizers',
                         sot.base_path)
        self.assertEqual('authorizer_list', sot.resources_key)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_patch)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_commit)

    def test_make_it(self):
        sot = custom_authorizer.CustomAuthorizer(**EXAMPLE_CUSTOM_AUTHORIZER)
        self.assertEqual(EXAMPLE_CUSTOM_AUTHORIZER['gateway_id'],
                         sot.gateway_id)
        self.assertEqual(EXAMPLE_CUSTOM_AUTHORIZER['id'], sot.id)
        self.assertEqual(EXAMPLE_CUSTOM_AUTHORIZER['name'], sot.name)
        self.assertEqual(EXAMPLE_CUSTOM_AUTHORIZER['type'], sot.type)
        self.assertEqual(EXAMPLE_CUSTOM_AUTHORIZER['authorizer_type'],
                         sot.authorizer_type)
        self.assertEqual(EXAMPLE_CUSTOM_AUTHORIZER['authorizer_uri'],
                         sot.authorizer_uri)
        self.assertEqual(EXAMPLE_CUSTOM_AUTHORIZER['network_type'],
                         sot.network_type)
        self.assertEqual(EXAMPLE_CUSTOM_AUTHORIZER['authorizer_version'],
                         sot.authorizer_version)
        self.assertEqual(EXAMPLE_CUSTOM_AUTHORIZER['authorizer_alias_uri'],
                         sot.authorizer_alias_uri)
        self.assertEqual(EXAMPLE_CUSTOM_AUTHORIZER['ttl'], sot.ttl)
        self.assertEqual(EXAMPLE_CUSTOM_AUTHORIZER['user_data'], sot.user_data)
        self.assertEqual(EXAMPLE_CUSTOM_AUTHORIZER['ld_api_id'], sot.ld_api_id)
        self.assertEqual(EXAMPLE_CUSTOM_AUTHORIZER['need_body'], sot.need_body)
        self.assertEqual(EXAMPLE_CUSTOM_AUTHORIZER['create_time'],
                         sot.create_time)
        self.assertEqual(EXAMPLE_CUSTOM_AUTHORIZER['roma_app_id'],
                         sot.roma_app_id)
        self.assertEqual(EXAMPLE_CUSTOM_AUTHORIZER['roma_app_name'],
                         sot.roma_app_name)
        self.assertEqual(len(EXAMPLE_CUSTOM_AUTHORIZER['identities']),
                         len(sot.identities))
        self.assertEqual(EXAMPLE_CUSTOM_AUTHORIZER['identities'][0]['name'],
                         sot.identities[0].name)
        self.assertEqual(
            EXAMPLE_CUSTOM_AUTHORIZER['identities'][0]['location'],
            sot.identities[0].location)
        self.assertEqual(
            EXAMPLE_CUSTOM_AUTHORIZER['identities'][0]['validation'],
            sot.identities[0].validation)
