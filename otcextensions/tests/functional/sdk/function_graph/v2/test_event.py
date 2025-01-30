# Licensed under the Apache License, Version 2.0 (the 'License'); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import uuid
from otcextensions.sdk.function_graph.v2 import function
from otcextensions.tests.functional import base

from openstack import _log

_logger = _log.setup_logging('openstack')


class TestFunctionEvent(base.BaseFunctionalTest):
    ID = None
    uuid = uuid.uuid4().hex[:8]

    def setUp(self):
        super(TestFunctionEvent, self).setUp()
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

        self.event_attrs = {
            'name': 'event-xx',
            'content': 'eyJrIjoidiJ9'
        }
        self.event = self.conn.functiongraph.create_event(
            self.function, **self.event_attrs
        )
        self.ID = self.event.id

        self.addCleanup(
            self.conn.functiongraph.delete_function,
            self.function
        )
        self.addCleanup(
            self.conn.functiongraph.delete_event,
            self.function, self.event
        )

    def test_function_events(self):
        elist = list(self.conn.functiongraph.events(
            func_urn=self.function.func_urn))
        self.assertIn(self.ID, elist[0].events[0].id)

    def test_get_function_event(self):
        e = self.conn.functiongraph.get_event(
            self.function, self.event)
        self.assertIn(self.ID, e.id)

    def test_update_function_event(self):
        event_attrs = {
            'content': 'ewogICAgImJvZHkiOiAiIiwKICAgICJy'
        }
        updated = self.conn.functiongraph.update_event(
            self.function, self.event, **event_attrs)
        self.assertIn(event_attrs['content'], updated.content)
