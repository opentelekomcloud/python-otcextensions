#   Copyright 2013 Nebula Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
import mock

from otcextensions.osclient.dms.v1 import queue
from otcextensions.tests.unit.osclient.dms.v1 import fakes


class TestDMSQueue(fakes.TestDMS):

    def setUp(self):
        super(TestDMSQueue, self).setUp()
        self.client = self.app.client_manager.dms


class TestListDMSQueue(TestDMSQueue):

    queues = fakes.FakeQueue.create_multiple(3)

    columns = ('ID', 'name', 'queue_mode', 'description', 'redrive_policy',
               'max_consume_count', 'retention_hours')

    data = []

    for s in queues:
        data.append((
            s.id,
            s.name,
            s.queue_mode,
            s.description,
            s.redrive_policy,
            s.max_consume_count,
            s.retention_hours
        ))

    def setUp(self):
        super(TestListDMSQueue, self).setUp()

        self.cmd = queue.ListDMSQueue(self.app, None)

        self.client.queues = mock.Mock()

    def test_list_queue(self):
        arglist = [
        ]

        verifylist = [
            # ('group', None),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.queues.side_effect = [
            self.queues
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.queues.assert_called_once_with()

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))


class TestShowDMSQueue(TestDMSQueue):

    _data = fakes.FakeQueue.create_one()

    columns = ('ID', 'name', 'queue_mode', 'description', 'redrive_policy',
               'max_consume_count', 'retention_hours')

    data = (
        _data.id,
        _data.name,
        _data.queue_mode,
        _data.description,
        _data.redrive_policy,
        _data.max_consume_count,
        _data.retention_hours
    )

    def setUp(self):
        super(TestShowDMSQueue, self).setUp()

        self.cmd = queue.ShowDMSQueue(self.app, None)

        self.client.show_queue = mock.Mock()

    def test_show_default(self):
        arglist = [
            'test_queue'
        ]
        verifylist = [
            ('queue', 'test_queue')
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.get_queue.side_effect = [
            self._data
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.get_queue.assert_called()

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestDeleteDMSQueue(TestDMSQueue):

    def setUp(self):
        super(TestDeleteDMSQueue, self).setUp()

        self.cmd = queue.DeleteDMSQueue(self.app, None)

        self.client.delete_queue = mock.Mock()

    def test_delete(self):
        arglist = ['t1']
        verifylist = [
            ('queue', ['t1'])
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.delete_queue.side_effect = [{}]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        calls = [mock.call('t1')]

        self.client.delete_queue.assert_has_calls(calls)
        self.assertEqual(1, self.client.delete_queue.call_count)

    def test_delete_multiple(self):
        arglist = [
            't1',
            't2',
        ]
        verifylist = [
            ('queue', ['t1', 't2'])
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.delete_queue.side_effect = [{}, {}]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        calls = [mock.call('t1'), mock.call('t2')]

        self.client.delete_queue.assert_has_calls(calls)
        self.assertEqual(2, self.client.delete_queue.call_count)


class TestCreateDMSQueue(TestDMSQueue):

    _data = fakes.FakeQueue.create_one()

    columns = ('ID', 'name', 'queue_mode', 'description', 'redrive_policy',
               'max_consume_count', 'retention_hours')

    data = (
        _data.id,
        _data.name,
        _data.queue_mode,
        _data.description,
        _data.redrive_policy,
        _data.max_consume_count,
        _data.retention_hours
    )

    def setUp(self):
        super(TestCreateDMSQueue, self).setUp()

        self.cmd = queue.CreateDMSQueue(self.app, None)

        self.client.create_queue = mock.Mock()

    def test_show_default(self):
        arglist = [
            'name',
            'NORMAL',
            '--description', 'descr',
            '--redrive_policy', 'enable',
            '--max_consume_count', '1',
            '--retention_hours', '2'
        ]
        verifylist = [
            ('name', 'name'),
            ('queue_mode', 'NORMAL'),
            ('description', 'descr'),
            ('redrive_policy', 'enable'),
            ('max_consume_count', 1),
            ('retention_hours', 2)
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.create_queue.side_effect = [
            self._data
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_queue.assert_called_with(
            description='descr',
            max_consume_count=1,
            name='name',
            queue_mode='NORMAL',
            redrive_policy='enable',
            retention_hours=2
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)
