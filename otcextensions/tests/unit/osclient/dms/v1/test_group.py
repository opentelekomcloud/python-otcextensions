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

from otcextensions.osclient.dms.v1 import group
from otcextensions.tests.unit.osclient.dms.v1 import fakes


class TestGroup(fakes.TestDMS):

    def setUp(self):
        super(TestGroup, self).setUp()
        self.client = self.app.client_manager.dms


class TestListGroup(TestGroup):

    groups = fakes.FakeGroup.create_multiple(3)
    queue = fakes.FakeQueue.create_one()

    columns = ('ID', 'name', 'produced_messages', 'consumed_messages',
               'available_messages')
    columns_with_dead = ('ID', 'name', 'produced_messages',
                         'consumed_messages', 'available_messages',
                         'produced_deadletters', 'available_deadletters')

    data = []
    data_with_dead = []

    for s in groups:
        data.append((
            s.id,
            s.name,
            s.produced_messages,
            s.consumed_messages,
            s.available_messages,
        ))
        data_with_dead.append((
            s.id,
            s.name,
            s.produced_messages,
            s.consumed_messages,
            s.available_messages,
            s.produced_deadletters,
            s.available_deadletters,
        ))

    def setUp(self):
        super(TestListGroup, self).setUp()

        self.cmd = group.ListGroup(self.app, None)

        self.client.groups = mock.Mock()
        self.client.find_queue = mock.Mock()

    def test_list_group(self):
        arglist = [
            'queue_id'
        ]

        verifylist = [
            ('queue', 'queue_id'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.groups.side_effect = [
            self.groups
        ]
        self.client.find_queue.side_effect = [
            self.queue
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.groups.assert_called_once_with(
            queue=self.queue.id,
            include_deadletter=False)

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))

    def test_list_group_ext(self):
        arglist = [
            'queue_id',
            '--include_deadletter'
        ]

        verifylist = [
            ('queue', 'queue_id'),
            ('include_deadletter', True)
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.groups.side_effect = [
            self.groups
        ]
        self.client.find_queue.side_effect = [
            self.queue
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.groups.assert_called_once_with(
            queue=self.queue.id,
            include_deadletter=True)

        self.assertEqual(self.columns_with_dead, columns)
        self.assertEqual(self.data_with_dead, list(data))


class TestDeleteGroup(TestGroup):

    def setUp(self):
        super(TestDeleteGroup, self).setUp()

        self.cmd = group.DeleteGroup(self.app, None)

        self.client.delete_group = mock.Mock()

    def test_delete(self):
        arglist = [
            'queue',
            't1',
        ]

        verifylist = [
            ('queue', 'queue'),
            ('group', ['t1'])
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.delete_group.side_effect = [{}]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        calls = [mock.call(queue='queue', group='t1')]

        self.client.delete_group.assert_has_calls(calls)
        self.assertEqual(1, self.client.delete_group.call_count)

    def test_delete_multiple(self):
        arglist = [
            'queue',
            't1',
            't2',
        ]
        verifylist = [
            ('queue', 'queue'),
            ('group', ['t1', 't2'])
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.delete_group.side_effect = [{}, {}]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        calls = [
            mock.call(queue='queue', group='t1'),
            mock.call(queue='queue', group='t2')
        ]

        self.client.delete_group.assert_has_calls(calls)
        self.assertEqual(2, self.client.delete_group.call_count)


class TestCreateGroup(TestGroup):

    _data = fakes.FakeGroup.create_one()

    columns = ('ID', 'name')

    data = (
        _data.id,
        _data.name,
    )

    def setUp(self):
        super(TestCreateGroup, self).setUp()

        self.cmd = group.CreateGroup(self.app, None)

        self.client.create_group = mock.Mock()

    def test_show_default(self):
        arglist = [
            'queue_id',
            'name',
        ]
        verifylist = [
            ('queue', 'queue_id'),
            ('name', 'name'),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.create_group.side_effect = [
            self._data
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_group.assert_called_with(
            group='name', queue='queue_id'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)
