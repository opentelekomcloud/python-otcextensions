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

from otcextensions.osclient.vlb.v3 import load_balancer
from otcextensions.sdk.vlb.v3 import load_balancer as lbSDK
from otcextensions.tests.unit.osclient.vlb.v3 import fakes


class TestLoadBalancer(fakes.TestVLB):

    def setUp(self):
        super(TestLoadBalancer, self).setUp()

    def test_flatten(self):
        obj = fakes.FakeLoadBalancer.create_one()

        flat_data = load_balancer._flatten_loadbalancer(obj)

        data = (
            flat_data['id'],
            flat_data['name'],
            flat_data['description'],
            flat_data['provisioning_status'],
            flat_data['provider'],
            flat_data['operating_status'],
            flat_data['vip_address'],
            flat_data['vip_subnet_cidr_id'],
            flat_data['project_id'],
            flat_data['vip_port_id'],
            flat_data['created_at'],
            flat_data['updated_at'],
            flat_data['guaranteed'],
            flat_data['vpc_id'],
            flat_data['ipv6_vip_address'],
            flat_data['ipv6_vip_virsubnet_id'],
            flat_data['ipv6_vip_port_id'],
            flat_data['availability_zone_list'],
            flat_data['l4_flavor_id'],
            flat_data['l4_scale_flavor_id'],
            flat_data['l7_flavor_id'],
            flat_data['l7_scale_flavor_id'],
            flat_data['elb_virsubnet_ids'],
            flat_data['pools']
        )

        cmp_data = (
            obj.id,
            obj.name,
            obj.description,
            obj.provisioning_status,
            obj.provider,
            obj.operating_status,
            obj.vip_address,
            obj.vip_subnet_id,
            obj.project_id,
            obj.vip_port_id,
            obj.created_at,
            obj.updated_at,
            obj.guaranteed,
            obj.vpc_id,
            obj.ipv6_vip_address,
            obj.ipv6_vip_subnet_id,
            obj.ipv6_vip_port_id,
            obj.availability_zones,
            obj.l4_flavor_id,
            obj.l4_scale_flavor_id,
            obj.l7_flavor_id,
            obj.l7_scale_flavor_id,
            obj.network_ids,
            obj.pools
        )

        self.assertEqual(data, cmp_data)

    def test_add_eips_to_loadbalancer_output(self):
        obj = fakes.FakeLoadBalancer.create_one()

        column = ()
        data = ()
        verify_column = (
            'eip_id_1',
            'eip_address_1',
            'ip_version_1'

        )
        verify_data = (
            'eip-uuid',
            'eip-address',
            'ip-version'
        )

        data, column = load_balancer._add_eips_to_load_balancer_obj(
            obj, data, column
        )

        self.assertEqual(data, verify_data)
        self.assertEqual(column, verify_column)


    def test_add_publicips_to_loadbalancer_output(self):
        obj = fakes.FakeLoadBalancer.create_one()

        column = ()
        data = ()
        verify_column = (
            'publicip_id_1',
            'publicip_address_1',
            'piblicip_ip_version_1'

        )
        verify_data = (
            'publicip-uuid',
            'publicip-address',
            'ip-version'
        )

        data, column = load_balancer._add_publicips_to_load_balancer_obj(
            obj, data, column
        )

        self.assertEqual(data, verify_data)
        self.assertEqual(column, verify_column)

    def test_add_pools_to_load_balancer_output(self):
        obj = fakes.FakeLoadBalancer.create_one()

        column = ()
        data = ()
        verify_column = (
            'pool_id_1',
        )
        verify_data = (
            'pool-uuid',
        )

        data, column = load_balancer._add_pools_to_load_balancer_obj(
            obj, data, column)

        self.assertEqual(data, verify_data)
        self.assertEqual(column, verify_column)

    def test_add_listeners_to_load_balancer_output(self):
        obj = fakes.FakeLoadBalancer.create_one()

        column = ()
        data = ()
        verify_column = (
            'listener_id_1',
        )
        verify_data = (
            'listener-uuid',
        )

        data, column = load_balancer._add_listeners_to_load_balancer_obj(
            obj, data, column)

        self.assertEqual(data, verify_data)
        self.assertEqual(column, verify_column)

    def test_add_tags_to_vault_output(self):
        obj = fakes.FakeLoadBalancer.create_one()

        column = ()
        data = ()
        verify_column = (
            'tags',
        )
        verify_data = (
            ('value=tag-value, key=tag-key',)
        )

        data, column = load_balancer._add_tags_to_load_balancer_obj(
            obj, data, column)

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

        result = load_balancer._normalize_tags(tags)

        self.assertEqual(result, verify_result)


class TestListLoadBalancers(fakes.TestVLB):

    objects = fakes.FakeLoadBalancer.create_multiple(3)

    columns = ('ID', 'Name',)

    data = []

    for s in objects:
        flat_data = load_balancer._flatten_loadbalancer(s)
        data.append((
            flat_data['id'],
            flat_data['name']
        ))

    def setUp(self):
        super(TestListLoadBalancers, self).setUp()

        self.cmd = load_balancer.ListLoadBalancers(self.app, None)

        self.client.loadbalancers = mock.Mock()
        self.client.api_mock = self.client.load_balancers

    def test_default(self):
        arglist = [
            '--id', 'lb-id',
            '--name', 'lb-name'
        ]

        verifylist = [
            ('id', 'lb-id'),
            ('name', 'lb-name')
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [
            self.objects
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_once_with(
            id='lb-id',
            name='lb-name'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))


class TestShowLoadBalancer(fakes.TestVLB):

    object = fakes.FakeLoadBalancer.create_one()

    columns = (
        'id',
        'name',
        'description',
        'provisioning_status',
        'provider',
        'operating_status',
        'vip_address',
        'vip_subnet_cidr_id',
        'project_id',
        'vip_port_id',
        'created_at',
        'updated_at',
        'guaranteed',
        'vpc_id',
        'availability_zone_list',
        'l4_flavor_id',
        'l4_scale_flavor_id',
        'l7_flavor_id',
        'l7_scale_flavor_id',
        'elb_virsubnet_ids'
    )


    flat_data = load_balancer._flatten_loadbalancer(object)

    data = (
        flat_data['id'],
        flat_data['name'],
        flat_data['description'],
        flat_data['provisioning_status'],
        flat_data['provider'],
        flat_data['operating_status'],
        flat_data['vip_address'],
        flat_data['vip_subnet_cidr_id'],
        flat_data['project_id'],
        flat_data['vip_port_id'],
        flat_data['created_at'],
        flat_data['updated_at'],
        flat_data['guaranteed'],
        flat_data['vpc_id'],
        flat_data['availability_zone_list'],
        flat_data['l4_flavor_id'],
        flat_data['l4_scale_flavor_id'],
        flat_data['l7_flavor_id'],
        flat_data['l7_scale_flavor_id'],
        flat_data['elb_virsubnet_ids']
    )

    def setUp(self):
        super(TestShowLoadBalancer, self).setUp()

        self.cmd = load_balancer.ShowLoadBalancer(self.app, None)

        self.client.find_load_balancer = mock.Mock()

    def test_default(self):
        arglist = [
            'loadbalancer'
        ]
        verifylist = [
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.find_load_balancer.side_effect = [
            self.object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_load_balancer.assert_called_once_with(
            name_or_id='loadbalancer',
            ignore_missing=False,)

        self.data, self.columns = load_balancer._add_eips_to_load_balancer_obj(
            self.object,
            self.data,
            self.columns
        )

        self.data, self.columns = load_balancer._add_publicips_to_load_balancer_obj(
            self.object,
            self.data,
            self.columns,
        )

        self.data, self.columns = load_balancer._add_listeners_to_load_balancer_obj(
            self.object,
            self.data,
            self.columns
        )

        self.data, self.columns = load_balancer._add_pools_to_load_balancer_obj(
            self.object,
            self.data,
            self.columns
        )
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestCreateLoadBalancer(fakes.TestVLB):

    object = fakes.FakeLoadBalancer.create_one()

    columns = (
        'ID',
        'description',
        'provisioning_status',
        'provider',
        'operating_status',
        'vip_address',
        'vip_subnet_cidr_id',
        'name',
        'project_id',
        'vip_port_id',
        'created_at',
        'updated_at',
        'guaranteed',
        'vpc_id',
        'availability_zone_list',
        'l4_flavor_id',
        'l4_scale_flavor_id',
        'l7_flavor_id',
        'l7_scale_flavor_id',
        'elb_virsubnet_ids'
    )

    flat_data = load_balancer._flatten_loadbalancer(object)

    data = (
        flat_data['id'],
        flat_data['description'],
        flat_data['provisioning_status'],
        flat_data['provider'],
        flat_data['operating_status'],
        flat_data['vip_address'],
        flat_data['vip_subnet_cidr_id'],
        flat_data['name'],
        flat_data['project_id'],
        flat_data['vip_port_id'],
        flat_data['created_at'],
        flat_data['updated_at'],
        flat_data['guaranteed'],
        flat_data['vpc_id'],
        flat_data['availability_zone_list'],
        flat_data['l4_flavor_id'],
        flat_data['l4_scale_flavor_id'],
        flat_data['l7_flavor_id'],
        flat_data['l7_scale_flavor_id'],
        flat_data['elb_virsubnet_ids']
    )

    def setUp(self):
        super(TestCreateLoadBalancer, self).setUp()

        self.cmd = load_balancer.CreateLoadBalancer(self.app, None)
        self.app.client_manager.sdk_connection = mock.Mock()

        self.client.create_load_balancer = mock.Mock()

    def test_default(self):
        arglist = [
            '--name', 'lb-name',
            '--description', 'lb-description',
            '--vip-address', 'vip-adrress',
            '--vip-network_id', 'vip-network-id',
            '--vip-subnet-cidr-id', 'vip-subnet-cidr-id',
            '--provider', 'vlb',
            '--l4-flavor-id', 'l4-flavor-id',
            '--project-id', 'project-id',
            '--vpc-id', 'vpc-id',
            '--availability-zone-list', 'availability-zone-list',
            '--tag', 'key=mykey1,value=myvalue1',
            '--tag', 'key=mykey2,value=myvalue2',
            '--l7-flavor-id', 'l7-flavor-id',
            '--ipv6-bandwidth', 'ipv6-bandwidth',
            '--publicip-id', 'publicip-id',
            '--ip-version', 'ip-version',
            '--network-type', 'network-type',
            '--publicip-billing-info', 'publicip-billing-info',
            '--publicip-description', 'publicip-description',
            '--bandwidth', 'bandwidth',
            '--elb-virsubnet-id', 'elb-virsubnet-id'
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



#
# class TestDeleteVault(fakes.TestCBR):
#
#     def setUp(self):
#         super(TestDeleteVault, self).setUp()
#
#         self.cmd = vault.DeleteVault(self.app, None)
#
#         self.client.delete_vault = mock.Mock()
#
#     def test_delete(self):
#         arglist = [
#             'p1'
#         ]
#         verifylist = [
#             ('vault', 'p1')
#         ]
#         # Verify cm is triggereg with default parameters
#         parsed_args = self.check_parser(self.cmd, arglist, verifylist)
#
#         # Set the response
#         self.client.delete_vault.side_effect = [{}]
#
#         # Set the response for find_policy
#         self.client.find_vault.side_effect = [
#             vaultSDK.Vault(id='p1')
#         ]
#
#         # Trigger the action
#         self.cmd.take_action(parsed_args)
#
#         delete_calls = [
#             mock.call(
#                 vault='p1',
#                 ignore_missing=False),
#         ]
#
#         find_calls = [
#             mock.call(
#                 name_or_id='p1',
#                 ignore_missing=False),
#         ]
#
#         self.client.delete_vault.assert_has_calls(delete_calls)
#         self.client.find_vault.assert_has_calls(find_calls)
#         self.assertEqual(1, self.client.delete_vault.call_count)
#
#
# class TestCreateVault(fakes.TestCBR):
#
#     object = fakes.FakeVault.create_one()
#
#     columns = (
#         'ID',
#         'name',
#         'auto_bind',
#         'auto_expand',
#         'backup_policy_id',
#         'created_at',
#         'description',
#         'project_id',
#         'provider_id',
#         'user_id',
#         'status',
#         'operation_type',
#         'object_type',
#         'spec_code',
#         'size',
#         'consistent_level',
#         'charging_mode',
#         'is_auto_pay',
#         'is_auto_renew',
#     )
#
#     flat_data = vault._flatten_vault(object)
#
#     data = (
#         flat_data['id'],
#         flat_data['name'],
#         flat_data['auto_bind'],
#         flat_data['auto_expand'],
#         flat_data['backup_policy_id'],
#         flat_data['created_at'],
#         flat_data['description'],
#         flat_data['project_id'],
#         flat_data['provider_id'],
#         flat_data['user_id'],
#         flat_data['status'],
#         flat_data['operation_type'],
#         flat_data['object_type'],
#         flat_data['spec_code'],
#         flat_data['size'],
#         flat_data['consistent_level'],
#         flat_data['charging_mode'],
#         flat_data['is_auto_pay'],
#         flat_data['is_auto_renew'],
#     )
#
#     def setUp(self):
#         super(TestCreateVault, self).setUp()
#
#         self.cmd = vault.CreateVault(self.app, None)
#         self.app.client_manager.sdk_connection = mock.Mock()
#
#         self.client.create_vault = mock.Mock()
#
#     def test_default(self):
#         arglist = [
#             'vault_name',
#             '--consistent-level', 'crash_consistent',
#             '--backup-policy', 'id',
#             '--object-type', 'disk',
#             '--size', '40',
#         ]
#         verifylist = [
#             ('name', 'vault_name'),
#             ('consistent_level', 'crash_consistent'),
#             ('backup_policy', 'id'),
#             ('object_type', 'disk'),
#             ('size', 40)
#         ]
#
#         # Verify cmd is triggered with default parameters
#         parsed_args = self.check_parser(self.cmd, arglist, verifylist)
#
#         # Set the response
#         self.client.create_vault.side_effect = [
#             self.object
#         ]
#
#         # Trigger the action
#         columns, data = self.cmd.take_action(parsed_args)
#
#         self.client.create_vault.assert_called_once_with(
#             resources=[],
#             backup_policy_id='id',
#             bind_rules={'tags': []},
#             billing={
#                 'cloud_type': 'public',
#                 'protect_type': 'backup',
#                 'charging_mode': 'post_paid',
#                 'consistent_level': 'crash_consistent',
#                 'object_type': 'disk',
#                 'size': 40,
#                 'is_auto_renew': True,
#                 'is_auto_pay': True
#             },
#             name='vault_name'
#         )
#
#         self.data, self.columns = vault._add_resources_to_vault_obj(
#             self.object,
#             self.data,
#             self.columns
#         )
#
#         self.data, self.columns = vault._add_bind_rules_to_vault_obj(
#             self.object,
#             self.data,
#             self.columns
#         )
#
#         self.data, self.columns = vault._add_tags_to_vault_obj(
#             self.object,
#             self.data,
#             self.columns
#         )
#
#         self.assertEqual(self.columns, columns)
#         self.assertEqual(self.data, data)
#
#
# class TestUpdateVault(fakes.TestCBR):
#
#     object = fakes.FakeVault.create_one()
#
#     columns = (
#         'ID',
#         'name',
#         'auto_bind',
#         'auto_expand',
#         'backup_policy_id',
#         'created_at',
#         'description',
#         'project_id',
#         'provider_id',
#         'user_id',
#         'status',
#         'operation_type',
#         'object_type',
#         'spec_code',
#         'size',
#         'consistent_level',
#         'charging_mode',
#         'is_auto_pay',
#         'is_auto_renew',
#     )
#
#     flat_data = vault._flatten_vault(object)
#
#     data = (
#         flat_data['id'],
#         flat_data['name'],
#         flat_data['auto_bind'],
#         flat_data['auto_expand'],
#         flat_data['backup_policy_id'],
#         flat_data['created_at'],
#         flat_data['description'],
#         flat_data['project_id'],
#         flat_data['provider_id'],
#         flat_data['user_id'],
#         flat_data['status'],
#         flat_data['operation_type'],
#         flat_data['object_type'],
#         flat_data['spec_code'],
#         flat_data['size'],
#         flat_data['consistent_level'],
#         flat_data['charging_mode'],
#         flat_data['is_auto_pay'],
#         flat_data['is_auto_renew'],
#     )
#
#     def setUp(self):
#         super(TestUpdateVault, self).setUp()
#
#         self.cmd = vault.UpdateVault(self.app, None)
#         self.app.client_manager.sdk_connection = mock.Mock()
#
#         self.client.update_vault = mock.Mock()
#
#     def test_default(self):
#         arglist = [
#             'vault_id',
#             '--name', 'vault_name',
#             '--size', '40',
#         ]
#         verifylist = [
#             ('vault', 'vault_id'),
#             ('name', 'vault_name'),
#             ('size', 40),
#         ]
#
#         # Verify cm is triggereg with default parameters
#         parsed_args = self.check_parser(self.cmd, arglist, verifylist)
#
#         # Set the response
#         self.client.update_vault.side_effect = [
#             self.object
#         ]
#
#         # Trigger the action
#         columns, data = self.cmd.take_action(parsed_args)
#
#         self.client.find_vault.assert_called_with(
#             name_or_id='vault_id',
#             ignore_missing=False)
#
#         self.client.update_vault.assert_called_once_with(
#             vault=mock.ANY,
#             billing={
#                 'size': 40,
#             },
#             name='vault_name'
#         )
#
#         self.data, self.columns = vault._add_resources_to_vault_obj(
#             self.object,
#             self.data,
#             self.columns
#         )
#
#         self.data, self.columns = vault._add_bind_rules_to_vault_obj(
#             self.object,
#             self.data,
#             self.columns
#         )
#
#         self.data, self.columns = vault._add_tags_to_vault_obj(
#             self.object,
#             self.data,
#             self.columns
#         )
#
#         self.assertEqual(self.columns, columns)
#         self.assertEqual(self.data, data)
#
#
# class TestDissociateVaultResource(fakes.TestCBR):
#
#     def setUp(self):
#         super(TestDissociateVaultResource, self).setUp()
#
#         self.cmd = vault.DissociateVaultResource(self.app, None)
#
#         self.client.dissociate_resources = mock.Mock()
#
#     def test_delete(self):
#         arglist = [
#             'vault',
#             '--resource', 'resource'
#         ]
#         verifylist = [
#             ('vault', 'vault'),
#             ('resource', ['resource']),
#         ]
#         # Verify cm is triggereg with default parameters
#         parsed_args = self.check_parser(self.cmd, arglist, verifylist)
#
#         # Set the response for find_vault
#         self.client.find_vault.side_effect = [
#             vaultSDK.Vault(id='vault')
#         ]
#
#         # Set the response
#         self.client.dissociate_resources.side_effect = [{}]
#
#         # Trigger the action
#         self.cmd.take_action(parsed_args)
#
#         dissociate_calls = [
#             mock.call(
#                 vault='vault',
#                 resources=['resource']),
#         ]
#
#         find_calls = [
#             mock.call(
#                 name_or_id='vault',
#                 ignore_missing=False),
#         ]
#
#         self.client.find_vault.assert_has_calls(find_calls)
#         self.client.dissociate_resources.assert_has_calls(dissociate_calls)
#         self.assertEqual(1, self.client.dissociate_resources.call_count)
#
#
# class TestUnbindVaultPolicy(fakes.TestCBR):
#
#     def setUp(self):
#         super(TestUnbindVaultPolicy, self).setUp()
#
#         self.cmd = vault.UnbindVaultPolicy(self.app, None)
#
#         self.client.unbind_policy = mock.Mock()
#
#     def test_delete(self):
#         arglist = [
#             'vault',
#             'policy'
#         ]
#         verifylist = [
#             ('vault', 'vault'),
#             ('policy', 'policy'),
#         ]
#         # Verify cm is triggereg with default parameters
#         parsed_args = self.check_parser(self.cmd, arglist, verifylist)
#
#         # Set the response for find_vault
#         self.client.find_vault.side_effect = [
#             vaultSDK.Vault(id='vault')
#         ]
#
#         # Set the response
#         self.client.unbind_policy.side_effect = [{}]
#
#         # Trigger the action
#         self.cmd.take_action(parsed_args)
#
#         unbind_calls = [
#             mock.call(
#                 vault='vault',
#                 policy='policy'),
#         ]
#
#         find_calls = [
#             mock.call(
#                 name_or_id='vault',
#                 ignore_missing=False),
#         ]
#
#         self.client.find_vault.assert_has_calls(find_calls)
#         self.client.unbind_policy.assert_has_calls(unbind_calls)
#         self.assertEqual(1, self.client.unbind_policy.call_count)
#
#
# class TestAssociateVaultResource(fakes.TestCBR):
#     object = fakes.VaultDefaultStruct(
#         **{
#             '_content': b'{"add_resource_ids": ["resource_id"]}'
#         }
#     )
#     columns = (
#         'resource_1',
#     )
#     data = (
#         'resource_id',
#     )
#
#     def setUp(self):
#         super(TestAssociateVaultResource, self).setUp()
#
#         self.cmd = vault.AssociateVaultResource(self.app, None)
#         self.app.client_manager.sdk_connection = mock.Mock()
#
#         self.client.associate_resources = mock.Mock()
#
#     def test_default(self):
#         arglist = [
#             'vault_id',
#             '--resource', 'id=resource_id,type=resource_type'
#         ]
#         verifylist = [
#             ('vault', 'vault_id'),
#             ('resource', [{'id': 'resource_id', 'type': 'resource_type'}]),
#         ]
#
#         # Verify cm is triggereg with default parameters
#         parsed_args = self.check_parser(self.cmd, arglist, verifylist)
#
#         # Set the response for find_vault
#         self.client.find_vault.side_effect = [
#             vaultSDK.Vault(id='vault_id')
#         ]
#
#         # Set the response
#         self.client.associate_resources.side_effect = [
#             self.object
#         ]
#
#         # Trigger the action
#         columns, data = self.cmd.take_action(parsed_args)
#
#         self.client.associate_resources.assert_called_with(
#             vault='vault_id',
#             resources=[{'id': 'resource_id', 'type': 'resource_type'}]
#         )
#
#         self.client.associate_resources.assert_called_once_with(
#             vault='vault_id',
#             resources=[{'id': 'resource_id', 'type': 'resource_type'}]
#         )
#
#         self.assertEqual(self.columns, columns)
#         self.assertEqual(self.data, data)
#
#
# class TestBindVaultPolicy(fakes.TestCBR):
#     object = fakes.VaultDefaultStruct(
#         **{
#             '_content': b'{"associate_policy": '
#                         b'{"vault_id" : "vault_id",'
#                         b'"policy_id" : "policy_id"}}'
#         }
#     )
#     columns = (
#         'vault_id',
#         'policy_id',
#     )
#     data = (
#         'vault_id',
#         'policy_id',
#     )
#
#     def setUp(self):
#         super(TestBindVaultPolicy, self).setUp()
#
#         self.cmd = vault.BindVaultPolicy(self.app, None)
#         self.app.client_manager.sdk_connection = mock.Mock()
#
#         self.client.bind_policy = mock.Mock()
#
#     def test_default(self):
#         arglist = [
#             'vault_id',
#             'policy_id',
#         ]
#         verifylist = [
#             ('vault', 'vault_id'),
#             ('policy', 'policy_id'),
#         ]
#
#         # Verify cm is triggereg with default parameters
#         parsed_args = self.check_parser(self.cmd, arglist, verifylist)
#
#         # Set the response for find_vault
#         self.client.find_vault.side_effect = [
#             vaultSDK.Vault(id='vault_id')
#         ]
#
#         # Set the response
#         self.client.bind_policy.side_effect = [
#             self.object
#         ]
#
#         # Trigger the action
#         columns, data = self.cmd.take_action(parsed_args)
#
#         self.client.bind_policy.assert_called_with(
#             vault='vault_id',
#             policy='policy_id'
#         )
#
#         self.client.bind_policy.assert_called_once_with(
#             vault='vault_id',
#             policy='policy_id'
#         )
#
#         self.assertEqual(self.columns, columns)
#         self.assertEqual(self.data, data)
