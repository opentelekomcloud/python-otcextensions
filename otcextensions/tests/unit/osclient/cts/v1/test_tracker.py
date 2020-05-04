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

from otcextensions.osclient.cts.v1 import tracker
from otcextensions.tests.unit.osclient.cts.v1 import fakes


class TestShowTracker(fakes.TestCTS):

    _data = fakes.FakeTracker.create_one()

    columns = (
        'bucket_name', 'file_prefix_name', 'id', 'name',
        'smn', 'status')

    data = (
        _data.bucket_name,
        _data.file_prefix_name,
        _data.id,
        _data.name,
        _data.smn,
        _data.status
    )

    def setUp(self):
        super(TestShowTracker, self).setUp()

        self.cmd = tracker.ShowTracker(self.app, None)

        self.client.get_tracker = mock.Mock()

    def test_show_default(self):
        arglist = [
            'name_or_id',
        ]
        verifylist = [
            ('tracker', 'name_or_id'),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.get_tracker.side_effect = [
            self._data
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.get_tracker.assert_called_with(
            tracker='name_or_id'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestDeleteTracker(fakes.TestCTS):

    def setUp(self):
        super(TestDeleteTracker, self).setUp()

        self.cmd = tracker.DeleteTracker(self.app, None)

        self.client.delete_tracker = mock.Mock()

    def test_delete_multiple(self):
        arglist = [
            't1',
            't2',
        ]
        verifylist = [
            ('tracker', ['t1', 't2'])
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.delete_tracker.side_effect = [{}, {}]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        calls = [
            mock.call(tracker='t1', ignore_missing=False),
            mock.call(tracker='t2', ignore_missing=False)
        ]

        self.client.delete_tracker.assert_has_calls(calls)
        self.assertEqual(2, self.client.delete_tracker.call_count)


class TestCreateTracker(fakes.TestCTS):

    _data = fakes.FakeTracker.create_one()

    columns = (
        'bucket_name', 'file_prefix_name', 'id', 'name',
        'smn', 'status')

    data = (
        _data.bucket_name,
        _data.file_prefix_name,
        _data.id,
        _data.name,
        _data.smn,
        _data.status
    )

    def setUp(self):
        super(TestCreateTracker, self).setUp()

        self.cmd = tracker.CreateTracker(self.app, None)

        self.client.create_tracker = mock.Mock()

    def test_create_default(self):
        arglist = [
            '--bucket_name', '1',
            '--file_prefix_name', '2',
            '--enable_smn',
            '--topic_id', '4',
            '--operation', 'create',
            '--operation', 'delete',
            '--send_all_key',
            '--notify_user', '8',
            '--notify_user', '9',
        ]
        verifylist = [
            ('bucket_name', '1'),
            ('file_prefix_name', '2'),
            ('enable_smn', True),
            ('topic_id', '4'),
            ('operation', ['create', 'delete']),
            ('send_all_key', True),
            ('notify_user', ['8', '9']),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.create_tracker.side_effect = [
            self._data
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_tracker.assert_called_with(
            bucket_name='1',
            file_prefix_name='2',
            smn={
                'enable': True,
                'topic_id': '4',
                'operations': ['create', 'delete'],
                'notify_users': ['8', '9']
            }
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)

    def test_create_no_smn(self):
        arglist = [
            '--bucket_name', '1',
            '--file_prefix_name', '2',
            '--topic_id', '4',
            '--operation', 'create',
            '--operation', 'delete',
            '--send_all_key',
            '--notify_user', '8',
            '--notify_user', '9',
        ]
        verifylist = [
            ('bucket_name', '1'),
            ('file_prefix_name', '2'),
            ('enable_smn', False),
            ('topic_id', '4'),
            ('operation', ['create', 'delete']),
            ('send_all_key', True),
            ('notify_user', ['8', '9']),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.create_tracker.side_effect = [
            self._data
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_tracker.assert_called_with(
            bucket_name='1',
            file_prefix_name='2',
            smn={
                'enable': False,
            }
        )


class TestSetTracker(fakes.TestCTS):

    _data = fakes.FakeTracker.create_one()

    columns = (
        'bucket_name', 'file_prefix_name', 'id', 'name',
        'smn', 'status')

    data = (
        _data.bucket_name,
        _data.file_prefix_name,
        _data.id,
        _data.name,
        _data.smn,
        _data.status
    )

    def setUp(self):
        super(TestSetTracker, self).setUp()

        self.cmd = tracker.SetTracker(self.app, None)

        self.client.update_tracker = mock.Mock()

    def test_update_default(self):
        arglist = [
            'system',
            '--bucket_name', '1',
            '--file_prefix_name', '2',
            '--enable_smn',
            '--topic_id', '4',
            '--operation', 'create',
            '--operation', 'delete',
            '--send_all_key',
            '--notify_user', '8',
            '--notify_user', '9',
            '--enable'
        ]
        verifylist = [
            ('tracker', 'system'),
            ('bucket_name', '1'),
            ('file_prefix_name', '2'),
            ('enable_smn', True),
            ('topic_id', '4'),
            ('operation', ['create', 'delete']),
            ('send_all_key', True),
            ('notify_user', ['8', '9']),
            ('enable', True)
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.update_tracker.side_effect = [
            self._data
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.update_tracker.assert_called_with(
            tracker='system',
            bucket_name='1',
            file_prefix_name='2',
            smn={
                'enable': True,
                'topic_id': '4',
                'operations': ['create', 'delete'],
                'notify_users': ['8', '9']
            },
            status='enabled'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)

    def test_update_disable(self):
        arglist = [
            'system',
            '--bucket_name', '1',
            '--disable'
        ]
        verifylist = [
            ('tracker', 'system'),
            ('bucket_name', '1'),
            # ('enable_smn', False),
            # ('send_all_key', False),
            ('disable', True)
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.update_tracker.side_effect = [
            self._data
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.update_tracker.assert_called_with(
            tracker='system',
            bucket_name='1',
            smn={'enable': False},
            status='disabled'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)
