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

from otcextensions.osclient.nat.v2 import snat
from otcextensions.tests.unit.osclient.nat.v2 import fakes


class TestListSnatRules(fakes.TestNat):

    objects = fakes.FakeSnatRule.create_multiple(3)

    column_list_headers = (
        'Id',
        'Nat Gateway Id',
        'Network Id',
        'Cidr',
        'Floating Ip Address',
        'Status'
    )
    columns = (
        'id',
        'nat_gateway_id',
        'network_id',
        'cidr',
        'floating_ip_address',
        'status'
    )

    data = []

    for s in objects:
        data.append((
            s.id,
            s.nat_gateway_id,
            s.network_id,
            s.cidr,
            s.floating_ip_address,
            s.status
        ))

    def setUp(self):
        super(TestListSnatRules, self).setUp()

        self.cmd = snat.ListSnatRules(self.app, None)

        self.client.snat_rules = mock.Mock()
        self.client.api_mock = self.client.snat_rules

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
            '--network-id', '4',
            '--project-id', '5',
            '--cidr', '6',
            '--source-type', '7',
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
            ('network_id', '4'),
            ('project_id', '5'),
            ('cidr', '6'),
            ('source_type', '7'),
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
            network_id='4',
            project_id='5',
            cidr='6',
            source_type='7',
            floating_ip_id='8',
            floating_ip_address='9',
            admin_state_up='10',
            created_at='11',
            status='12',
        )


class TestShowSnatRule(fakes.TestNat):

    _data = fakes.FakeSnatRule.create_one()

    columns = (
        'admin_state_up',
        'cidr',
        'created_at',
        'floating_ip_address',
        'floating_ip_id',
        'id',
        'nat_gateway_id',
        'network_id',
        'project_id',
        'source_type',
        'status'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestShowSnatRule, self).setUp()

        self.cmd = snat.ShowSnatRule(self.app, None)

        self.client.get_snat_rule = mock.Mock(return_value=self._data)

    def test_show(self):
        arglist = [
            'test_snat_rule_id',
        ]

        verifylist = [
            ('snat_rule_id', 'test_snat_rule_id'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.get_snat_rule.assert_called_with('test_snat_rule_id')

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestDeleteSnatRule(fakes.TestNat):

    data = fakes.FakeSnatRule.create_one()

    def setUp(self):
        super(TestDeleteSnatRule, self).setUp()

        self.cmd = snat.DeleteSnatRule(self.app, None)

        self.client.get_snat_rule = mock.Mock(return_value=self.data)
        self.client.delete_snat_rule = mock.Mock(return_value=self.data)

    def test_delete(self):
        arglist = [
            'test_snat_rule_id',
        ]

        verifylist = [
            ('snat_rule_id', 'test_snat_rule_id'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.get_snat_rule.assert_called_with('test_snat_rule_id')

        self.client.delete_snat_rule.assert_called_with(self.data.id)
