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


class TestAclApiBinding(TestApiG):
    gateway_id = "560de602c9f74969a05ff01d401a53ed"

    def setUp(self):
        super(TestAclApiBinding, self).setUp()

    def test_list_apis_for_acl(self):
        attrs = {
            'acl_id': '1142260d5e654b9590a1d329926bea52'
        }
        found = list(self.client.list_apis_for_acl(
            gateway=TestAclApiBinding.gateway_id, **attrs))
        self.assertGreater(len(found), 0)

    def test_list_api_not_bound_to_acl(self):
        attrs = {
            'acl_id': '1142260d5e654b9590a1d329926bea52'
        }
        found = list(self.client.list_api_not_bound_to_acl(
            gateway=TestAclApiBinding.gateway_id, **attrs))
        self.assertGreater(len(found), 0)

    def test_list_acl_for_api(self):
        attrs = {
            'api_id': '64182cc7e77245ebbae8cf3b8522a540'
        }
        found = list(self.client.list_acl_for_api(
            gateway=TestAclApiBinding.gateway_id, **attrs))
        self.assertGreater(len(found), 0)

    def test_bind_acl_to_api(self):
        attrs = {
            "acl_id": "d5645ed3c454492f8d6aa68ab034c6d3",
            "publish_ids": ["293fe0a8e3f04a1ab151bd0d913900a9"]
        }
        result = list(self.client.bind_acl_to_api(
            gateway=TestAclApiBinding.gateway_id,
            **attrs))
        self.assertGreater(len(result), 0)

    def test_unbind_acl(self):
        self.client.unbind_acl(
            gateway=TestAclApiBinding.gateway_id,
            acl='e37364eb93c44ef093d686383354689b')
        attrs = {
            'api_id': '12259302184a4972ac64277537a6aa20'
        }
        found = list(self.client.list_acl_for_api(
            gateway=TestAclApiBinding.gateway_id, **attrs))
        self.assertEqual(len(found), 0)

    def test_unbind_acls(self):
        attrs = {
            "acl_bindings": ["332c5db1458a477b89b2ea741fec94a3"]
        }
        result = list(self.client.unbind_acls(
            gateway=TestAclApiBinding.gateway_id,
            **attrs
        ))
        self.assertGreater(len(result), 0)
