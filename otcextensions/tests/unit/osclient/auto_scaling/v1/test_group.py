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

from otcextensions.osclient.auto_scaling.v1 import group


class TestAutoScalingGroup(fakes.TestAutoScaling):

    def setUp(self):
        super(TestAutoScalingGroup, self).setUp()


class TestListAutoScalingGroup(TestAutoScalingGroup):

    groups = fakes.FakeGroup.create_multiple(3)

    columns = ('ID', 'Name', 'Status', 'Detail')

    data = []

    for s in groups:
        data.append((
            s.id,
            s.name,
            s.status,
            s.detail
        ))

    def setUp(self):
        super(TestListAutoScalingGroup, self).setUp()

        self.cmd = group.ListAutoScalingGroup(self.app, None)

        self.app.client_manager.auto_scaling.groups = mock.Mock()

    def test_list_default(self):
        arglist = [
        ]

        verifylist = [
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.app.client_manager.auto_scaling.groups.side_effect = [
            self.groups
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.app.client_manager.auto_scaling.groups.assert_called_once_with()
        # self.app.client_manager.obs.buckets.assert_called()

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))


class TestShowAutoScalingGroup(TestAutoScalingGroup):

    columns = ('create_time', 'detail', 'id', 'name', 'status', 'vpc_id')

    _group = fakes.FakeGroup.create_one()

    data = (
        _group.create_time,
        _group.detail,
        _group.id,
        _group.name,
        _group.status,
        _group.vpc_id,
    )

    def setUp(self):
        super(TestShowAutoScalingGroup, self).setUp()

        self.cmd = group.ShowAutoScalingGroup(self.app, None)

        self.app.client_manager.auto_scaling.find_group = mock.Mock()

    def test_show_default(self):
        arglist = [
            'test_group'
        ]
        verifylist = [
            ('group', 'test_group')
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.app.client_manager.auto_scaling.find_group.side_effect = [
            self._group
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.app.client_manager.auto_scaling.find_group.assert_called()

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestCreateAutoScalingGroup(TestAutoScalingGroup):

    def setUp(self):
        super(TestCreateAutoScalingGroup, self).setUp()

        self.cmd = group.CreateAutoScalingGroup(self.app, None)

        # self.app.client_manager.auto_scaling.find_group = mock.Mock()

    def test_show_default(self):
        arglist = [
        ]
        verifylist = [
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.assertRaises(NotImplementedError,
                          self.cmd.take_action, parsed_args)


class TestDeleteAutoScalingGroup(TestAutoScalingGroup):

    def setUp(self):
        super(TestDeleteAutoScalingGroup, self).setUp()

        self.cmd = group.DeleteAutoScalingGroup(self.app, None)

        # self.app.client_manager.auto_scaling.find_group = mock.Mock()

    def test_show_default(self):
        arglist = [
        ]
        verifylist = [
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.assertRaises(NotImplementedError,
                          self.cmd.take_action, parsed_args)


class TestUpdateAutoScalingGroup(TestAutoScalingGroup):

    def setUp(self):
        super(TestUpdateAutoScalingGroup, self).setUp()

        self.cmd = group.UpdateAutoScalingGroup(self.app, None)

        # self.app.client_manager.auto_scaling.find_group = mock.Mock()

    def test_show_default(self):
        arglist = [
        ]
        verifylist = [
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.assertRaises(NotImplementedError,
                          self.cmd.take_action, parsed_args)


class TestEnableAutoScalingGroup(TestAutoScalingGroup):

    def setUp(self):
        super(TestEnableAutoScalingGroup, self).setUp()

        self.cmd = group.EnableAutoScalingGroup(self.app, None)

        # self.app.client_manager.auto_scaling.find_group = mock.Mock()

    def test_show_default(self):
        arglist = [
        ]
        verifylist = [
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.assertRaises(NotImplementedError,
                          self.cmd.take_action, parsed_args)


class TestDisableAutoScalingGroup(TestAutoScalingGroup):

    def setUp(self):
        super(TestDisableAutoScalingGroup, self).setUp()

        self.cmd = group.DisableAutoScalingGroup(self.app, None)

        # self.app.client_manager.auto_scaling.find_group = mock.Mock()

    def test_show_default(self):
        arglist = [
        ]
        verifylist = [
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.assertRaises(NotImplementedError,
                          self.cmd.take_action, parsed_args)
