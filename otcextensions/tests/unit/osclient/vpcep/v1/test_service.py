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

from otcextensions.osclient.vpcep.v1 import service
from otcextensions.tests.unit.osclient.vpcep.v1 import fakes


class TestListServices(fakes.TestVpcep):

    objects = fakes.FakeService.create_multiple(3)

    column_list_headers = (
        'Id',
        'Service Name',
        'Service Type',
        'Server Type',
        'Connection Count',
        'Status',
    )

    columns = (
        'id',
        'service_name',
        'service_type',
        'server_type',
        'connection_count',
        'status',
    )

    data = []

    for s in objects:
        data.append(
            (
                s.id,
                s.service_name,
                s.service_type,
                s.server_type,
                s.connection_count,
                s.status,
            )
        )

    def setUp(self):
        super(TestListServices, self).setUp()

        self.cmd = service.ListServices(self.app, None)

        self.client.services = mock.Mock()
        self.client.api_mock = self.client.services

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
            '--name',
            '2',
            '--status',
            '3',
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
            ('name', '2'),
            ('status', '3'),
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
            name='2',
            status='3',
            sort_key='created_at',
            sort_dir='desc',
            limit=6,
            offset=7,
        )


class TestCreateService(fakes.TestVpcep):

    _data = fakes.FakeService.create_one()

    columns = (
        'created_at',
        'id',
        'is_approval_enabled',
        'pool_id',
        'port_id',
        'ports',
        'project_id',
        'router_id',
        'server_type',
        'service_name',
        'service_type',
        'status',
    )

    data = fakes.gen_data(_data, columns, formatters=service._formatters)

    def setUp(self):
        super(TestCreateService, self).setUp()

        self.cmd = service.CreateService(self.app, None)
        self.client.create_service = mock.Mock(
            return_value=fakes.FakeService.create_one()
        )

    def test_create(self):
        arglist = [
            'test-endpoint-service',
            '--port-id',
            'test-port-uuid',
            '--pool-id',
            'test-pool-uuid',
            '--router-id',
            'test-router-uuid',
            '--disable-approval',
            '--server-type',
            'VM',
            '--service-type',
            'Interface',
            '--ports',
            'client_port=80,server_port=80,protocol=TCP',
            '--tags',
            'key=tag-key,value=tag-value',
            '--tcp-proxy',
            'open',
        ]
        verifylist = [
            ('name', 'test-endpoint-service'),
            ('port_id', 'test-port-uuid'),
            ('pool_id', 'test-pool-uuid'),
            ('vpc_id', 'test-router-uuid'),
            ('disable_approval', True),
            ('server_type', 'VM'),
            ('service_type', 'interface'),
            (
                'ports',
                [
                    {
                        'client_port': '80',
                        'server_port': '80',
                        'protocol': 'TCP',
                    }
                ],
            ),
            ('tags', [{'key': 'tag-key', 'value': 'tag-value'}]),
            ('tcp_proxy', 'open'),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        attrs = {
            'service_name': 'test-endpoint-service',
            'port_id': 'test-port-uuid',
            'pool_id': 'test-pool-uuid',
            'vpc_id': 'test-router-uuid',
            'approval_enabled': False,
            'server_type': 'VM',
            'service_type': 'interface',
            'ports': [
                {'client_port': 80, 'server_port': 80, 'protocol': 'TCP'}
            ],
            'tags': [{'key': 'tag-key', 'value': 'tag-value'}],
            'tcp_proxy': 'open',
        }

        self.client.create_service.assert_called_with(**attrs)
        self.assertEqual(self.columns, columns)


class TestShowService(fakes.TestVpcep):

    _data = fakes.FakeService.create_one()

    columns = (
        'created_at',
        'id',
        'is_approval_enabled',
        'pool_id',
        'port_id',
        'ports',
        'project_id',
        'router_id',
        'server_type',
        'service_name',
        'service_type',
        'status',
    )

    data = fakes.gen_data(_data, columns, formatters=service._formatters)

    def setUp(self):
        super(TestShowService, self).setUp()

        self.cmd = service.ShowService(self.app, None)

        self.client.find_service = mock.Mock(return_value=self._data)

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
            ('service', self._data.id),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.find_service.assert_called_with(self._data.id)

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)

    def test_show_non_existent(self):
        arglist = [
            'non-existing-service',
        ]

        verifylist = [
            ('service', 'non-existing-service'),
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
        self.client.find_service.assert_called_with('non-existing-service')


class TestUpdateService(fakes.TestVpcep):

    _data = fakes.FakeService.create_one()

    columns = (
        'created_at',
        'id',
        'is_approval_enabled',
        'pool_id',
        'port_id',
        'ports',
        'project_id',
        'router_id',
        'server_type',
        'service_name',
        'service_type',
        'status',
    )

    data = fakes.gen_data(_data, columns, formatters=service._formatters)

    def setUp(self):
        super(TestUpdateService, self).setUp()

        self.cmd = service.UpdateService(self.app, None)

        self.client.find_service = mock.Mock(return_value=self._data)
        self.client.update_service = mock.Mock(return_value=self._data)

    def test_update(self):
        arglist = [
            self._data.name,
            '--name',
            'test-endpoint-service',
            '--ports',
            'client_port=80,server_port=80,protocol=TCP',
            '--port-id',
            'test-port-uuid',
            '--tcp-proxy',
            'open',
            '--enable-approval',
        ]
        verifylist = [
            ('service', self._data.name),
            ('service_name', 'test-endpoint-service'),
            (
                'ports',
                [
                    {
                        'client_port': '80',
                        'server_port': '80',
                        'protocol': 'TCP',
                    }
                ],
            ),
            ('port_id', 'test-port-uuid'),
            ('tcp_proxy', 'open'),
            ('enable_approval', True),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_service.assert_called_with(self._data.name)

        attrs = {
            'service_name': 'test-endpoint-service',
            'port_id': 'test-port-uuid',
            'ports': [
                {'client_port': 80, 'server_port': 80, 'protocol': 'TCP'}
            ],
            'tcp_proxy': 'open',
            'approval_enabled': True,
        }
        self.client.update_service.assert_called_with(self._data, **attrs)
        self.assertEqual(self.columns, columns)


class TestDeleteService(fakes.TestVpcep):

    _data = fakes.FakeService.create_multiple(2)

    def setUp(self):
        super(TestDeleteService, self).setUp()

        self.client.delete_service = mock.Mock(return_value=None)

        # Get the command object to test
        self.cmd = service.DeleteService(self.app, None)

    def test_delete(self):
        arglist = [
            self._data[0].name,
        ]

        verifylist = [
            ('service', [self._data[0].name]),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.client.find_service = mock.Mock(return_value=self._data[0])

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.delete_service.assert_called_with(self._data[0].id)
        self.assertIsNone(result)

    def test_multiple_delete(self):
        arglist = []

        for data in self._data:
            arglist.append(data.name)

        verifylist = [
            ('service', arglist),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_result = self._data
        self.client.find_service = mock.Mock(side_effect=find_mock_result)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)

        calls = []
        for data in self._data:
            calls.append(call(data.id))
        self.client.delete_service.assert_has_calls(calls)
        self.assertIsNone(result)

    def test_multiple_delete_with_exception(self):
        arglist = [
            self._data[0].name,
            'non-existing-service',
        ]
        verifylist = [
            ('service', arglist),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_result = [self._data[0], exceptions.CommandError]
        self.client.find_service = mock.Mock(side_effect=find_mock_result)

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual(
                '1 of 2 Vpc Endpoint Services(s) failed to delete.', str(e)
            )

        self.client.find_service.assert_any_call(self._data[0].name)
        self.client.find_service.assert_any_call('non-existing-service')
        self.client.delete_service.assert_called_once_with(self._data[0].id)
