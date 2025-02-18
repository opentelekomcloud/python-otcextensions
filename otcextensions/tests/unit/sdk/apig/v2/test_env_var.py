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
from openstack.tests.unit import base
from otcextensions.sdk.apig.v2 import apienvironmentvar as var

EXAMPLE_VAR = {
    "variable_value" : "192.168.1.5",
    "env_id" : "7a1ad0c350844ee69479b47df9a881cb",
    "group_id" : "c77f5e81d9cb4424bf704ef2b0ac7600",
    "id" : "25054838a624400bbf2267cf5b3a3f70",
    "variable_name" : "address"
}


class TestApiEnvironment(base.TestCase):

    def test_basic(self):
        sot = var.ApiEnvironmentVar()
        self.assertEqual(
            '/apigw/instances/%(gateway_id)s/env-variables',
            sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_fetch)
        self.assertEqual('variables', sot.resources_key)

    def test_make_it(self):
        sot = var.ApiEnvironmentVar(**EXAMPLE_VAR)
        self.assertEqual(EXAMPLE_VAR['variable_value'], sot.variable_value)
        self.assertEqual(EXAMPLE_VAR['env_id'], sot.env_id)
        self.assertEqual(EXAMPLE_VAR['group_id'], sot.group_id)
        self.assertEqual(EXAMPLE_VAR['id'], sot.id)
        self.assertEqual(EXAMPLE_VAR['variable_name'], sot.variable_name)
