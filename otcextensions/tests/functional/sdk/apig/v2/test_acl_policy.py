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


class TestACPolicy(TestApiG):
    gateway_id = "560de602c9f74969a05ff01d401a53ed"
    acl_id = None

    def setUp(self):
        super(TestACPolicy, self).setUp()

    def test_create_acl_policy(self):
        attrs = {
            "acl_name": "acl_demo",
            "acl_type": "PERMIT",
            "acl_value": "192.168.1.5,192.168.10.1",
            "entity_type": "IP"
        }
        created = self.client.create_acl_policy(
            gateway=TestACPolicy.gateway_id,
            **attrs)
        self.assertIsNotNone(created.id)
        TestACPolicy.acl_id = created.id

    def test_update_acl_policy(self):
        check = "DENY"
        attrs = {
            "acl_name": "acl_demo",
            "entity_type": "IP",
            "acl_type": check,
            "acl_value": "192.168.1.5,192.168.10.1"
        }
        updated = self.client.update_acl_policy(
            gateway=TestACPolicy.gateway_id,
            acl_policy=TestACPolicy.acl_id,
            **attrs)
        self.assertEqual(updated.acl_type, check)

    def test_list_acl_policies(self):
        found = list(self.client.acl_policies(gateway=TestACPolicy.gateway_id))
        self.assertGreater(len(found), 0)

    def test_get_acl_policy(self):
        found = self.client.get_acl_policy(gateway=TestACPolicy.gateway_id,
                                           acl_policy=TestACPolicy.acl_id)
        self.assertIsNotNone(found.id)

    def test_delete_ac_policy(self):
        self.client.delete_acl_policy(gateway=TestACPolicy.gateway_id,
                                      ac_policy=TestACPolicy.acl_id)
        found = self.client.acl_policies(gateway=TestACPolicy.gateway_id)
        self.assertEqual(len(list(found)), 0)

    def test_delete_acl_policies(self):
        attrs = {
            "acl_name": "acl_demo1",
            "acl_type": "PERMIT",
            "acl_value": "192.168.1.5,192.168.10.1",
            "entity_type": "IP"
        }
        created = self.client.create_acl_policy(
            gateway=TestACPolicy.gateway_id,
            **attrs)
        attrs = {
            'acls': [TestACPolicy.acl_id, created.id]
        }
        self.client.delete_acl_policies(gateway=TestACPolicy.gateway_id,
                                        **attrs)
        found = self.client.acl_policies(gateway=TestACPolicy.gateway_id)
        self.assertEqual(len(list(found)), 0)
