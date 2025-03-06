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
        self.create_gateway()
        self.gateway_id = TestGwFeatures.gateway.id
        # self.gateway_id = "be76ca6de5fe4aa7af503c03b3b44dea"
        self.attrs = {
            "name": "route",
            "enable": True,
            "config": "{\"user_routes\":[\"172.16.128.0/20\","
                      "\"172.16.0.0/20\"]}",
        }
        self.feat = self.client.configure_gateway_feature(
            gateway=self.gateway_id,
            **self.attrs
        )

        self.disable_attrs = {
            "name": "route",
            "enable": False,
            "config": "{\"user_routes\":[]}",
        }
        self.addCleanup(
            self.client.configure_gateway_feature,
            gateway=self.gateway_id,
            **self.disable_attrs
        )
        self.addCleanup(self.delete_gateway())

    def test_list_gateway_features(self):
        features = list(self.client.gateway_features(
            gateway=self.gateway_id))
        self.assertGreaterEqual(len(features), 10)

    def test_list_available_gateway_features(self):
        features = list(self.client.supported_gateway_features(
            gateway=self.gateway_id, limit=500))
        self.assertGreaterEqual(len(features), 1)
