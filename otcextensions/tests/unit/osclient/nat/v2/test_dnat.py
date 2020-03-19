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

from otcextensions.osclient.nat.v2 import dnat
from otcextensions.tests.unit.osclient.nat.v2 import fakes


class TestListDnatRules(fakes.TestNat):

    objects = fakes.FakeDnatRule.create_multiple(3)

    column_list_headers = (
        'Id',
        'Nat Gateway Id',
        'Port Id',
        'Private IP',
        'Floating Ip Address',
        'Protocol',
        'Status'
    )
    columns = (
        'id',
        'nat_gateway_id',
        'port_id',
        'private_ip',
        'floating_ip_address',
        'protocol',
        'status'
    )

    data = []

    for s in objects:
        data.append((
            s.id,
            s.nat_gateway_id,
            s.port_id,
            s.private_ip,
            s.floating_ip_address,
            s.protocol,
            s.status
        ))

    def setUp(self):
        super(TestListDnatRules, self).setUp()

        self.cmd = dnat.ListDnatRules(self.app, None)

        self.client.dnat_rules = mock.Mock()
        self.client.api_mock = self.client.dnat_rules

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
            '--nat-gateway-id', '3',
            '--project-id', '4',
            '--private-ip', '5',
            '--internal-service-port', '6',
            '--protocol', '7',
            '--floating-ip-id', '8',
            '--floating-ip-address', '9',
            '--admin-state-up', '10',
            '--created-at', '11',
            '--status', '12'
        ]

        verifylist = [
            ('limit', 1),
            ('id', '2'),
            ('nat_gateway_id', '3'),
            ('project_id', '4'),
            ('private_ip', '5'),
            ('internal_service_port', '6'),
            ('protocol', '7'),
            ('floating_ip_id', '8'),
            ('floating_ip_address', '9'),
            ('admin_state_up', '10'),
            ('created_at', '11'),
            ('status', '12'),
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
            nat_gateway_id='3',
            project_id='4',
            private_ip='5',
            internal_service_port='6',
            protocol='7',
            floating_ip_id='8',
            floating_ip_address='9',
            admin_state_up='10',
            created_at='11',
            status='12',
        )


class TestShowDnatRule(fakes.TestNat):

    _data = fakes.FakeDnatRule.create_one()

    columns = (
        'admin_state_up',
        'created_at',
        'external_service_port',
        'floating_ip_address',
        'floating_ip_id',
        'id',
        'internal_service_port',
        'nat_gateway_id',
        'port_id',
        'private_ip',
        'project_id',
        'protocol',
        'status'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestShowDnatRule, self).setUp()

        self.cmd = dnat.ShowDnatRule(self.app, None)

        self.client.get_dnat_rule = mock.Mock(return_value=self._data)

    def test_show(self):
        arglist = [
            'test_dnat_rule_id',
        ]

        verifylist = [
            ('dnat', 'test_dnat_rule_id'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.get_dnat_rule.assert_called_with('test_dnat_rule_id')

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestCreateDnatRule(fakes.TestNat):

    _data = fakes.FakeDnatRule.create_one()

    columns = (
        'admin_state_up',
        'created_at',
        'external_service_port',
        'floating_ip_address',
        'floating_ip_id',
        'id',
        'internal_service_port',
        'nat_gateway_id',
        'port_id',
        'private_ip',
        'project_id',
        'protocol',
        'status'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestCreateDnatRule, self).setUp()

        self.cmd = dnat.CreateDnatRule(self.app, None)

        self.client.create_dnat_rule = mock.Mock(return_value=self._data)

    def test_create(self):
        arglist = [
            '--nat-gateway-id', 'test-nat-uuid',
            '--floating-ip-id', 'test-floating-ip-uuid',
            '--protocol', 'tcp',
            '--internal-service-port', '80',
            '--external-service-port', '80',
            '--private-ip', '192.168.0.99',
        ]

        verifylist = [
            ('nat_gateway_id', 'test-nat-uuid'),
            ('floating_ip_id', 'test-floating-ip-uuid'),
            ('protocol', 'tcp'),
            ('internal_service_port', '80'),
            ('external_service_port', '80'),
            ('private_ip', '192.168.0.99'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.create_dnat_rule.assert_called_with(
            nat_gateway_id='test-nat-uuid',
            floating_ip_id='test-floating-ip-uuid',
            protocol='tcp',
            internal_service_port='80',
            external_service_port='80',
            private_ip='192.168.0.99')

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestDeleteDnatRule(fakes.TestNat):

    data = fakes.FakeDnatRule.create_one()

    def setUp(self):
        super(TestDeleteDnatRule, self).setUp()

        self.cmd = dnat.DeleteDnatRule(self.app, None)

        self.client.get_dnat_rule = mock.Mock(return_value=self.data)
        self.client.delete_dnat_rule = mock.Mock(return_value=self.data)

    def test_delete(self):
        arglist = [
            'test_dnat_rule_id',
        ]

        verifylist = [
            ('dnat', 'test_dnat_rule_id'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.get_dnat_rule.assert_called_with('test_dnat_rule_id')

        self.client.delete_dnat_rule.assert_called_with(self.data.id)
