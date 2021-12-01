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

from otcextensions.osclient.vpc.v2 import route
from otcextensions.tests.unit.osclient.vpc.v1 import fakes

from openstackclient.tests.unit import utils as tests_utils


class TestListVpcRoutes(fakes.TestVpc):

    objects = fakes.FakeVpcRoute.create_multiple(3)

    column_list_headers = (
        'Id',
        'Type',
        'Router Id',
        'Project Id',
        'NextHop',
        'Destination'
    )

    columns = (
        'id',
        'type',
        'router_id',
        'project_id',
        'nexthop',
        'destination'
    )

    data = []

    for s in objects:
        data.append(
            (s.id, s.type, s.router_id, s.project_id,
                s.nexthop, s.destination))

    def setUp(self):
        super(TestListVpcRoutes, self).setUp()

        self.cmd = route.ListVpcRoutes(self.app, None)

        self.client.routes = mock.Mock()
        self.client.api_mock = self.client.routes

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
            '--marker', '2',
            '--id', '3',
            '--destination', '4',
            '--project-id', '5',
            '--router-id', '6'
        ]

        verifylist = [
            ('limit', 1),
            ('marker', '2'),
            ('id', '3'),
            ('destination', '4'),
            ('project_id', '5'),
            ('router_id', '6')
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(
            limit=1,
            marker='2',
            id='3',
            destination='4',
            project_id='5',
            router_id='6',
        )


class TestAddVpcRoute(fakes.TestVpc):

    _data = fakes.FakeVpcRoute.create_one()

    columns = (
        'id',
        'type',
        'nexthop',
        'destination',
        'router_id',
        'project_id'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestAddVpcRoute, self).setUp()

        self.cmd = route.AddVpcRoute(self.app, None)
        self.client.add_route = mock.Mock(
            return_value=fakes.FakeVpcRoute.create_one())

    def test_add_route(self):
        arglist = [
            '--nexthop', 'test-peering-uuid',
            '--destination', '192.168.1.0/24',
            '--router-id', 'test-router-uuid',
        ]
        verifylist = [
            ('nexthop', 'test-peering-uuid'),
            ('type', 'peering'),
            ('destination', '192.168.1.0/24'),
            ('router_id', 'test-router-uuid'),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        attrs = {
            'nexthop': 'test-peering-uuid',
            'type': 'peering',
            'destination': '192.168.1.0/24',
            'router_id': 'test-router-uuid'
        }

        self.client.add_route.assert_called_with(**attrs)
        self.assertEqual(self.columns, columns)


class TestShowVpcRoute(fakes.TestVpc):

    _data = fakes.FakeVpcRoute.create_one()

    columns = (
        'id',
        'type',
        'nexthop',
        'destination',
        'router_id',
        'project_id'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestShowVpcRoute, self).setUp()

        self.cmd = route.ShowVpcRoute(self.app, None)

        self.client.get_route = mock.Mock(return_value=self._data)

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
            ('route', self._data.id),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.get_route.assert_called_with(self._data.id)

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)

    def test_show_non_existent(self):
        arglist = [
            'unexist_vpc_route',
        ]

        verifylist = [
            ('route', 'unexist_vpc_route'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_result = exceptions.CommandError('Resource Not Found')
        self.client.get_route = (
            mock.Mock(side_effect=find_mock_result)
        )

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual('Resource Not Found', str(e))
        self.client.get_route.assert_called_with('unexist_vpc_route')


class TestDeleteVpcRoute(fakes.TestVpc):

    _data = fakes.FakeVpcRoute.create_multiple(2)

    def setUp(self):
        super(TestDeleteVpcRoute, self).setUp()

        self.client.delete_route = mock.Mock(return_value=None)

        # Get the command object to test
        self.cmd = route.DeleteVpcRoute(self.app, None)

    def test_delete(self):
        arglist = [
            self._data[0].id,
        ]

        verifylist = [
            ('route', [self._data[0].id]),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.client.get_route = (
            mock.Mock(return_value=self._data[0])
        )

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.delete_route.assert_called_with(self._data[0].id)
        self.assertIsNone(result)

    def test_multiple_delete(self):
        arglist = []

        for data in self._data:
            arglist.append(data.id)

        verifylist = [
            ('route', arglist),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        get_mock_result = self._data
        self.client.get_route = (
            mock.Mock(side_effect=get_mock_result)
        )

        # Trigger the action
        result = self.cmd.take_action(parsed_args)

        calls = []
        for data in self._data:
            calls.append(call(data.id))
        self.client.delete_route.assert_has_calls(calls)
        self.assertIsNone(result)

    def test_multiple_delete_with_exception(self):
        arglist = [
            self._data[0].id,
            'unexist_vpc_route',
        ]
        verifylist = [
            ('route', arglist),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        get_mock_result = [self._data[0], exceptions.CommandError]
        self.client.get_route = (
            mock.Mock(side_effect=get_mock_result)
        )

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual(
                '1 of 2 VPC route(s) failed to delete.', str(e))

        self.client.get_route.assert_any_call(self._data[0].id)
        self.client.get_route.assert_any_call('unexist_vpc_route')
        self.client.delete_route.assert_called_once_with(self._data[0].id)
