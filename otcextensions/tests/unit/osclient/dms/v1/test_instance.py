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
import mock

from otcextensions.osclient.dms.v1 import instance
from otcextensions.tests.unit.osclient.dms.v1 import fakes


class TestDMSInstance(fakes.TestDMS):

    def setUp(self):
        super(TestDMSInstance, self).setUp()
        self.client = self.app.client_manager.dms


class TestListDMSInstance(TestDMSInstance):

    instances = fakes.FakeInstance.create_multiple(3)

    columns = ('ID', 'name', 'engine_name', 'engine_version',
               'storage_spec_code', 'status', 'connect_address', 'router_id',
               'security_group_id', 'subnet_id', 'user_name', 'storage',
               'total_storage', 'used_storage')

    data = []

    for s in instances:
        data.append((
            s.id,
            s.name,
            s.engine_name,
            s.engine_version,
            s.storage_spec_code,
            s.status,
            s.connect_address,
            s.router_id,
            s.security_group_id,
            s.subnet_id,
            s.user_name,
            s.storage,
            s.total_storage,
            s.used_storage
        ))

    def setUp(self):
        super(TestListDMSInstance, self).setUp()

        self.cmd = instance.ListDMSInstance(self.app, None)

        self.client.instances = mock.Mock()

    def test_list_queue(self):
        arglist = [
        ]

        verifylist = [
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.instances.side_effect = [
            self.instances
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.instances.assert_called_once_with(include_failure=False)

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))

    def test_list_queue_args(self):
        arglist = [
            '--engine-name', 'engine',
            '--status', 'Creating',
            '--include-failure'
        ]

        verifylist = [
            ('engine_name', 'engine'),
            ('status', 'CREATING'),
            ('include_failure', True)
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.instances.side_effect = [
            self.instances
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.instances.assert_called_once_with(
            engine_name='engine',
            status='CREATING',
            include_failure=True)

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))


class TestShowDMSInstance(TestDMSInstance):

    _data = fakes.FakeInstance.create_one()

    columns = ('access_user', 'availability_zones', 'description',
               'engine_name', 'engine_version', 'is_public', 'is_ssl',
               'kafka_public_status', 'maintenance_end', 'name', 'password',
               'product_id', 'public_bandwidth', 'retention_policy',
               'router_id', 'router_name', 'security_group_id',
               'security_group_name', 'storage', 'storage_spec_code',
               'subnet_id')

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestShowDMSInstance, self).setUp()

        self.cmd = instance.ShowDMSInstance(self.app, None)

        self.client.find_instance = mock.Mock()

    def test_show_default(self):
        arglist = [
            'test_instance'
        ]
        verifylist = [
            ('instance', 'test_instance')
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.find_instance.side_effect = [
            self._data
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_instance.assert_called()

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestDeleteDMSInstance(TestDMSInstance):

    def setUp(self):
        super(TestDeleteDMSInstance, self).setUp()

        self.cmd = instance.DeleteDMSInstance(self.app, None)

        self.client.delete_instance = mock.Mock()

    def test_delete(self):
        arglist = ['t1']
        verifylist = [
            ('instance', ['t1'])
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.delete_instance.side_effect = [{}]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        calls = [mock.call('t1')]

        self.client.delete_instance.assert_has_calls(calls)
        self.assertEqual(1, self.client.delete_instance.call_count)

    def test_delete_multiple(self):
        arglist = [
            't1',
            't2',
        ]
        verifylist = [
            ('instance', ['t1', 't2'])
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.delete_instance.side_effect = [{}, {}]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        calls = [mock.call('t1'), mock.call('t2')]

        self.client.delete_instance.assert_has_calls(calls)
        self.assertEqual(2, self.client.delete_instance.call_count)


class TestCreateDMSInstance(TestDMSInstance):

    _data = fakes.FakeInstance.create_one()

    columns = ('access_user', 'availability_zones', 'description',
               'engine_name', 'engine_version', 'is_public', 'is_ssl',
               'kafka_public_status', 'maintenance_end', 'name', 'password',
               'product_id', 'public_bandwidth', 'retention_policy',
               'router_id', 'router_name', 'security_group_id',
               'security_group_name', 'storage', 'storage_spec_code',
               'subnet_id')

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestCreateDMSInstance, self).setUp()

        self.cmd = instance.CreateDMSInstance(self.app, None)

        self.client.create_instance = mock.Mock()
        self.app.client_manager.network = mock.Mock()
        self.app.client_manager.network.find_router = mock.Mock()
        self.app.client_manager.network.find_subnet = mock.Mock()
        self.app.client_manager.compute = mock.Mock()

    def test_create_default(self):
        arglist = [
            'name',
            '--description', 'descr',
            '--engine-name', 'kafka',
            '--engine-version', '2.1.0',
            '--storage', '15',
            '--access-user', 'u1',
            '--password', 'pwd',
            '--router', 'router_id',
            '--security-group', 'sg_id',
            '--subnet', 'subnet_id',
            '--availability-zone', 'az1',
            '--availability-zone', 'az2',
            '--product-id', 'pid',
            '--maintenance-begin', 'mwb',
            '--maintenance-end', 'mwe',
            '--enable-public-access',
            '--enable-ssl',
            '--public-bandwidth', '14',
            '--retention-policy', 'produce_reject',
            '--storage-spec-code', 'dms.physical.storage.high'
        ]
        verifylist = [
            ('name', 'name'),
            ('description', 'descr'),
            ('engine_name', 'kafka'),
            ('engine_version', '2.1.0'),
            ('storage', 15),
            ('access_user', 'u1'),
            ('password', 'pwd'),
            ('router', 'router_id'),
            ('security_group', 'sg_id'),
            ('subnet', 'subnet_id'),
            ('availability_zone', ['az1', 'az2']),
            ('product_id', 'pid'),
            ('maintenance_begin', 'mwb'),
            ('maintenance_end', 'mwe'),
            ('enable_public_access', True),
            ('enable_ssl', True),
            ('public_bandwidth', 14),
            ('retention_policy', 'produce_reject'),
            ('storage_spec_code', 'dms.physical.storage.high')
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.create_instance.side_effect = [
            self._data
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.app.client_manager.network.find_router.assert_called_with(
            'router_id', ignore_missing=False)
        self.app.client_manager.network.find_subnet.assert_called_with(
            'subnet_id', ignore_missing=False)
        self.app.client_manager.compute.find_security_group.assert_called_with(
            'sg_id', ignore_missing=False)

        self.client.create_instance.assert_called_with(
            access_user='u1',
            availability_zone=['az1', 'az2'],
            description='descr',
            engine_name='kafka',
            engine_version='2.1.0',
            is_public=True,
            is_ssl=True,
            maintenance_begin='mwb',
            maintenance_end='mwe',
            name='name',
            password='pwd',
            product_id='pid',
            public_bandwidth=14,
            retention_policy='produce_reject',
            router_id=mock.ANY,
            security_group_id=mock.ANY,
            storage=15,
            storage_spec_code='dms.physical.storage.high',
            subnet_id=mock.ANY
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)
