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


class TestGwFeatures(TestApiG):
    def setUp(self):
        super(TestGwFeatures, self).setUp()
        # self.create_gateway()
        # self.gateway_id = TestGwFeatures.gateway.id
        self.gateway_id = "be76ca6de5fe4aa7af503c03b3b44dea"
        # self.addCleanup(self.delete_gateway())

    def test_get_api_quantities(self):
        api_q = self.client.get_api_quantities(
            gateway=self.gateway_id)
        self.assertIsNotNone(api_q)

    def test_get_api_group_quantities(self):
        api_group_q = self.client.get_api_group_quantities(
            gateway=self.gateway_id)
        self.assertIsNotNone(api_group_q)

    def test_get_app_quantities(self):
        api_group_q = self.client.get_app_quantities(
            gateway=self.gateway_id)
        self.assertIsNotNone(api_group_q)
