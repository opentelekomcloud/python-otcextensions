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


class TestEnvironment(TestApiG):
    environment = None

    def setUp(self):
        super(TestEnvironment, self).setUp()
        self.create_gateway()

    def test_01_create_environment(self):
        attrs = {
            "name": "DEV",
            "remark": "Development environment"
        }
        environment = self.client.create_environment(
            gateway=TestEnvironment.gateway,
            **attrs)
        TestEnvironment.environment = environment

    def test_02_update_environment(self):
        new_remark = "Updated remark"
        attrs = {
            "name": "DEV",
            "remark": new_remark
        }
        environment = self.client.update_environment(
            environment=TestEnvironment.environment,
            gateway=TestEnvironment.gateway,
            **attrs
        )
        self.assertEqual(environment.remark, new_remark)

    def test_03_list_environments(self):
        environments = list(self.client.environments(
            gateway=TestEnvironment.gateway))
        self.assertGreater(len(environments), 1)

    def test_04_delete_environment(self):
        self.client.delete_environment(gateway=TestEnvironment.gateway,
                                       environment=TestEnvironment.environment,
                                       )
        self.assertEqual(1, len(list(self.client.environments(
            gateway=TestEnvironment.gateway)
        )))
        self.delete_gateway()
