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

from otcextensions.tests.functional.sdk.vlb import TestVlb


class TestSecurityPolicy(TestVlb):

    def setUp(self):
        super(TestSecurityPolicy, self).setUp()
        self.create_security_policy()

    def test_01_list_security_policies(self):
        sec_policies = list(self.client.security_policies(
            name=TestSecurityPolicy.security_policy.name))
        self.assertGreaterEqual(len(sec_policies), 0)

    def test_02_get_security_policy(self):
        sec_policy = self.client.get_security_policy(
            TestVlb.security_policy)
        self.assertIsNotNone(sec_policy)

    def test_03_find_security_policy(self):
        sec_policy = self.client.find_security_policy(
            TestVlb.security_policy.name)
        self.assertIsNotNone(sec_policy)

    def test_04_update_security_policy(self):
        new_description = 'changed'
        protocols = ["TLSv1.3"]
        ciphers = ["TLS_AES_128_GCM_SHA256"]
        sec_policy = self.client.update_security_policy(
            TestVlb.security_policy,
            description=new_description,
            protocols=protocols,
            ciphers=ciphers
        )
        self.assertEqual(sec_policy['description'], new_description)
        self.assertEqual(sec_policy['protocols'], protocols)
        self.assertEqual(sec_policy['ciphers'], ciphers)

        # cleanup
        self.client.delete_security_policy(
            TestVlb.security_policy
        )
