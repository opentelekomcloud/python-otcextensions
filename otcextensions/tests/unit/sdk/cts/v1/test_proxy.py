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

from otcextensions.sdk.cts.v1 import _proxy
from otcextensions.sdk.cts.v1 import trace as _trace
from otcextensions.sdk.cts.v1 import tracker as _tracker

from openstack.tests.unit import test_proxy_base


class TestCTSProxy(test_proxy_base.TestProxyBase):

    def setUp(self):
        super(TestCTSProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)

    def test_traces(self):
        self.verify_list(
            self.proxy.traces, _trace.Trace, paginated=True,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._list',
            expected_kwargs={
                'limit': 50,
                'tracker_name': 'system'
            }
        )

    def test_traces_query(self):
        self.verify_list(
            self.proxy.traces, _trace.Trace, paginated=True,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._list',
            method_kwargs={
                'next': '1',
                'limit': '2',
                'service_type': '3',
                'res_type': '4',
                'res_id': '5',
                'res_name': '6',
                'trace_name': '7',
                'from': '8',
                'to': '9',
                'trace_id': '10',
                'level': '11',
                'user': '12'
            },
            expected_kwargs={
                'next': '1',
                'limit': '2',
                'service_type': '3',
                'res_type': '4',
                'res_id': '5',
                'res_name': '6',
                'trace_name': '7',
                'from': '8',
                'to': '9',
                'trace_id': '10',
                'level': '11',
                'user': '12',
                'tracker_name': 'system',
            }
        )

    def test_get_tracker(self):
        self.verify_get(
            self.proxy.get_tracker, _tracker.Tracker,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._get',
            expected_args=[_tracker.Tracker, 'value'],
            expected_kwargs={
                'requires_id': False
            }
        )

    def test_create_tracker(self):
        self.verify_create(
            self.proxy.create_tracker, _tracker.Tracker,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._create',
        )

    def test_update_tracker(self):
        self.verify_update(
            self.proxy.update_tracker, _tracker.Tracker,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._update',
        )

    def test_delete_tracker(self):
        self.verify_delete(
            self.proxy.delete_tracker, _tracker.Tracker, True,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._delete',
        )
