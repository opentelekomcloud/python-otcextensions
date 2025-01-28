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


class TestFunctionInvocation(base.BaseFunctionalTest):
    ID = None
    uuid = uuid.uuid4().hex[:8]

    def setUp(self):
        super(TestFunctionInvocation, self).setUp()
        self.attrs = {
            'func_name': 'test-function-' + self.uuid,
            'package': 'default',
            'runtime': 'Python3.9',
            'handler': 'index.handler',
            'timeout': 30,
            'memory_size': 128,
            'code_type': 'inline',
            'func_code': {
                'file': 'CmltcG9ydCBqc29uCgpkZWYgaGFuZGxlcihldmVudCwgY29udGV4d'
                        'Ck6CiAgICB0cnk6CiAgICAgICAgIyBQYXJzZSB0aGUgaW5wdXQgZX'
                        'ZlbnQgKGRhdGEpCiAgICAgICAgaW5wdXRfZGF0YSA9IGpzb24ubG9'
                        'hZHMoZXZlbnQpCiAgICAgICAgCiAgICAgICAgIyBQcmludCB0aGUg'
                        'cHJvdmlkZWQgZGF0YQogICAgICAgIHByaW50KCJSZWNlaXZlZCBkY'
                        'XRhOiIsIGlucHV0X2RhdGEpCiAgICAgICAgCiAgICAgICAgIyBSZX'
                        'R1cm4gYSByZXNwb25zZQogICAgICAgIHJlc3BvbnNlID0gewogICA'
                        'gICAgICAgICAic3RhdHVzQ29kZSI6IDIwMCwKICAgICAgICAgICAg'
                        'ImJvZHkiOiBmIkRhdGEgcmVjZWl2ZWQ6IHtpbnB1dF9kYXRhfSIKI'
                        'CAgICAgICB9CiAgICAgICAgcmV0dXJuIGpzb24uZHVtcHMocmVzcG'
                        '9uc2UpCgogICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBlOgogICAgICA'
                        'gICMgSGFuZGxlIGVycm9ycwogICAgICAgIGVycm9yX3Jlc3BvbnNl'
                        'ID0gewogICAgICAgICAgICAic3RhdHVzQ29kZSI6IDUwMCwKICAgI'
                        'CAgICAgICAgImJvZHkiOiBmIkVycm9yOiB7c3RyKGUpfSIKICAgIC'
                        'AgICB9CiAgICAgICAgcmV0dXJuIGpzb24uZHVtcHMoZXJyb3JfcmV'
                        'zcG9uc2UpCg=='
            }
        }

        self.NAME = 'test-function-' + self.uuid
        self.UPDATE_NAME = 'test-function-upd-' + self.uuid

        self.function = self.conn.functiongraph.create_function(**self.attrs)
        assert isinstance(self.function, function.Function)
        self.assertEqual(self.NAME, self.function.func_name)
        self.ID = self.function.func_id
        self.addCleanup(self.conn.functiongraph.delete_function, self.function)

    def test_function_invoke_sync(self):
        inv = self.conn.functiongraph.executing_function_synchronously(
            self.function.func_urn, attrs={'a': 'b'}
        )
        self.assertEqual(inv.err_code, '0')
        self.assertEqual(inv.err, 'false')

    def test_function_invoke_async(self):
        inv = self.conn.functiongraph.executing_function_asynchronously(
            self.function.func_urn, attrs={'a': 'b'}
        )
        self.assertIsNotNone(inv.request_id)
