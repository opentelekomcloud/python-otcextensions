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
import uuid
from otcextensions.sdk.function_graph.v2 import function
from otcextensions.tests.functional import base

from openstack import _log

_logger = _log.setup_logging('openstack')


class TestFunction(base.BaseFunctionalTest):
    ID = None
    uuid = uuid.uuid4().hex[:8]

    def setUp(self):
        super(TestFunction, self).setUp()
        #   "func_name" : "xxx",
        #   "package" : "xxx",
        #   "runtime" : "Python2.7",
        #   "handler" : "index.py",
        #   "type" : "v2",
        #   "memory_size" : 128,
        #   "timeout" : 3,
        #   "code_type" : "inline",
        attrs = {
            'func_name': "test-function-" + self.uuid,
            'package': 'default',
            'runtime': 'Python3.9',
            'handler': 'index.handler',
            'timeout': 30,
            'memory_size': 128,
            'code_type': 'inline',
        }

        self.NAME = "test-function-" + self.uuid
        self.UPDATE_NAME = "test-function-upd-" + self.uuid

        self.function = self.conn.functiongraph.create_function(**attrs)
        assert isinstance(self.function, function.Function)
        self.assertEqual(self.NAME, self.function.func_name)
        self.ID = self.function.func_id
        self.addCleanup(self.conn.functiongraph.delete_function, self.function)

    # def tearDown(self):
    #     super(TestFunction, self).tearDown()
    #     self.conn.functiongraph.delete_function(self.function)

    def test_find_function(self):
        found = self.conn.functiongraph.find_function(self.NAME)
        self.assertEqual(found.id, self.ID)

    def test_get_function(self):
        found = self.conn.functiongraph.get_function(self.ID)
        self.assertEqual(found.func_name, self.NAME)
        self.assertEqual(found.id, self.ID)

    def test_list_functions(self):
        functions = [f.func_name for f in self.conn.functiongraph.functions()]
        self.assertIn(self.NAME, functions)

    def test_update_function(self):
        new_attrs = {
            'func_name': self.UPDATE_NAME,
            'timeout': 60,
            'memory_size': 256
        }
        updated = self.conn.functiongraph.update_function(self.ID, **new_attrs)
        self.assertEqual(updated.func_name, new_attrs['func_name'])
        self.assertEqual(updated.timeout, new_attrs['timeout'])
        self.assertEqual(updated.memory_size, new_attrs['memory_size'])
