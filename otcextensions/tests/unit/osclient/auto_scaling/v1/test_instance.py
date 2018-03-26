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

from osc_lib import exceptions

from otcextensions.tests.unit.osclient.auto_scaling.v1 import fakes

from otcextensions.osclient.auto_scaling.v1 import instance


class TestAutoScalingInstance(fakes.TestAutoScaling):

    def setUp(self):
        super(TestAutoScalingInstance, self).setUp()
        self.client = self.app.client_manager.auto_scaling


class TestListAutoScalingInstance(TestAutoScalingInstance):

    instances = fakes.FakeInstance.create_multiple(3)

    columns = ('ID', 'Name', 'scaling_group_name',
               'scaling_configuration_id', 'scaling_configuration_name',
               'lifecycle_state', 'health_status', 'create_time')

    data = []

    for s in instances:
        data.append((
            s.id,
            s.name,
            s.scaling_group_name,
            s.scaling_configuration_id,
            s.scaling_configuration_name,
            s.lifecycle_state,
            s.health_status,
            s.create_time,
        ))

    def setUp(self):
        super(TestListAutoScalingInstance, self).setUp()

        self.cmd = instance.ListAutoScalingInstance(self.app, None)

        self.client.instances = mock.Mock()

    def test_list(self):
        arglist = [
            'grp',
            '--life_cycle_state', 'lc',
            '--health_status', 'hs',
            '--limit', '12'
        ]

        verifylist = [
            ('group', 'grp'),
            ('life_cycle_state', 'lc'),
            ('health_status', 'hs'),
            ('limit', 12)
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        grp_mock = mock.Mock()
        grp_mock.id = 2

        self.client.find_group = mock.Mock(return_value=grp_mock)
        self.client.groups.side_effect = [
            self.instances
        ]

        self.client.instances.side_effect = [
            self.instances
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.instances.assert_called_once_with(
            group=grp_mock.id,
            life_cycle_state='lc',
            health_status='hs',
            limit=12)

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))


class TestDeleteAutoScalingInstance(TestAutoScalingInstance):

    def setUp(self):
        super(TestDeleteAutoScalingInstance, self).setUp()

        self.cmd = instance.RemoveAutoScalingInstance(self.app, None)

        self.client.delete_instance = mock.Mock()

    def test_remove(self):
        arglist = [
            'Instance1',
            '--delete_instance'
        ]
        verifylist = [
            ('instance', 'Instance1'),
            ('delete_instance', True)
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.remove_instance.side_effect = [{}]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.remove_instance.assert_called_once()


class TestBatchAutoScalingInstanceAction(TestAutoScalingInstance):

    def setUp(self):
        super(TestBatchAutoScalingInstanceAction, self).setUp()

        self.cmd = instance.BatchActionAutoScalingInstance(self.app, None)

        self.client.batch_instance_action = mock.Mock()

    def test_wrong_action(self):
        arglist = [
            'grp1',
            'ADD1',
            'Instance1',
            '--delete_instance',
        ]
        verifylist = [
            ('instance', ['Instance1']),
            ('delete_instance', True),
            ('action', 'ADD1')
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.assertRaises(
            exceptions.CommandError, self.cmd.take_action, parsed_args
        )

    def test_add(self):
        arglist = [
            'grp1',
            'ADD',
            'Instance1',
        ]
        verifylist = [
            ('instance', ['Instance1']),
            ('action', 'ADD')
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.batch_instance_action.side_effect = [{}]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.batch_instance_action.assert_called_with(
            action='ADD',
            delete_instance=False,
            group='grp1',
            ignore_missing=False, instance=['Instance1']
        )

    def test_remove(self):
        arglist = [
            'grp1',
            'REMOVE',
            'Instance1',
            'Instance2',
            '--delete_instance',
        ]
        verifylist = [
            ('instance', ['Instance1', 'Instance2']),
            ('delete_instance', True),
            ('action', 'REMOVE')
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.batch_instance_action.side_effect = [{}]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.batch_instance_action.assert_called_with(
            action='REMOVE',
            delete_instance=True,
            group='grp1',
            ignore_missing=False, instance=['Instance1', 'Instance2']
        )

    def test_protect(self):
        arglist = [
            'grp1',
            'protect',
            'Instance1',
            'Instance2',
        ]
        verifylist = [
            ('instance', ['Instance1', 'Instance2']),
            ('action', 'protect')
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.batch_instance_action.side_effect = [{}]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.batch_instance_action.assert_called_with(
            action='PROTECT',
            delete_instance=False,
            group='grp1',
            ignore_missing=False, instance=['Instance1', 'Instance2']
        )

    def test_unprotect(self):
        arglist = [
            'grp1',
            'unProtect',
            'Instance1',
            'Instance2',
        ]
        verifylist = [
            ('instance', ['Instance1', 'Instance2']),
            ('action', 'unProtect')
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.batch_instance_action.side_effect = [{}]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.batch_instance_action.assert_called_with(
            action='UNPROTECT',
            delete_instance=False,
            group='grp1',
            ignore_missing=False, instance=['Instance1', 'Instance2']
        )
