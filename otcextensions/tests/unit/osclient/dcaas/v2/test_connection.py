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

from otcextensions.osclient.dcaas.v2 import connection
from otcextensions.tests.unit.osclient.dcaas.v2 import fakes

from osc_lib import exceptions

from openstackclient.tests.unit import utils as tests_utils


class TestListDirectConnection(fakes.TestDcaas):

    objects = fakes.FakeDirectConnection.create_multiple(3)
    column_list_headers = (
        'id',
        'name',
        'port type',
        'provider',
        'bandwidth',
        'location',
        'status'
    )
    columns = (
        'id',
        'name',
        'port type',
        'provider',
        'bandwidth',
        'location',
        'status'
    )
    data = []
    for s in objects:
        data.append((
            s.id,
            s.name,
            s.port_type,
            s.provider,
            s.bandwidth,
            s.location,
            s.status
        ))

    def setUp(self):
        super(TestListDirectConnection, self).setUp()
        self.cmd = connection.ListDirectConnections(self.app, None)
        self.client.connections = mock.Mock()
        self.client.api_mock = self.client.connections

    def test_list(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.client.api_mock.side_effect = [self.objects]
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with()
        self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(self.data, list(data))

    def test_list_args(self):
        arglist = [
            '--id', '1',
            '--name', 'test',
            '--port_type', '1G',
            '--bandwidth', '10',
            '--location', 'Biere',
            '--provider', 'OTC'
        ]
        verifylist = [
            ('id', '1'),
            ('name', 'test'),
            ('port_type', '1G'),
            ('bandwidth', 10),
            ('location', 'Biere'),
            ('provider', 'OTC')
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.client.api_mock.side_effect = [self.objects]
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(
            id='1',
            name='test',
            port_type='1G',
            bandwidth=10,
            location='Biere',
            provider='OTC'
        )


class TestCreateDirectConnection(fakes.TestDcaas):

    _data = fakes.FakeDirectConnection.create_one()

    columns = (
        'admin_state_up',
        'bandwidth',
        'charge_mode',
        'description',
        'device_id',
        'hosting_id',
        'id',
        'interface_name',
        'location',
        'name',
        'order_id',
        'peer_location',
        'port_type',
        'product_id',
        'provider',
        'provider_status',
        'redundant_id',
        'status',
        'type',
        'vlan'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestCreateDirectConnection, self).setUp()
        self.cmd = connection.CreateDirectConnection(self.app, None)
        self.client.create_connection = mock.Mock(return_value=self._data)

    def test_create(self):
        arglist = [
            '1G',
            '10',
            'Biere',
            'OTC',
            '--name', 'test',
            '--description', 'test description',
            '--peer_location', 'test_peer_loc',
            '--device_id', '172.16.40.2',
            '--interface_name', 'Eth-Trunk2',
            '--redundant_id', '11111',
            '--provider_status', 'ACTIVE',
            '--type', 'hosted',
            '--hosting_id', 'test_11',
            '--vlan', '111',
            '--charge_mode', 'traffic',
            '--order_id', 'id1',
            '--product_id', 'idp1',
            '--status', 'ACTIVE',
            '--admin_state_up', 'True'
        ]
        verifylist = [
            ('port_type', '1G'),
            ('bandwidth', 10),
            ('location', 'Biere'),
            ('provider', 'OTC'),
            ('name', 'test'),
            ('description', 'test description'),
            ('peer_location', 'test_peer_loc'),
            ('device_id', '172.16.40.2'),
            ('interface_name', 'Eth-Trunk2'),
            ('redundant_id', '11111'),
            ('provider_status', 'ACTIVE'),
            ('type', 'hosted'),
            ('hosting_id', 'test_11'),
            ('vlan', 111),
            ('charge_mode', 'traffic'),
            ('order_id', 'id1'),
            ('product_id', 'idp1'),
            ('status', 'ACTIVE'),
            ('admin_state_up', True)
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)
        self.client.create_connection.assert_called_with(
            name='test',
            port_type='1G',
            bandwidth=10,
            location='Biere',
            provider='OTC',
            description='test description',
            peer_location='test_peer_loc',
            device_id='172.16.40.2',
            interface_name='Eth-Trunk2',
            redundant_id='11111',
            provider_status='ACTIVE',
            type='hosted',
            hosting_id='test_11',
            vlan=111,
            charge_mode='traffic',
            order_id='id1',
            product_id='idp1',
            status='ACTIVE',
            admin_state_up=True
        )
        self.assertEqual(self.columns, columns)


class TestShowDirectConnection(fakes.TestDcaas):

    _data = fakes.FakeDirectConnection.create_one()

    columns = (
        'admin_state_up',
        'bandwidth',
        'charge_mode',
        'description',
        'device_id',
        'hosting_id',
        'id',
        'interface_name',
        'location',
        'name',
        'order_id',
        'peer_location',
        'port_type',
        'product_id',
        'provider',
        'provider_status',
        'redundant_id',
        'status',
        'type',
        'vlan'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestShowDirectConnection, self).setUp()
        self.cmd = connection.ShowDirectConnection(self.app, None)
        self.client.find_connection = mock.Mock(return_value=self._data)

    def test_show_no_options(self):
        arglist = []
        verifylist = []
        self.assertRaises(tests_utils.ParserException,
                          self.check_parser, self.cmd, arglist, verifylist)

    def test_show(self):
        arglist = [
            self._data.id,
        ]

        verifylist = [
            ('direct_connection', self._data.id),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        columns, data = self.cmd.take_action(parsed_args)
        self.client.find_connection.assert_called_with(self._data.id)

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)

    def test_show_non_existing(self):
        arglist = [
            'unexist_direct_connection'
        ]

        verifylist = [
            ('direct_connection', 'unexist_direct_connection')
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_result = exceptions.CommandError('Resource Not Found')
        self.client.find_connection = (
            mock.Mock(side_effect=find_mock_result)
        )
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual('Resource Not Found', str(e))
        self.client.find_connection.assert_called_with(
            'unexist_direct_connection'
        )


class TestUpdateDirectConnection(fakes.TestDcaas):

    _data = fakes.FakeDirectConnection.create_one()

    columns = (
        'admin_state_up',
        'bandwidth',
        'charge_mode',
        'description',
        'device_id',
        'hosting_id',
        'id',
        'interface_name',
        'location',
        'name',
        'order_id',
        'peer_location',
        'port_type',
        'product_id',
        'provider',
        'provider_status',
        'redundant_id',
        'status',
        'type',
        'vlan'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestUpdateDirectConnection, self).setUp()
        self.cmd = connection.UpdateDirectConnection(self.app, None)
        self.client.find_connection = mock.Mock(return_value=self._data)
        self.client.update_connection = mock.Mock(return_value=self._data)
        self.client.api_mock = self.client.update_connection

    def test_update(self):
        arglist = [
            self._data.id,
            '--name', 'updated_name',
            '--description', 'updated description',
            '--bandwidth', '150',
            '--provider_status', 'DOWN',
            '--order_id', 'id2',
            '--product_id', 'idp2'
        ]
        verifylist = [
            ('direct_connection', self._data.id),
            ('name', 'updated_name'),
            ('description', 'updated description'),
            ('bandwidth', 150),
            ('provider_status', 'DOWN'),
            ('order_id', 'id2'),
            ('product_id', 'idp2')
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.side_effect = [
            self._data
        ]

        self.client.api_mock.assert_called_with(
            direct_connection=self._data.id,
            name='updated_name',
            description='updated description',
            bandwidth=150,
            provider_status='DOWN',
            order_id='id2',
            product_id='idp2'
        )
        self.assertEqual(self.columns, columns)


class TestDeleteDirectConnection(fakes.TestDcaas):
    _data = fakes.FakeDirectConnection.create_one()

    def setUp(self):
        super(TestDeleteDirectConnection, self).setUp()
        self.client.delete_connection = mock.Mock(return_value=None)
        self.cmd = connection.DeleteDirectConnection(self.app, None)

    def test_delete_by_name(self):
        arglist = [
            self._data.name,
        ]
        verifylist = [
            ('direct_connection', self._data.name),
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.client.find_connection = (
            mock.Mock(return_value=self._data)
        )
        result = self.cmd.take_action(parsed_args)
        self.client.delete_connection.assert_called_with(self._data.id)
        self.assertIsNone(result)
