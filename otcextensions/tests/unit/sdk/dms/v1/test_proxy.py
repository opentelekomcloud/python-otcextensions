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
from unittest import mock

from otcextensions.sdk.dms.v1 import _proxy
from otcextensions.sdk.dms.v1 import az as _az
from otcextensions.sdk.dms.v1 import group as _group
from otcextensions.sdk.dms.v1 import instance as _instance
from otcextensions.sdk.dms.v1 import maintenance_window as _mw
from otcextensions.sdk.dms.v1 import message as _message
from otcextensions.sdk.dms.v1 import product as _product
from otcextensions.sdk.dms.v1 import queue as _queue
from otcextensions.sdk.dms.v1 import topic as _topic

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
        )

    def test_queues(self):
        self.verify_list(
            self.proxy.queues,
            _queue.Queue,
            expected_kwargs={
                'paginated': False
            }
        )

    def test_queues_qp(self):
        self.verify_list(
            self.proxy.queues,
            _queue.Queue,
            method_kwargs={
                'include_deadletter': True,
            },
            expected_kwargs={
                'include_deadletter': True,
                'paginated': False
            }
        )

    def test_get_queue(self):
        self.verify_get(
            self.proxy.get_queue,
            _queue.Queue
        )

    def test_delete_queue(self):
        self.verify_delete(
            self.proxy.delete_queue,
            _queue.Queue,
            False
        )

    def test_delete_queue_ignore(self):
        self.verify_delete(
            self.proxy.delete_queue,
            _queue.Queue,
            True
        )

    def test_create_group(self):
        self.verify_create(
            self.proxy.create_group,
            _group.Group,
            method_kwargs={'queue': 'qip', 'name': 'grp'},
            expected_kwargs={'queue_id': 'qip', 'name': 'grp'})

    def test_groups(self):
        self.verify_list(
            self.proxy.groups,
            _group.Group,
            method_kwargs={'queue': 'qid'},
            expected_kwargs={
                'queue_id': 'qid',
                'paginated': False}
        )

    def test_delete_group(self):
        self.verify_delete(
            self.proxy.delete_group,
            _group.Group,
            False,
            method_args=['QID', 'resource_or_id'],
            expected_kwargs={
                'ignore_missing': False,
                'queue_id': 'QID'
            },
            expected_args=['resource_or_id']
        )

    def test_delete_group_ignore(self):
        self.verify_delete(
            self.proxy.delete_group,
            _group.Group,
            ignore_missing=True,
            method_args=['QID', 'resource_or_id'],
            expected_kwargs={
                'ignore_missing': True,
                'queue_id': 'QID'
            },
            expected_args=['resource_or_id']
        )

    ######
    # Messages

    def test_send_messages_dict(self):
        self.verify_create(
            self.proxy.send_messages,
            _message.Messages,
            method_kwargs={
                'queue': 'qid',
                'messages': [{
                    'body': 'b1',
                    'attributes': {
                        'attribute1': 'value1',
                        'attribute2': 'value2'}
                }]
            },
            expected_kwargs={
                'queue_id': 'qid',
                'messages': [{
                    'body': 'b1',
                    'attributes': {
                        'attribute1': 'value1',
                        'attribute2': 'value2'}
                }],
                'return_id': False
            }
        )

    def test_send_messages_msg(self):
        self.verify_create(
            self.proxy.send_messages,
            _message.Messages,
            method_kwargs={
                'queue': 'qid',
                'messages': [
                    _message.Message(
                        body='b1',
                        attributes={
                            'attribute1': 'value1',
                            'attribute2': 'value2'}
                    )
                ]
            },
            expected_kwargs={
                'queue_id': 'qid',
                'messages': [{
                    'body': 'b1',
                    'attributes': {
                        'attribute1': 'value1',
                        'attribute2': 'value2'}
                }],
                'return_id': False
            }
        )

    def test_send_message(self):
        value = _message.Message(id='1')
        self._verify(
            'openstack.proxy.Proxy._create',
            self.proxy.send_message,
            method_kwargs={
                'queue': 'qid',
                'body': 'b1',
                'attributes': {
                    'p1': 'v1'
                }
            },
            expected_kwargs={
                'queue_id': 'qid',
                'messages': [
                    {'attributes': {'p1': 'v1'}, 'body': 'b1'}
                ],
                'return_id': True
            },
            method_result=value,
            expected_result=_message.Messages(
                messages=[value]),
            expected_args=[_message.Messages]
        )

    def test_consume_message(self):
        self.verify_list(
            self.proxy.consume_message,
            _message.Message,
            method_kwargs={
                'queue': 'qid',
                'group': 'gid'
            },
            expected_kwargs={
                'queue_id': 'qid',
                'group_id': 'gid'
            },
            base_path='/queues/%(queue_id)s/groups/%(group_id)s/messages'
        )

    def test_ack_consumed_message(self):
        pass

    def test_quotas(self):
        pass

    ######
    # Instances
    def test_instances(self):
        self.verify_list(
            self.proxy.instances,
            _instance.Instance,
            expected_kwargs={
                'paginated': False
            }
        )

    def test_create_instance(self):
        self.verify_create(
            self.proxy.create_instance,
            _instance.Instance
        )

    def test_delete_instance(self):
        self.verify_delete(
            self.proxy.delete_instance,
            _instance.Instance,
            False,
        )

    def test_delete_instance_ignore(self):
        self.verify_delete(
            self.proxy.delete_instance,
            _instance.Instance,
            True,
        )

    def test_find_instance(self):
        self.verify_find(
            self.proxy.find_instance,
            _instance.Instance
        )

    def test_get_instance(self):
        self.verify_get(
            self.proxy.get_instance,
            _instance.Instance
        )

    def test_update_instance(self):
        self.verify_update(
            self.proxy.update_instance,
            _instance.Instance
        )

    def test_restart_instance(self):
        self._verify(
            'otcextensions.sdk.dms.v1.instance.Instance._action',
            self.proxy.restart_instance,
            method_args=['value'],
            expected_args=[self.proxy, 'restart', ['value']]
        )

    def test_restart_instances(self):
        self._verify(
            'otcextensions.sdk.dms.v1.instance.Instance._action',
            self.proxy.restart_instances,
            method_args=[['1', '2']],
            expected_args=[self.proxy, 'restart', ['1', '2']]
        )

    def test_delete_failed(self):
        self._verify(
            'otcextensions.sdk.dms.v1.instance.Instance.delete_failed',
            self.proxy.delete_failed,
            method_args=[]
        )

    def test_delete_batch(self):
        self._verify(
            'otcextensions.sdk.dms.v1.instance.Instance._action',
            self.proxy.delete_batch,
            method_args=[['1', '2']],
            expected_args=[self.proxy, 'delete', ['1', '2']]
        )

    def test_create_topic(self):
        self.verify_create(
            self.proxy.create_topic,
            _topic.Topic,
            method_args=['iid'],
            expected_kwargs={'instance_id': 'iid', 'x': 1, 'y': 2, 'z': 3},
            expected_args=[]
        )

    @mock.patch('otcextensions.sdk.dms.v1._proxy.Proxy.post')
    def test_delete_topics(self, post_mock):
        response = mock.Mock()
        response.status_code = 200
        post_mock.return_value = response
        self.proxy.delete_topic('instance', ['t1', 't2'])

        post_mock.assert_called_with(
            '/instances/instance/topics/delete',
            json={'topics': ['t1', 't2']})

        self.proxy.delete_topic('instance', 't1')

        post_mock.assert_called_with(
            '/instances/instance/topics/delete',
            json={'topics': ['t1']})

    def test_topics(self):
        self.verify_list(
            self.proxy.topics,
            _topic.Topic,
            method_args=['iid'],
            expected_kwargs={
                'instance_id': 'iid'
            },
            expected_args=[]
        )

    # Misc
    def test_az(self):
        self.verify_list(
            self.proxy.availability_zones,
            _az.AvailabilityZone,
        )

    def test_products(self):
        self.verify_list(
            self.proxy.products,
            _product.Product
        )

    def test_mws(self):
        self.verify_list(
            self.proxy.maintenance_windows,
            _mw.MaintenanceWindow
        )
