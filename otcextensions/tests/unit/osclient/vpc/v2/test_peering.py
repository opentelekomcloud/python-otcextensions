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

from otcextensions.osclient.vpc.v2 import peering
from otcextensions.tests.unit.osclient.vpc.v2 import fakes

from openstackclient.tests.unit import utils as tests_utils


class TestListVpcPeerings(fakes.TestVpc):

    objects = fakes.FakeVpcPeering.create_multiple(3)

    column_list_headers = (
        'Id',
        'Name',
        'Status',
        'Local Router Id',
        'Peer Router Id',
        'Peer Project Id',
    )

    columns = (
        'id',
        'name',
        'status',
        'local_router_id',
        'peer_router_id',
        'peer_project_id'
    )

    data = []

    for s in objects:
        data.append(
            (s.id, s.name, s.status, s.local_vpc_info['vpc_id'],
                s.peer_vpc_info['vpc_id'], s.peer_vpc_info['tenant_id']))

    def setUp(self):
        super(TestListVpcPeerings, self).setUp()

        self.cmd = peering.ListVpcPeerings(self.app, None)

        self.client.peerings = mock.Mock()
        self.client.api_mock = self.client.peerings

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
            '--name', '4',
            '--project-id', '5',
            '--router-id', '6',
            '--status', 'ACTIVE'
        ]

        verifylist = [
            ('limit', 1),
            ('marker', '2'),
            ('id', '3'),
            ('name', '4'),
            ('project_id', '5'),
            ('router_id', '6'),
            ('status', 'ACTIVE'),
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
            name='4',
            project_id='5',
            router_id='6',
            status='ACTIVE',
        )


class TestCreateVpcPeering(fakes.TestVpc):

    _data = fakes.FakeVpcPeering.create_one()

    columns = (
        'id',
        'name',
        'local_vpc_info',
        'peer_vpc_info',
        'description',
        'created_at',
        'updated_at',
        'status'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestCreateVpcPeering, self).setUp()

        self.cmd = peering.CreateVpcPeering(self.app, None)
        self.client.create_peering = mock.Mock(
            return_value=fakes.FakeVpcPeering.create_one())
        self.client.get_project_id = mock.Mock(
            return_value='test-local-project-uuid')

    def test_create_different_project(self):
        arglist = [
            'test-peering',
            '--local-router-id', 'test-local-router-uuid',
            '--peer-router-id', 'test-peer-router-uuid',
            '--peer-project-id', 'test-peer-project-uuid',
            '--description', 'test-peering',
        ]
        verifylist = [
            ('name', 'test-peering'),
            ('local_router_id', 'test-local-router-uuid'),
            ('peer_router_id', 'test-peer-router-uuid'),
            ('peer_project_id', 'test-peer-project-uuid'),
            ('description', 'test-peering'),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        attrs = {
            'name': 'test-peering',
            'request_vpc_info': {
                'vpc_id': 'test-local-router-uuid',
                'tenant_id': 'test-local-project-uuid'
            },
            'accept_vpc_info': {
                'vpc_id': 'test-peer-router-uuid',
                'tenant_id': 'test-peer-project-uuid'
            },
            'description': 'test-peering'
        }

        self.client.create_peering.assert_called_with(**attrs)
        self.assertEqual(self.columns, columns)

    def test_create_same_project(self):
        arglist = [
            'test-peering',
            '--local-router-id', 'test-local-router-uuid',
            '--peer-router-id', 'test-peer-router-uuid',
            '--description', 'test-peering',
        ]
        verifylist = [
            ('name', 'test-peering'),
            ('local_router_id', 'test-local-router-uuid'),
            ('peer_router_id', 'test-peer-router-uuid'),
            ('description', 'test-peering'),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        attrs = {
            'name': 'test-peering',
            'request_vpc_info': {
                'vpc_id': 'test-local-router-uuid'
            },
            'accept_vpc_info': {
                'vpc_id': 'test-peer-router-uuid'
            },
            'description': 'test-peering'
        }

        self.client.create_peering.assert_called_with(**attrs)
        self.assertEqual(self.columns, columns)


class TestUpdateVpcPeering(fakes.TestVpc):

    _data = fakes.FakeVpcPeering.create_one()

    columns = (
        'id',
        'name',
        'local_vpc_info',
        'peer_vpc_info',
        'description',
        'created_at',
        'updated_at',
        'status'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestUpdateVpcPeering, self).setUp()

        self.cmd = peering.UpdateVpcPeering(self.app, None)

        self.client.find_peering = mock.Mock(return_value=self._data)
        self.client.update_peering = mock.Mock(return_value=self._data)

    def test_update(self):
        arglist = [
            self._data.name,
            '--name', 'test-peering-updated',
            '--description', 'vpc peering updated',
        ]
        verifylist = [
            ('peering', self._data.name),
            ('name', 'test-peering-updated'),
            ('description', 'vpc peering updated'),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_peering.assert_called_with(self._data.name)
        self.client.update_peering.assert_called_with(
            self._data.id,
            name='test-peering-updated',
            description='vpc peering updated'
        )
        self.assertEqual(self.columns, columns)


class TestShowVpcPeering(fakes.TestVpc):

    _data = fakes.FakeVpcPeering.create_one()

    columns = (
        'id',
        'name',
        'local_vpc_info',
        'peer_vpc_info',
        'description',
        'created_at',
        'updated_at',
        'status'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestShowVpcPeering, self).setUp()

        self.cmd = peering.ShowVpcPeering(self.app, None)

        self.client.find_peering = mock.Mock(return_value=self._data)

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
            ('peering', self._data.id),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.find_peering.assert_called_with(self._data.id)

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)

    def test_show_non_existent(self):
        arglist = [
            'unexist_vpc_peering',
        ]

        verifylist = [
            ('peering', 'unexist_vpc_peering'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_result = exceptions.CommandError('Resource Not Found')
        self.client.find_peering = (
            mock.Mock(side_effect=find_mock_result)
        )

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual('Resource Not Found', str(e))
        self.client.find_peering.assert_called_with('unexist_vpc_peering')


class TestSetVpcPeering(fakes.TestVpc):

    _data = fakes.FakeVpcPeering.create_one()

    columns = (
        'id',
        'name',
        'local_vpc_info',
        'peer_vpc_info',
        'description',
        'created_at',
        'updated_at',
        'status'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestSetVpcPeering, self).setUp()

        self.cmd = peering.SetVpcPeering(self.app, None)

        self.client.find_peering = mock.Mock(return_value=self._data)
        self.client.set_peering = mock.Mock(return_value=self._data)

    def test_set(self):
        arglist = [
            self._data.name,
            '--accept'
        ]

        verifylist = [
            ('peering', self._data.name),
            ('accept', True),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.find_peering.assert_called_with(self._data.name)
        self.client.set_peering.assert_called_with(self._data.id, 'accept')

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestDeleteVpcPeering(fakes.TestVpc):

    _data = fakes.FakeVpcPeering.create_multiple(2)

    def setUp(self):
        super(TestDeleteVpcPeering, self).setUp()

        self.client.delete_peering = mock.Mock(return_value=None)

        # Get the command object to test
        self.cmd = peering.DeleteVpcPeering(self.app, None)

    def test_delete(self):
        arglist = [
            self._data[0].name,
        ]

        verifylist = [
            ('peering', [self._data[0].name]),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.client.find_peering = (
            mock.Mock(return_value=self._data[0])
        )

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.delete_peering.assert_called_with(self._data[0].id)
        self.assertIsNone(result)

    def test_multiple_delete(self):
        arglist = []

        for data in self._data:
            arglist.append(data.name)

        verifylist = [
            ('peering', arglist),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_result = self._data
        self.client.find_peering = (
            mock.Mock(side_effect=find_mock_result)
        )

        # Trigger the action
        result = self.cmd.take_action(parsed_args)

        calls = []
        for data in self._data:
            calls.append(call(data.id))
        self.client.delete_peering.assert_has_calls(calls)
        self.assertIsNone(result)

    def test_multiple_delete_with_exception(self):
        arglist = [
            self._data[0].name,
            'unexist_vpc_peering',
        ]
        verifylist = [
            ('peering', arglist),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_result = [self._data[0], exceptions.CommandError]
        self.client.find_peering = (
            mock.Mock(side_effect=find_mock_result)
        )

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual(
                '1 of 2 VPC peering(s) failed to delete.', str(e))

        self.client.find_peering.assert_any_call(self._data[0].name)
        self.client.find_peering.assert_any_call('unexist_vpc_peering')
        self.client.delete_peering.assert_called_once_with(self._data[0].id)
