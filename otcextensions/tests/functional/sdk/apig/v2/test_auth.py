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


class TestAuth(TestApiG):

    def setUp(self):
        super(TestAuth, self).setUp()

    def test_list_apps_bound_to_api(self):
        found = self.client.list_apps_bound_to_api(
            gateway="560de602c9f74969a05ff01d401a53ed")
        self.assertIsNotNone(list(found))

    def test_list_api_bound_to_app(self):
        attrs = {
            'app_id': '74593f5c94f64a139db38b61a7705df3'
        }
        found = self.client.list_api_bound_to_app(
            gateway="560de602c9f74969a05ff01d401a53ed",
            **attrs)
        self.assertIsNotNone(list(found))

    def test_list_api_not_bound_to_app(self):
        attrs = {
            'app_id': '74593f5c94f64a139db38b61a7705df3',
            'env_id': 'DEFAULT_ENVIRONMENT_RELEASE_ID'
        }
        found = self.client.list_api_not_bound_to_app(
            gateway="560de602c9f74969a05ff01d401a53ed",
            **attrs)
        self.assertIsNotNone(list(found))

    def test_create_auth(self):
        attrs = {
            "env_id": "DEFAULT_ENVIRONMENT_RELEASE_ID",
            "app_ids": ["74593f5c94f64a139db38b61a7705df3"],
            "api_ids": ["64182cc7e77245ebbae8cf3b8522a540"]
        }
        result = self.client.create_auth_in_api(
            gateway="560de602c9f74969a05ff01d401a53ed",
            **attrs)
        self.assertIsNotNone(list(result))

    def test_delete_auth_from_api(self):
        found = list(self.client.list_apps_bound_to_api(
            gateway="560de602c9f74969a05ff01d401a53ed"))
        to_delete = [item for item in found
                     if item['app_id'] == "id"][0]
        self.client.delete_auth_from_api(
            gateway="560de602c9f74969a05ff01d401a53ed",
            auth_id=to_delete.id
        )
        found = list(self.client.list_apps_bound_to_api(
            gateway="560de602c9f74969a05ff01d401a53ed"))
        self.assertEqual(1, len(found))
