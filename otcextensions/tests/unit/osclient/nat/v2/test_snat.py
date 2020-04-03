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

from otcextensions.osclient.nat.v2 import snat
from otcextensions.tests.unit.osclient.nat.v2 import fakes

from openstackclient.tests.unit import utils as tests_utils


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


class TestCreateSnatRule(fakes.TestNat):

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
        super(TestCreateSnatRule, self).setUp()

        self.cmd = snat.CreateSnatRule(self.app, None)

        self.client.create_snat_rule = mock.Mock(return_value=self._data)

    def test_create(self):
        arglist = [
            '--nat-gateway-id', 'test-nat-uuid',
            '--floating-ip-id', 'test-floating-ip-uuid',
            '--network-id', 'test-network-uuid',
        ]

        verifylist = [
            ('nat_gateway_id', 'test-nat-uuid'),
            ('floating_ip_id', 'test-floating-ip-uuid'),
            ('network_id', 'test-network-uuid'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.create_snat_rule.assert_called_with(
            nat_gateway_id='test-nat-uuid',
            floating_ip_id='test-floating-ip-uuid',
            network_id='test-network-uuid')

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


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
            ('snat', self._data.id),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.get_snat_rule.assert_called_with(self._data.id)

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)

    def test_show_non_existent(self):
        arglist = [
            'unexist_snat_rule_id',
        ]

        verifylist = [
            ('snat', arglist[0]),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_result = exceptions.CommandError('Resource Not Found')
        self.client.get_snat_rule = (
            mock.Mock(side_effect=find_mock_result)
        )

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual('Resource Not Found', str(e))
        self.client.get_snat_rule.assert_called_with(arglist[0])


class TestDeleteSnatRule(fakes.TestNat):

    _data = fakes.FakeSnatRule.create_multiple(2)

    def setUp(self):
        super(TestDeleteSnatRule, self).setUp()

        self.client.delete_snat_rule = mock.Mock(return_value=None)

        self.cmd = snat.DeleteSnatRule(self.app, None)

    def test_delete(self):
        arglist = [
            self._data[0].id,
        ]

        verifylist = [
            ('snat', arglist),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.client.get_snat_rule = (
            mock.Mock(return_value=self._data[0])
        )

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.get_snat_rule.assert_called_with(self._data[0].id)
        self.client.delete_snat_rule.assert_called_with(self._data[0].id)
        self.assertIsNone(result)

    def test_multiple_delete(self):
        arglist = []

        for snat_rule in self._data:
            arglist.append(snat_rule.id)

        verifylist = [
            ('snat', arglist),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_result = self._data
        self.client.get_snat_rule = (
            mock.Mock(side_effect=find_mock_result)
        )

        # Trigger the action
        result = self.cmd.take_action(parsed_args)

        calls = []
        for snat_rule in self._data:
            calls.append(call(snat_rule.id))
        self.client.delete_snat_rule.assert_has_calls(calls)
        self.assertIsNone(result)

    def test_multiple_delete_with_exception(self):
        arglist = [
            self._data[0].id,
            'unexist_snat_rule_id',
        ]
        verifylist = [
            ('snat', arglist),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_result = [self._data[0], exceptions.CommandError]
        self.client.get_snat_rule = (
            mock.Mock(side_effect=find_mock_result)
        )

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual('1 of 2 SNAT Rule(s) failed to delete.', str(e))

        self.client.get_snat_rule.assert_any_call(arglist[0])
        self.client.get_snat_rule.assert_any_call(arglist[1])
        self.client.delete_snat_rule.assert_called_once_with(arglist[0])
