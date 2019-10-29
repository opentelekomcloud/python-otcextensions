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
#
import mock

from osc_lib import exceptions

from otcextensions.osclient.rds.v3 import instance
from otcextensions.tests.unit.osclient.rds.v3 import fakes


class TestListDatabaseInstances(fakes.TestRds):

    objects = fakes.FakeInstance.create_multiple(3)

    column_list_headers = (
        'ID', 'Name', 'Datastore Type', 'Datastore Version', 'Status',
        'Flavor_ref', 'Type', 'Size', 'Region'
    )

    columns = (
        'id', 'name', 'datastore_type', 'datastore_version'
    )

    data = []

    for s in objects:
        data.append(
            (s.id, s.name, s.datastore['type'], s.datastore['version'],
             s.status, s.flavor_ref, s.type, s.volume['size'], s.region))

    def setUp(self):
        super(TestListDatabaseInstances, self).setUp()

        self.cmd = instance.ListDatabaseInstances(self.app, None)

        self.client.instances = mock.Mock()
        self.client.api_mock = self.client.instances

    def test_list(self):
        arglist = []

        verifylist = []

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with()

        self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(self.data, list(data))

    def test_list_args(self):
        arglist = [
            '--limit', '1',
            '--id', '2',
            '--name', '3',
            '--type', 'ha',
            '--datastore-type', 'postgreSqL',
            '--router-id', '6',
            '--network-id', '7',
            '--offset', '8',
        ]

        verifylist = [
            ('limit', 1),
            ('id', '2'),
            ('name', '3'),
            ('type', 'ha'),
            ('datastore_type', 'postgresql'),
            ('router_id', '6'),
            ('network_id', '7'),
            ('offset', 8),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(
            datastore_type='PostgreSQL',
            id='2',
            limit=1,
            name='3',
            offset=8,
            router_id='6',
            network_id='7',
            type='Ha',
            paginated=False
        )

    def test_list_args_paginated(self):
        arglist = [
            '--id', '2',
            '--name', '3',
            '--type', 'ha',
            '--datastore-type', 'postgreSqL',
            '--router-id', '6',
            '--network-id', '7',
            '--offset', '8',
        ]

        verifylist = [
            ('id', '2'),
            ('name', '3'),
            ('type', 'ha'),
            ('datastore_type', 'postgresql'),
            ('router_id', '6'),
            ('network_id', '7'),
            ('offset', 8),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(
            datastore_type='PostgreSQL',
            id='2',
            name='3',
            offset=8,
            router_id='6',
            network_id='7',
            type='Ha',
        )


class TestShowDatabaseInstance(fakes.TestRds):

    _data = fakes.FakeInstance.create_one()

    columns = (
        'datastore', 'flavor_ref', 'id', 'name', 'region', 'status', 'volume'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestShowDatabaseInstance, self).setUp()

        self.cmd = instance.ShowDatabaseInstance(self.app, None)

        self.client.find_instance = mock.Mock(return_value=self._data)

    def test_show(self):
        arglist = [
            'test_instance',
        ]

        verifylist = [
            ('instance', 'test_instance'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.find_instance.assert_called_with('test_instance',
                                                     ignore_missing=False)

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestDeleteDatabaseInstance(fakes.TestRds):

    data = fakes.FakeInstance.create_one()

    def setUp(self):
        super(TestDeleteDatabaseInstance, self).setUp()

        self.cmd = instance.DeleteDatabaseInstance(self.app, None)

        self.client.delete_instance = mock.Mock(return_value=self.data)
        self.client.find_instance = mock.Mock(return_value=self.data)
        self.client.wait_for_job = mock.Mock()

    def test_delete(self):
        arglist = [
            'test_obj',
        ]

        verifylist = [
            ('instance', 'test_obj'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.find_instance.assert_called_with('test_obj')

        self.client.delete_instance.assert_called_with(self.data.id)
        self.client.wait_for_job.assert_not_called()

    def test_delete_wait(self):
        arglist = [
            'test_obj',
            '--wait'
        ]

        verifylist = [
            ('instance', 'test_obj'),
            ('wait', True)
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.find_instance.assert_called_with('test_obj')

        self.client.delete_instance.assert_called_with(self.data.id)

        self.client.wait_for_job.assert_called_with(self.data.job_id)


class TestCreateDatabaseInstance(fakes.TestRds):

    _data = fakes.FakeInstance.create_one()
    other_instance = fakes.FakeInstance.create_one()
    flavors = fakes.FakeFlavor.create_multiple(10)

    columns = ()

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestCreateDatabaseInstance, self).setUp()

        self.cmd = instance.CreateDatabaseInstance(self.app, None)

        self.client.flavors = mock.Mock(return_value=self.flavors)
        self.flavor = self.find_flavor('single')
        self.client.find_instance = mock.Mock(return_value=self.other_instance)
        self.client.create_instance = mock.Mock(return_value=self._data)
        self.client.get_instance = mock.Mock(return_value=self._data)
        self.client.wait_for_job = mock.Mock()

    def test_create(self):
        arglist = [
            'inst_name',
            self.flavor.name,
            '--availability-zone', 'test-az-01',
            '--configuration', '123',
            '--datastore-type', 'MySQL',
            '--datastore-version', '5.7',
            '--disk-encryption-id', '234',
            '--router-id', 'test-vpc-id',
            '--network-id', 'test-network-id',
            '--security-group-id', 'test-sec_grp-id',
            '--volume-type', 'ULTRAHIGH',
            '--size', '100',
            '--password', 'testtest',
            '--region', 'test-region',
            '--port', '12345'
        ]

        verifylist = [
            ('name', 'inst_name'),
            ('configuration_id', '123'),
            ('flavor_ref', self.flavor.name),
            ('availability_zone', 'test-az-01'),
            ('datastore_type', 'MySQL'),
            ('datastore_version', '5.7'),
            ('disk_encryption_id', '234'),
            ('router_id', 'test-vpc-id'),
            ('network_id', 'test-network-id'),
            ('security_group_id', 'test-sec_grp-id'),
            ('port', 12345),
            ('volume_type', 'ULTRAHIGH'),
            ('size', 100),
            ('password', 'testtest'),
            ('region', 'test-region')]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.find_instance.assert_not_called()

        self.client.create_instance.assert_called_with(
            availability_zone='test-az-01',
            charge_info={'charge_mode': 'postPaid'},
            configuration_id='123',
            datastore={'type': 'MySQL', 'version': '5.7'},
            disk_encryption_id='234',
            flavor_ref=self.flavor.name,
            name='inst_name',
            password='testtest',
            port=12345,
            region='test-region',
            router_id='test-vpc-id',
            security_group_id='test-sec_grp-id',
            volume={'size': 100, 'type': 'ULTRAHIGH'},
            network_id='test-network-id'
        )

    def test_create_ha(self):
        flavor = self.find_flavor('ha')
        arglist = [
            'inst_name',
            flavor.name,
            '--availability-zone', 'test-az-01,az2',
            '--configuration', '123',
            '--datastore-type', 'MySQL',
            '--datastore-version', '5.7',
            '--disk-encryption-id', '234',
            '--ha-mode', 'async',
            '--router-id', 'test-vpc-id',
            '--network-id', 'test-network-id',
            '--security-group-id', 'test-sec_grp-id',
            '--volume-type', 'ULTRAHIGH',
            '--size', '100',
            '--password', 'testtest',
            '--region', 'test-region',
            '--port', '12345',
            '--wait'
        ]

        verifylist = [
            ('name', 'inst_name'),
            ('configuration_id', '123'),
            ('flavor_ref', flavor.name),
            ('ha_mode', 'async'),
            ('availability_zone', 'test-az-01,az2'),
            ('datastore_type', 'MySQL'),
            ('datastore_version', '5.7'),
            ('disk_encryption_id', '234'),
            ('router_id', 'test-vpc-id'),
            ('network_id', 'test-network-id'),
            ('security_group_id', 'test-sec_grp-id'),
            ('port', 12345),
            ('volume_type', 'ULTRAHIGH'),
            ('size', 100),
            ('password', 'testtest'),
            ('region', 'test-region'),
            ('wait', True)
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.find_instance.assert_not_called()

        self.client.create_instance.assert_called_with(
            availability_zone='test-az-01,az2',
            charge_info={'charge_mode': 'postPaid'},
            configuration_id='123',
            datastore={'type': 'MySQL', 'version': '5.7'},
            disk_encryption_id='234',
            flavor_ref=flavor.name,
            name='inst_name',
            password='testtest',
            port=12345,
            region='test-region',
            router_id='test-vpc-id',
            security_group_id='test-sec_grp-id',
            volume={'size': 100, 'type': 'ULTRAHIGH'},
            network_id='test-network-id',
            ha={'mode': 'ha', 'replication_mode': 'async'}
        )

        self.client.wait_for_job.assert_called_with(self._data.job_id)
        self.client.get_instance.assert_called_with(self._data.id)

    def test_create_ha_wrong_az(self):
        flavor = self.find_flavor('ha')
        arglist = [
            'inst_name',
            flavor.name,
            '--availability-zone', 'test-az-01',
            '--configuration', '123',
            '--datastore-type', 'MySQL',
            '--datastore-version', '5.7',
            '--disk-encryption-id', '234',
            '--ha-mode', 'sync',
            '--router-id', 'test-vpc-id',
            '--network-id', 'test-network-id',
            '--security-group-id', 'test-sec_grp-id',
            '--volume-type', 'ULTRAHIGH',
            '--size', '100',
            '--password', 'testtest',
            '--region', 'test-region',
            '--port', '12345',
            '--wait'
        ]

        verifylist = [
            ('name', 'inst_name'),
            ('configuration_id', '123'),
            ('flavor_ref', flavor.name),
            ('ha_mode', 'sync'),
            ('availability_zone', 'test-az-01'),
            ('datastore_type', 'MySQL'),
            ('datastore_version', '5.7'),
            ('disk_encryption_id', '234'),
            ('router_id', 'test-vpc-id'),
            ('network_id', 'test-network-id'),
            ('security_group_id', 'test-sec_grp-id'),
            ('port', 12345),
            ('volume_type', 'ULTRAHIGH'),
            ('size', 100),
            ('password', 'testtest'),
            ('region', 'test-region'),
            ('wait', True)
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        self.assertRaises(
            exceptions.CommandError,
            self.cmd.take_action,
            parsed_args)

    def test_create_ha_wrong_mode_pg(self):
        flavor = self.find_flavor('ha')
        arglist = [
            'inst_name',
            flavor.name,
            '--availability-zone', 'test-az-01,az2',
            '--configuration', '123',
            '--datastore-type', 'postgresql',
            '--datastore-version', '5.7',
            '--disk-encryption-id', '234',
            '--ha-mode', 'semisync',
            '--router-id', 'test-vpc-id',
            '--network-id', 'test-network-id',
            '--security-group-id', 'test-sec_grp-id',
            '--volume-type', 'ULTRAHIGH',
            '--size', '100',
            '--password', 'testtest',
            '--region', 'test-region',
            '--port', '12345',
            '--wait'
        ]

        verifylist = [
            ('name', 'inst_name'),
            ('configuration_id', '123'),
            ('flavor_ref', flavor.name),
            ('ha_mode', 'semisync'),
            ('availability_zone', 'test-az-01,az2'),
            ('datastore_type', 'postgresql'),
            ('datastore_version', '5.7'),
            ('disk_encryption_id', '234'),
            ('router_id', 'test-vpc-id'),
            ('network_id', 'test-network-id'),
            ('security_group_id', 'test-sec_grp-id'),
            ('port', 12345),
            ('volume_type', 'ULTRAHIGH'),
            ('size', 100),
            ('password', 'testtest'),
            ('region', 'test-region'),
            ('wait', True)
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        self.assertRaises(
            exceptions.CommandError,
            self.cmd.take_action,
            parsed_args)

    def test_create_ha_wrong_mode_mysql(self):
        flavor = self.find_flavor('ha')
        arglist = [
            'inst_name',
            flavor.name,
            '--availability-zone', 'test-az-01,az2',
            '--configuration', '123',
            '--datastore-type', 'MySQL',
            '--datastore-version', '5.7',
            '--disk-encryption-id', '234',
            '--ha-mode', 'sync',
            '--router-id', 'test-vpc-id',
            '--network-id', 'test-network-id',
            '--security-group-id', 'test-sec_grp-id',
            '--volume-type', 'ULTRAHIGH',
            '--size', '100',
            '--password', 'testtest',
            '--region', 'test-region',
            '--port', '12345',
            '--wait'
        ]

        verifylist = [
            ('name', 'inst_name'),
            ('configuration_id', '123'),
            ('flavor_ref', flavor.name),
            ('ha_mode', 'sync'),
            ('availability_zone', 'test-az-01,az2'),
            ('datastore_type', 'MySQL'),
            ('datastore_version', '5.7'),
            ('disk_encryption_id', '234'),
            ('router_id', 'test-vpc-id'),
            ('network_id', 'test-network-id'),
            ('security_group_id', 'test-sec_grp-id'),
            ('port', 12345),
            ('volume_type', 'ULTRAHIGH'),
            ('size', 100),
            ('password', 'testtest'),
            ('region', 'test-region'),
            ('wait', True)
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        self.assertRaises(
            exceptions.CommandError,
            self.cmd.take_action,
            parsed_args)

    def test_create_ha_wrong_mode_mssql(self):
        flavor = self.find_flavor('ha')
        arglist = [
            'inst_name',
            flavor.name,
            '--availability-zone', 'test-az-01,az2',
            '--configuration', '123',
            '--datastore-type', 'sqlserver',
            '--datastore-version', '5.7',
            '--disk-encryption-id', '234',
            '--ha-mode', 'async',
            '--router-id', 'test-vpc-id',
            '--network-id', 'test-network-id',
            '--security-group-id', 'test-sec_grp-id',
            '--volume-type', 'ULTRAHIGH',
            '--size', '100',
            '--password', 'testtest',
            '--region', 'test-region',
            '--port', '12345',
            '--wait'
        ]

        verifylist = [
            ('name', 'inst_name'),
            ('configuration_id', '123'),
            ('flavor_ref', flavor.name),
            ('ha_mode', 'async'),
            ('availability_zone', 'test-az-01,az2'),
            ('datastore_type', 'sqlserver'),
            ('datastore_version', '5.7'),
            ('disk_encryption_id', '234'),
            ('router_id', 'test-vpc-id'),
            ('network_id', 'test-network-id'),
            ('security_group_id', 'test-sec_grp-id'),
            ('port', 12345),
            ('volume_type', 'ULTRAHIGH'),
            ('size', 100),
            ('password', 'testtest'),
            ('region', 'test-region'),
            ('wait', True)
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        self.assertRaises(
            exceptions.CommandError,
            self.cmd.take_action,
            parsed_args)

        arglist = [
            'inst_name',
            flavor.name,
            '--availability-zone', 'test-az-01,az2',
            '--configuration', '123',
            '--datastore-type', 'sqlserver',
            '--datastore-version', '5.7',
            '--disk-encryption-id', '234',
            '--ha-mode', 'semisync',
            '--router-id', 'test-vpc-id',
            '--network-id', 'test-network-id',
            '--security-group-id', 'test-sec_grp-id',
            '--volume-type', 'ULTRAHIGH',
            '--size', '100',
            '--password', 'testtest',
            '--region', 'test-region',
            '--port', '12345',
            '--wait'
        ]

        verifylist = [
            ('name', 'inst_name'),
            ('configuration_id', '123'),
            ('flavor_ref', flavor.name),
            ('ha_mode', 'semisync'),
            ('availability_zone', 'test-az-01,az2'),
            ('datastore_type', 'sqlserver'),
            ('datastore_version', '5.7'),
            ('disk_encryption_id', '234'),
            ('router_id', 'test-vpc-id'),
            ('network_id', 'test-network-id'),
            ('security_group_id', 'test-sec_grp-id'),
            ('port', 12345),
            ('volume_type', 'ULTRAHIGH'),
            ('size', 100),
            ('password', 'testtest'),
            ('region', 'test-region'),
            ('wait', True)
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        self.assertRaises(
            exceptions.CommandError,
            self.cmd.take_action,
            parsed_args)

    def find_flavor(self, instance_mode):
        flavor = None
        for f in self.flavors:
            if f.instance_mode == instance_mode:
                flavor = f
        if not flavor:
            self.flavors[0].instance_mode = instance_mode
            flavor = self.flavors[0]
        # For the moment just ensure we have found something
        self.assertIsNotNone(flavor)
        return flavor

    def test_create_replica(self):
        flavor = self.find_flavor('replica')
        arglist = [
            'inst_name',
            flavor.name,
            '--availability-zone', 'test-az-01',
            '--configuration', '123',
            '--datastore-type', 'MySQL',
            '--datastore-version', '5.7',
            '--disk-encryption-id', '234',
            '--replica-of', 'fake_name',
            '--volume-type', 'ULTRAHIGH',
            '--size', '100',
            '--region', 'test-region',
        ]

        verifylist = [
            ('name', 'inst_name'),
            ('configuration_id', '123'),
            ('flavor_ref', flavor.name),
            ('availability_zone', 'test-az-01'),
            ('datastore_type', 'MySQL'),
            ('datastore_version', '5.7'),
            ('disk_encryption_id', '234'),
            ('replica_of', 'fake_name'),
            ('volume_type', 'ULTRAHIGH'),
            ('size', 100),
            ('region', 'test-region')]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.create_instance.assert_called_with(
            availability_zone='test-az-01',
            charge_info={'charge_mode': 'postPaid'},
            configuration_id='123',
            datastore={'type': 'MySQL', 'version': '5.7'},
            disk_encryption_id='234',
            flavor_ref=flavor.name,
            name='inst_name',
            region='test-region',
            replica_of_id=self.other_instance.id,
            volume={'size': 100, 'type': 'ULTRAHIGH'},
        )

    def test_create_replica_exception(self):
        arglist = [
            'inst_name',
            'test-flavor',
            '--availability-zone', 'test-az-01',
            '--configuration', '123',
            '--datastore-type', 'MySQL',
            '--datastore-version', '5.7',
            '--disk-encryption-id', '234',
            '--ha-mode', 'semisync',
            '--replica-of', 'fake_name',
            '--port', '5432',
            '--volume-type', 'ULTRAHIGH',
            '--size', '100',
            '--region', 'test-region',
        ]

        verifylist = [
            ('name', 'inst_name'),
            ('configuration_id', '123'),
            ('flavor_ref', 'test-flavor'),
            ('availability_zone', 'test-az-01'),
            ('datastore_type', 'MySQL'),
            ('datastore_version', '5.7'),
            ('disk_encryption_id', '234'),
            ('ha_mode', 'semisync'),
            ('replica_of', 'fake_name'),
            ('port', 5432),
            ('volume_type', 'ULTRAHIGH'),
            ('size', 100),
            ('region', 'test-region')]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        self.assertRaises(exceptions.CommandError,
                          self.cmd.take_action, parsed_args)

    def test_create_from_instance_pir(self):
        arglist = [
            'inst_name',
            self.flavor.name,
            '--availability-zone', 'test-az-01',
            '--configuration', '123',
            '--datastore-type', 'MySQL',
            '--datastore-version', '5.7',
            '--disk-encryption-id', '234',
            '--router-id', 'test-vpc-id',
            '--network-id', 'test-network-id',
            '--security-group-id', 'test-sec_grp-id',
            '--volume-type', 'ULTRAHIGH',
            '--size', '100',
            '--password', 'testtest',
            '--region', 'test-region',
            '--port', '12345',
            '--from-instance', 'source_instance',
            '--restore-time', 'abcde'
        ]

        verifylist = [
            ('name', 'inst_name'),
            ('configuration_id', '123'),
            ('flavor_ref', self.flavor.name),
            ('availability_zone', 'test-az-01'),
            ('datastore_type', 'MySQL'),
            ('datastore_version', '5.7'),
            ('disk_encryption_id', '234'),
            ('router_id', 'test-vpc-id'),
            ('network_id', 'test-network-id'),
            ('security_group_id', 'test-sec_grp-id'),
            ('port', 12345),
            ('volume_type', 'ULTRAHIGH'),
            ('size', 100),
            ('password', 'testtest'),
            ('region', 'test-region'),
            ('from_instance', 'source_instance'),
            ('restore_time', 'abcde')
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.find_instance.assert_called_with('source_instance',
                                                     ignore_missing=False)

        self.client.create_instance.assert_called_with(
            availability_zone='test-az-01',
            charge_info={'charge_mode': 'postPaid'},
            configuration_id='123',
            datastore={'type': 'MySQL', 'version': '5.7'},
            disk_encryption_id='234',
            flavor_ref=self.flavor.name,
            name='inst_name',
            password='testtest',
            port=12345,
            region='test-region',
            router_id='test-vpc-id',
            security_group_id='test-sec_grp-id',
            volume={'size': 100, 'type': 'ULTRAHIGH'},
            network_id='test-network-id',
            restore_point={
                'type': 'timestamp',
                'restore_time': 'abcde',
                'instance_id': self.other_instance.id}
        )

        self.client.find_instance.assert_called_with('source_instance',
                                                     ignore_missing=False)

    def test_create_from_backup(self):
        arglist = [
            'inst_name',
            self.flavor.name,
            '--availability-zone', 'test-az-01',
            '--configuration', '123',
            '--datastore-type', 'MySQL',
            '--datastore-version', '5.7',
            '--disk-encryption-id', '234',
            '--router-id', 'test-vpc-id',
            '--network-id', 'test-network-id',
            '--security-group-id', 'test-sec_grp-id',
            '--volume-type', 'ULTRAHIGH',
            '--size', '100',
            '--password', 'testtest',
            '--region', 'test-region',
            '--port', '12345',
            '--backup', 'source_backup',
            '--from-instance', 'source_instance'
        ]

        verifylist = [
            ('name', 'inst_name'),
            ('configuration_id', '123'),
            ('flavor_ref', self.flavor.name),
            ('availability_zone', 'test-az-01'),
            ('datastore_type', 'MySQL'),
            ('datastore_version', '5.7'),
            ('disk_encryption_id', '234'),
            ('router_id', 'test-vpc-id'),
            ('network_id', 'test-network-id'),
            ('security_group_id', 'test-sec_grp-id'),
            ('port', 12345),
            ('volume_type', 'ULTRAHIGH'),
            ('size', 100),
            ('password', 'testtest'),
            ('region', 'test-region'),
            ('backup', 'source_backup'),
            ('from_instance', 'source_instance')
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        backup = self.backup_mock.create_one()
        self.client.find_backup = mock.Mock(return_value=backup)

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.create_instance.assert_called_with(
            availability_zone='test-az-01',
            charge_info={'charge_mode': 'postPaid'},
            configuration_id='123',
            datastore={'type': 'MySQL', 'version': '5.7'},
            disk_encryption_id='234',
            flavor_ref=self.flavor.name,
            name='inst_name',
            password='testtest',
            port=12345,
            region='test-region',
            router_id='test-vpc-id',
            security_group_id='test-sec_grp-id',
            volume={'size': 100, 'type': 'ULTRAHIGH'},
            network_id='test-network-id',
            restore_point={
                'type': 'backup',
                'backup_id': backup.id,
                'instance_id': backup.instance_id}
        )

        self.client.find_instance.assert_called_with('source_instance',
                                                     ignore_missing=False)
        self.client.find_backup.assert_called_with(
            instance=self.other_instance,
            name_or_id='source_backup',
            ignore_missing=False)

    def test_create_from_backup_no_instance(self):
        arglist = [
            'inst_name',
            'test-flavor',
            '--availability-zone', 'test-az-01',
            '--configuration', '123',
            '--datastore-type', 'MySQL',
            '--datastore-version', '5.7',
            '--disk-encryption-id', '234',
            '--ha-mode', 'semisync',
            '--router-id', 'test-vpc-id',
            '--network-id', 'test-network-id',
            '--security-group-id', 'test-sec_grp-id',
            '--volume-type', 'ULTRAHIGH',
            '--size', '100',
            '--password', 'testtest',
            '--region', 'test-region',
            '--port', '12345',
            '--backup', 'source_backup',
        ]

        verifylist = [
            ('name', 'inst_name'),
            ('configuration_id', '123'),
            ('flavor_ref', 'test-flavor'),
            ('availability_zone', 'test-az-01'),
            ('datastore_type', 'MySQL'),
            ('datastore_version', '5.7'),
            ('disk_encryption_id', '234'),
            ('ha_mode', 'semisync'),
            ('router_id', 'test-vpc-id'),
            ('network_id', 'test-network-id'),
            ('security_group_id', 'test-sec_grp-id'),
            ('port', 12345),
            ('volume_type', 'ULTRAHIGH'),
            ('size', 100),
            ('password', 'testtest'),
            ('region', 'test-region'),
            ('backup', 'source_backup'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        self.assertRaises(
            exceptions.CommandError,
            self.cmd.take_action,
            parsed_args
        )

    def test_create_primary_missing_params(self):
        arglist = [
            'inst_name',
            'test-flavor',
            '--availability-zone', 'test-az-01',
            '--configuration', '123',
            '--datastore-type', 'MySQL',
            '--datastore-version', '5.7',
            '--disk-encryption-id', '234',
            '--ha-mode', 'semisync',
            '--router-id', 'test-vpc-id',
            '--volume-type', 'ULTRAHIGH',
            '--size', '100',
            '--password', 'testtest',
            '--region', 'test-region',
            '--port', '12345'
        ]

        verifylist = [
            ('name', 'inst_name'),
            ('configuration_id', '123'),
            ('flavor_ref', 'test-flavor'),
            ('availability_zone', 'test-az-01'),
            ('datastore_type', 'MySQL'),
            ('datastore_version', '5.7'),
            ('disk_encryption_id', '234'),
            ('ha_mode', 'semisync'),
            ('router_id', 'test-vpc-id'),
            ('port', 12345),
            ('volume_type', 'ULTRAHIGH'),
            ('size', 100),
            ('password', 'testtest'),
            ('region', 'test-region')]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        self.assertRaises(exceptions.CommandError,
                          self.cmd.take_action,
                          parsed_args)


class TestRestoreDatabaseInstance(fakes.TestRds):

    def setUp(self):
        super(TestRestoreDatabaseInstance, self).setUp()

        self.cmd = instance.RestoreDatabaseInstance(self.app, None)

        self.instance = self.instance_mock.create_one()
        self.backup = self.backup_mock.create_one()

        self.client.find_instance = mock.Mock(return_value=self.instance)
        self.restore_result = mock.Mock()
        self.restore_result.job_id = 'some_job_id'
        self.client.restore_instance = mock.Mock(
            return_value=self.restore_result)
        self.client.find_backup = mock.Mock(return_value=self.backup)
        self.client.wait_for_job = mock.Mock()

    def test_action_from_backup(self):
        arglist = [
            'inst_name',
            '--backup', 'backup',
        ]

        verifylist = [
            ('instance', 'inst_name'),
            ('backup', 'backup'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.find_instance.assert_called_with('inst_name',
                                                     ignore_missing=False)

        self.client.find_backup.assert_called_with(name_or_id='backup',
                                                   instance=self.instance,
                                                   ignore_missing=False)

        self.client.restore_instance.assert_called_with(
            backup=self.client.find_backup(),
            instance=self.instance,
            restore_time=None
        )

    def test_action_pit(self):
        arglist = [
            'inst_name',
            '--restore-time', 'some_time',
        ]

        verifylist = [
            ('instance', 'inst_name'),
            ('restore_time', 'some_time'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.find_instance.assert_called_with('inst_name',
                                                     ignore_missing=False)

        self.client.restore_instance.assert_called_with(
            backup=None,
            instance=self.instance,
            restore_time='some_time'
        )

    def test_action_wait(self):
        arglist = [
            'inst_name',
            '--restore-time', 'some_time',
            '--wait',
            '--wait-interval', '5'
        ]

        verifylist = [
            ('instance', 'inst_name'),
            ('restore_time', 'some_time'),
            ('wait', True),
            ('wait_interval', 5)
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.find_instance.assert_called_with('inst_name',
                                                     ignore_missing=False)

        self.client.restore_instance.assert_called_with(
            backup=None,
            instance=self.instance,
            restore_time='some_time'
        )

        self.client.wait_for_job.assert_called_with(
            self.restore_result.job_id,
            interval=5
        )


class TestShowBackupPolicy(fakes.TestRds):

    _instance = fakes.FakeInstance.create_one()
    _data = {'keep_days': 1, 'period': '2', 'start_time': '3'}

    columns = (
        'keep_days', 'period', 'start_time'
    )

    data = (1, '2', '3')

    def setUp(self):
        super(TestShowBackupPolicy, self).setUp()

        self.cmd = instance.ShowBackupPolicy(self.app, None)

        self.client.find_instance = mock.Mock()
        self.client.get_instance_backup_policy = mock.Mock()

    def test_action(self):
        arglist = [
            'inst'
        ]

        verifylist = [
            ('instance', 'inst'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.find_instance.return_value = self._instance
        self.client.get_instance_backup_policy.return_value = self._data

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_instance.assert_called_with('inst',
                                                     ignore_missing=False)

        self.client.get_instance_backup_policy.assert_called_once_with(
            self._instance
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestSetBackupPolicy(fakes.TestRds):

    _instance = fakes.FakeInstance.create_one()

    def setUp(self):
        super(TestSetBackupPolicy, self).setUp()

        self.cmd = instance.SetBackupPolicy(self.app, None)

        self.client.find_instance = mock.Mock()
        self.client.set_instance_backup_policy = mock.Mock()

    def test_action(self):
        arglist = [
            'inst',
            '--keep-days', '1',
            '--period', '2',
            '--start-time', '3'
        ]

        verifylist = [
            ('instance', 'inst'),
            ('keep_days', 1),
            ('period', '2'),
            ('start_time', '3')
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.find_instance.return_value = self._instance

        # Trigger the action
        self.assertIsNone(self.cmd.take_action(parsed_args))

        self.client.find_instance.assert_called_with('inst',
                                                     ignore_missing=False)

        self.client.set_instance_backup_policy.assert_called_once_with(
            self._instance,
            keep_days=1, period='2', start_time='3'
        )

    def test_action_set_0(self):
        arglist = [
            'inst',
            '--keep-days', '0'
        ]

        verifylist = [
            ('instance', 'inst'),
            ('keep_days', 0),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.find_instance.return_value = self._instance

        # Trigger the action
        self.assertIsNone(self.cmd.take_action(parsed_args))

        self.client.find_instance.assert_called_with('inst',
                                                     ignore_missing=False)

        self.client.set_instance_backup_policy.assert_called_once_with(
            self._instance,
            keep_days=0
        )


class TestShowAvailableRestoreTime(fakes.TestRds):

    instance = fakes.FakeInstance.create_one()

    objects = [
        {
            'start_time': 'some_fake_start',
            'end_time': 'some_fake_end'
        }
    ]

    column_list_headers = (
        'Start time', 'End time'
    )

    columns = (
        'start_time', 'end_time'
    )

    data = []

    for s in objects:
        data.append((s['start_time'], s['end_time']))

    def setUp(self):
        super(TestShowAvailableRestoreTime, self).setUp()

        self.cmd = instance.ShowAvailableRestoreTime(self.app, None)

        self.client.find_instance = mock.Mock(return_value=self.instance)
        self.client.get_instance_restore_time = mock.Mock(
            return_value=self.objects)

    def test_action(self):
        arglist = [
            'test_inst'
        ]

        verifylist = [
            ('instance', 'test_inst')
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_instance.assert_called_with('test_inst',
                                                     ignore_missing=False)
        self.client.get_instance_restore_time.assert_called_with(self.instance)

        self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(self.data, list(data))
