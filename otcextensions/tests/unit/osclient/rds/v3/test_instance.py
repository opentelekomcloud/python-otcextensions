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

from osc_lib.cli import format_columns

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

    data = (
        format_columns.DictColumn(_data.datastore),
        _data.flavor_ref,
        _data.id,
        _data.name,
        _data.region,
        _data.status,
        format_columns.DictColumn(_data.volume)
    )

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
        self.assertItemEqual(self.data, data)


class TestDeleteDatabaseInstance(fakes.TestRds):

    def setUp(self):
        super(TestDeleteDatabaseInstance, self).setUp()

        self.cmd = instance.DeleteDatabaseInstance(self.app, None)

        self.sdk_client.delete_instance = mock.Mock()

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

        self.sdk_client.delete_rds_instance.assert_called_with(
            instance='test_obj', wait=False)

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

        self.sdk_client.delete_rds_instance.assert_called_with(
            instance='test_obj', wait=True)


class TestCreateDatabaseInstance(fakes.TestRds):

    _data = fakes.FakeInstance.create_one()

    columns = ()

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestCreateDatabaseInstance, self).setUp()

        self.cmd = instance.CreateDatabaseInstance(self.app, None)

        self.sdk_client.create_rds_instance = mock.Mock(
            return_value=self._data)

    def test_create(self):
        arglist = [
            'inst_name',
            'test-flavor',
            '--availability-zone', 'test-az-01',
            '--backup', 'source_backup',
            '--backup-keepdays', 'bkd',
            '--backup-timeframe', 'xxx',
            '--charge-mode', 'postpaid',
            '--configuration', '123',
            '--datastore-type', 'MySQL',
            '--datastore-version', '5.7',
            '--disk-encryption-id', '234',
            '--from-instance', 'source_instance',
            '--ha-mode', 'async',
            '--network-id', 'test-network-id',
            '--password', 'CrackMe123',
            '--port', '12345',
            '--region', 'test-region',
            '--replica-of', 'replica_instance',
            '--restore-time', 'restore_time_123',
            '--router-id', 'test-vpc-id',
            '--security-group-id', 'test-sec_grp-id',
            '--volume-type', 'ULTRAHIGH',
            '--size', '100'
        ]

        verifylist = [
            ('name', 'inst_name'),
            ('configuration', '123'),
            ('flavor', 'test-flavor'),
            ('availability_zone', 'test-az-01'),
            ('datastore_type', 'MySQL'),
            ('datastore_version', '5.7'),
            ('disk_encryption_id', '234'),
            ('router', 'test-vpc-id'),
            ('network', 'test-network-id'),
            ('security_group', 'test-sec_grp-id'),
            ('port', 12345),
            ('volume_type', 'ULTRAHIGH'),
            ('volume_size', 100),
            ('password', 'CrackMe123'),
            ('region', 'test-region')]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.sdk_client.create_rds_instance.assert_called_with(
            availability_zone='test-az-01', backup='source_backup',
            backup_keepdays='bkd', backup_timeframe='xxx',
            charge_mode='postpaid', configuration='123',
            datastore_type='MySQL', datastore_version='5.7',
            disk_encryption_id='234', flavor='test-flavor',
            from_instance='source_instance', ha_mode='async', name='inst_name',
            network='test-network-id', password='CrackMe123', port=12345,
            region='test-region', replica_of='replica_instance',
            restore_time='restore_time_123', router='test-vpc-id',
            security_group='test-sec_grp-id', volume_size=100,
            volume_type='ULTRAHIGH', wait=False
        )


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
