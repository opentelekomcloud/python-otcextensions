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

from otcextensions.osclient.vpcep.v1 import connection
from otcextensions.tests.unit.osclient.vpcep.v1 import fakes


class TestListWhitelist(fakes.TestVpcep):

    _service = fakes.FakeService.create_one()
    objects = fakes.FakeConnection.create_multiple(3)
    column_list_headers = (
        'Id',
        'Domain Id',
        'Status',
        'Created At',
        'Updated At',
    )

    columns = (
        'id',
        'domain_id',
        'status',
        'created_at',
        'updated_at',
    )

    data = []

    for s in objects:
        data.append(
            (
                s.id,
                s.domain_id,
                s.status,
                s.created_at,
                s.updated_at,
            )
        )

    def setUp(self):
        super(TestListWhitelist, self).setUp()

        self.cmd = connection.ListConnections(self.app, None)

        self.client.find_service = mock.Mock(return_value=self._service)
        self.client.service_connections = mock.Mock()
        self.client.api_mock = self.client.service_connections

    def test_list(self):
        arglist = [self._service.name]

        verifylist = [
            ('service', self._service.name),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(self._service)

        self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(self.data, list(data))

    def test_list_args(self):
        arglist = [
            self._service.name,
            '--sort-key',
            'created_at',
            '--sort-dir',
            'asc',
            '--limit',
            '2',
            '--offset',
            '3',
        ]

        verifylist = [
            ('service', self._service.name),
            ('sort_key', 'created_at'),
            ('sort_dir', 'asc'),
            ('limit', 2),
            ('offset', 3),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(
            self._service,
            sort_key='created_at',
            sort_dir='asc',
            limit=2,
            offset=3,
        )


class TestManageConnections(fakes.TestVpcep):

    _service = fakes.FakeService.create_one()
    objects = fakes.FakeConnection.create_multiple(3)
    column_list_headers = (
        'Id',
        'Domain Id',
        'Status',
        'Created At',
        'Updated At',
    )

    columns = (
        'id',
        'domain_id',
        'status',
        'created_at',
        'updated_at',
    )

    data = []

    for s in objects:
        data.append(
            (
                s.id,
                s.domain_id,
                s.status,
                s.created_at,
                s.updated_at,
            )
        )

    def setUp(self):
        super(TestManageConnections, self).setUp()

        self.cmd = connection.ManageConnections(self.app, None)

        self.client.find_service = mock.Mock(return_value=self._service)
        self.client.manage_service_connections = mock.Mock()
        self.client.api_mock = self.client.manage_service_connections

    def test_accept_connection(self):
        arglist = [self._service.name, '123', 'xyz', '--accept']

        verifylist = [
            ('service', self._service.name),
            ('endpoint', ['123', 'xyz']),
            ('receive', True),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(
            self._service,
            action='receive',
            endpoints=['123', 'xyz'],
        )

        self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(self.data, list(data))
