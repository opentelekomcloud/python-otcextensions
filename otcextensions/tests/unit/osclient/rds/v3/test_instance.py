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

from osc_lib import exceptions

from otcextensions.osclient.rds.v3 import instance
from otcextensions.tests.unit.osclient.rds.v3 import fakes as rds_fakes


class TestListDatabaseInstances(rds_fakes.TestRds):

    column_list_headers = [
        'ID', 'Name', 'Datastore Type', 'Datastore Version', 'Status',
        'Flavor_ref', 'Type', 'Size', 'Region'
    ]

    def setUp(self):
        super(TestListDatabaseInstances, self).setUp()

        self.cmd = instance.ListDatabaseInstances(self.app, None)

        self.client.instances = mock.Mock()
        self.client.api_mock = self.client.instances

        self.objects = self.instance_mock.create_multiple(3)
        self.object_data = []
        for s in self.objects:
            self.object_data.append(
                (s.id, s.name, s.datastore['type'], s.datastore['version'],
                 s.status, s.flavor_ref, s.type, s.volume['size'], s.region))

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
        self.assertEqual(tuple(self.object_data), tuple(data))

    def test_list_args(self):
        arglist = [
            '--limit', '1',
            '--id', '2',
            '--name', '3',
            '--type', '4',
            '--database', '5',
            '--router_id', '6',
            '--subnet_id', '7',
            '--offset', '8',
        ]

        verifylist = [
            ('limit', 1),
            ('id', '2'),
            ('name', '3'),
            ('type', '4'),
            ('datastore_type', '5'),
            ('router_id', '6'),
            ('subnet_id', '7'),
            ('offset', 8),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(
            datastore_type='5',
            id='2',
            limit=1,
            name='3',
            offset=8,
            router_id='6',
            subnet_id='7',
            type='4'
        )


class TestShowDatabaseInstance(rds_fakes.TestRds):

    column_list_headers = [
        'datastore', 'flavor_ref', 'id', 'name', 'region'
        'status', 'volume'
    ]

    def setUp(self):
        super(TestShowDatabaseInstance, self).setUp()

        self.cmd = instance.ShowDatabaseInstance(self.app, None)

        self.object = self.instance_mock.create_one()

        self.client.find_instance = mock.Mock(return_value=self.object)

        self.object_data = (
            self.object.datastore,
            self.object.flavor_ref,
            self.object.id,
            self.object.name,
            self.object.region,
            self.object.status,
            self.object.volume,
        )

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
        self.client.find_instance.assert_called_with('test_instance')

        # self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(self.object_data, data)


class TestDeleteDatabaseInstance(rds_fakes.TestRds):

    def setUp(self):
        super(TestDeleteDatabaseInstance, self).setUp()

        self.cmd = instance.DeleteDatabaseInstance(self.app, None)

        self.object = self.instance_mock.create_one()

        self.client.delete_instance = mock.Mock()
        self.client.find_instance = mock.Mock(return_value=self.object)

    def test_delete(self):
        arglist = [
            'test_obj',
        ]

        verifylist = [
            ('instance', 'test_obj'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.delete_instance.side_effect = [True]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.find_instance.assert_called_with('test_obj')

        self.client.delete_instance.assert_called_with(self.object.id)


class TestCreateDatabaseInstance(rds_fakes.TestRds):

    def setUp(self):
        super(TestCreateDatabaseInstance, self).setUp()

        self.cmd = instance.CreateDatabaseInstance(self.app, None)

        self.client.find_flavor = mock.Mock()
        self.client.create_instance = mock.Mock()

        self.instance = self.instance_mock.create_one()
        self.flavor = self.flavor_mock.create_one()

    def test_create(self):
        arglist = [
            'inst_name',
            'test-flavor',
            '--availability-zone', 'test-az-01',
            '--configuration', '123',
            '--datastore', 'MySQL',
            '--datastore-version', '5.7',
            '--disk-encryption-id', '234',
            '--ha-mode', 'semisync',
            '--router-id', 'test-vpc-id',
            '--subnet-id', 'test-subnet-id',
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
            ('flavor_ref', 'test-flavor'),
            ('availability_zone', 'test-az-01'),
            ('datastore', 'MySQL'),
            ('datastore_version', '5.7'),
            ('disk_encryption_id', '234'),
            ('ha_mode', 'semisync'),
            ('router_id', 'test-vpc-id'),
            ('subnet_id', 'test-subnet-id'),
            ('security_group_id', 'test-sec_grp-id'),
            ('port', 12345),
            ('volume_type', 'ULTRAHIGH'),
            ('size', 100),
            ('password', 'testtest'),
            ('region', 'test-region')]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.create_instance.side_effect = [
            self.instance
        ]

        self.client.find_instance.return_value = self.instance

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.create_instance.assert_called_with(
            availability_zone='test-az-01',
            charge_info={'charge_mode': 'postPaid'},
            configuration_id='123',
            datastore={'type': 'MySQL', 'version': '5.7'},
            disk_encryption_id='234',
            flavor_ref='test-flavor',
            ha={'mode': 'ha', 'replication_mode': 'semisync'},
            name='inst_name',
            password='testtest',
            port=12345,
            region='test-region',
            router_id='test-vpc-id',
            security_group_id='test-sec_grp-id',
            volume={'size': 100, 'type': 'ULTRAHIGH'},
            subnet_id='test-subnet-id'
        )

    def test_create_replica(self):
        arglist = [
            'inst_name',
            'test-flavor',
            '--availability-zone', 'test-az-01',
            '--configuration', '123',
            '--datastore', 'MySQL',
            '--datastore-version', '5.7',
            '--disk-encryption-id', '234',
            '--ha-mode', 'semisync',
            '--replica-of', 'fake_name',
            '--volume-type', 'ULTRAHIGH',
            '--size', '100',
            '--region', 'test-region',
        ]

        verifylist = [
            ('name', 'inst_name'),
            ('configuration_id', '123'),
            ('flavor_ref', 'test-flavor'),
            ('availability_zone', 'test-az-01'),
            ('datastore', 'MySQL'),
            ('datastore_version', '5.7'),
            ('disk_encryption_id', '234'),
            ('ha_mode', 'semisync'),
            ('replica_of', 'fake_name'),
            ('volume_type', 'ULTRAHIGH'),
            ('size', 100),
            ('region', 'test-region')]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.create_instance.side_effect = [
            self.instance
        ]

        self.client.find_instance.return_value = self.instance

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.create_instance.assert_called_with(
            availability_zone='test-az-01',
            charge_info={'charge_mode': 'postPaid'},
            configuration_id='123',
            datastore={'type': 'MySQL', 'version': '5.7'},
            disk_encryption_id='234',
            flavor_ref='test-flavor',
            ha={'mode': 'ha', 'replication_mode': 'semisync'},
            name='inst_name',
            region='test-region',
            replica_of_id=self.instance.id,
            volume={'size': 100, 'type': 'ULTRAHIGH'},
        )

    def test_create_replica_exception(self):
        arglist = [
            'inst_name',
            'test-flavor',
            '--availability-zone', 'test-az-01',
            '--configuration', '123',
            '--datastore', 'MySQL',
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
            ('datastore', 'MySQL'),
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
            'test-flavor',
            '--availability-zone', 'test-az-01',
            '--configuration', '123',
            '--datastore', 'MySQL',
            '--datastore-version', '5.7',
            '--disk-encryption-id', '234',
            '--ha-mode', 'semisync',
            '--router-id', 'test-vpc-id',
            '--subnet-id', 'test-subnet-id',
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
            ('flavor_ref', 'test-flavor'),
            ('availability_zone', 'test-az-01'),
            ('datastore', 'MySQL'),
            ('datastore_version', '5.7'),
            ('disk_encryption_id', '234'),
            ('ha_mode', 'semisync'),
            ('router_id', 'test-vpc-id'),
            ('subnet_id', 'test-subnet-id'),
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

        # Set the response
        self.client.create_instance.side_effect = [
            self.instance
        ]

        self.client.find_instance.return_value = self.instance

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.create_instance.assert_called_with(
            availability_zone='test-az-01',
            charge_info={'charge_mode': 'postPaid'},
            configuration_id='123',
            datastore={'type': 'MySQL', 'version': '5.7'},
            disk_encryption_id='234',
            flavor_ref='test-flavor',
            ha={'mode': 'ha', 'replication_mode': 'semisync'},
            name='inst_name',
            password='testtest',
            port=12345,
            region='test-region',
            router_id='test-vpc-id',
            security_group_id='test-sec_grp-id',
            volume={'size': 100, 'type': 'ULTRAHIGH'},
            subnet_id='test-subnet-id',
            restore_point={
                'type': 'timestamp',
                'restore_time': 'abcde',
                'instance_id': self.instance.id}
        )

        self.client.find_instance.assert_called_with('source_instance',
                                                     ignore_missing=False)

    def test_create_from_backup(self):
        arglist = [
            'inst_name',
            'test-flavor',
            '--availability-zone', 'test-az-01',
            '--configuration', '123',
            '--datastore', 'MySQL',
            '--datastore-version', '5.7',
            '--disk-encryption-id', '234',
            '--ha-mode', 'semisync',
            '--router-id', 'test-vpc-id',
            '--subnet-id', 'test-subnet-id',
            '--security-group-id', 'test-sec_grp-id',
            '--volume-type', 'ULTRAHIGH',
            '--size', '100',
            '--password', 'testtest',
            '--region', 'test-region',
            '--port', '12345',
            '--from-backup', 'source_backup'
        ]

        verifylist = [
            ('name', 'inst_name'),
            ('configuration_id', '123'),
            ('flavor_ref', 'test-flavor'),
            ('availability_zone', 'test-az-01'),
            ('datastore', 'MySQL'),
            ('datastore_version', '5.7'),
            ('disk_encryption_id', '234'),
            ('ha_mode', 'semisync'),
            ('router_id', 'test-vpc-id'),
            ('subnet_id', 'test-subnet-id'),
            ('security_group_id', 'test-sec_grp-id'),
            ('port', 12345),
            ('volume_type', 'ULTRAHIGH'),
            ('size', 100),
            ('password', 'testtest'),
            ('region', 'test-region'),
            ('from_backup', 'source_backup')
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.create_instance.side_effect = [
            self.instance
        ]

        self.client.find_instance.return_value = self.instance
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
            flavor_ref='test-flavor',
            ha={'mode': 'ha', 'replication_mode': 'semisync'},
            name='inst_name',
            password='testtest',
            port=12345,
            region='test-region',
            router_id='test-vpc-id',
            security_group_id='test-sec_grp-id',
            volume={'size': 100, 'type': 'ULTRAHIGH'},
            subnet_id='test-subnet-id',
            restore_point={
                'type': 'backup',
                'backup_id': backup.id,
                'instance_id': backup.instance_id}
        )

        self.client.find_backup.assert_called_with('source_backup',
                                                   ignore_missing=False)


class TestRestoreDatabaseInstance(rds_fakes.TestRds):

    def setUp(self):
        super(TestRestoreDatabaseInstance, self).setUp()

        self.cmd = instance.RestoreDatabaseInstance(self.app, None)

        self.instance = self.instance_mock.create_one()
        self.backup = self.backup_mock.create_one()

        self.client.find_instance = mock.Mock(return_value=self.instance)
        self.client.restore_instance = mock.Mock()
        self.client.find_backup = mock.Mock(return_value=self.backup)

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

        find_calls = [
            mock.call('inst_name'),
        ]

        self.client.find_instance.assert_has_calls(find_calls)
        self.client.find_backup.assert_called_with('backup',
                                                   ignore_missing=False)

        self.client.restore_instance.assert_called_with(
            backup=self.client.find_backup(),
            instance=self.instance,
            source_instance=self.backup.instance_id,
            restore_time=None
        )

    def test_action_pit(self):
        arglist = [
            'inst_name',
            '--restore_time', 'some_time',
            '--source_instance', '12345'
        ]

        verifylist = [
            ('instance', 'inst_name'),
            ('restore_time', 'some_time'),
            ('source_instance', '12345')
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        self.cmd.take_action(parsed_args)

        find_calls = [
            mock.call('inst_name'),
            mock.call('12345')
        ]

        self.client.find_instance.assert_has_calls(find_calls)

        self.client.restore_instance.assert_called_with(
            backup=None,
            instance=self.instance,
            source_instance=self.instance,
            restore_time='some_time'
        )
