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
from otcextensions.tests.functional.sdk.apig import TestApiG


class TestCustomAuthorizer(TestApiG):
    custom_authorizer = None
    gateway = '560de602c9f74969a05ff01d401a53ed'

    def setUp(self):
        super(TestCustomAuthorizer, self).setUp()
        attrs = {
            'name': 'custom_auth_test',
            'type': 'BACKEND',
            'authorizer_type': 'FUNC',
            'authorizer_uri': 'urn:fss:eu-de:7ed5f793b8354ea9b27a849f17af4733'
                              ':function:default:test_apig_authorizer:latest',
            'authorizer_version': '1'
        }
        result = self.client.create_custom_authorizer(
            gateway=TestCustomAuthorizer.gateway,
            **attrs)
        self.assertIsNotNone(result.id)
        TestCustomAuthorizer.custom_authorizer = result

    def tearDown(self):
        super(TestCustomAuthorizer, self).tearDown()
        self.client.delete_custom_authorizer(
            gateway=TestCustomAuthorizer.gateway,
            custom_authorizer=TestCustomAuthorizer.custom_authorizer.id
        )
        found = list(self.client.custom_authorizers(
            gateway=TestCustomAuthorizer.gateway,
        ))
        self.assertEqual(len(found), 0)

    def test_02_get_custom_authorizer(self):
        found = self.client.get_custom_authorizer(
            gateway=TestCustomAuthorizer.gateway,
            custom_authorizer=TestCustomAuthorizer.custom_authorizer.id)
        self.assertEqual(TestCustomAuthorizer.custom_authorizer.id, found.id)

    def test_03_list_custom_authorizer(self):
        attrs = {
            'limit': 2
        }
        found = list(self.client.custom_authorizers(
            gateway=TestCustomAuthorizer.gateway,
            **attrs
        ))
        self.assertEqual(len(found), 1)

    def test_04_update_custom_authorizer(self):
        change = 'BACKEND'
        attrs = {
            'name': 'custom_auth_test',
            'type': change,
            'authorizer_type': 'FUNC',
            'authorizer_uri': 'urn:fss:eu-de:7ed5f793b8354ea9b27a849f17af4733'
                              ':function:default:test_apig_authorizer:latest',
            'authorizer_version': '1',
            'ttl': 5,
            "identities": [{
                "name": "header",
                "location": "HEADER"
            }]
        }
        updated = self.client.update_custom_authorizer(
            gateway=TestCustomAuthorizer.gateway,
            custom_authorizer=TestCustomAuthorizer.custom_authorizer.id,
            **attrs
        )
        self.assertEqual(updated.type, change)
