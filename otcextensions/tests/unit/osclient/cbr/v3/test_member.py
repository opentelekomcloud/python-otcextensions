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

from otcextensions.osclient.cbr.v3 import member
from otcextensions.sdk.cbr.v3 import member as memberSDK
from otcextensions.sdk.cbr.v3 import backup as backupSDK
from otcextensions.tests.unit.osclient.cbr.v3 import fakes


class TestMember(fakes.TestCBR):

    def setUp(self):
        super(TestMember, self).setUp()

    def test_flatten(self):
        obj = fakes.FakeMember.create_one()

        flat_data = member._flatten_member(obj)

        data = (
            flat_data['id'],
            flat_data['status'],
            flat_data['created_at'],
            flat_data['updated_at'],
            flat_data['backup_id'],
            flat_data['image_id'],
            flat_data['dest_project_id'],
            flat_data['vault_id']
        )

        cmp_data = (
            obj.id,
            obj.status,
            obj.created_at,
            obj.updated_at,
            obj.backup_id,
            obj.image_id,
            obj.dest_project_id,
            obj.vault_id
        )

        self.assertEqual(data, cmp_data)


class TestListMembers(fakes.TestCBR):

    objects = fakes.FakeMember.create_multiple(3)
    backup_obj = fakes.FakeBackup.create_one()

    columns = ('id', 'status', 'created_at', 'updated_at', 'backup_id',
               'image_id', 'dest_project_id', 'vault_id')

    data = []

    for s in objects:
        flat_data = member._flatten_member(s)
        data.append((
            flat_data['id'],
            flat_data['status'],
            flat_data['created_at'],
            flat_data['updated_at'],
            flat_data['backup_id'],
            flat_data['image_id'],
            flat_data['dest_project_id'],
            flat_data['vault_id']
        ))

    def setUp(self):
        super(TestListMembers, self).setUp()

        self.cmd = member.ListMembers(self.app, None)

        self.client.members = mock.Mock()
        self.client.find_backup = mock.Mock()
        self.client.api_mock = self.client.members

    def test_default(self):
        arglist = [
            'backup',
            '--dest-project-id', 'project_uuid',
            '--image-id', 'image_uuid',
            '--limit', '5',
            '--marker', 'marker',
            '--offset', '5',
            '--sort', 'sort',
            '--status', 'status',
            '--vault-id', 'vault_uuid'
        ]

        verifylist = [
            ('dest_project_id', 'project_uuid'),
            ('image_id', 'image_uuid'),
            ('limit', 5),
            ('marker', 'marker'),
            ('offset', 5),
            ('sort', 'sort'),
            ('status', 'status'),
            ('vault_id', 'vault_uuid'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [
            self.objects
        ]
        self.client.find_backup.side_effect = [
            self.backup_obj
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_once_with(
            backup=self.backup_obj.id,
            dest_project_id='project_uuid',
            image_id='image_uuid',
            limit=5,
            marker='marker',
            offset=5,
            sort='sort',
            status='status',
            vault_id='vault_uuid'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))


class TestShowMember(fakes.TestCBR):

    object = fakes.FakeMember.create_one()
    backup_obj = fakes.FakeBackup.create_one()

    columns = ('id', 'status', 'created_at', 'updated_at', 'backup_id',
               'image_id', 'dest_project_id', 'vault_id')

    flat_data = member._flatten_member(object)

    data = (
        flat_data['id'],
        flat_data['status'],
        flat_data['created_at'],
        flat_data['updated_at'],
        flat_data['backup_id'],
        flat_data['image_id'],
        flat_data['dest_project_id'],
        flat_data['vault_id']
    )

    def setUp(self):
        super(TestShowMember, self).setUp()

        self.cmd = member.ShowMember(self.app, None)

        self.client.get_member = mock.Mock()
        self.client.find_backup = mock.Mock()

    def test_default(self):
        arglist = [
            'backup',
            'member'
        ]
        verifylist = [
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.find_backup.side_effect = [
            self.backup_obj
        ]
        self.client.get_member.side_effect = [
            self.object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.get_member.assert_called_once_with(
            member='member',
            backup=self.backup_obj.id,
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestAddMembers(fakes.TestCBR):

    object = fakes.FakeMember.create_one()
    backup_obj = fakes.FakeBackup.create_one()

    columns = ('id', 'status', 'created_at', 'updated_at', 'backup_id',
               'image_id', 'dest_project_id', 'vault_id')

    data = []
    flat_data = member._flatten_member(object)
    data.append((
        flat_data['id'],
        flat_data['status'],
        flat_data['created_at'],
        flat_data['updated_at'],
        flat_data['backup_id'],
        flat_data['image_id'],
        flat_data['dest_project_id'],
        flat_data['vault_id']
    ))

    def setUp(self):
        super(TestAddMembers, self).setUp()

        self.cmd = member.AddMembers(self.app, None)
        self.app.client_manager.sdk_connection = mock.Mock()

        self.backup_client = self.app.client_manager.cbr
        self.backup_client.add_members = mock.Mock()
        self.client.find_backup = mock.Mock()


    def test_default(self):
        arglist = [
            'backup',
            '--members', 'project_uuid'
        ]
        verifylist = [
            ('backup', 'backup'),
            ('members', ['project_uuid'])
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.backup_client.add_members.side_effect = [
            [self.object]
        ]

        self.client.find_backup.side_effect = [
            self.backup_obj
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.backup_client.add_members.assert_called_once_with(
            backup=self.backup_obj.id,
            members=['project_uuid']
        )

        self.assertEqual(self.columns, columns)
        data_list = []
        for d in data:
            data_list.append(d)
        self.assertEqual(self.data, data_list)


class TestUpdateMember(fakes.TestCBR):

    object = fakes.FakeMember.create_one()

    columns = ('id', 'status', 'created_at', 'updated_at', 'backup_id',
               'image_id', 'dest_project_id', 'vault_id')

    flat_data = member._flatten_member(object)

    data = (
        flat_data['id'],
        flat_data['status'],
        flat_data['created_at'],
        flat_data['updated_at'],
        flat_data['backup_id'],
        flat_data['image_id'],
        flat_data['dest_project_id'],
        flat_data['vault_id']
    )

    def setUp(self):
        super(TestUpdateMember, self).setUp()

        self.cmd = member.UpdateMember(self.app, None)
        self.app.client_manager.sdk_connection = mock.Mock()

        self.client.update_member = mock.Mock()

    def test_default(self):
        arglist = [
            'backup',
            'member',
            '--status', 'pending',
            '--vault-id', 'vault_uuid'
        ]
        verifylist = [
            ('backup', 'backup'),
            ('member', 'member'),
            ('status', 'pending'),
            ('vault_id', 'vault_uuid')
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.update_member.side_effect = [
            self.object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.update_member.assert_called_once_with(
            backup='backup',
            member='member',
            status='pending',
            vault='vault_uuid'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestDeleteMember(fakes.TestCBR):

    backup_obj = fakes.FakeBackup.create_one()

    def setUp(self):
        super(TestDeleteMember, self).setUp()

        self.cmd = member.DeleteMember(self.app, None)

        self.client.delete_member = mock.Mock()

    def test_delete(self):
        arglist = [
            'backup',
            'member-uuid'
        ]
        verifylist = [
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.delete_member.side_effect = [{}]

        # Set the response for find_policy
        self.client.find_backup.side_effect = [
            self.backup_obj
        ]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        delete_calls = [
            mock.call(
                backup=self.backup_obj.id,
                member='member-uuid',
                ignore_missing=False),
        ]

        self.client.delete_member.assert_has_calls(delete_calls)
        self.assertEqual(1, self.client.delete_member.call_count)
