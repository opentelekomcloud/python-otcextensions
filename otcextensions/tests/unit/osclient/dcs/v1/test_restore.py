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

from otcextensions.osclient.dcs.v1 import restore_record
from otcextensions.tests.unit.osclient.dcs.v1 import fakes


class TestListRestoreRecords(fakes.TestDCS):

    objects = fakes.FakeRestoreRecord.create_multiple(3)
    inst = fakes.FakeInstance.create_one()

    columns = ('id', 'name', 'backup_id', 'progress', 'status', 'error_code')

    data = []

    for s in objects:
        data.append((
            s.id,
            s.name,
            s.backup_id,
            s.progress,
            s.status,
            s.error_code,
        ))

    def setUp(self):
        super(TestListRestoreRecords, self).setUp()

        self.cmd = restore_record.ListRestoreRecords(self.app, None)

        self.client.restore_records = mock.Mock()
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
        self.client.restore_records.side_effect = [
            self.objects
        ]
        self.client.find_instance.side_effect = [
            self.inst
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.restore_records.assert_called_once_with(
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
        self.client.restore_records.side_effect = [
            self.objects
        ]
        self.client.find_instance.side_effect = [
            self.inst
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.restore_records.assert_called_once_with(
            instance={'id': self.inst.id},
            limit=1,
            start=2,
            begin_time='3',
            end_time='4'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))


class TestRecoverBackup(fakes.TestDCS):

    _data = fakes.FakeRestoreRecord.create_one()
    inst = fakes.FakeInstance.create_one()

    columns = ()

    data = (

    )

    def setUp(self):
        super(TestRecoverBackup, self).setUp()

        self.cmd = restore_record.RestoreBackup(self.app, None)

        self.client.restore_instance = mock.Mock()
        self.client.find_instance = mock.Mock()

    def test_backup_create(self):
        arglist = [
            'inst',
            '--backup', '2',
        ]
        verifylist = [
            ('instance', 'inst'),
            ('backup', '2'),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.restore_instance.side_effect = [
            self._data
        ]
        self.client.find_instance.side_effect = [
            self.inst
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.restore_instance.assert_called_with(
            instance={'id': self.inst.id},
            backup_id='2',
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)
