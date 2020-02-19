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

from otcextensions.osclient.nat.v2 import gateway
from otcextensions.tests.unit.osclient.nat.v2 import fakes


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
            ('tenant_id', '4'),
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
            tenant_id='4',
            spec='5',
            router_id='6',
            internal_network_id='7',
            admin_state_up='8',
            created_at='9',
            status='10',
        )


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

    def test_show(self):
        arglist = [
            'test_gateway',
        ]

        verifylist = [
            ('nat_gateway', 'test_gateway'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.find_gateway.assert_called_with('test_gateway')

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestDeleteNatGateway(fakes.TestNat):

    data = fakes.FakeNatGateway.create_one()

    def setUp(self):
        super(TestDeleteNatGateway, self).setUp()

        self.cmd = gateway.DeleteNatGateway(self.app, None)

        self.client.find_gateway = mock.Mock(return_value=self.data)
        self.client.delete_gateway = mock.Mock(return_value=self.data)

    def test_delete(self):
        arglist = [
            'test_gateway',
        ]

        verifylist = [
            ('nat_gateway', 'test_gateway'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.find_gateway.assert_called_with('test_gateway')

        self.client.delete_gateway.assert_called_with(self.data.id)
