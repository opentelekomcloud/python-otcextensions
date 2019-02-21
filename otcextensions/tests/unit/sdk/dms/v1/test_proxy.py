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

import mock

from otcextensions.sdk.dms.v1 import _proxy
from otcextensions.sdk.dms.v1 import queue as _queue

from openstack.tests.unit import test_proxy_base

GROUP_ID = 'g-5ec247fd-d4a2-4d4f-9876-e4ff3280c461'


class TestDMSProxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestDMSProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)

    def test_create_queue(self):
        self.verify_create(
            self.proxy.create_queue,
            _queue.Queue,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._create',
            method_kwargs={
                'name': 'queue_001'
            },
            expected_kwargs={
                'name': 'queue_001'
            }
        )

    def test_queues(self):
        self.verify_list(
            self.proxy.queues,
            _queue.Queue,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._list',
            expected_kwargs={
                'paginated': False
            }
        )

    def test_get_queue(self):
        self.verify_get(
            self.proxy.get_queue,
            _queue.Queue,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._get',
            expected_kwargs={}
        )

    def test_delete_queue(self):
        self.verify_delete(
            self.proxy.delete_queue,
            _queue.Queue,
            True,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._delete',
            expected_kwargs={}
        )

    def test_create_group(self):
        self._verify2(
            'otcextensions.sdk.dms.v1.group.Group.create',
            self.proxy.create_group,
            method_args=['queue', 'name'],
            expected_args=[mock.ANY],
            expected_kwargs={'group': 'name'})

    def test_groups(self):
        self._verify2(
            'otcextensions.sdk.sdk_proxy.Proxy._list',
            self.proxy.groups,
            method_args=['queue'],
            expected_args=[mock.ANY],
            expected_kwargs={
                'queue_id': 'queue',
                'paginated': False,
                'include_deadletter': False})

    def test_delete_group(self):
        self._verify2(
            'otcextensions.sdk.sdk_proxy.Proxy._delete',
            self.proxy.delete_group,
            method_args=['queue', 'group'],
            expected_args=[mock.ANY, 'group'],
            expected_kwargs={'queue_id': 'queue'})

    def test_send_messages(self):
        self._verify2(
            'otcextensions.sdk.sdk_proxy.Proxy._create',
            self.proxy.send_messages,
            method_args=['queue'],
            expected_args=[mock.ANY],
            expected_kwargs={'queue_id': 'queue'})

    def test_consume_message(self):
        self._verify2(
            'otcextensions.sdk.dms.v1.group_message.GroupMessage.list',
            self.proxy.consume_message,
            method_args=['queue', 'group'],
            expected_args=[mock.ANY],
            expected_kwargs={
                'queue_id': 'queue',
                'consumer_group_id': 'group',
                'endpoint_override': None,
                'headers': None,
                'paginated': False,
                'requests_auth': None})

    def test_ack_consumed_message(self):
        pass

    def test_quotas(self):
        pass
