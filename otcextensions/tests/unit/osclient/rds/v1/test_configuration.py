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

from otcextensions.osclient.rds.v1 import configuration
from otcextensions.tests.unit.osclient.rds.v1 import fakes as rds_fakes


class TestRdsListConfigurations(rds_fakes.TestRds):

    column_list_headers = [
        'ID',
        'Name',
        'Description',
        'Datastore Name',
        'Datastore Version Name',
        # 'Str_ID',
        # 'Values'
    ]

    def setUp(self):
        super(TestRdsListConfigurations, self).setUp()

        self.cmd = configuration.ListConfigurations(self.app, None)

        self.app.client_manager.rds.configurations = mock.Mock()

        self.configurations = self.configuration_mock.create_multiple(3)
        self.configuration_data = []
        for s in self.configurations:
            self.configuration_data.append((
                s.id,
                s.name,
                s.description,
                s.datastore_name,
                s.datastore_version_name,
                # s.flavor_detail,
            ))

    def test_list(self):
        arglist = [
        ]

        verifylist = [
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.app.client_manager.rds.configurations.side_effect = [
            self.configurations
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.app.client_manager.rds.configurations.assert_called()

        self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(tuple(self.configuration_data), tuple(data))


class TestRdsShowConfiguration(rds_fakes.TestRds):

    columns = [
        'ID',
        'Name',
        'Description',
        'Datastore Name',
        'Datastore Version Name',
        'Values',
    ]

    def setUp(self):
        super(TestRdsShowConfiguration, self).setUp()

        self.cmd = configuration.ShowConfiguration(self.app, None)

        self.app.client_manager.rds.get_configuration = mock.Mock()
        self.app.client_manager.rds.find_configuration = mock.Mock()

        self.config = self.configuration_mock.create_one()

        self.config_data = (
            self.config.id,
            self.config.name,
            self.config.description,
            self.config.datastore_name,
            self.config.datastore_version_name,
            self.config.values
        )

    def test_show(self):
        arglist = [
            'test_obj',
        ]

        verifylist = [
            ('configuration_group', 'test_obj'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.app.client_manager.rds.find_configuration.side_effect = [
            self.config
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.app.client_manager.rds.find_configuration.assert_called()

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.config_data, data)
