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
import argparse

import mock

from otcextensions.osclient.auto_scaling.v1 import config
from otcextensions.tests.unit.osclient.auto_scaling.v1 import fakes


class TestAutoScalingConfig(fakes.TestAutoScaling):

    def setUp(self):
        super(TestAutoScalingConfig, self).setUp()
        self.client = self.app.client_manager.auto_scaling


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

        self.client.configs = mock.Mock()

    def test_list_default(self):
        arglist = [
        ]

        verifylist = [
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.configs.side_effect = [
            self.configs
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.configs.assert_called_once_with()

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))


class TestShowAutoScalingConfig(TestAutoScalingConfig):

    columns = ['ID', 'Name', 'instance_id', 'instance_name',
               'flavor_id', 'image_id', 'disk',
               'key_name', 'public_ip', 'user_data', 'metadata'
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
        _config.instance_config.user_data,
        _config.instance_config.metadata,
        # format_columns.DictColumn(_config.instance_config).human_readable(),
    )

    def setUp(self):
        super(TestShowAutoScalingConfig, self).setUp()

        self.cmd = config.ShowAutoScalingConfig(self.app, None)

        self.client.find_config = mock.Mock()

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
        self.client.find_config.side_effect = [
            self._config
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_config.assert_called()

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestCreateAutoScalingGroup(TestAutoScalingConfig):

    columns = ['ID', 'Name', 'instance_id', 'instance_name',
               'flavor_id', 'image_id', 'disk',
               'key_name', 'public_ip', 'user_data', 'metadata'
               ]

    _config = fakes.FakeConfig.create_one()

    data = (
        _config.id,
        _config.name,
        _config.instance_config.instance_id,
        _config.instance_config.instance_name,
        _config.instance_config.flavor_id,
        _config.instance_config.image_id,
        _config.instance_config.disk,
        _config.instance_config.key_name,
        _config.instance_config.public_ip,
        _config.instance_config.user_data,
        _config.instance_config.metadata,
    )

    def setUp(self):
        super(TestCreateAutoScalingGroup, self).setUp()

        self.cmd = config.CreateAutoScalingConfig(self.app, None)

        self.client.create_config = mock.Mock()

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

        self.client.create_config.side_effect = [
            self._config
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_config.assert_called()

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestDeleteAutoScalingConfig(TestAutoScalingConfig):

    def setUp(self):
        super(TestDeleteAutoScalingConfig, self).setUp()

        self.cmd = config.DeleteAutoScalingConfig(self.app, None)

        self.client.delete_config = mock.Mock()
        self.client.batch_delete_configs = mock.Mock()

    def test_delete_single(self):
        arglist = [
            'config_id'
        ]
        verifylist = [
            ('config', ['config_id'])
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.client.delete_config.side_effect = [{}]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.delete_config.assert_called_with(
            'config_id',
            ignore_missing=False)

    def test_delete_multiple(self):
        arglist = [
            'config_id1',
            'config_id2'
        ]
        verifylist = [
            ('config', ['config_id1', 'config_id2'])
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.client.batch_delete_configs.side_effect = [{}]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.delete_config.assert_not_called()
        self.client.batch_delete_configs.assert_called_with(
            ['config_id1', 'config_id2'])
