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

from otcextensions.osclient.rds.v3 import backup
from otcextensions.tests.unit.osclient.rds.v3 import fakes as fakes


class TestList(fakes.TestRds):

    _instance = fakes.FakeInstance.create_one()

    _objects = fakes.FakeBackup.create_multiple(3)

    column_headers = ('ID', 'Name', 'Type', 'Instance Id', 'Size')
    columns = ('id', 'name', 'type', 'instance_id', 'size')

    data = []

    for s in _objects:
        data.append(fakes.gen_data(s, columns))

    def setUp(self):
        super(TestList, self).setUp()

        self.cmd = backup.ListBackup(self.app, None)

        self.client.backups = mock.Mock()
        self.client.find_instance = mock.Mock(return_value=self._instance)

    def test_list_default(self):
        arglist = ['test-instance']

        verifylist = [
            ('instance', 'test-instance'),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.backups.side_effect = [self._objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_instance.assert_called_with('test-instance',
                                                     ignore_missing=False)
        self.client.backups.assert_called_once_with(instance=self._instance)

        self.assertEqual(self.column_headers, columns)
        self.assertEqual(self.data, list(data))

    def test_list_params(self):
        arglist = [
            'test-instance',
            '--backup-id', 'bid',
            '--backup-type', 'manual',
            '--offset', '1',
            '--limit', '2',
            # '--begin-time', '3',
            # '--end-time', '4'
        ]

        verifylist = [
            ('instance', 'test-instance'),
            ('backup_id', 'bid'),
            ('backup_type', 'manual'),
            ('offset', 1),
            ('limit', 2),
            # ('begin_time', '3'),
            # ('end_time', '4')
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.backups.side_effect = [self._objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_instance.assert_called_with(
            'test-instance',
            ignore_missing=False)
        self.client.backups.assert_called_once_with(
            instance=self._instance,
            backup_id='bid',
            backup_type='manual',
            offset=1,
            limit=2,
            paginated=False,
            # begin_time='3',
            # end_time='4'
        )

        self.assertEqual(self.column_headers, columns)
        self.assertEqual(self.data, list(data))


class TestCreate(fakes.TestRds):

    _data = fakes.FakeBackup.create_one()
    _instance = fakes.FakeInstance.create_one()

    columns = (
        'begin_time', 'datastore', 'description',
        'end_time', 'id', 'instance_id', 'name',
        'size', 'status', 'type'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestCreate, self).setUp()

        self.cmd = backup.CreateBackup(self.app, None)

        self.client.create_backup = mock.Mock(return_value=self._data)
        self.client.find_instance = mock.Mock(return_value=self._instance)

    def test_create(self):
        arglist = [
            'test-backup',
            'test-instance',
            '--description',
            'test description',
        ]
        verifylist = [
            ('name', 'test-backup'),
            ('instance', 'test-instance'),
            ('description', 'test description'),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_instance.assert_called_with('test-instance',
                                                     ignore_missing=False)
        self.client.create_backup.assert_called_with(
            instance=self._instance,
            description='test description',
            name='test-backup'
        )
        self.assertEqual(self.columns, columns)

    def test_create_sqlserver(self):
        arglist = [
            'test-backup',
            'test-instance',
            '--description', 'test description',
            '--databases', 'a,b,c'
        ]
        verifylist = [
            ('name', 'test-backup'),
            ('instance', 'test-instance'),
            ('description', 'test description'),
            ('databases', 'a,b,c')
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self._instance.datastore.update({'type': 'sqlserver'})
        self.client.find_instance.return_value = self._instance

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_instance.assert_called_with('test-instance',
                                                     ignore_missing=False)
        self.client.create_backup.assert_called_with(
            instance=self._instance,
            description='test description',
            name='test-backup',
            databases=[{'name': 'a'}, {'name': 'b'}, {'name': 'c'}]
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
        self.client.delete_backup.side_effect = [{}]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.delete_backup.assert_called_once_with(backup='bck1',
                                                          ignore_missing=False)

    def test_delete_multiple(self):
        arglist = ['bck1', 'bck2']

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


class TestListLinks(fakes.TestRds):

    _objects = fakes.FakeBackupFile.create_multiple(3)

    column_headers = ('Size', 'URL', 'Expires at')
    columns = ('size', 'download_link', 'expires_at')

    data = []

    for s in _objects:
        data.append(fakes.gen_data(s, columns))

    def setUp(self):
        super(TestListLinks, self).setUp()

        self.cmd = backup.ListBackupDownloadLinks(self.app, None)

        self.client.backup_download_links = mock.Mock(
            return_value=self._objects)

    def test_list_default(self):
        arglist = ['test-backup']

        verifylist = [
            ('backup_id', 'test-backup'),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.backup_download_links.assert_called_once_with(
            backup_id='test-backup')

        self.assertEqual(self.column_headers, columns)
        self.assertEqual(self.data, list(data))
