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


class TestConfig(TestApiG):
    gateway_id = "560de602c9f74969a05ff01d401a53ed"

    def setUp(self):
        super(TestConfig, self).setUp()

    def test_list_config(self):
        configs = list(self.client.configs())
        self.assertGreater(len(configs), 0)

    def test_list_config_for_gateway(self):
        configs = list(self.client.configs_for_gateway(
            gateway_id=TestConfig.gateway_id))
        self.assertGreater(len(configs), 0)
