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
import mock

from openstackclient.tests.unit import utils

from otcextensions.osclient.dcs.v1 import instance
from otcextensions.tests.unit.osclient.dcs.v1 import fakes


class TestListInstance(fakes.TestDCS):

    objects = fakes.FakeInstance.create_multiple(3)

    columns = ('id', 'name', 'engine', 'status', 'error_code')

    data = []

    for s in objects:
        data.append((
            s.id,
            s.name,
            s.engine,
            s.status,
            s.error_code,
        ))

    def setUp(self):
        super(TestListInstance, self).setUp()

        self.cmd = instance.ListInstance(self.app, None)

        self.client.instances = mock.Mock()

    def test_list(self):
        arglist = [
        ]

        verifylist = [
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.instances.side_effect = [
            self.objects
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.instances.assert_called_once_with(
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))

    def test_list_query(self):
        arglist = [
            '--limit', '1',
            '--start', '2',
            '--name', '3',
            '--status', 'CREATING',
            '--include_failure',
            '--exact_match'
        ]

        verifylist = [
            ('limit', 1),
            ('start', 2),
            ('name', '3'),
            ('status', 'CREATING'),
            ('include_failure', True),
            ('exact_match', True)
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.instances.side_effect = [
            self.objects
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.instances.assert_called_once_with(
            exactMatchName=True,
            includeFailure=True,
            limit=1,
            name='3',
            start=2,
            status='CREATING'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))

    def test_list_bad_arg(self):
        arglist = [
            '--status', 'BAD',
        ]

        verifylist = [
            ('status', 'BAD'),
        ]

        self.assertRaises(
            utils.ParserException,
            self.check_parser, self.cmd, arglist, verifylist)


class TestBasicInstance(fakes.TestDCS):

    _data = fakes.FakeInstance.create_one()

    columns = (
        'available_zones', 'capacity', 'charging_mode', 'created_at',
        'description', 'engine', 'engine_version', 'error_code',
        'id', 'internal_version', 'ip', 'maintain_begin', 'maintain_end',
        'max_memory', 'name', 'order_id', 'port', 'product_id',
        'resource_spec_code', 'security_group_id', 'security_group_name',
        'status', 'subnet_cidr', 'subnet_id', 'subnet_name',
        'used_memory', 'user_id', 'user_name', 'vpc_id', 'vpc_name')

    data = (
        _data.available_zones,
        _data.capacity,
        _data.charging_mode,
        _data.created_at,
        _data.description,
        _data.engine,
        _data.engine_version,
        _data.error_code,
        _data.id,
        _data.internal_version,
        _data.ip,
        _data.maintain_begin,
        _data.maintain_end,
        _data.max_memory,
        _data.name,
        _data.order_id,
        _data.port,
        _data.product_id,
        _data.resource_spec_code,
        _data.security_group_id,
        _data.security_group_name,
        _data.status,
        _data.subnet_cidr,
        _data.subnet_id,
        _data.subnet_name,
        _data.used_memory,
        _data.user_id,
        _data.user_name,
        _data.vpc_id,
        _data.vpc_name
    )

    def setUp(self):
        super(TestBasicInstance, self).setUp()


class TestShowInstance(TestBasicInstance):

    def setUp(self):
        super(TestShowInstance, self).setUp()

        self.cmd = instance.ShowInstance(self.app, None)

        self.client.find_instance = mock.Mock()

    def test_show_default(self):
        arglist = [
            'name_or_id',
        ]
        verifylist = [
            ('instance', 'name_or_id'),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.find_instance.side_effect = [
            self._data
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_instance.assert_called_with(
            name_or_id='name_or_id'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestDeleteInstance(fakes.TestDCS):

    def setUp(self):
        super(TestDeleteInstance, self).setUp()

        self.cmd = instance.DeleteInstance(self.app, None)

        self.client.delete_instance = mock.Mock()

    def test_delete(self):
        arglist = [
            't1',
        ]

        verifylist = [
            ('instance', ['t1'])
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.delete_instance.side_effect = [{}]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        calls = [mock.call(instance='t1')]

        self.client.delete_instance.assert_has_calls(calls)
        self.assertEqual(1, self.client.delete_instance.call_count)

    def test_delete_multiple(self):
        arglist = [
            't1',
            't2',
        ]
        verifylist = [
            ('instance', ['t1', 't2'])
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.delete_instance.side_effect = [{}, {}]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        calls = [
            mock.call(instance='t1'),
            mock.call(instance='t2')
        ]

        self.client.delete_instance.assert_has_calls(calls)
        self.assertEqual(2, self.client.delete_instance.call_count)


class TestCreateInstance(TestBasicInstance):

    def setUp(self):
        super(TestCreateInstance, self).setUp()

        self.cmd = instance.CreateInstance(self.app, None)

        self.client.create_instance = mock.Mock()

    def test_show_default(self):
        arglist = [
            '--name', '1',
            '--description', '2',
            '--engine', '3',
            '--engine_version', '4',
            '--capacity', '4',
            '--password', '6',
            '--vpc_id', '7',
            '--security_group_id', '8',
            '--subnet_id', '9',
            '--az', '10',
            '--product_id', 'OTC_DCS_SINGLE',
            '--backup_policy', '{}',
            '--maintain_begin', '11',
            '--maintain_end', '12'
        ]
        verifylist = [
            ('name', '1'),
            ('description', '2'),
            ('engine', '3'),
            ('engine_version', '4'),
            ('password', '6'),
            ('capacity', 4),
            ('vpc_id', '7'),
            ('security_group_id', '8'),
            ('subnet_id', '9'),
            ('az', '10'),
            ('product_id', 'OTC_DCS_SINGLE'),
            ('backup_policy', '{}'),
            ('maintain_begin', '11'),
            ('maintain_end', '12')
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.create_instance.side_effect = [
            self._data
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_instance.assert_called_with(
            name='1',
            description='2',
            engine='3',
            engine_version='4',
            capacity=4,
            password='6',
            vpc_id='7',
            security_group_id='8',
            subnet_id='9',
            az='10',
            product_id='OTC_DCS_SINGLE',
            backup_policy='{}',
            maintain_begin='11',
            maintain_end='12'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestSetInstance(TestBasicInstance):

    def setUp(self):
        super(TestSetInstance, self).setUp()

        self.cmd = instance.SetInstance(self.app, None)

        self.client.update_instance = mock.Mock()

    def test_show_default(self):
        arglist = [
            'inst',
            '--name', '1',
            '--description', '2',
            '--security_group_id', '8',
            '--backup_policy', '{}',
            '--maintain_begin', '11',
            '--maintain_end', '12'
        ]
        verifylist = [
            ('instance', 'inst'),
            ('name', '1'),
            ('description', '2'),
            ('security_group_id', '8'),
            ('backup_policy', '{}'),
            ('maintain_begin', '11'),
            ('maintain_end', '12')
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.update_instance.side_effect = [
            self._data
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.update_instance.assert_called_with(
            backup_policy='{}',
            description='2',
            instance='inst',
            maintain_begin='11',
            maintain_end='12',
            name='1',
            security_group_id='8'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestExtendInstance(TestBasicInstance):

    def setUp(self):
        super(TestExtendInstance, self).setUp()

        self.cmd = instance.ExtendInstance(self.app, None)

    def test_default(self):
        arglist = [
            'inst',
            '--capacity', '2',
        ]
        verifylist = [
            ('instance', 'inst'),
            ('capacity', 2),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.extend_instance.side_effect = [
            self._data
        ]
        self.client.find_instance.side_effect = [
            self._data
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_instance.assert_called_with(
            name_or_id='inst',
            ignore_missing=False
        )
        self.client.extend_instance.assert_called_with(
            instance=self._data.id,
            capacity=2,
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestStopInstance(TestBasicInstance):

    def setUp(self):
        super(TestStopInstance, self).setUp()

        self.cmd = instance.StopInstance(self.app, None)

    def test_default(self):
        arglist = [
            'inst',
        ]
        verifylist = [
            ('instance', 'inst'),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.stop_instance.side_effect = [
            self._data
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.stop_instance.assert_called_with(
            instance='inst',
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestStartInstance(TestBasicInstance):

    def setUp(self):
        super(TestStartInstance, self).setUp()

        self.cmd = instance.StartInstance(self.app, None)

    def test_default(self):
        arglist = [
            'inst',
        ]
        verifylist = [
            ('instance', 'inst'),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.start_instance.side_effect = [
            self._data
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.start_instance.assert_called_with(
            instance='inst',
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestRestartInstance(TestBasicInstance):

    def setUp(self):
        super(TestRestartInstance, self).setUp()

        self.cmd = instance.RestartInstance(self.app, None)

    def test_default(self):
        arglist = [
            'inst',
        ]
        verifylist = [
            ('instance', 'inst'),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.restart_instance.side_effect = [
            self._data
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.restart_instance.assert_called_with(
            instance='inst',
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestChangePwdInstance(TestBasicInstance):

    def setUp(self):
        super(TestChangePwdInstance, self).setUp()

        self.cmd = instance.ChangePasswordInstance(self.app, None)

    def test_default(self):
        arglist = [
            'inst',
            '--current_password', 'curr',
            '--new_password', 'new'
        ]
        verifylist = [
            ('instance', 'inst'),
            ('current_password', 'curr'),
            ('new_password', 'new')
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.change_instance_password.side_effect = [
            self._data
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.change_instance_password.assert_called_with(
            instance='inst',
            current_password='curr',
            new_password='new'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)
