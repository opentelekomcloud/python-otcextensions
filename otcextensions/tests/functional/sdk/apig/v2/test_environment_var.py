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


class TestEnvironmentVar(TestApiG):
    environment = None

    def setUp(self):
        super(TestEnvironmentVar, self).setUp()
        self.create_gateway()
        self.gateway_id = TestEnvironmentVar.gateway.id
        # self.gateway_id = "be76ca6de5fe4aa7af503c03b3b44dea"
        env_attrs = {
            "name": "DEV",
            "remark": "Development environment"
        }
        environment = self.client.create_environment(
            gateway=self.gateway_id,
            **env_attrs)
        self.assertIsNotNone(environment.id)

        group_attrs = {
            "name": "api_group_001",
            "remark": "API group 1"
        }
        self.group = self.client.create_api_group(
            gateway=self.gateway_id,
            **group_attrs
        )
        self.assertIsNotNone(self.group.id)

        self.attrs = {
            "variable_name" : "address",
            "variable_value" : "192.168.1.5",
            "env_id" : environment.id,
            "group_id" : self.group.id
        }
        self.variable = self.client.create_environment_variable(
            gateway=self.gateway_id,
            **self.attrs
        )

        self.addCleanup(
            self.client.delete_environment_variable,
            gateway=self.gateway_id,
            var=self.variable
        )
        self.addCleanup(
            self.client.delete_environment,
            gateway=self.gateway_id,
            environment=environment.id,
        )
        self.addCleanup(
            self.client.delete_api_group,
            gateway=self.gateway_id,
            api_group=self.group.id,
        )

    def test_list_environment_variables(self):
        vars = list(self.client.environment_variables(
            gateway=self.gateway_id,
            group_id=self.group.id))
        self.assertEqual(len(vars), 1)

    def test_get_environment_variable(self):
        var = self.client.get_environment_variable(
            gateway=self.gateway_id,
            var=self.variable.id)
        self.assertEqual(var.id, self.variable.id)

    def test_update_environment_variable(self):
        attrs = {
            "variable_value": "192.168.1.6",
        }
        updated = self.client.update_environment_variable(
            gateway=self.gateway_id,
            var=self.variable.id,
            **attrs
        )
        self.assertEqual(updated.variable_value, attrs["variable_value"])
