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

from otcextensions.sdk.function_graph.v2 import function


EXAMPLE = {
    'func_name': 'test-function',
    'package': 'default',
    'runtime': 'Python3.9',
    'handler': 'index.handler',
    'timeout': 30,
    'memory_size': 128,
    'code_type': 'inline',
}


class TestFunction(base.TestCase):

    def test_basic(self):
        sot = function.Function()
        self.assertEqual('functions', sot.resources_key)
        path = '/fgs/functions'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = function.Function(**EXAMPLE)
        self.assertEqual(EXAMPLE['func_name'], sot.func_name)
        self.assertEqual(EXAMPLE['package'], sot.package)
        self.assertEqual(EXAMPLE['runtime'], sot.runtime)
        self.assertEqual(EXAMPLE['handler'], sot.handler)
        self.assertEqual(EXAMPLE['timeout'], sot.timeout)
        self.assertEqual(EXAMPLE['memory_size'], sot.memory_size)
        self.assertEqual(EXAMPLE['code_type'], sot.code_type)
