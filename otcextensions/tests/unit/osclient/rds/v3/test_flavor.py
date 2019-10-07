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

from otcextensions.osclient.rds.v3 import flavor
from otcextensions.tests.unit.osclient.rds.v3 import fakes as rds_fakes


class TestListDatabaseFlavors(rds_fakes.TestRds):

    column_list_headers = [
        'name',
        'instance_mode',
        'vcpus',
        'ram',
    ]

    def setUp(self):
        super(TestListDatabaseFlavors, self).setUp()

        self.cmd = flavor.ListDatabaseFlavors(self.app, None)

        self.app.client_manager.rds.flavors = mock.Mock()

        self.flavors = self.flavor_mock.create_multiple(3)
        self.flavor_data = []
        for s in self.flavors:
            self.flavor_data.append((
                s.name,
                s.instance_mode,
                s.vcpus,
                s.ram
            ))

    def test_list_flavors(self):
        arglist = [
            'MySQL',
            '5.7'
        ]

        verifylist = [
            ('database', 'mysql'),
            ('version', '5.7')
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.app.client_manager.rds.flavors.side_effect = [
            self.flavors
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.app.client_manager.rds.flavors.assert_called()

        self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(tuple(self.flavor_data), tuple(data))
