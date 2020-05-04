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

from otcextensions.osclient.dcs.v1 import backup
from otcextensions.tests.unit.osclient.dcs.v1 import fakes


class TestListBackup(fakes.TestDCS):

    objects = fakes.FakeBackup.create_multiple(3)
    inst = fakes.FakeInstance.create_one()

    columns = ('id', 'name', 'progress', 'status', 'error_code')

    data = []

    for s in objects:
        data.append((
            s.id,
            s.name,
            s.progress,
            s.status,
            s.error_code,
        ))

    def setUp(self):
        super(TestListBackup, self).setUp()

        self.cmd = backup.ListBackup(self.app, None)

        self.client.backups = mock.Mock()
        self.client.find_instance = mock.Mock()

    def test_list(self):
        arglist = [
            'inst'
        ]

        verifylist = [
            ('instance', 'inst')
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.backups.side_effect = [
            self.objects
        ]
        self.client.find_instance.side_effect = [
            self.inst
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.backups.assert_called_once_with(
            instance={'id': self.inst.id},
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))

    def test_list_query(self):
        arglist = [
            'inst',
            '--limit', '1',
            '--start', '2',
            '--from_time', '3',
            '--to_time', '4',
        ]

        verifylist = [
            ('instance', 'inst'),
            ('limit', 1),
            ('start', 2),
            ('from_time', '3'),
            ('to_time', '4'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.backups.side_effect = [
            self.objects
        ]
        self.client.find_instance.side_effect = [
            self.inst
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.backups.assert_called_once_with(
            instance={'id': self.inst.id},
            limit=1,
            start=2,
            begin_time='3',
            end_time='4'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))


class TestDeleteBackup(fakes.TestDCS):

    inst = fakes.FakeInstance.create_one()

    def setUp(self):
        super(TestDeleteBackup, self).setUp()

        self.cmd = backup.DeleteBackup(self.app, None)

        self.client.delete_instance_backup = mock.Mock()
        self.client.find_instance = mock.Mock()

    def test_delete(self):
        arglist = [
            'inst',
            't1',
            't2',
        ]
        verifylist = [
            ('instance', 'inst'),
            ('backup', ['t1', 't2'])
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.delete_instance_backup.side_effect = [{}, {}]
        self.client.find_instance.side_effect = [
            self.inst
        ]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        calls = [
            mock.call(instance_id=self.inst.id, backup='t1'),
            mock.call(instance_id=self.inst.id, backup='t2')
        ]

        self.client.delete_instance_backup.assert_has_calls(calls)
        self.assertEqual(2, self.client.delete_instance_backup.call_count)


class TestCreateBackup(fakes.TestDCS):

    _data = fakes.FakeBackup.create_one()
    inst = fakes.FakeInstance.create_one()

    columns = (
        'created_at', 'description', 'error_code', 'id',
        'name', 'period', 'progress', 'size', 'type', 'updated_at')

    data = (
        _data.created_at,
        _data.description,
        _data.error_code,
        _data.id,
        _data.name,
        _data.period,
        _data.progress,
        _data.size,
        _data.type,
        _data.updated_at
    )

    def setUp(self):
        super(TestCreateBackup, self).setUp()

        self.cmd = backup.CreateBackup(self.app, None)

        self.client.backup_instance = mock.Mock()
        self.client.find_instance = mock.Mock()

    def test_backup_create(self):
        arglist = [
            'inst',
            '--description', '2',
        ]
        verifylist = [
            ('instance', 'inst'),
            ('description', '2'),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.backup_instance.side_effect = [
            self._data
        ]
        self.client.find_instance.side_effect = [
            self.inst
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.backup_instance.assert_called_with(
            instance={'id': self.inst.id},
            description='2',
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)
