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

from otcextensions.sdk.function_graph.v2 import function_invocation


EXAMPLE = {
    'func_urn': 'test-function',
    'attrs': {'a': 'b'}
}


class TestFunction(base.TestCase):

    def test_basic(self):
        sot = function_invocation.FunctionInvocation()
        path = '/fgs/functions/%(func_urn)s'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_create)

    def test_make_it(self):
        sot = function_invocation.FunctionInvocation(**EXAMPLE)
        self.assertEqual(EXAMPLE['func_urn'], sot.func_urn)
