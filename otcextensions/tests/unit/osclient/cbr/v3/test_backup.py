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

from otcextensions.osclient.cbr.v3 import backup
from otcextensions.sdk.cbr.v3 import backup as backupSDK
from otcextensions.tests.unit.osclient.cbr.v3 import fakes


class TestBackup(fakes.TestCBR):

    def setUp(self):
        super(TestBackup, self).setUp()

    def test_add_children_to_backup_obj(self):
        obj = fakes.FakeBackup.create_one()

        column = ()
        data = ()
        verify_column = (
            'child_backup_1',
            'child_backup_2'
        )
        verify_data = (
            'child_backup_uuid_1',
            'child_backup_uuid_2'
        )

        data, column = backup._add_children_to_backup_obj(obj, data, column)

        self.assertEqual(data, verify_data)
        self.assertEqual(column, verify_column)

    def test_flatten(self):
        obj = fakes.FakeBackup.create_one()

        flat_data = backup._flatten_backup(obj)

        data = (
            flat_data['id'],
            flat_data['name'],
            flat_data['checkpoint_id'],
            flat_data['created_at'],
            flat_data['description'],
            flat_data['expired_at'],
            flat_data['image_type'],
            flat_data['parent_id'],
            flat_data['project_id'],
            flat_data['protected_at'],
            flat_data['resource_az'],
            flat_data['resource_id'],
            flat_data['resource_name'],
            flat_data['resource_size'],
            flat_data['resource_type'],
            flat_data['status'],
            flat_data['updated_at'],
            flat_data['vault_id'],
            flat_data['provider_id']
        )

        cmp_data = (
            obj.id,
            obj.name,
            obj.checkpoint_id,
            obj.created_at,
            obj.description,
            obj.expired_at,
            obj.image_type,
            obj.parent_id,
            obj.project_id,
            obj.protected_at,
            obj.resource_az,
            obj.resource_id,
            obj.resource_name,
            obj.resource_size,
            obj.resource_type,
            obj.status,
            obj.updated_at,
            obj.vault_id,
            obj.provider_id
        )

        self.assertEqual(data, cmp_data)


class TestListBackup(fakes.TestCBR):

    objects = fakes.FakeBackup.create_multiple(3)

    columns = (
        'id',
        'name',
        'checkpoint_id',
        'created_at',
        'description',
        'expired_at',
        'image_type',
        'parent_id',
        'project_id',
        'protected_at',
        'resource_az',
        'resource_id',
        'resource_name',
        'resource_size',
        'resource_type',
        'status',
        'updated_at',
        'vault_id',
        'provider_id',
    )

    data = []

    for s in objects:
        flat_data = backup._flatten_backup(s)
        data.append((
            flat_data['id'],
            flat_data['name'],
            flat_data['checkpoint_id'],
            flat_data['created_at'],
            flat_data['description'],
            flat_data['expired_at'],
            flat_data['image_type'],
            flat_data['parent_id'],
            flat_data['project_id'],
            flat_data['protected_at'],
            flat_data['resource_az'],
            flat_data['resource_id'],
            flat_data['resource_name'],
            flat_data['resource_size'],
            flat_data['resource_type'],
            flat_data['status'],
            flat_data['updated_at'],
            flat_data['vault_id'],
            flat_data['provider_id']
        ))

    def setUp(self):
        super(TestListBackup, self).setUp()

        self.cmd = backup.ListBackups(self.app, None)

        self.client.backups = mock.Mock()
        self.client.api_mock = self.client.backups

    def test_default(self):
        arglist = [
            '--checkpoint-id', 'checkpoint_uuid',
            '--dec', 'True',
            '--end-time', '2018-02-01T12:00:00Z',
            '--image-type', 'backup',
            '--limit', '5',
            '--marker', 'marker',
            '--member-status', 'accept',
            '--name', 'name',
            '--offset', '5',
            '--own-type', 'all_granted',
            '--parent-id', 'parent_uuid',
            '--resource-az', 'resource_az',
            '--resource-id', 'resource_uuid',
            '--resource-name', 'resource_name',
            '--resource-type', 'OS::Cinder::Volume',
            '--sort', 'sort',
            '--start-time', 'start_time',
            '--status', 'available',
            '--used-percent', 'used_percent',
            '--vault-id', 'vault_uuid'
        ]

        verifylist = [
            ('checkpoint_id', 'checkpoint_uuid'),
            ('dec', True),
            ('end_time', '2018-02-01T12:00:00Z'),
            ('image_type', 'backup'),
            ('limit', 5),
            ('marker', 'marker'),
            ('member_status', 'accept'),
            ('name', 'name'),
            ('offset', 5),
            ('own_type', 'all_granted'),
            ('parent_id', 'parent_uuid'),
            ('resource_az', 'resource_az'),
            ('resource_id', 'resource_uuid'),
            ('resource_name', 'resource_name'),
            ('resource_type', 'OS::Cinder::Volume'),
            ('sort', 'sort'),
            ('start_time', 'start_time'),
            ('status', 'available'),
            ('used_percent', 'used_percent'),
            ('vault_id', 'vault_uuid'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [
            self.objects
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_once_with(
            checkpoint_id='checkpoint_uuid',
            dec=True,
            end_time='2018-02-01T12:00:00Z',
            image_type='backup',
            limit=5,
            marker='marker',
            member_status='accept',
            name='name',
            offset=5,
            own_type='all_granted',
            parent_id='parent_uuid',
            resource_az='resource_az',
            resource_id='resource_uuid',
            resource_name='resource_name',
            resource_type='OS::Cinder::Volume',
            sort='sort',
            start_time='start_time',
            status='available',
            used_percent='used_percent',
            vault_id='vault_uuid',
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))


class TestShowBackup(fakes.TestCBR):

    object = fakes.FakeBackup.create_one()

    columns = (
        'id',
        'name',
        'checkpoint_id',
        'created_at',
        'description',
        'expired_at',
        'image_type',
        'parent_id',
        'project_id',
        'protected_at',
        'resource_az',
        'resource_id',
        'resource_name',
        'resource_size',
        'resource_type',
        'status',
        'updated_at',
        'vault_id',
        'provider_id'
    )

    flat_data = backup._flatten_backup(object)

    data = (
        flat_data['id'],
        flat_data['name'],
        flat_data['checkpoint_id'],
        flat_data['created_at'],
        flat_data['description'],
        flat_data['expired_at'],
        flat_data['image_type'],
        flat_data['parent_id'],
        flat_data['project_id'],
        flat_data['protected_at'],
        flat_data['resource_az'],
        flat_data['resource_id'],
        flat_data['resource_name'],
        flat_data['resource_size'],
        flat_data['resource_type'],
        flat_data['status'],
        flat_data['updated_at'],
        flat_data['vault_id'],
        flat_data['provider_id']
    )

    def setUp(self):
        super(TestShowBackup, self).setUp()

        self.cmd = backup.ShowBackup(self.app, None)

        self.client.find_backup = mock.Mock()

    def test_default(self):
        arglist = [
            'backup'
        ]
        verifylist = [
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.find_backup.side_effect = [
            self.object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_backup.assert_called_once_with(
            name_or_id='backup',
            ignore_missing=False,
        )

        self.data, self.columns = backup._add_children_to_backup_obj(
            self.object,
            self.data,
            self.columns
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestDeleteBackup(fakes.TestCBR):

    def setUp(self):
        super(TestDeleteBackup, self).setUp()

        self.cmd = backup.DeleteBackup(self.app, None)

        self.client.delete_backup = mock.Mock()

    def test_delete(self):
        arglist = [
            'b1'
        ]
        verifylist = [
            ('backup', 'b1')
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.delete_backup.side_effect = [{}]

        # Set the response for find_policy
        self.client.find_backup.side_effect = [
            backupSDK.Backup(id='b1')
        ]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        delete_calls = [
            mock.call(
                backup='b1',
                ignore_missing=False),
        ]

        find_calls = [
            mock.call(
                name_or_id='b1',
                ignore_missing=False),
        ]

        self.client.delete_backup.assert_has_calls(delete_calls)
        self.client.find_backup.assert_has_calls(find_calls)
        self.assertEqual(1, self.client.delete_backup.call_count)


class TestRestoreBackup(fakes.TestCBR):

    object = fakes.FakeBackup.create_one()

    columns = (
        'id',
        'name',
        'checkpoint_id',
        'created_at',
        'description',
        'expired_at',
        'image_type',
        'parent_id',
        'project_id',
        'protected_at',
        'resource_az',
        'resource_id',
        'resource_name',
        'resource_size',
        'resource_type',
        'status',
        'updated_at',
        'vault_id',
        'provider_id',
    )

    flat_data = backup._flatten_backup(object)

    data = (
        flat_data['id'],
        flat_data['name'],
        flat_data['checkpoint_id'],
        flat_data['created_at'],
        flat_data['description'],
        flat_data['expired_at'],
        flat_data['image_type'],
        flat_data['parent_id'],
        flat_data['project_id'],
        flat_data['protected_at'],
        flat_data['resource_az'],
        flat_data['resource_id'],
        flat_data['resource_name'],
        flat_data['resource_size'],
        flat_data['resource_type'],
        flat_data['status'],
        flat_data['updated_at'],
        flat_data['vault_id'],
        flat_data['provider_id']
    )

    def setUp(self):
        super(TestRestoreBackup, self).setUp()

        self.cmd = backup.RestoreBackup(self.app, None)
        self.app.client_manager.sdk_connection = mock.Mock()

        self.client.restore_data = mock.Mock()

    def test_default(self):
        arglist = [
            '--mappings', 'backup_id=backup_uuid volume_id=volume_uuid',
            '--server-id', 'server_uuid',
            '--volume-id', 'volume_uuid'
        ]
        verifylist = [
            ('power_on', False),
            ('server_id', 'server_uuid'),
            ('volume_id', 'volume_uuid'),
            ('mappings', ['backup_id=backup_uuid volume_id=volume_uuid'])
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        #
        # Set the response
        self.client.restore_data.side_effect = [
            self.object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.restore_data.assert_called_once_with(
            mappings=[{'backup_id': 'backup_uuid',
                       'volume_id': 'volume_uuid'}],
            power_on=False,
            server_id='server_uuid',
            volume_id='volume_uuid'
        )

        self.data, self.columns = backup._add_children_to_backup_obj(
            self.object,
            self.data,
            self.columns
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)
