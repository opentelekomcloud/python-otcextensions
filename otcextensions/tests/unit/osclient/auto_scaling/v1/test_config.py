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

import argparse
import mock
# from osc_lib import utils as common_utils
from osc_lib.cli import format_columns

from otcextensions.tests.unit.osclient.auto_scaling.v1 import fakes

from otcextensions.osclient.auto_scaling.v1 import config


class TestAutoScalingConfig(fakes.TestAutoScaling):

    def setUp(self):
        super(TestAutoScalingConfig, self).setUp()


class TestListAutoScalingConfig(TestAutoScalingConfig):

    configs = fakes.FakeConfig.create_multiple(3)

    columns = ('ID', 'Name')

    data = []

    for s in configs:
        data.append((
            s.id,
            s.name,
        ))

    def setUp(self):
        super(TestListAutoScalingConfig, self).setUp()

        self.cmd = config.ListAutoScalingConfig(self.app, None)

        self.app.client_manager.auto_scaling.configs = mock.Mock()

    def test_list_default(self):
        arglist = [
        ]

        verifylist = [
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.app.client_manager.auto_scaling.configs.side_effect = [
            self.configs
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.app.client_manager.auto_scaling.configs.assert_called_once_with()
        # self.app.client_manager.obs.buckets.assert_called()

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))


class TestShowAutoScalingConfig(TestAutoScalingConfig):

    columns = ['ID', 'Name', 'Instance ID', 'Instance Name',
               'Flavor ID', 'Image ID', 'Disk',
               'Key Name', 'Public IP'
               ]

    _config = fakes.FakeConfig.create_one()

    data = (
        # _config.create_time,
        _config.id,
        _config.name,
        _config.instance_config.instance_id,
        _config.instance_config.instance_name,
        _config.instance_config.flavor_id,
        _config.instance_config.image_id,
        _config.instance_config.disk,
        _config.instance_config.key_name,
        _config.instance_config.public_ip,
        # format_columns.DictColumn(_config.instance_config).human_readable(),
    )

    def setUp(self):
        super(TestShowAutoScalingConfig, self).setUp()

        self.cmd = config.ShowAutoScalingConfig(self.app, None)

        self.app.client_manager.auto_scaling.find_config = mock.Mock()

    def test_show_default(self):
        arglist = [
            'test_config'
        ]
        verifylist = [
            ('config', 'test_config')
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.app.client_manager.auto_scaling.find_config.side_effect = [
            self._config
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.app.client_manager.auto_scaling.find_config.assert_called()

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestCreateAutoScalingGroup(TestAutoScalingConfig):

    columns = ['ID', 'Name', 'Instance ID', 'Instance Name',
               'Flavor ID', 'Image ID', 'Disk',
               'Key Name', 'Public IP'
               ]

    _config = fakes.FakeConfig.create_one()

    data = (
        # _config.create_time,
        _config.id,
        _config.name,
        _config.instance_config.instance_id,
        _config.instance_config.instance_name,
        _config.instance_config.flavor_id,
        _config.instance_config.image_id,
        _config.instance_config.disk,
        _config.instance_config.key_name,
        _config.instance_config.public_ip,
        # format_columns.DictColumn(_config.instance_config).human_readable(),
    )

    def setUp(self):
        super(TestCreateAutoScalingGroup, self).setUp()

        self.cmd = config.CreateAutoScalingConfig(self.app, None)

        self.app.client_manager.auto_scaling.create_config = mock.Mock()

    def test_create_no_details(self):
        arglist = [
            'config_name',
        ]
        verifylist = [
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.assertRaises(argparse.ArgumentTypeError,
                          self.cmd.take_action, parsed_args)

    def test_create_ok(self):
        arglist = [
            'config_name',
            '--flavor', 'some_flavor',
            '--image_id', 'some_image',
            '--disk', 'SYS,SSD,10',
            '--disk', 'DATA,SSD,5',
        ]
        verifylist = [
            ('name', 'config_name'),
            ('flavor', 'some_flavor'),
            ('image_id', 'some_image'),
            ('disk', ['SYS,SSD,10', 'DATA,SSD,5']),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.app.client_manager.auto_scaling.create_config.side_effect = [
            self._config
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.app.client_manager.auto_scaling.create_config.assert_called()

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestDeleteAutoScalingConfig(TestAutoScalingConfig):

    def setUp(self):
        super(TestDeleteAutoScalingConfig, self).setUp()

        self.cmd = config.DeleteAutoScalingConfig(self.app, None)

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
