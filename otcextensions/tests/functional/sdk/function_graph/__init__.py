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

from otcextensions.tests.functional import base


class TestFg(base.BaseFunctionalTest):
    uuid_v4 = uuid.uuid4().hex[:8]
    function_attrs = {
        'func_name': 'test-function-' + uuid_v4,
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

    def setUp(self):
        super(TestFg, self).setUp()
        self.client = self.conn.functiongraph
