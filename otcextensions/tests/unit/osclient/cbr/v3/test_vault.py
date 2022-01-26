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
from otcextensions.sdk.cbr.v3 import vault as vaultSDK

class TestVault(fakes.TestCBR):

    def setUp(self):
        super(TestVault, self).setUp()

    def test_flatten(self):
        obj = fakes.FakeVault.create_one()

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
            flat_data['status'],
            flat_data['operation_type'],
            flat_data['object_type'],
            flat_data['spec_code'],
            flat_data['size'],
            flat_data['consistent_level'],
            flat_data['charging_mode'],
            flat_data['is_auto_pay'],
            flat_data['is_auto_renew'],
            flat_data['bind_rules'],
            flat_data['resources'],
            flat_data['tags']
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
            obj.billing.status,
            obj.billing.protect_type,
            obj.billing.object_type,
            obj.billing.spec_code,
            obj.billing.size,
            obj.billing.consistent_level,
            obj.billing.charging_mode,
            obj.billing.is_auto_pay,
            obj.billing.is_auto_renew,
            obj.bind_rules.tags,
            obj.resources,
            obj.tags,
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
        'status',
        'operation_type',
        'object_type',
        'spec_code',
        'size',
        'consistent_level',
        'charging_mode',
        'is_auto_pay',
        'is_auto_renew',
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
        flat_data['status'],
        flat_data['operation_type'],
        flat_data['object_type'],
        flat_data['spec_code'],
        flat_data['size'],
        flat_data['consistent_level'],
        flat_data['charging_mode'],
        flat_data['is_auto_pay'],
        flat_data['is_auto_renew'],
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

        self.client.find_vault.assert_called_once_with(
            name_or_id='vault',
            ignore_missing=False,)

        self.data, self.columns = vault._add_resources_to_vault_obj(
            self.object,
            self.data,
            self.columns
        )

        self.data, self.columns = vault._add_tags_to_vault_obj(
            self.object,
            self.data,
            self.columns,
            'tags'
        )

        self.data, self.columns = vault._add_tags_to_vault_obj(
            self.object,
            self.data,
            self.columns,
            'bind_rules'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestDeleteVault(fakes.TestCBR):

    def setUp(self):
        super(TestDeleteVault, self).setUp()

        self.cmd = vault.DeleteVault(self.app, None)

        self.client.delete_vault = mock.Mock()

    def test_delete(self):
        arglist = [
            'p1'
        ]
        verifylist = [
            ('vault', 'p1')
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.delete_vault.side_effect = [{}]

        # Set the response for find_policy
        self.client.find_vault.side_effect = [
            vaultSDK.Vault(id='p1')
        ]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        delete_calls = [
            mock.call(
                vault='p1',
                ignore_missing=False),
        ]

        find_calls = [
            mock.call(
                name_or_id='p1',
                ignore_missing=False),
        ]

        self.client.delete_vault.assert_has_calls(delete_calls)
        self.client.find_vault.assert_has_calls(find_calls)
        self.assertEqual(1, self.client.delete_vault.call_count)


class TestCreateVault(fakes.TestCBR):

    object = fakes.FakeVault.create_one()

    columns = (
        'ID',
        'name',
        'backup_policy',
        'description',
        'enterprise_project_id',
        'auto_bind',
        'status',
        'operation_type',
        'object_type',
        'spec_code',
        'size',
        'consistent_level',
        'charging_mode',
        'is_auto_pay',
        'is_auto_renew',
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
        flat_data['status'],
        flat_data['operation_type'],
        flat_data['object_type'],
        flat_data['spec_code'],
        flat_data['size'],
        flat_data['consistent_level'],
        flat_data['charging_mode'],
        flat_data['is_auto_pay'],
        flat_data['is_auto_renew'],
    )

    def setUp(self):
        super(TestCreateVault, self).setUp()

        self.cmd = vault.CreateVault(self.app, None)
        self.app.client_manager.sdk_connection = mock.Mock()

        self.client.create_vault = mock.Mock()

    def test_default(self):
        arglist = [
            'vault_name',
            '--consistent_level', 'crash_consistent',
            '--object_type', 'disk',
            '--size', '40',
        ]
        verifylist = [
            ('name', 'vault_name'),
            ('consistent_level', 'crash_consistent'),
            ('object_type', 'disk'),
            ('size', 40)
        ]

        # Verify cmd is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.create_vault.side_effect = [
            self.object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_vault.assert_called_once_with(
            resources=[],
            bind_rules={'tags': []},
            billing={
                'cloud_type': 'public',
                'protect_type': 'backup',
                'charging_mode': 'post_paid',
                'consistent_level': 'crash_consistent',
                'object_type': 'disk',
                'size': 40,
                'is_auto_renew': True,
                'is_auto_pay': True
            },
            name='vault_name'
        )

        self.data, self.columns = vault._add_resources_to_vault_obj(
            self.object,
            self.data,
            self.columns
        )

        self.data, self.columns = vault._add_tags_to_vault_obj(
            self.object,
            self.data,
            self.columns,
            'tags'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)