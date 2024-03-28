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

from otcextensions.osclient.vpcep.v1 import whitelist
from otcextensions.tests.unit.osclient.vpcep.v1 import fakes


class TestListWhitelist(fakes.TestVpcep):

    _service = fakes.FakeService.create_one()
    objects = fakes.FakeWhitelist.create_multiple(3)
    column_list_headers = ('Id', 'Permission', 'Created At')

    columns = (
        'id',
        'persmission',
        'created_at',
    )

    data = []

    for s in objects:
        data.append(
            (
                s.id,
                s.permission,
                s.created_at,
            )
        )

    def setUp(self):
        super(TestListWhitelist, self).setUp()

        self.cmd = whitelist.ListWhitelist(self.app, None)

        self.client.find_service = mock.Mock(return_value=self._service)
        self.client.service_whitelist = mock.Mock()
        self.client.api_mock = self.client.service_whitelist

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


class TestManageWhitelist(fakes.TestVpcep):

    _service = fakes.FakeService.create_one()
    objects = fakes.FakeWhitelist.create_multiple(3)
    column_list_headers = ('Permission',)

    columns = ('persmission',)

    data = []

    for s in objects:
        data.append((s.permission,))

    def setUp(self):
        super(TestManageWhitelist, self).setUp()

        self.cmd = whitelist.ManageWhitelist(self.app, None)

        self.client.find_service = mock.Mock(return_value=self._service)
        self.client.manage_service_whitelist = mock.Mock()
        self.client.api_mock = self.client.manage_service_whitelist

    def test_add_whitelist(self):
        arglist = [self._service.name, '123', 'xyz', '--add']

        verifylist = [
            ('service', self._service.name),
            ('domain', ['123', 'xyz']),
            ('add', True),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(
            self._service,
            domains=['123', 'xyz'],
            action='add',
        )

        self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(self.data, list(data))

    def test_remove_whitelist(self):
        arglist = [self._service.name, '123', 'xyz', '--remove']

        verifylist = [
            ('service', self._service.name),
            ('domain', ['123', 'xyz']),
            ('remove', True),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(
            self._service,
            domains=['123', 'xyz'],
            action='remove',
        )

        self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(self.data, list(data))
