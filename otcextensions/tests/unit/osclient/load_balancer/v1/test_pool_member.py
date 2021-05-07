#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#
import mock

from openstackclient.tests.unit import utils

from otcextensions.osclient.load_balancer.v1 import pool_member
from otcextensions.tests.unit.osclient.load_balancer.v1 import fakes


class TestListPoolMember(fakes.TestLoadBalancer):

    _objects = fakes.FakePoolMember.create_multiple(3)

    columns = (
        'id', 'name', 'project_id', 'provisioning_status', 'address',
        'protocol_port', 'operating_status', 'weight')

    data = []

    for s in _objects:
        data.append((
            s.id,
            s.name,
            s.project_id,
            '',  # provisioning_status
            s.address,
            s.protocol_port,
            s.operating_status,
            s.weight,
        ))

    def setUp(self):
        super(TestListPoolMember, self).setUp()

        self.cmd = pool_member.ListPoolMember(self.app, None)

        self.client.pool_members = mock.Mock()

    def test_list_default(self):
        arglist = [
            'pool'
        ]

        verifylist = [
            ('pool', 'pool')
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.pool_members.side_effect = [
            self._objects
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.pool_members.assert_called_once_with(
            pool='pool'
        )

        self.assertEqual(self.columns, columns)
        self.assertListItemEqual(self.data, list(data))

    def test_list_filter_values(self):
        arglist = [
            'pool',
            '--name', 'name',
            '--protocol_port', '15',
            '--address', 'address',
            '--weight', '13',
        ]

        verifylist = [
            ('pool', 'pool'),
            ('name', 'name'),
            ('protocol_port', 15),
            ('address', 'address'),
            ('weight', 13),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.pool_members.side_effect = [
            {}
        ]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.pool_members.assert_called_once_with(
            pool='pool',
            address='address',
            name='name',
            protocol_port=15,
            weight=13
        )

    def test_list_filter_exceptions_proto_port(self):
        arglist = [
            'pool',
            '--protocol_port', '15c',
        ]

        verifylist = [
            ('protocol_port', 12)
        ]

        # Ensure exception is raised
        self.assertRaises(
            utils.ParserException,
            self.check_parser, self.cmd, arglist, verifylist)

    def test_list_filter_exceptions_weight(self):
        arglist = [
            'pool',
            '--weight', '15c',
        ]

        verifylist = [
            ('weight', 12)
        ]

        # Ensure exception is raised
        self.assertRaises(
            utils.ParserException,
            self.check_parser, self.cmd, arglist, verifylist)


class TestShowPoolMember(fakes.TestLoadBalancer):

    _object = fakes.FakePoolMember.create_one()

    columns = (
        'address', 'admin_state_up', 'id', 'name',
        # 'operating_status',
        'protocol_port', 'subnet_id', 'weight')

    data = (
        _object.address,
        _object.is_admin_state_up,
        _object.id,
        _object.name,
        # _object.operating_status,
        _object.protocol_port,
        _object.subnet_id,
        _object.weight,
    )

    def setUp(self):
        super(TestShowPoolMember, self).setUp()

        self.cmd = pool_member.ShowPoolMember(self.app, None)

        self.client.find_pool_member = mock.Mock()

    def test_show_default(self):
        arglist = [
            'pool_id',
            'member'
        ]

        verifylist = [
            ('pool', 'pool_id'),
            ('member', 'member')
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.find_pool_member.side_effect = [
            self._object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_pool_member.assert_called_once_with(
            name_or_id='member',
            pool='pool_id',
            ignore_missing=False
        )

        self.assertEqual(self.columns, columns)
        self.assertItemEqual(self.data, data)


class TestCreatePoolMember(fakes.TestLoadBalancer):

    _object = fakes.FakePoolMember.create_one()

    columns = (
        'address', 'admin_state_up', 'id', 'name',
        # 'operating_status',
        'protocol_port', 'subnet_id', 'weight')

    data = (
        _object.address,
        _object.is_admin_state_up,
        _object.id,
        _object.name,
        # _object.operating_status,
        _object.protocol_port,
        _object.subnet_id,
        _object.weight,
    )

    def setUp(self):
        super(TestCreatePoolMember, self).setUp()

        self.cmd = pool_member.CreatePoolMember(self.app, None)

        self.client.create_pool_member = mock.Mock()

    def test_create_default(self):
        arglist = [
            'pool_id',
            '--address', 'addr',
            '--protocol_port', '123',
            '--disable',
            '--name', 'name',
            '--subnet_id', 'subnet',
            '--weight', '13'
        ]

        verifylist = [
            ('pool', 'pool_id'),
            ('address', 'addr'),
            ('protocol_port', 123),
            ('disable', True),
            ('name', 'name'),
            ('subnet_id', 'subnet'),
            ('weight', 13),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.create_pool_member.side_effect = [
            self._object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_pool_member.assert_called_once_with(
            address='addr',
            is_admin_state_up=False,
            name='name',
            pool='pool_id',
            protocol_port=123,
            subnet_id='subnet',
            weight=13
        )

        self.assertEqual(self.columns, columns)
        self.assertItemEqual(self.data, data)


class TestUpdatePoolMember(fakes.TestLoadBalancer):

    _object = fakes.FakePoolMember.create_one()

    columns = (
        'address', 'admin_state_up', 'id', 'name',
        # 'operating_status',
        'protocol_port', 'subnet_id', 'weight')

    data = (
        _object.address,
        _object.is_admin_state_up,
        _object.id,
        _object.name,
        # _object.operating_status,
        _object.protocol_port,
        _object.subnet_id,
        _object.weight,
    )

    def setUp(self):
        super(TestUpdatePoolMember, self).setUp()

        self.cmd = pool_member.SetPoolMember(self.app, None)

        self.client.update_pool_member = mock.Mock()

    def test_update_default(self):
        arglist = [
            'pool_id',
            'member',
            '--disable',
            '--name', 'name',
            '--weight', '13'
        ]

        verifylist = [
            ('pool', 'pool_id'),
            ('member', 'member'),
            ('disable', True),
            ('name', 'name'),
            ('weight', 13),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.update_pool_member.side_effect = [
            self._object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.update_pool_member.assert_called_once_with(
            pool_member='member',
            is_admin_state_up=False,
            name='name',
            pool='pool_id',
            weight=13
        )

        self.assertEqual(self.columns, columns)
        self.assertItemEqual(self.data, data)


class TestDeletePoolMember(fakes.TestLoadBalancer):

    _object = fakes.FakePoolMember.create_one()
    _pool = fakes.FakePool.create_one()

    def setUp(self):
        super(TestDeletePoolMember, self).setUp()

        self.cmd = pool_member.DeletePoolMember(self.app, None)

        self.client.delete_pool_member = mock.Mock()
        self.client.find_pool_member = mock.Mock()

    def test_delete_default(self):
        arglist = [
            'pool_id',
            'member',
        ]

        verifylist = [
            ('pool', 'pool_id'),
            ('member', ['member']),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.delete_pool_member.side_effect = [
            {}
        ]
        self.client.find_pool_member.side_effect = [
            self._object
        ]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.delete_pool_member.assert_called_once_with(
            pool_member=self._object.id,
            pool='pool_id',
            ignore_missing=False
        )
