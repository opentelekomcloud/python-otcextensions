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


class TestFunctionAsyncNotification(TestFg):
    ID = None
    uuid = uuid.uuid4().hex[:8]

    def setUp(self):
        super(TestFunctionAsyncNotification, self).setUp()
        self.function = self.client.create_function(**TestFg.function_attrs)
        assert isinstance(self.function, function.Function)

        enable = self.conn.functiongraph.configure_async_notification(
            self.function,
            max_async_event_age_in_seconds=1000,
            # enable_async_status_log=True
        )
        self.assertIsNotNone(enable)

        self.inv = self.conn.functiongraph.executing_function_asynchronously(
            self.function.func_urn, attrs={'a': 'b'}
        )
        self.assertIsNotNone(self.inv.request_id)

        self.addCleanup(
            self.client.delete_function,
            self.function
        )
        self.addCleanup(
            self.client.delete_async_notification,
            self.function
        )

    def test_async_notifications(self):
        notifications = list(self.client.async_notifications(
            self.function.func_urn))
        self.assertIn(self.function.func_urn, notifications[0].func_urn)

    def test_all_versions_async_notifications(self):
        notifications = list(self.client.all_versions_async_notifications(
            self.function.func_urn))
        self.assertIn(self.function.func_urn, notifications[0].func_urn)

    def test_async_invocation_requests(self):
        requests = list(self.client.async_invocation_requests(
            self.function, **{'request_id': self.inv.request_id}))
        self.assertIsNotNone(requests)

    # def test_stop_async_invocation_request(self):
    #     stop = self.client.stop_async_invocation_request(
    #         self.function, request_id=self.inv.request_id)
    #     self.assertIsNone(stop)
