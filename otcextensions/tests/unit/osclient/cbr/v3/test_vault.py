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
from otcextensions.sdk.cbr.v3 import vault as vaultSDK
from otcextensions.tests.unit.osclient.cbr.v3 import fakes


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
            obj.bind_rules["tags"],
            obj.resources,
            obj.tags,
        )

        self.assertEqual(data, cmp_data)

    def test_add_resources_to_vault_output(self):
        obj = fakes.FakeVault.create_one()

        column = ()
        data = ()
        verify_column = (
            'resource_id_1',
            'resource_type_1',
        )
        verify_data = (
            'resource_id',
            'OS::Nova::Server',
        )

        data, column = vault._add_resources_to_vault_obj(obj, data, column)

        self.assertEqual(data, verify_data)
        self.assertEqual(column, verify_column)

    def test_add_tags_to_vault_output(self):
        obj = fakes.FakeVault.create_one()

        column = ()
        data = ()
        verify_column = (
            'tags',
        )
        verify_data = (
            ('value=val-tags, key=key-tags',)
        )

        data, column = vault._add_tags_to_vault_obj(obj, data, column)

        self.assertEqual(data, verify_data)
        self.assertEqual(column, verify_column)

    def test_add_bind_rules_to_vault_output(self):
        obj = fakes.FakeVault.create_one()

        column = ()
        data = ()
        verify_column = (
            'bind_rules',
        )
        verify_data = (
            ('value=val-bind, key=key-bind',)
        )

        data, column = vault._add_bind_rules_to_vault_obj(obj, data, column)

        self.assertEqual(data, verify_data)
        self.assertEqual(column, verify_column)

    def test_add_associated_policy_to_vault_output(self):
        obj = {
            'associate_policy': {
                'vault_id': 'cc56d0c6-c0c3-47e6-84cc-d7840dccb706',
                'policy_id': '6359dd6f-4146-42f8-9d7f-fbd6fa740d9f'
            }
        }

        column = ()
        verify_column = (
            'vault_id',
            'policy_id'
        )
        verify_data = (
            'cc56d0c6-c0c3-47e6-84cc-d7840dccb706',
            '6359dd6f-4146-42f8-9d7f-fbd6fa740d9f'
        )

        data, column = vault._add_associated_policy_to_vault_obj(obj, column)

        self.assertEqual(data, verify_data)
        self.assertEqual(column, verify_column)

    def test_add_associated_resources_to_vault_output(self):
        obj = {
            'add_resource_ids': [
                'cc56d0c6-c0c3-47e6-84cc-d7840dccb706',
                '6359dd6f-4146-42f8-9d7f-fbd6fa740d9f'
            ]
        }

        column = ()
        verify_column = (
            'resource_1',
            'resource_2'
        )
        verify_data = (
            'cc56d0c6-c0c3-47e6-84cc-d7840dccb706',
            '6359dd6f-4146-42f8-9d7f-fbd6fa740d9f'
        )

        data, column = vault._add_associated_resources_to_vault_obj(
            obj, column
        )

        self.assertEqual(data, verify_data)
        self.assertEqual(column, verify_column)

    def test_normalize_tags(self):
        tags = [
            'key1=value',
            'key2=',
            'key3'
        ]

        verify_result = [
            {'key': 'key1', 'value': 'value'},
            {'key': 'key2', 'value': ''},
            {'key': 'key3', 'value': ''}
        ]

        result = vault._normalize_tags(tags)

        self.assertEqual(result, verify_result)


class TestListVault(fakes.TestCBR):

    objects = fakes.FakeVault.create_multiple(3)

    columns = ('ID', 'name', 'backup_policy_id', 'description', 'created_at',
               'tags', 'resource_id_1', 'resource_type_1')

    data = []

    for s in objects:
        flat_data = vault._flatten_vault(s)
        resource_data, _ = vault._add_resources_to_vault_obj(s, (), ())
        tag_data, _ = vault._add_tags_to_vault_obj(s, (), ())
        data.append((
            flat_data['id'],
            flat_data['name'],
            flat_data['backup_policy_id'],
            flat_data['description'],
            flat_data['created_at'],
            resource_data[0] if resource_data else None,
            resource_data[1] if len(resource_data) > 1 else None,
            tag_data[0] if tag_data else None,
        ))

    def setUp(self):
        super(TestListVault, self).setUp()

        self.cmd = vault.ListVaults(self.app, None)

        self.client.vaults = mock.Mock()
        self.client.api_mock = self.client.vaults

    def test_default(self):
        arglist = [
            '--id', 'vault-id',
            '--name', 'vault-name',
            '--cloud-type', 'cloud-type',
            '--limit', '12',
            '--object-type', 'object-type',
            '--offset', '1',
            '--policy-id', 'policy-id',
            '--protect-type', 'protect-type',
            '--status', 'status',
        ]

        verifylist = [
            ('id', 'vault-id'),
            ('name', 'vault-name'),
            ('cloud_type', 'cloud-type'),
            ('limit', 12),
            ('object_type', 'object-type'),
            ('offset', 1),
            ('policy_id', 'policy-id'),
            ('protect_type', 'protect-type'),
            ('status', 'status')
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
            id='vault-id',
            name='vault-name',
            cloud_type='cloud-type',
            limit=12,
            object_type='object-type',
            offset=1,
            policy_id='policy-id',
            protect_type='protect-type',
            status='status'
        )

        self.assertEqual(self.columns, columns)
        for i, (expected, actual) in enumerate(zip(self.data, list(data))):
            if expected != actual:
                print(f"Row {i} mismatch:")
                print("Expected:", expected)
                print("Actual:  ", actual)

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
        )

        self.data, self.columns = vault._add_bind_rules_to_vault_obj(
            self.object,
            self.data,
            self.columns
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
        super(TestCreateVault, self).setUp()

        self.cmd = vault.CreateVault(self.app, None)
        self.app.client_manager.sdk_connection = mock.Mock()

        self.client.create_vault = mock.Mock()

    def test_default(self):
        arglist = [
            'vault_name',
            '--consistent-level', 'crash_consistent',
            '--backup-policy', 'id',
            '--object-type', 'disk',
            '--size', '40',
        ]
        verifylist = [
            ('name', 'vault_name'),
            ('consistent_level', 'crash_consistent'),
            ('backup_policy', 'id'),
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
            backup_policy_id='id',
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

        self.data, self.columns = vault._add_bind_rules_to_vault_obj(
            self.object,
            self.data,
            self.columns
        )

        self.data, self.columns = vault._add_tags_to_vault_obj(
            self.object,
            self.data,
            self.columns
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestUpdateVault(fakes.TestCBR):

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
        super(TestUpdateVault, self).setUp()

        self.cmd = vault.UpdateVault(self.app, None)
        self.app.client_manager.sdk_connection = mock.Mock()

        self.client.update_vault = mock.Mock()

    def test_default(self):
        arglist = [
            'vault_id',
            '--name', 'vault_name',
            '--size', '40',
        ]
        verifylist = [
            ('vault', 'vault_id'),
            ('name', 'vault_name'),
            ('size', 40),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.update_vault.side_effect = [
            self.object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_vault.assert_called_with(
            name_or_id='vault_id',
            ignore_missing=False)

        self.client.update_vault.assert_called_once_with(
            vault=mock.ANY,
            billing={
                'size': 40,
            },
            name='vault_name'
        )

        self.data, self.columns = vault._add_resources_to_vault_obj(
            self.object,
            self.data,
            self.columns
        )

        self.data, self.columns = vault._add_bind_rules_to_vault_obj(
            self.object,
            self.data,
            self.columns
        )

        self.data, self.columns = vault._add_tags_to_vault_obj(
            self.object,
            self.data,
            self.columns
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestDissociateVaultResource(fakes.TestCBR):

    def setUp(self):
        super(TestDissociateVaultResource, self).setUp()

        self.cmd = vault.DissociateVaultResource(self.app, None)

        self.client.dissociate_resources = mock.Mock()

    def test_delete(self):
        arglist = [
            'vault',
            '--resource', 'resource'
        ]
        verifylist = [
            ('vault', 'vault'),
            ('resource', ['resource']),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response for find_vault
        self.client.find_vault.side_effect = [
            vaultSDK.Vault(id='vault')
        ]

        # Set the response
        self.client.dissociate_resources.side_effect = [{}]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        dissociate_calls = [
            mock.call(
                vault='vault',
                resources=['resource']),
        ]

        find_calls = [
            mock.call(
                name_or_id='vault',
                ignore_missing=False),
        ]

        self.client.find_vault.assert_has_calls(find_calls)
        self.client.dissociate_resources.assert_has_calls(dissociate_calls)
        self.assertEqual(1, self.client.dissociate_resources.call_count)


class TestUnbindVaultPolicy(fakes.TestCBR):

    def setUp(self):
        super(TestUnbindVaultPolicy, self).setUp()

        self.cmd = vault.UnbindVaultPolicy(self.app, None)

        self.client.unbind_policy = mock.Mock()

    def test_delete(self):
        arglist = [
            'vault',
            'policy'
        ]
        verifylist = [
            ('vault', 'vault'),
            ('policy', 'policy'),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response for find_vault
        self.client.find_vault.side_effect = [
            vaultSDK.Vault(id='vault')
        ]

        # Set the response
        self.client.unbind_policy.side_effect = [{}]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        unbind_calls = [
            mock.call(
                vault='vault',
                policy='policy'),
        ]

        find_calls = [
            mock.call(
                name_or_id='vault',
                ignore_missing=False),
        ]

        self.client.find_vault.assert_has_calls(find_calls)
        self.client.unbind_policy.assert_has_calls(unbind_calls)
        self.assertEqual(1, self.client.unbind_policy.call_count)


class TestAssociateVaultResource(fakes.TestCBR):
    object = fakes.VaultDefaultStruct(
        **{
            '_content': b'{"add_resource_ids": ["resource_id"]}'
        }
    )
    columns = (
        'resource_1',
    )
    data = (
        'resource_id',
    )

    def setUp(self):
        super(TestAssociateVaultResource, self).setUp()

        self.cmd = vault.AssociateVaultResource(self.app, None)
        self.app.client_manager.sdk_connection = mock.Mock()

        self.client.associate_resources = mock.Mock()

    def test_default(self):
        arglist = [
            'vault_id',
            '--resource', 'id=resource_id,type=resource_type'
        ]
        verifylist = [
            ('vault', 'vault_id'),
            ('resource', [{'id': 'resource_id', 'type': 'resource_type'}]),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response for find_vault
        self.client.find_vault.side_effect = [
            vaultSDK.Vault(id='vault_id')
        ]

        # Set the response
        self.client.associate_resources.side_effect = [
            self.object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.associate_resources.assert_called_with(
            vault='vault_id',
            resources=[{'id': 'resource_id', 'type': 'resource_type'}]
        )

        self.client.associate_resources.assert_called_once_with(
            vault='vault_id',
            resources=[{'id': 'resource_id', 'type': 'resource_type'}]
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestBindVaultPolicy(fakes.TestCBR):
    object = fakes.VaultDefaultStruct(
        **{
            '_content': b'{"associate_policy": '
                        b'{"vault_id" : "vault_id",'
                        b'"policy_id" : "policy_id"}}'
        }
    )
    columns = (
        'vault_id',
        'policy_id',
    )
    data = (
        'vault_id',
        'policy_id',
    )

    def setUp(self):
        super(TestBindVaultPolicy, self).setUp()

        self.cmd = vault.BindVaultPolicy(self.app, None)
        self.app.client_manager.sdk_connection = mock.Mock()

        self.client.bind_policy = mock.Mock()

    def test_default(self):
        arglist = [
            'vault_id',
            'policy_id',
        ]
        verifylist = [
            ('vault', 'vault_id'),
            ('policy', 'policy_id'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response for find_vault
        self.client.find_vault.side_effect = [
            vaultSDK.Vault(id='vault_id')
        ]

        # Set the response
        self.client.bind_policy.side_effect = [
            self.object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.bind_policy.assert_called_with(
            vault='vault_id',
            policy='policy_id'
        )

        self.client.bind_policy.assert_called_once_with(
            vault='vault_id',
            policy='policy_id'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)
