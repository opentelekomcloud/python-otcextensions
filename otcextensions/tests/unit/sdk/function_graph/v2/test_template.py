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

from otcextensions.sdk.function_graph.v2 import template


EXAMPLE = {
    "id": "41d5d9ca-cea3-4ba9-b866-e30c46f45f1f",
    "type": 1,
    "title": "access-mysql",
    "template_name": "access-mysql-js-12.13",
    "runtime": "Node.js12.13",
    "handler": "index.handler",
    "code_type": "",
    "code": "",
    "timeout": 30,
    "memory_size": 256,
    "temp_detail": {
        "input": "None",
        "output": "Execution successful: Database query results",
        "warning": ""
    },
    "scene": "basic_function_usage",
    "service": "FunctionGraph"
}


class TestFunctionInvocation(base.TestCase):

    def test_basic(self):
        sot = template.Template()
        path = 'fgs/templates/%(template_id)s'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_fetch)

    def test_make_it(self):
        sot = template.Template(**EXAMPLE)
        self.assertEqual(EXAMPLE['id'], sot.id)
        self.assertEqual(EXAMPLE['type'], sot.type)
        self.assertEqual(EXAMPLE['title'], sot.title)
        self.assertEqual(EXAMPLE['template_name'], sot.template_name)
