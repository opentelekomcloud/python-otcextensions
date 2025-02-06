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

        self.addCleanup(
            self.client.delete_function,
            self.function
        )

    def test_export(self):
        inst = self.client.export_function(self.function, type="code")
        self.assertIsNotNone(inst.file_name)
        self.assertIsNotNone(inst.code_url)

    def test_import(self):
        attrs = {
            'func_name': 'test',
            'file_type': 'zip',
            'file_name': 'test.zip',
            'file_code': 'UEsDBBQAAAAIAPBbPFpOs3AMAgEAAEwCAAAGAAAAZGVwLnB5jVHB'
                         'asMwDL37K4R3iSGMMtglsNNW2HH0B4oXq9SjtY2shJbSf5/tpl5y'
                         'GFQX23qS3nuWPQZPDD/ROyGEwR3stTMHpAZHdNxC7x3jiVUnIAXT'
                         '+XbJ8QRfmiIC7xGsCwND6YHGaNaqlhVom3PwVoieD16beCNQYj6O'
                         'bGrP4wL50Ro0kNtqRch4IzfYox0nsJPtjGExboM8kAMNhDF4F7Fi'
                         '90QSdKnJHDKy5iG+e4Oyg5fVql3C396cE7CTH9kOTUI6uPxJuMra'
                         'cp0RFinFvRmOITZ3CZNiPPUYGNblsD6pjoDzr/4sawEk8hRrvjy3'
                         'D9p5/d/OOs9JNiKnxasHLSzJlfgFUEsBAhQDFAAAAAgA8Fs8Wk6z'
                         'cAwCAQAATAIAAAYAAAAAAAAAAAAAAKSBAAAAAGRlcC5weVBLBQYA'
                         'AAAAAQABADQAAAAmAQAAAAA='
        }
        inst = self.client.import_function(**attrs)
        self.assertIsNotNone(inst.file_name)
        self.assertIsNotNone(inst.code_url)
