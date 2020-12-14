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

from otcextensions.osclient.vpcep.v1 import endpoint_service
from otcextensions.tests.unit.osclient.vpcep.v1 import fakes

from openstackclient.tests.unit import utils as tests_utils


class TestListEndpointServices(fakes.TestVpcep):

    objects = fakes.FakeEndpointService.create_multiple(3)

    column_list_headers = (
        'Id',
        'Service Name',
        'Service Type',
        'Server Type',
        'Connection Count',
        'Status'
    )

    columns = (
        'id',
        'service_name',
        'service_type',
        'server_type',
        'connection_count',
        'status'
    )

    data = []

    for s in objects:
        data.append((
            s.id,
            s.service_name,
            s.service_type,
            s.server_type,
            s.connection_count,
            s.status
        ))

    def setUp(self):
        super(TestListEndpointServices, self).setUp()

        self.cmd = endpoint_service.ListEndpointServices(self.app, None)

        self.client.endpoint_services = mock.Mock()
        self.client.api_mock = self.client.endpoint_services

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
            '--id', '1',
            '--name', '2',
            '--status', '3',
            '--sort-key', '4',
            '--sort-dir', '5',
            '--limit', '6',
            '--offset', '7',
        ]

        verifylist = [
            ('id', '1'),
            ('name', '2'),
            ('status', '3'),
            ('sort_key', '4'),
            ('sort_dir', '5'),
            ('limit', 6),
            ('offset', 7)
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(
            id='1',
            name='2',
            status='3',
            sort_key='4',
            sort_dir='5',
            limit=6,
            offset=7,
        )


class TestCreateEndpointService(fakes.TestVpcep):

    _data = fakes.FakeEndpointService.create_one()

    columns = (
        'approval_enabled',
        'created_at',
        'id',
        'pool_id',
        'port_id',
        'ports',
        'project_id',
        'router_id',
        'server_type',
        'service_name',
        'service_type',
        'status'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestCreateEndpointService, self).setUp()

        self.cmd = endpoint_service.CreateEndpointService(self.app, None)
        self.client.create_endpoint_service = mock.Mock(
            return_value=fakes.FakeEndpointService.create_one())

    def test_create(self):
        arglist = [
            '--service-name', 'test-endpointservice',
            '--port-id', 'test-port-uuid',
            '--pool-id', 'test-pool-uuid',
            '--vip-port-id', 'test-vip-port-uuid',
            '--router-id', 'test-router-uuid',
            '--approval-enabled', False,
            '--server-type', 'VM',
            '--service-type', 'Interface',
            '--ports', 'client_port=80,server_port=80,protocol=TCP',
            '--tags', 'key=tag-key,value=tag-value',
            '--tcp-proxy', '127.0.0.1:8080'
        ]
        verifylist = [
            ('service_name', 'test-endpointservice'),
            ('port_id', 'test-port-uuid'),
            ('pool_id', 'test-pool-uuid'),
            ('vip_port_id', 'test-vip-port-uuid'),
            ('router_id', 'test-router-uuid'),
            ('approval_enabled', False),
            ('server_type', 'vm'),
            ('service_type', 'interface'),
            ('ports', [{'client_port': '80',
                        'server_port': '80',
                        'protocol': 'TCP'}]),
            ('tags', [{'key': 'tag-key', 'value': 'tag-value'}]),
            ('tcp_proxy', '127.0.0.1:8080'),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        attrs = {
            'service_name': 'test-endpointservice',
            'port_id': 'test-port-uuid',
            'pool_id': 'test-pool-uuid',
            'vip_port_id': 'test-vip-port-uuid',
            'router_id': 'test-router-uuid',
            'approval_enabled': False,
            'server_type': 'vm',
            'service_type': 'interface',
            'ports': [
                {
                    'client_port': 80,
                    'server_port': 80,
                    'protocol': 'TCP'
                }
            ],
            'tags': [
                {
                    'key': 'tag-key',
                    'value': 'tag-value'
                }
            ],
            'tcp_proxy': '127.0.0.1:8080'
        }

        self.client.create_endpoint_service.assert_called_with(**attrs)
        self.assertEqual(self.columns, columns)


class TestShowEndpointService(fakes.TestVpcep):

    _data = fakes.FakeEndpointService.create_one()

    columns = (
        'approval_enabled',
        'created_at',
        'id',
        'pool_id',
        'port_id',
        'ports',
        'project_id',
        'router_id',
        'server_type',
        'service_name',
        'service_type',
        'status'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestShowEndpointService, self).setUp()

        self.cmd = endpoint_service.ShowEndpointService(self.app, None)

        self.client.get_endpoint_service = mock.Mock(return_value=self._data)

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
            ('endpointservice', self._data.id),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.get_endpoint_service.assert_called_with(self._data.id)

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)

    def test_show_non_existent(self):
        arglist = [
            'unexist_vpc_endpoint_service',
        ]

        verifylist = [
            ('endpointservice', 'unexist_vpc_endpoint_service'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_result = exceptions.CommandError('Resource Not Found')
        self.client.get_endpoint_service = (
            mock.Mock(side_effect=find_mock_result)
        )

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual('Resource Not Found', str(e))
        self.client.get_endpoint_service.assert_called_with(
            'unexist_vpc_endpoint_service')


class TestDeleteEndpointService(fakes.TestVpcep):

    _data = fakes.FakeEndpointService.create_multiple(2)

    def setUp(self):
        super(TestDeleteEndpointService, self).setUp()

        self.client.delete_endpoint_service = mock.Mock(return_value=None)

        # Get the command object to test
        self.cmd = endpoint_service.DeleteEndpointService(self.app, None)

    def test_delete(self):
        arglist = [
            self._data[0].name,
        ]

        verifylist = [
            ('endpointservice', [self._data[0].name]),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.client.get_endpoint_service = (
            mock.Mock(return_value=self._data[0])
        )

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.delete_endpoint_service.assert_called_with(
            self._data[0].id)
        self.assertIsNone(result)

    def test_multiple_delete(self):
        arglist = []

        for data in self._data:
            arglist.append(data.name)

        verifylist = [
            ('endpointservice', arglist),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_result = self._data
        self.client.get_endpoint_service = (
            mock.Mock(side_effect=find_mock_result)
        )

        # Trigger the action
        result = self.cmd.take_action(parsed_args)

        calls = []
        for data in self._data:
            calls.append(call(data.id))
        self.client.delete_endpoint_service.assert_has_calls(calls)
        self.assertIsNone(result)

    def test_multiple_delete_with_exception(self):
        arglist = [
            self._data[0].name,
            'unexist_vpc_endpoint_service',
        ]
        verifylist = [
            ('endpointservice', arglist),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_result = [self._data[0], exceptions.CommandError]
        self.client.get_endpoint_service = (
            mock.Mock(side_effect=find_mock_result)
        )

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual(
                '1 of 2 Vpc Endpoint Services(s) failed to delete.', str(e))

        self.client.get_endpoint_service.assert_any_call(
            self._data[0].name)
        self.client.get_endpoint_service.assert_any_call(
            'unexist_vpc_endpoint_service')
        self.client.delete_endpoint_service.assert_called_once_with(
            self._data[0].id)


class TestListWhitelist(fakes.TestVpcep):

    objects = fakes.FakeWhitelist.create_multiple(3)

    column_list_headers = ('Id', 'Permission', 'Created At')

    columns = ('id', 'permission', 'created_at')

    data = []

    for s in objects:
        data.append(
            (s.id, s.permission, s.created_at))

    def setUp(self):
        super(TestListWhitelist, self).setUp()

        self.cmd = endpoint_service.ListWhitelist(self.app, None)

        self.client.whitelist = mock.Mock()
        self.client.api_mock = self.client.whitelist

    def test_list(self):
        arglist = [
            'test-endpoint-service'
        ]

        verifylist = (
            ('endpointservice', 'test-endpoint-service'),
        )

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with('test-endpoint-service')

        self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(self.data, list(data))

    def test_list_args(self):
        arglist = [
            'test-endpoint-service',
            '--sort-key', '1',
            '--sort-dir', '2',
            '--limit', '3',
            '--offset', '4',
        ]

        verifylist = [
            ('endpointservice', 'test-endpoint-service'),
            ('sort_key', '1'),
            ('sort_dir', '2'),
            ('limit', 3),
            ('offset', 4)
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(
            'test-endpoint-service',
            sort_key='1',
            sort_dir='2',
            limit=3,
            offset=4,
        )


class TestManageWhitelist(fakes.TestVpcep):

    objects = fakes.FakeManageWhitelist.create_one()

    column_list_headers = ('Domain Id', 'Status')
    columns = ('domain_id', 'status')

    data = objects.permissions

    def setUp(self):
        super(TestManageWhitelist, self).setUp()

        self.cmd = endpoint_service.ManageWhitelist(self.app, None)

        self.client.manage_whitelist = mock.Mock()
        self.client.api_mock = self.client.manage_whitelist

    def test_create(self):
        arglist = [
            'test-endpoint-service',
            'domain1-id',
            'domain2-id',
            '--add'
        ]
        verifylist = [
            ('endpointservice', 'test-endpoint-service'),
            ('domain', ['domain1-id', 'domain2-id']),
            ('add', True),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.manage_whitelist.assert_called_with(
            'test-endpoint-service',
            domains=['domain1-id', 'domain2-id'],
            action='add')
        self.assertEqual(self.column_list_headers, columns)
