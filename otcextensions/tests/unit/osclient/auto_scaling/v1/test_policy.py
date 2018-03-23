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
# from osc_lib import utils as common_utils

from otcextensions.tests.unit.osclient.auto_scaling.v1 import fakes

from otcextensions.osclient.auto_scaling.v1 import policy


class TestAutoScalingPolicy(fakes.TestAutoScaling):

    def setUp(self):
        super(TestAutoScalingPolicy, self).setUp()
        self.client = self.app.client_manager.auto_scaling


class TestListAutoScalingPolicy(TestAutoScalingPolicy):

    policies = fakes.FakePolicy.create_multiple(3)

    columns = ['ID', 'Name']

    data = []

    for s in policies:
        data.append((
            s.id,
            s.name,
            # s.scaling_group_id,
            # s.status,
            # s.type,
            # s.alarm_id,
            # s.scheduled_policy,
            # s.scaling_policy_action,
            # s.cool_down_time,
        ))

    def setUp(self):
        super(TestListAutoScalingPolicy, self).setUp()

        self.cmd = policy.ListAutoScalingPolicy(self.app, None)

        self.client.groups = mock.Mock()

    # def test_list_default(self):
    #     arglist = [
    #     ]
    #
    #     verifylist = [
    #     ]
    #     # Verify cm is triggereg with default parameters
    #     parsed_args = self.check_parser(self.cmd, arglist, verifylist)
    #
    #     # Set the response
    #     self.client.groups.side_effect = [
    #         self.policies
    #     ]
    #
    #     self.assertRaises(argparse.ArgumentTypeError,
    #                       self.cmd.take_action, parsed_args)

    def test_list(self):
        arglist = [
            '--group', 'grp',
        ]

        verifylist = [
            ('group', 'grp')
        ]

        # Set the response
        self.client.groups.side_effect = [
            self.policies
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        grp_mock = mock.Mock()
        grp_mock.id = 2

        self.client.find_group = mock.Mock(return_value=grp_mock)
        # Set the response
        self.client.policies.side_effect = [
            self.policies
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.policies.assert_called_once_with(group=grp_mock.id)
        # self.app.client_manager.obs.buckets.assert_called()

        self.assertEqual(self.columns, list(columns))
        self.assertEqual(self.data, list(data))


class TestShowAutoScalingPolicy(TestAutoScalingPolicy):

    _policy = fakes.FakePolicy.create_one()

    columns = ['ID', 'Name', 'scaling_group_id', 'status',
           'type', 'alarm_id', 'scheduled_policy',
           'scaling_policy_action', 'cool_down_time'
          ]

    data = (
            _policy.id,
            _policy.name,
            _policy.scaling_group_id,
            _policy.status,
            _policy.type,
            _policy.alarm_id,
            _policy.scheduled_policy,
            _policy.scaling_policy_action,
            _policy.cool_down_time,
        )

    def setUp(self):
        super(TestShowAutoScalingPolicy, self).setUp()

        self.cmd = policy.ShowAutoScalingPolicy(self.app, None)

        self.client.find_group = mock.Mock()

    def test_show_default(self):
        arglist = [
            'test_policy'
        ]
        verifylist = [
            ('policy', 'test_policy')
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.get_policy.side_effect = [
            self._policy
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.get_policy.assert_called()

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestCreateAutoScalingPolicy(TestAutoScalingPolicy):

    columns = ['ID', 'Name', 'scaling_group_id', 'status',
               'type', 'alarm_id', 'scheduled_policy',
               'scaling_policy_action', 'cool_down_time'
               ]

    _obj = fakes.FakePolicy.create_one()

    data = (
        _obj.id,
        _obj.name,
        _obj.scaling_group_id,
        _obj.status,
        _obj.type,
        _obj.alarm_id,
        _obj.scheduled_policy,
        _obj.scaling_policy_action,
        _obj.cool_down_time,
    )

    def setUp(self):
        super(TestCreateAutoScalingPolicy, self).setUp()

        self.cmd = policy.CreateAutoScalingPolicy(self.app, None)

        self.client.create_policy = mock.Mock()

    def test_create(self):
        arglist = [
            '--group', 'group1',
            '--type', 'ALARM',
            '--cool_down_time', '1',
            '--alarm_id', 'alarm1',
            '--action_operation', 'ADD',
            '--action_instance_number', '7',
            '--launch_time', 'launch_time1',
            '--recurrence_type', 'recurrence_type1',
            '--recurrence_value', 'recurrence_value1',
            '--start_time', 'st1',
            '--end_time', 'et1',

            'test_name'
        ]
        verifylist = [
            ('group', 'group1'),
            ('cool_down_time', 1),
            ('type', 'ALARM'),
            ('alarm_id', 'alarm1'),
            ('action_operation', 'ADD'),
            ('action_instance_number', 7),
            ('launch_time', 'launch_time1'),
            ('recurrence_type', 'recurrence_type1'),
            ('recurrence_value', 'recurrence_value1'),
            ('start_time', 'st1'),
            ('end_time', 'et1'),
            ('name', 'test_name')
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.create_policy.side_effect = [
            self._obj
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_policy.assert_called_with(
            alarm_id='alarm1',
            cool_down_time=1,
            name='test_name',
            scaling_group_id='group1',
            scaling_policy_action={'operation': 'ADD', 'instance_number': 7},
            scheduled_policy={
                'launch_time': 'launch_time1',
                'recurrence_type': 'recurrence_type1',
                'recurrence_value': 'recurrence_value1',
                'start_time': 'st1',
                'end_time': 'et1'
            },
            type='ALARM'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestDeleteAutoScalingPolicy(TestAutoScalingPolicy):

    def setUp(self):
        super(TestDeleteAutoScalingPolicy, self).setUp()

        self.cmd = policy.DeleteAutoScalingPolicy(self.app, None)

        self.client.delete_policy = mock.Mock()

    def test_delete(self):
        arglist = [
            'policy1',
            'policy2',
        ]
        verifylist = [
            ('policy', ['policy1', 'policy2'])
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.delete_policy.side_effect = [ {}, {} ]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        calls = [mock.call('policy1'), mock.call('policy2')]

        self.client.delete_policy.assert_has_calls(calls)
        self.assertEquals(2, self.client.delete_policy.call_count)
#
#
# class TestUpdateAutoScalingPolicy(TestAutoScalingPolicy):
#
#     def setUp(self):
#         super(TestUpdateAutoScalingPolicy, self).setUp()
#
#         self.cmd = group.UpdateAutoScalingPolicy(self.app, None)
#
#         # self.client.find_group = mock.Mock()
#
#     def test_show_default(self):
#         arglist = [
#         ]
#         verifylist = [
#         ]
#         # Verify cm is triggereg with default parameters
#         parsed_args = self.check_parser(self.cmd, arglist, verifylist)
#
#         self.assertRaises(NotImplementedError,
#                           self.cmd.take_action, parsed_args)
#
#
# class TestEnableAutoScalingPolicy(TestAutoScalingPolicy):
#
#     _group = fakes.FakePolicy.create_one()
#
#     def setUp(self):
#         super(TestEnableAutoScalingPolicy, self).setUp()
#
#         self.cmd = group.EnableAutoScalingPolicy(self.app, None)
#
#         self.client.find_group = mock.Mock()
#         self.client.resume_group = mock.Mock()
#
#     def test_enable(self):
#         arglist = [
#             'group1'
#         ]
#         verifylist = [
#             ('group', 'group1')
#         ]
#         # Verify cm is triggereg with default parameters
#         parsed_args = self.check_parser(self.cmd, arglist, verifylist)
#
#         # Set the response
#         self.client.find_group.side_effect = [
#             self._group
#         ]
#         self.client.resume_group.side_effect = [ {} ]
#
#         # Trigger the action
#         self.cmd.take_action(parsed_args)
#
#         self.client.find_group.assert_called()
#         self.client.resume_group.assert_called()
#
#
# class TestDisableAutoScalingPolicy(TestAutoScalingPolicy):
#
#     _group = fakes.FakePolicy.create_one()
#
#     def setUp(self):
#         super(TestDisableAutoScalingPolicy, self).setUp()
#
#         self.cmd = group.DisableAutoScalingPolicy(self.app, None)
#
#         self.client.find_group = mock.Mock()
#         self.client.pause_group = mock.Mock()
#
#     def test_disable(self):
#         arglist = [
#             'group1'
#         ]
#         verifylist = [
#             ('group', 'group1')
#         ]
#         # Verify cm is triggereg with default parameters
#         parsed_args = self.check_parser(self.cmd, arglist, verifylist)
#
#         # Set the response
#         self.client.find_group.side_effect = [
#             self._group
#         ]
#         self.client.pause_group.side_effect = [ {} ]
#
#         # Trigger the action
#         self.cmd.take_action(parsed_args)
#
#         self.client.find_group.assert_called()
#         self.client.pause_group.assert_called()
