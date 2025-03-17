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


class TestSignature(TestApiG):
    environment = None

    def setUp(self):
        super(TestSignature, self).setUp()
        self.create_gateway()
        self.gateway_id = TestSignature.gateway.id
        # self.gateway_id = "be76ca6de5fe4aa7af503c03b3b44dea"
        self.attrs = {
            "name": "otce_signature_1",
            "sign_type": "aes",
            "sign_algorithm": "aes-256-cfb",
        }
        self.sign = self.client.create_signature(
            gateway=self.gateway_id,
            **self.attrs
        )

        self.addCleanup(
            self.client.delete_signature,
            gateway=self.gateway_id,
            sign=self.sign
        )
        self.addCleanup(self.delete_gateway())

    def test_list_signatures(self):
        sign = list(self.client.signatures(
            gateway=self.gateway_id))
        self.assertEqual(len(sign), 1)

    def test_update_signature(self):
        attrs = {
            "name": "otce_signature_1",
            "sign_type": "aes",
            "sign_algorithm": "aes-128-cfb",
        }
        updated = self.client.update_signature(
            gateway=self.gateway_id,
            sign=self.sign.id,
            **attrs
        )
        self.assertEqual(updated.sign_algorithm, attrs["sign_algorithm"])
