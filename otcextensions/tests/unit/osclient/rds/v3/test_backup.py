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
#
import mock

from otcextensions.osclient.rds.v3 import backup
from otcextensions.tests.unit.osclient.rds.v3 import fakes as fakes


class TestList(fakes.TestRds):

    _objects = fakes.FakeBackup.create_multiple(3)

    columns = ('ID', 'Name', 'Type', 'Instance Id', 'Datastore Type',
               'Datastore Version')

    data = []

    for s in _objects:
        data.append((
            s.id,
            s.name,
            s.type,
            s.instance_id,
            s.datastore['type'],
            s.datastore['version'],
        ))

    def setUp(self):
        super(TestList, self).setUp()

        self.cmd = backup.ListBackup(self.app, None)

        self.client.backups = mock.Mock()

    def test_list_default(self):
        arglist = ['test-instance'
        ]

        verifylist = [('instance', 'test-instance'),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.backups.side_effect = [
            self._objects
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.backups.assert_called_once_with('test-instance')

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))


class TestCreate(fakes.TestRds):

    _obj = fakes.FakeBackup.create_one()

    columns = ('ID', 'Name', 'type', 'instance_id',
               'status', 'begin_time', 'databases')

    data = (
        _obj.id,
        _obj.name,
        _obj.instance_id,
        _obj.status,
        _obj.begin_time,
        _obj.type,
        _obj.databases,
    )

    def setUp(self):
        super(TestCreate, self).setUp()

        self.cmd = backup.CreateBackup(self.app, None)

        self.client.create_backup = mock.Mock()
        self.app.client_manager.rds.find_instance = mock.Mock()

    def test_create(self):
        arglist = [
            'test-backup',
            'test-instance',
            '--description', 'test description',
        ]
        verifylist = [
            ('name', 'test-backup'),
            ('instance', 'test-instance'),
            ('description', 'test description'),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.create_backup.side_effect = [
            self._obj
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_backup.assert_called_with(
            'test-instance',
            description='test description',
            name='test-backup',
        )
        self.assertEqual(self.columns, columns)


class TestDelete(fakes.TestRds):

    def setUp(self):
        super(TestDelete, self).setUp()

        self.cmd = backup.DeleteBackup(self.app, None)

        self.client.delete_backup = mock.Mock()

    def test_delete_default(self):
        arglist = [
            'bck1',
        ]

        verifylist = [
            ('backup', ['bck1']),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.delete_backup.side_effect = [
            {}
        ]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.delete_backup.assert_called_once_with(
            backup='bck1',
            ignore_missing=False
        )

    def test_delete_multiple(self):
        arglist = [
            'bck1',
            'bck2'
        ]

        verifylist = [
            ('backup', ['bck1', 'bck2']),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.delete_backup.side_effect = [{}, {}]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        calls = [
            mock.call(backup='bck1', ignore_missing=False),
            mock.call(backup='bck2', ignore_missing=False),
        ]

        self.client.delete_backup.assert_has_calls(calls)
        self.assertEqual(2, self.client.delete_backup.call_count)
