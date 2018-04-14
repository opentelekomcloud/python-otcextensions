#   Copyright 2013 Nebula Inc.
#
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

from otcextensions.tests.unit.osclient.load_balancer.v1 import fakes

from otcextensions.osclient.load_balancer.v1 import pool_member


class TestListPoolMember(fakes.TestLoadBalancer):

    _objects = fakes.FakePoolMember.create_multiple(3)

    columns = ('ID', 'Name', 'address', 'is_admin_state_up',
               'protocol_port', 'subnet_id', 'operating_status', 'weight')

    data = []

    for s in _objects:
        data.append((
            s.id,
            s.name,
            s.address,
            s.is_admin_state_up,
            s.protocol_port,
            s.subnet_id,
            '',  # s.operating_status,
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

    columns = ('ID', 'Name', 'address', 'is_admin_state_up',
               'protocol_port', 'operating_status',
               'subnet_id', 'weight', 'pool_id')

    data = (
        _object.id,
        _object.name,
        _object.address,
        _object.is_admin_state_up,
        _object.protocol_port,
        '',  # _object.operating_status,
        _object.subnet_id,
        _object.weight,
        _object.pool_id,
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
            pool='pool_id'
        )

        self.assertEqual(self.columns, columns)
        self.assertItemEqual(self.data, data)


class TestCreatePoolMember(fakes.TestLoadBalancer):

    _object = fakes.FakePoolMember.create_one()

    columns = ('ID', 'Name', 'address', 'is_admin_state_up',
               'protocol_port', 'operating_status',
               'subnet_id', 'weight', 'pool_id')

    data = (
        _object.id,
        _object.name,
        _object.address,
        _object.is_admin_state_up,
        _object.protocol_port,
        '',  # _object.operating_status,
        _object.subnet_id,
        _object.weight,
        _object.pool_id,
    )

    def setUp(self):
        super(TestCreatePoolMember, self).setUp()

        self.cmd = pool_member.CreatePoolMember(self.app, None)

        self.client.create_pool_member = mock.Mock()

    def test_create_default(self):
        arglist = [
            'pool_id',
            'addr',
            '123',
            '--admin_state_up', 'true',
            '--name', 'name',
            '--subnet_id', 'subnet',
            '--weight', '13'
        ]

        verifylist = [
            ('pool', 'pool_id'),
            ('address', 'addr'),
            ('protocol_port', 123),
            ('admin_state_up', True),
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
            admin_state_up=True,
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

    columns = ('ID', 'Name', 'address', 'is_admin_state_up',
               'protocol_port', 'operating_status',
               'subnet_id', 'weight', 'pool_id')

    data = (
        _object.id,
        _object.name,
        _object.address,
        _object.is_admin_state_up,
        _object.protocol_port,
        '',  # _object.operating_status,
        _object.subnet_id,
        _object.weight,
        _object.pool_id,
    )

    def setUp(self):
        super(TestUpdatePoolMember, self).setUp()

        self.cmd = pool_member.UpdatePoolMember(self.app, None)

        self.client.update_pool_member = mock.Mock()

    def test_update_default(self):
        arglist = [
            'pool_id',
            'member',
            '--admin_state_up', 'true',
            '--name', 'name',
            '--weight', '13'
        ]

        verifylist = [
            ('pool', 'pool_id'),
            ('member', 'member'),
            ('admin_state_up', True),
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
            admin_state_up=True,
            name='name',
            pool='pool_id',
            weight=13
        )

        self.assertEqual(self.columns, columns)
        self.assertItemEqual(self.data, data)


class TestDeletePoolMember(fakes.TestLoadBalancer):

    def setUp(self):
        super(TestDeletePoolMember, self).setUp()

        self.cmd = pool_member.DeletePoolMember(self.app, None)

        self.client.delete_pool_member = mock.Mock()

    def test_update_default(self):
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
        self.client.update_pool_member.side_effect = [
            {}
        ]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.delete_pool_member.assert_called_once_with(
            pool_member='member',
            pool='pool_id',
            ignore_missing=False
        )
