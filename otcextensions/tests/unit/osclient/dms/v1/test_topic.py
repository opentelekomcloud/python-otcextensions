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

from otcextensions.osclient.dms.v1 import topic
from otcextensions.tests.unit.osclient.dms.v1 import fakes


class TestDMSInstanceTopic(fakes.TestDMS):

    def setUp(self):
        super(TestDMSInstanceTopic, self).setUp()
        self.client = self.app.client_manager.dms
        self.instance = fakes.FakeInstance.create_one()
        self.client.find_instance = mock.Mock(return_value=self.instance)


class TestListDMSInstanceTopic(TestDMSInstanceTopic):

    topics = fakes.FakeTopic.create_multiple(3)

    columns = ('ID', 'replication', 'partition', 'retention_time',
               'is_sync_flush', 'is_sync_replication')

    data = []

    for s in topics:
        data.append((
            s.id,
            s.replication,
            s.partition,
            s.retention_time,
            s.is_sync_flush,
            s.is_sync_replication
        ))

    def setUp(self):
        super(TestListDMSInstanceTopic, self).setUp()

        self.cmd = topic.ListDMSInstanceTopic(self.app, None)

        self.client.topics = mock.Mock()

    def test_list_topics(self):
        arglist = [
            'inst'
        ]

        verifylist = [
            ('instance', 'inst')
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.topics.side_effect = [
            self.topics
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_instance.assert_called_once_with(
            'inst', ignore_missing=False)
        self.client.topics.assert_called_once_with(instance=self.instance)

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))


class TestDeleteDMSInstanceTopic(TestDMSInstanceTopic):

    def setUp(self):
        super(TestDeleteDMSInstanceTopic, self).setUp()

        self.cmd = topic.DeleteDMSInstanceTopic(self.app, None)

        self.client.delete_topic = mock.Mock()

    def test_delete(self):
        arglist = ['inst', 't1']
        verifylist = [
            ('instance', 'inst'),
            ('topic', ['t1'])
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.delete_instance.side_effect = [{}]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        calls = [mock.call(instance=self.instance, topics=['t1'])]

        self.client.find_instance.assert_called_with(
            'inst', ignore_missing=False)
        self.client.delete_topic.assert_has_calls(calls)
        self.assertEqual(1, self.client.delete_topic.call_count)

    def test_delete_multiple(self):
        arglist = [
            'inst',
            't1',
            't2',
        ]
        verifylist = [
            ('instance', 'inst'),
            ('topic', ['t1', 't2'])
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.delete_instance.side_effect = [{}, {}]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        calls = [mock.call(instance=self.instance, topics=['t1', 't2'])]

        self.client.find_instance.assert_called_with(
            'inst', ignore_missing=False)
        self.client.delete_topic.assert_has_calls(calls)
        self.assertEqual(1, self.client.delete_topic.call_count)


class TestCreateDMSInstanceTopic(TestDMSInstanceTopic):

    _data = fakes.FakeTopic.create_one()

    columns = ('id', 'is_sync_flush', 'is_sync_replication', 'partition',
               'replication', 'retention_time')

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestCreateDMSInstanceTopic, self).setUp()

        self.cmd = topic.CreateDMSInstanceTopic(self.app, None)

        self.client.create_topic = mock.Mock()

    def test_create_default(self):
        arglist = [
            'inst',
            'topic',
            '--partition', '5',
            '--replication', '3',
            '--retention-time', '8',
            '--enable-sync-flush',
            '--enable-sync-replication'
        ]
        verifylist = [
            ('instance', 'inst'),
            ('id', 'topic'),
            ('partition', 5),
            ('replication', 3),
            ('retention_time', 8),
            ('enable_sync_flush', True),
            ('enable_sync_replication', True),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.create_topic.side_effect = [
            self._data
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_topic.assert_called_with(
            instance=self.instance,
            id='topic',
            is_sync_flush=True,
            is_sync_replication=True,
            partition=5,
            replication=3,
            retention_time=8
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)
