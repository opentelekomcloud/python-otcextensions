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

from otcextensions.osclient.cbr.v3 import vault
from otcextensions.tests.unit.osclient.cbr.v3 import fakes


class TestVault(fakes.TestCBR):

    def setUp(self):
        super(TestVault, self).setUp()

    def test_flatten(self):
        obj = fakes.FakeTask.create_one()

        flat_data = vault._flatten_vault(obj)

        data = (
            flat_data['id'],
            flat_data['name'],
            flat_data['auto_bind'],
            flat_data['auto_expand'],
            flat_data['backup_policy_id'],
            flat_data['created_at'],
            flat_data['description'],
            flat_data['project_id'],
            flat_data['provider_id'],
            flat_data['user_id'],
        )

        cmp_data = (
            obj.id,
            obj.name,
            obj.auto_bind,
            obj.auto_expand,
            obj.backup_policy_id,
            obj.created_at,
            obj.description,
            obj.project_id,
            obj.provider_id,
            obj.user_id,
        )

        self.assertEqual(data, cmp_data)


class TestListVault(fakes.TestCBR):

    objects = fakes.FakeVault.create_multiple(3)

    columns = ('ID', 'name', 'backup_policy_id', 'description', 'created_at')

    data = []

    for s in objects:
        flat_data = vault._flatten_vault(s)
        data.append((
            flat_data['id'],
            flat_data['name'],
            flat_data['backup_policy_id'],
            flat_data['description'],
            flat_data['created_at'],
        ))

    def setUp(self):
        super(TestListVault, self).setUp()

        self.cmd = vault.ListVaults(self.app, None)

        self.client.vaults = mock.Mock()
        self.client.api_mock = self.client.vaults

    def test_default(self):
        arglist = []

        verifylist = []

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [
            self.objects
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_once_with()

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))


class TestShowVault(fakes.TestCBR):

    object = fakes.FakeVault.create_one()

    columns = (
        'ID',
        'name',
        'auto_bind',
        'auto_expand',
        'backup_policy_id',
        'created_at',
        'description',
        'project_id',
        'provider_id',
        'user_id',
    )

    flat_data = vault._flatten_vault(object)

    data = (
        flat_data['id'],
        flat_data['name'],
        flat_data['auto_bind'],
        flat_data['auto_expand'],
        flat_data['backup_policy_id'],
        flat_data['created_at'],
        flat_data['description'],
        flat_data['project_id'],
        flat_data['provider_id'],
        flat_data['user_id'],
    )

    def setUp(self):
        super(TestShowVault, self).setUp()

        self.cmd = vault.ShowVault(self.app, None)

        self.client.find_vault = mock.Mock()

    def test_default(self):
        arglist = [
            'vault'
        ]
        verifylist = [
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.find_vault.side_effect = [
            self.object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.get_task.assert_called_once_with('vault')

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)
