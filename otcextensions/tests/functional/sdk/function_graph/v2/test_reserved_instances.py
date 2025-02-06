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

from openstack import _log

from otcextensions.tests.functional.sdk.function_graph import TestFg

_logger = _log.setup_logging('openstack')


class TestFunctionInstances(TestFg):
    ID = None
    uuid = uuid.uuid4().hex[:8]

    def setUp(self):
        super(TestFunctionInstances, self).setUp()
        self.function = self.client.create_function(**TestFg.function_attrs)
        assert isinstance(self.function, function.Function)

        attrs = {
            "count": 2
        }
        self.instances = self.client.update_instances_number(
            self.function,
            **attrs
        )
        assert isinstance(self.function, function.Function)

        self.addCleanup(
            self.client.delete_function,
            self.function
        )

    def test_instances_config(self):
        inst = list(self.client.reserved_instances_config())
        self.assertEqual(self.function.func_urn, inst[0].function_urn)
        self.assertEqual(False, inst[0].idle_mode)
        self.assertEqual(False, inst[0].idle_mode)
        self.assertEqual(2, inst[0].min_count)
        self.assertEqual("version", inst[0].qualifier_type)
        self.assertEqual("latest", inst[0].qualifier_name)

    def test_instances(self):
        inst = list(self.client.reserved_instances())
        self.assertEqual(self.function.func_urn, inst[0].func_urn)
        self.assertEqual(2, inst[0].count)
