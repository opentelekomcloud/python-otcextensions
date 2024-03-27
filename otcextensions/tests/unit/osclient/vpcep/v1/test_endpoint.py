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
from unittest.mock import call

import mock
from openstackclient.tests.unit import utils as tests_utils
from osc_lib import exceptions

from otcextensions.osclient.vpcep.v1 import endpoint
from otcextensions.tests.unit.osclient.vpcep.v1 import fakes


class TestListEndpoints(fakes.TestVpcep):

    objects = fakes.FakeEndpoint.create_multiple(3)

    column_list_headers = (
        'Id',
        'Endpoint Service Name',
        'Status',
        'Enable status',
    )

    columns = (
        'id',
        'endpoint_service_name',
        'status',
        'enable_status',
    )

    data = []

    for s in objects:
        data.append(
            (
                s.id,
                s.endpoint_service_name,
                s.status,
                s.enable_status,
            )
        )

    def setUp(self):
        super(TestListEndpoints, self).setUp()

        self.cmd = endpoint.ListEndpoints(self.app, None)

        self.client.endpoints = mock.Mock()
        self.client.api_mock = self.client.endpoints

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
            '--id',
            '1',
            '--service-name',
            '2',
            '--sort-key',
            'created_at',
            '--sort-dir',
            'desc',
            '--limit',
            '6',
            '--offset',
            '7',
        ]

        verifylist = [
            ('id', '1'),
            ('endpoint_service_name', '2'),
            ('sort_key', 'created_at'),
            ('sort_dir', 'desc'),
            ('limit', 6),
            ('offset', 7),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(
            id='1',
            endpoint_service_name='2',
            sort_key='created_at',
            sort_dir='desc',
            limit=6,
            offset=7,
        )


class TestCreateEndpoint(fakes.TestVpcep):

    _data = fakes.FakeEndpoint.create_one()

    columns = (
        'created_at',
        'endpoint_service_id',
        'endpoint_service_name',
        'id',
        'is_dns_enabled',
        'is_whitelist_enabled',
        'marker_id',
        'project_id',
        'router_id',
        'service_type',
        'status',
        'tags',
        'updated_at',
        'whitelist',
    )

    data = fakes.gen_data(_data, columns, formatters=endpoint._formatters)

    def setUp(self):
        super(TestCreateEndpoint, self).setUp()

        self.cmd = endpoint.CreateEndpoint(self.app, None)
        self.client.create_endpoint = mock.Mock(
            return_value=fakes.FakeEndpoint.create_one()
        )

    def test_create(self):
        arglist = [
            '--service-id',
            '1',
            '--router-id',
            '2',
            '--network-id',
            '3',
            '--port-ip',
            '4',
            '--route-tables',
            'abc',
            '123',
            '--whitelist',
            'xyz',
            '456',
            '--specification-name',
            '5',
            '--description',
            '6',
            '--tags',
            'key=tag-key,value=tag-value',
            '--enable-dns',
            '--enable-whitelist',
        ]
        verifylist = [
            ('endpoint_service_id', '1'),
            ('vpc_id', '2'),
            ('subnet_id', '3'),
            ('port_ip', '4'),
            ('routetables', ['abc', '123']),
            ('whitelist', ['xyz', '456']),
            ('specification_name', '5'),
            ('description', '6'),
            ('tags', [{'key': 'tag-key', 'value': 'tag-value'}]),
            ('enable_dns', True),
            ('enable_whitelist', True),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        attrs = {
            'endpoint_service_id': '1',
            'vpc_id': '2',
            'subnet_id': '3',
            'port_ip': '4',
            'routetables': ['abc', '123'],
            'whitelist': ['xyz', '456'],
            'specification_name': '5',
            'description': '6',
            'tags': [{'key': 'tag-key', 'value': 'tag-value'}],
            'enable_dns': True,
            'enable_whitelist': True,
        }

        self.client.create_endpoint.assert_called_with(**attrs)
        self.assertEqual(self.columns, columns)


class TestShowEndpoint(fakes.TestVpcep):

    _data = fakes.FakeEndpoint.create_one()

    columns = (
        'created_at',
        'endpoint_service_id',
        'endpoint_service_name',
        'id',
        'is_dns_enabled',
        'is_whitelist_enabled',
        'marker_id',
        'project_id',
        'router_id',
        'service_type',
        'status',
        'tags',
        'updated_at',
        'whitelist',
    )

    data = fakes.gen_data(_data, columns, formatters=endpoint._formatters)

    def setUp(self):
        super(TestShowEndpoint, self).setUp()

        self.cmd = endpoint.ShowEndpoint(self.app, None)

        self.client.get_endpoint = mock.Mock(return_value=self._data)

    def test_show_no_options(self):
        arglist = []
        verifylist = []

        # Testing that a call without the required argument will fail and
        # throw a "ParserExecption"
        self.assertRaises(
            tests_utils.ParserException,
            self.check_parser,
            self.cmd,
            arglist,
            verifylist,
        )

    def test_show(self):
        arglist = [
            self._data.id,
        ]

        verifylist = [
            ('endpoint', self._data.id),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.get_endpoint.assert_called_with(self._data.id)

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)

    def test_show_non_existent(self):
        arglist = [
            'non-existing-endpoint-id',
        ]

        verifylist = [
            ('endpoint', 'non-existing-endpoint-id'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_result = exceptions.CommandError('Resource Not Found')
        self.client.find_service = mock.Mock(side_effect=find_mock_result)

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual('Resource Not Found', str(e))
        self.client.get_endpoint.assert_called_with('non-existing-endpoint-id')


class TestDeleteEndpoint(fakes.TestVpcep):

    _data = fakes.FakeEndpoint.create_multiple(2)

    def setUp(self):
        super(TestDeleteEndpoint, self).setUp()

        self.client.delete_endpoint = mock.Mock(return_value=None)

        # Get the command object to test
        self.cmd = endpoint.DeleteEndpoint(self.app, None)

    def test_delete(self):
        arglist = [
            self._data[0].id,
        ]

        verifylist = [
            ('endpoint', [self._data[0].id]),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.delete_endpoint.assert_called_with(self._data[0].id)
        self.assertIsNone(result)

    def test_multiple_delete(self):
        arglist = []

        for data in self._data:
            arglist.append(data.id)

        verifylist = [
            ('endpoint', arglist),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)

        calls = []
        for data in self._data:
            calls.append(call(data.id))
        self.client.delete_endpoint.assert_has_calls(calls)
        self.assertIsNone(result)

    def test_multiple_delete_with_exception(self):
        arglist = [
            self._data[0].id,
            'non-existing-endpoint-id',
        ]
        verifylist = [
            ('endpoint', arglist),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        delete_mock_result = [None, exceptions.CommandError]
        self.client.delete_endpoint = mock.Mock(side_effect=delete_mock_result)

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual(
                '1 of 2 VPC endpoint(s) failed to delete.', str(e)
            )

        self.client.delete_endpoint.assert_any_call(self._data[0].id)
        self.client.delete_endpoint.assert_any_call('non-existing-endpoint-id')
