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

from openstackclient.tests.unit import utils

from osc_lib import exceptions

from otcextensions.common import sdk_utils
from otcextensions.osclient.volume_backup.v2 import policy
from otcextensions.tests.unit.osclient.volume_backup.v2 import fakes


class TestListPolicy(fakes.TestVolumeBackup):

    _objects = fakes.FakePolicy.create_multiple(3)

    columns = ('id', 'name', 'policy_resource_count', 'scheduled_policy',
               'tags')

    data = []

    for s in _objects:
        data.append((
            s.id,
            s.name,
            s.policy_resource_count,
            policy.BackupPolicy(s.scheduled_policy),
            s.tags
        ))

    def setUp(self):
        super(TestListPolicy, self).setUp()

        self.cmd = policy.ListVolumeBackupPolicy(self.app, None)

        self.client.backup_policies = mock.Mock()

    def test_list_default(self):
        arglist = [
        ]

        verifylist = [
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.backup_policies.side_effect = [
            self._objects
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.backup_policies.assert_called_once_with()

        self.assertEqual(self.columns, columns)
        self.assertListItemEqual(self.data, list(data))


class TestShowPolicy(fakes.TestVolumeBackup):

    _object = fakes.FakePolicy.create_one()

    columns = ('id', 'name', 'policy_resource_count', 'scheduled_policy',
               'tags')

    data = (
        _object.id,
        _object.name,
        _object.policy_resource_count,
        policy.BackupPolicy(_object.scheduled_policy),
        _object.tags
    )

    def setUp(self):
        super(TestShowPolicy, self).setUp()

        self.cmd = policy.ShowVolumeBackupPolicy(self.app, None)

        self.client.find_backup_policy = mock.Mock()

    def test_show_default(self):
        arglist = [
            'policy_name',
        ]

        verifylist = [
            ('policy', 'policy_name'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.find_backup_policy.side_effect = [
            self._object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_backup_policy.assert_called_once_with(
            name_or_id='policy_name',
        )

        self.assertEqual(self.columns, columns)
        self.assertItemEqual(self.data, data)


class TestCreatePolicy(fakes.TestVolumeBackup):

    _object = fakes.FakePolicy.create_one()

    columns = ('id', 'name', 'policy_resource_count', 'scheduled_policy',
               'tags')

    data = (
        _object.id,
        _object.name,
        _object.policy_resource_count,
        policy.BackupPolicy(_object.scheduled_policy),
        _object.tags
    )

    def setUp(self):
        super(TestCreatePolicy, self).setUp()

        self.cmd = policy.CreateVolumeBackupPolicy(self.app, None)

        self.client.create_backup_policy = mock.Mock()

    def test_create_default(self):
        arglist = [
            'policy_name',
            '--start_time', '12:12',
            '--frequency', '13',
            '--rentention_num', '14',
            '--tag', 'a=b'
        ]

        verifylist = [
            ('name', 'policy_name'),
            ('start_time', '12:12'),
            ('enable', False),
            ('frequency', 13),
            ('rentention_num', 14),
            ('remain_first_backup_of_curMonth', False),
            ('tag', ['a=b']),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.create_backup_policy.side_effect = [
            self._object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_backup_policy.assert_called_once_with(
            name='policy_name',
            scheduled_policy={
                'start_time': '12:12',
                'frequency': 13,
                'rentention_num': 14,
                'remain_first_backup_of_curMonth': 'N',
                'status': 'OFF'
            },
            tags=[{'key': 'a', 'value': 'b'}]
        )

        self.assertEqual(self.columns, columns)
        self.assertItemEqual(self.data, data)

    def test_create_optionals(self):
        arglist = [
            'policy_name',
            '--start_time', '12:12',
            '--enable',
            '--frequency', '13',
            '--rentention_num', '14',
            '--remain_first_backup_of_curMonth',
            '--tag', 'a=b',
            '--tag', 'c=d',
        ]

        verifylist = [
            ('name', 'policy_name'),
            ('start_time', '12:12'),
            ('enable', True),
            ('frequency', 13),
            ('rentention_num', 14),
            ('remain_first_backup_of_curMonth', True),
            ('tag', ['a=b', 'c=d']),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.create_backup_policy.side_effect = [
            self._object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_backup_policy.assert_called_once_with(
            name='policy_name',
            scheduled_policy={
                'start_time': '12:12',
                'frequency': 13,
                'rentention_num': 14,
                'remain_first_backup_of_curMonth': 'Y',
                'status': 'ON'
            },
            tags=[{'key': 'a', 'value': 'b'}, {'key': 'c', 'value': 'd'}]
        )

        self.assertEqual(self.columns, columns)
        self.assertItemEqual(self.data, data)

    def test_create_frequense_not_allowed(self):
        arglist = [
            'policy_name',
            '--start_time', '12:12',
            '--frequency', '15',
        ]

        verifylist = [
            ('name', 'policy_name'),
            ('start_time', '12:12'),
            ('enable', False),
            ('frequency', 15),
            ('remain_first_backup_of_curMonth', False),
        ]

        # Verify cm is raising exception due to the exclusive group
        self.assertRaises(
            utils.ParserException,
            self.check_parser,
            self.cmd, arglist, verifylist
        )


class TestUpdatePolicy(fakes.TestVolumeBackup):

    _object = fakes.FakePolicy.create_one()

    columns = ('id', 'name', 'policy_resource_count', 'scheduled_policy',
               'tags')

    data = (
        _object.id,
        _object.name,
        _object.policy_resource_count,
        policy.BackupPolicy(_object.scheduled_policy),
        _object.tags
    )

    def setUp(self):
        super(TestUpdatePolicy, self).setUp()

        self.cmd = policy.UpdateVolumeBackupPolicy(self.app, None)

        self.client.update_backup_policy = mock.Mock()

    def test_update_name(self):
        arglist = [
            'policy_id',
            '--name', 'policy_name',
            '--frequency', '13',
            '--rentention_num', '14',
        ]

        verifylist = [
            ('id', 'policy_id'),
            ('name', 'policy_name'),
            ('frequency', 13),
            ('rentention_num', 14),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.update_backup_policy.side_effect = [
            self._object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.update_backup_policy.assert_called_once_with(
            backup_policy='policy_id',
            name='policy_name',
            scheduled_policy={
                'frequency': 13,
                'rentention_num': 14
            }
        )

        self.assertEqual(self.columns, columns)
        self.assertItemEqual(self.data, data)

    def test_update_disable_remain_first(self):
        arglist = [
            'policy_id',
            '--remain_first_backup_of_curMonth', 'false',
        ]

        verifylist = [
            ('id', 'policy_id'),
            ('remain_first_backup_of_curMonth', False),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.update_backup_policy.side_effect = [
            self._object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.update_backup_policy.assert_called_once_with(
            backup_policy='policy_id',
            scheduled_policy={
                'remain_first_backup_of_curMonth': 'N'
            }
        )

        self.assertEqual(self.columns, columns)
        self.assertItemEqual(self.data, data)

    def test_update_enable_remain_first(self):
        arglist = [
            'policy_id',
            '--remain_first_backup_of_curMonth', '1',
        ]

        verifylist = [
            ('id', 'policy_id'),
            ('remain_first_backup_of_curMonth', True),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.update_backup_policy.side_effect = [
            self._object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.update_backup_policy.assert_called_once_with(
            backup_policy='policy_id',
            scheduled_policy={
                'remain_first_backup_of_curMonth': 'Y'
            }
        )

    def test_update_disable(self):
        arglist = [
            'policy_id',
            '--status', 'false',
        ]

        verifylist = [
            ('id', 'policy_id'),
            ('status', False),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.update_backup_policy.side_effect = [
            self._object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.update_backup_policy.assert_called_once_with(
            backup_policy='policy_id',
            scheduled_policy={
                'status': 'OFF'
            }
        )

    def test_update_enable(self):
        arglist = [
            'policy_id',
            '--status', 'True',
        ]

        verifylist = [
            ('id', 'policy_id'),
            ('status', True),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.update_backup_policy.side_effect = [
            self._object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.update_backup_policy.assert_called_once_with(
            backup_policy='policy_id',
            scheduled_policy={
                'status': 'ON'
            }
        )


class TestDeletePolicy(fakes.TestVolumeBackup):

    def setUp(self):
        super(TestDeletePolicy, self).setUp()

        self.cmd = policy.DeleteVolumeBackupPolicy(self.app, None)

        self.client.delete_backup_policy = mock.Mock()

    def test_delete_default(self):
        arglist = [
            'pol',
        ]

        verifylist = [
            ('policy', 'pol'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.delete_backup_policy.side_effect = [
            {}
        ]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.delete_backup_policy.assert_called_once_with(
            backup_policy='pol',
            ignore_missing=False
        )


class TestExecutePolicy(fakes.TestVolumeBackup):

    def setUp(self):
        super(TestExecutePolicy, self).setUp()

        self.cmd = policy.ExecuteVolumeBackupPolicy(self.app, None)

        self.client.execute_policy = mock.Mock()

    def test_execute_default(self):
        arglist = [
            'pol',
        ]

        verifylist = [
            ('policy', 'pol'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.execute_policy.side_effect = [
            {}
        ]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.execute_policy.assert_called_once_with(
            backup_policy='pol'
        )


class TestLinkResourceToPolicy(fakes.TestVolumeBackup):

    def setUp(self):
        super(TestLinkResourceToPolicy, self).setUp()

        self.cmd = policy.LinkResourceToVolumeBackupPolicy(self.app, None)

        self.client.link_resources_to_policy = mock.Mock()

    def test_execute_default(self):
        arglist = [
            'pol',
            '--volume', 'v1',
            '--volume', 'v2'
        ]

        verifylist = [
            ('policy', 'pol'),
            ('volume', ['v1', 'v2'])
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.link_resources_to_policy.side_effect = [
            {}
        ]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.link_resources_to_policy.assert_called_once_with(
            backup_policy='pol',
            resources=['v1', 'v2']
        )


class TestUnlinkResourceToPolicy(fakes.TestVolumeBackup):

    def setUp(self):
        super(TestUnlinkResourceToPolicy, self).setUp()

        self.cmd = policy.UnlinkResourceFromVolumeBackupPolicy(self.app, None)

        self.client.unlink_resources_of_policy = mock.Mock()

    def test_execute_default(self):
        arglist = [
            'pol',
            '--volume', 'v1',
            '--volume', 'v2'
        ]

        verifylist = [
            ('policy', 'pol'),
            ('volume', ['v1', 'v2'])
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.unlink_resources_of_policy.side_effect = [
            {}
        ]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.unlink_resources_of_policy.assert_called_once_with(
            backup_policy='pol',
            resources=['v1', 'v2']
        )
