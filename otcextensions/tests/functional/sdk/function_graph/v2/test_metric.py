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
from datetime import datetime

from openstack import _log

from otcextensions.sdk.function_graph.v2 import function
from otcextensions.tests.functional.sdk.function_graph import TestFg

_logger = _log.setup_logging('openstack')


class TestFunctionQuotas(TestFg):
    def test_list_metrics(self):
        m = list(self.client.metrics(filter='monitor_data'))
        self.assertIsNotNone(len(m[0].duration))

    def test_list_func_metrics(self):
        now = datetime.now().timestamp()
        self.function = self.client.create_function(**TestFg.function_attrs)
        assert isinstance(self.function, function.Function)
        self.addCleanup(
            self.client.delete_function,
            self.function
        )
        m = list(self.client.function_metrics(self.function, period=f'{now},{now - 3600}'))
        self.assertGreaterEqual(1, len(m))
