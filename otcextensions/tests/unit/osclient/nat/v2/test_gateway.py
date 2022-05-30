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
from unittest.mock import call

from osc_lib import exceptions

from otcextensions.osclient.nat.v2 import gateway
from otcextensions.tests.unit.osclient.nat.v2 import fakes

from openstackclient.tests.unit import utils as tests_utils


class TestListNatGateways(fakes.TestNat):

    objects = fakes.FakeNatGateway.create_multiple(3)

    column_list_headers = ('Id', 'Name', 'Spec', 'Router Id', 'Status')

    columns = ('id', 'name', 'spec', 'router_id', 'status')

    data = []

    for s in objects:
        data.append(
            (s.id, s.name, s.spec, s.router_id, s.status))

    def setUp(self):
        super(TestListNatGateways, self).setUp()

        self.cmd = gateway.ListNatGateways(self.app, None)

        self.client.gateways = mock.Mock()
        self.client.api_mock = self.client.gateways

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
            '--project-id', '4',
            '--spec', '5',
            '--router-id', '6',
            '--internal-network-id', '7',
            '--admin-state-up', '8',
            '--created-at', '9',
            '--status', '10'
        ]

        verifylist = [
            ('limit', 1),
            ('id', '2'),
            ('name', '3'),
            ('project_id', '4'),
            ('spec', '5'),
            ('router_id', '6'),
            ('internal_network_id', '7'),
            ('admin_state_up', '8'),
            ('created_at', '9'),
            ('status', '10'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(
            limit=1,
            id='2',
            name='3',
            project_id='4',
            spec='5',
            router_id='6',
            internal_network_id='7',
            admin_state_up='8',
            created_at='9',
            status='10',
        )


class TestCreateNatGateway(fakes.TestNat):

    _data = fakes.FakeNatGateway.create_one()

    columns = (
        'admin_state_up',
        'created_at',
        'description',
        'id',
        'internal_network_id',
        'name',
        'project_id',
        'router_id',
        'spec',
        'status'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestCreateNatGateway, self).setUp()

        self.cmd = gateway.CreateNatGateway(self.app, None)

        self.client.create_gateway = mock.Mock(return_value=self._data)

    def test_create(self):
        arglist = [
            'test-gateway',
            '--router-id', 'test-router-uuid',
            '--internal-network-id', 'test-network-uuid',
            '--spec', '1',
        ]
        verifylist = [
            ('name', 'test-gateway'),
            ('router_id', 'test-router-uuid'),
            ('internal_network_id', 'test-network-uuid'),
            ('spec', '1'),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_gateway.assert_called_with(
            name='test-gateway',
            router_id='test-router-uuid',
            internal_network_id='test-network-uuid',
            spec='1'
        )
        self.assertEqual(self.columns, columns)


class TestUpdateNatGateway(fakes.TestNat):

    _data = fakes.FakeNatGateway.create_one()

    columns = (
        'admin_state_up',
        'created_at',
        'description',
        'id',
        'internal_network_id',
        'name',
        'project_id',
        'router_id',
        'spec',
        'status'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestUpdateNatGateway, self).setUp()

        self.cmd = gateway.UpdateNatGateway(self.app, None)

        self.client.find_gateway = mock.Mock(return_value=self._data)
        self.client.update_gateway = mock.Mock(return_value=self._data)

    def test_update(self):
        arglist = [
            self._data.name,
            '--name', 'test-gateway-updated',
            '--description', 'nat gateway updated',
            '--spec', '2',
        ]
        verifylist = [
            ('gateway', self._data.name),
            ('name', 'test-gateway-updated'),
            ('description', 'nat gateway updated'),
            ('spec', '2'),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_gateway.assert_called_with(self._data.name)
        self.client.update_gateway.assert_called_with(
            self._data.id,
            name='test-gateway-updated',
            description='nat gateway updated',
            spec='2'
        )
        self.assertEqual(self.columns, columns)


class TestShowNatGateway(fakes.TestNat):

    _data = fakes.FakeNatGateway.create_one()

    columns = (
        'admin_state_up',
        'created_at',
        'description',
        'id',
        'internal_network_id',
        'name',
        'project_id',
        'router_id',
        'spec',
        'status'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestShowNatGateway, self).setUp()

        self.cmd = gateway.ShowNatGateway(self.app, None)

        self.client.find_gateway = mock.Mock(return_value=self._data)

    def test_show_no_options(self):
        arglist = []
        verifylist = []

        # Testing that a call without the required argument will fail and
        # throw a "ParserExecption"
        self.assertRaises(tests_utils.ParserException,
                          self.check_parser, self.cmd, arglist, verifylist)

    def test_show(self):
        arglist = [
            self._data.id,
        ]

        verifylist = [
            ('gateway', self._data.id),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.find_gateway.assert_called_with(self._data.id)

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)

    def test_show_non_existent(self):
        arglist = [
            'unexist_nat_gateway',
        ]

        verifylist = [
            ('gateway', 'unexist_nat_gateway'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_result = exceptions.CommandError('Resource Not Found')
        self.client.find_gateway = (
            mock.Mock(side_effect=find_mock_result)
        )

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual('Resource Not Found', str(e))
        self.client.find_gateway.assert_called_with('unexist_nat_gateway')


class TestDeleteNatGateway(fakes.TestNat):

    _data = fakes.FakeNatGateway.create_multiple(2)

    def setUp(self):
        super(TestDeleteNatGateway, self).setUp()

        self.client.delete_gateway = mock.Mock(return_value=None)

        # Get the command object to test
        self.cmd = gateway.DeleteNatGateway(self.app, None)

    def test_delete(self):
        arglist = [
            self._data[0].name,
        ]

        verifylist = [
            ('gateway', [self._data[0].name]),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.client.find_gateway = (
            mock.Mock(return_value=self._data[0])
        )

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.delete_gateway.assert_called_with(self._data[0].id)
        self.assertIsNone(result)

    def test_multiple_delete(self):
        arglist = []

        for nat_gw in self._data:
            arglist.append(nat_gw.name)

        verifylist = [
            ('gateway', arglist),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_result = self._data
        self.client.find_gateway = (
            mock.Mock(side_effect=find_mock_result)
        )

        # Trigger the action
        result = self.cmd.take_action(parsed_args)

        calls = []
        for nat_gw in self._data:
            calls.append(call(nat_gw.id))
        self.client.delete_gateway.assert_has_calls(calls)
        self.assertIsNone(result)

    def test_multiple_delete_with_exception(self):
        arglist = [
            self._data[0].name,
            'unexist_nat_gateway',
        ]
        verifylist = [
            ('gateway', arglist),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_result = [self._data[0], exceptions.CommandError]
        self.client.find_gateway = (
            mock.Mock(side_effect=find_mock_result)
        )

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual('1 of 2 NAT Gateway(s) failed to delete.', str(e))

        self.client.find_gateway.assert_any_call(self._data[0].name)
        self.client.find_gateway.assert_any_call('unexist_nat_gateway')
        self.client.delete_gateway.assert_called_once_with(self._data[0].id)
