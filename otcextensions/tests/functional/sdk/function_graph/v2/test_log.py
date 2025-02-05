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

from otcextensions.sdk.function_graph.v2 import function
from otcextensions.sdk.function_graph.v2 import log

from openstack import _log

from otcextensions.tests.functional.sdk.function_graph import TestFg

_logger = _log.setup_logging('openstack')


class TestFunctionLog(TestFg):

    def setUp(self):
        super(TestFunctionLog, self).setUp()
        self.function = self.client.create_function(**TestFg.function_attrs)
        assert isinstance(self.function, function.Function)

        self.log = self.client.enable_lts_log()
        assert isinstance(self.log, log.Log)
        self.addCleanup(
            self.client.delete_function,
            self.function
        )

    def test_get_lts_log_details(self):
        lg = self.client.get_lts_log_settings(
            self.function)
        self.assertIsNotNone(lg)
