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
from openstack.tests.unit import base

from openstack.tests.unit import test_proxy_base


class TestDMSProxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestDMSProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)

    def test_create_queue(self):
        self.verify_create(self.proxy.create_queue, _queue.Queue,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._create',
            method_kwargs={
                'name': 'queue_001'
            },
            expected_kwargs={
                'name': 'queue_001'
            }
        )

    def test_queues(self):
        self.verify_list(self.proxy.queues, _queue.Queue,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._list',
            expected_kwargs={
            }
        )

    def test_get_queue(self):
        self.verify_get(self.proxy.get_queue, _queue.Queue,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._get',
            expected_kwargs={
            }
        )

    def test_delete_queue(self):
        self.verify_delete(self.proxy.delete_queue, _queue.Queue, True,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._delete',
            expected_kwargs={
            }
        )

    def test_create_groups(self):
        self.verify_create(self.proxy.create_groups,_queue.Group,
            'otcextensions.sdk.dms.v1.queue.Group.create_groups',
            method_kwargs={
                'queue_id': 'queue'
            },
            expected_kwargs={
                'queue_id': 'queue'
            }            
                    #   method_args=['queue'],
                    #   expected_args=[mock.ANY],
                    #   expected_kwargs={'queue_id': 'queue'}
                      )

    def test_groups(self):
        self.verify_list(
            self.proxy.groups, _queue.Group,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._list',
            method_args=['group'],
            expected_kwargs={
                'scaling_group_id': 'group'
            },
            paginated=True,
        )        
        # self._verify2('openstack.proxy2.BaseProxy._list',
        #               self.proxy.groups,
        #               method_args=['queue'],
        #               expected_args=[mock.ANY],
        #               expected_kwargs={'queue_id': 'queue',
        #                                'paginated': False})

    def test_delete_group(self):
        self.verify_delete(
            self.proxy.delete_group, _queue.Group, True,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._delete'
                      #,expected_args=[mock.ANY, 'group'],
                      #expected_kwargs={'queue_id': 'queue'}
			)   
        # self._verify2('openstack.proxy2.BaseProxy._delete',
        #               self.proxy.delete_group,
        #               method_args=['queue', 'group'],
        #               expected_args=[mock.ANY, 'group'],
        #               expected_kwargs={'queue_id': 'queue'})

    # def test_send_messages(self):
    #     self._verify2('openstack.dms.v1.queue.Message.create_messages',
    #                   self.proxy.send_messages,
    #                   method_args=['queue'],
    #                   expected_args=[mock.ANY],
    #                   expected_kwargs={'queue_id': 'queue'})

    # def test_consume_message(self):
    #     self._verify2('openstack.dms.v1.queue.MessageConsume.list',
    #                   self.proxy.consume_message,
    #                   method_args=['queue', 'group'],
    #                   expected_args=[mock.ANY],
    #                   expected_kwargs={'queue_id': 'queue',
    #                                    'consumer_group_id': 'group',
    #                                    'paginated': False})

    def test_ack_consumed_message(self):
        pass

    def test_quotas(self):
        pass
