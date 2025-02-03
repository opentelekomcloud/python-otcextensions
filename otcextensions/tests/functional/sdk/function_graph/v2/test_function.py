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
        self.attrs = {
            'func_name': 'test-function-' + self.uuid,
            'package': 'default',
            'runtime': 'Python3.9',
            'handler': 'index.handler',
            'timeout': 30,
            'memory_size': 128,
            'code_type': 'inline',
        }

        self.NAME = 'test-function-' + self.uuid
        self.UPDATE_NAME = 'test-function-upd-' + self.uuid

        self.function = self.conn.functiongraph.create_function(**self.attrs)
        assert isinstance(self.function, function.Function)
        self.assertEqual(self.NAME, self.function.func_name)
        self.ID = self.function.func_id
        self.addCleanup(self.conn.functiongraph.delete_function, self.function)

    def test_get_function_code(self):
        found = self.conn.functiongraph.get_function_code(self.function)
        self.assertEqual(found.code_type, self.attrs['code_type'])
        self.assertEqual(found.runtime, self.attrs['runtime'])

    def test_get_function_metadata(self):
        found = self.conn.functiongraph.get_function_metadata(self.function)
        self.assertEqual(found.is_stateful_function, False)
        self.assertEqual(found.enable_dynamic_memory, False)

    def test_resource_tags(self):
        self.conn.functiongraph.create_resource_tags(
            self.function,
            tags=[
                {
                    'key': 'key',
                    'value': 'value'
                },
                {
                    'key': 'testKey2',
                    'value': 'testValue2'
                }
            ]
        )
        found = self.conn.functiongraph.get_resource_tags(self.function)
        self.assertEqual(len(found.tags), 2)
        self.conn.functiongraph.delete_resource_tags(
            self.function,
            tags=[
                {
                    'key': 'testKey2',
                    'value': 'testValue2'
                }
            ]
        )
        found = self.conn.functiongraph.get_resource_tags(self.function)
        self.assertEqual(len(found.tags), 1)

    def test_list_functions(self):
        functions = list(self.conn.functiongraph.functions())
        self.assertIn(self.NAME, functions[0].func_name)

    def test_update_function(self):
        code_attrs = {
            'code_filename': 'index.zip',
            'code_type': 'inline',
            'func_code': {
                'file': 'UEsDBAoAAAAIAPQ1M1gNImPLrAAAAAEBAAAIAAAAaW5kZXgucHlN'
                        'jtEOgjAMRd/5igVfxDAlxhjDo0S/wB+YrMgMdMvWGYnh390wEfrU'
                        '3nvb0xXjG85qLRU+Sk8NP0UhUb3RltjTaUwkNKwVKDuwbA0vQMrD'
                        'AhK8KSsTFsoCeYvsMw2xUkeCvKu0hLRk+6LIZ0u5s3BwPFwwUEEG'
                        '/yo6B4vEXcshyBG+lb437kfNFpEWhATrQmqGTkYVH0Pit8FEdCqM'
                        '6VQtSGncxYPpPz5O3fgFUEsBAh4DCgAAAAgA9DUzWA0iY8usAAAA'
                        'AQEAAAgAAAAAAAAAAAAAAPMCAAAAAGluZGV4LnB5UEsFBgAAAAAB'
                        'AAEANgAAANIAAAAAAA=='
            }
        }
        code = self.conn.functiongraph.update_function_code(
            self.function, **code_attrs)
        self.assertIsNotNone(code)
        self.assertEqual(code.code_type, code_attrs['code_type'])

        metadata_attrs = {
            'memory_size': 768,
            'handler': 'index.handler',
            'runtime': 'Python3.9',
            'mount_config': {
                'mount_user': {
                    'user_id': -1,
                    'user_group_id': -1
                },
            },
            'timeout': 40
        }
        metadata = self.conn.functiongraph.update_function_metadata(
            self.function, **metadata_attrs)
        self.assertIsNotNone(metadata)
        self.assertEqual(metadata.handler, metadata_attrs['handler'])
        self.assertEqual(metadata.memory_size, metadata_attrs['memory_size'])
        self.assertEqual(metadata.runtime, metadata_attrs['runtime'])
        self.assertEqual(metadata.timeout, metadata_attrs['timeout'])

        instances = self.conn.functiongraph.update_max_instances(
            self.function, 300)
        self.assertIsNotNone(instances)
        self.assertEqual(metadata.strategy_config['concurrency'], 300)
