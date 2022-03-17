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

from otcextensions.osclient.cbr.v3 import checkpoint
from otcextensions.sdk.cbr.v3 import checkpoint as checkpointSDK
from otcextensions.tests.unit.osclient.cbr.v3 import fakes


class TestCheckpoint(fakes.TestCBR):

    def setUp(self):
        super(TestCheckpoint, self).setUp()

    def test_flatten(self):
        obj = fakes.FakeCheckpoint.create_one()

        flat_data = checkpoint._flatten_checkpoint(obj)

        data = (
            flat_data['created_at'],
            flat_data['id'],
            flat_data['status'],
            flat_data['name'],
            flat_data['vault_id'],
            flat_data['vault_name'],
            flat_data['backup_name']
        )

        vault = obj.vault
        ei = obj.extra_info
        cmp_data = (
            obj.created_at,
            obj.id,
            obj.status,
            obj.name,
            vault.id,
            vault.name,
            ei.name
        )

        self.assertEqual(data, cmp_data)

class TestShowCheckpoint(fakes.TestCBR):

    object = fakes.FakeCheckpoint.create_one()

    columns = (
        'created_at',
        'id',
        'status',
        'name',
        'vault_id',
        'vault_name',
        'backup_name'
    )

    flat_data = checkpoint._flatten_checkpoint(object)

    data = (
        flat_data['created_at'],
        flat_data['id'],
        flat_data['status'],
        flat_data['name'],
        flat_data['vault_id'],
        flat_data['vault_name'],
        flat_data['backup_name']
    )

    def setUp(self):
        super(TestShowCheckpoint, self).setUp()

        self.cmd = checkpoint.ShowCheckpoint(self.app, None)

        self.client.get_checkpoint = mock.Mock()

    def test_default(self):
        arglist = [
            'checkpoint'
        ]
        verifylist = [
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.get_checkpoint.side_effect = [
            self.object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.get_checkpoint.assert_called_once_with(
            checkpoint='checkpoint'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestCreateCheckpoint(fakes.TestCBR):

    object = fakes.FakeCheckpoint.create_one()

    columns = (
        'created_at',
        'id',
        'status',
        'name',
        'vault_id',
        'vault_name',
        'backup_name',
    )

    flat_data = checkpoint._flatten_checkpoint(object)

    data = (
        flat_data['created_at'],
        flat_data['id'],
        flat_data['status'],
        flat_data['name'],
        flat_data['vault_id'],
        flat_data['vault_name'],
        flat_data['backup_name']
    )

    def setUp(self):
        super(TestCreateCheckpoint, self).setUp()

        self.cmd = checkpoint.CreateCheckpoint(self.app, None)
        self.app.client_manager.sdk_connection = mock.Mock()

        self.client.create_checkpoint = mock.Mock()

    def test_default(self):
        arglist = [
            '--vault-id', 'vault_id',
            '--auto-trigger',
            '--description', 'description',
            '--no-incremental',
            '--backup-name', 'backup_name',
            '--resources', 'resource-1-uuid',
            '--resources', 'resource-2-uuid'
        ]
        verifylist = [
            ('vault_id', 'vault_id'),
            ('auto_trigger', True),
            ('description', 'description'),
            ('no_incremental', False),
            ('backup_name', 'backup_name'),
            ('resources', ['resource-1-uuid', 'resource-2-uuid'])
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.create_checkpoint.side_effect = [
            self.object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_checkpoint.assert_called_once_with(
            parameters={
                'auto-trigger': True,
                'description': 'description',
                'incremental': False,
                'name': 'backup_name',
                'resources': ['resource-1-uuid', 'resource-2-uuid']},
            vault_id='vault_id',
        )

        a = 5

        # self.data, self.columns = policy._add_scheduling_patterns(
        #     self.object,
        #     self.data,
        #     self.columns
        # )
        #
        # self.assertEqual(self.columns, columns)
        # self.assertEqual(self.data, data)
