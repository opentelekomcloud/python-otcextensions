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

from otcextensions.osclient.rds.v1 import flavor
from otcextensions.tests.unit.osclient.rds.v1 import fakes as rds_fakes


class TestListDatabaseFlavors(rds_fakes.TestRds):

    column_list_headers = [
        'ID',
        'Name',
        'ram',
        'spec_code'
        # 'Str_ID',
        # 'vCPUs'
    ]

    def setUp(self):
        super(TestListDatabaseFlavors, self).setUp()

        self.cmd = flavor.ListDatabaseFlavors(self.app, None)

        self.app.client_manager.rds.flavors = mock.Mock()

        self.flavors = self.flavor_mock.create_multiple(3)
        self.flavor_data = []
        for s in self.flavors:
            self.flavor_data.append((
                s.id,
                s.name,
                s.ram,
                s.spec_code
            ))

    def test_list_flavors(self):
        arglist = [
            'dbId',
            'regio'
        ]

        verifylist = [
            ('dbId', 'dbId'),
            ('region', 'regio')
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

    def test_list_flavors_default_region(self):
        arglist = [
            'dbId',
        ]

        verifylist = [
            ('dbId', 'dbId'),
            ('region', 'eu-de')
        ]

        # Verify cm is triggereg with default parameters
        self.check_parser(self.cmd, arglist, verifylist)


class TestShowDatabaseFlavors(rds_fakes.TestRds):

    columns = ('ID', 'Name', 'ram', 'spec_code')

    def setUp(self):
        super(TestShowDatabaseFlavors, self).setUp()

        self.cmd = flavor.ShowDatabaseFlavor(self.app, None)

        self.app.client_manager.rds.get_flavor = mock.Mock()

        self.flavor = self.flavor_mock.create_one()

        self.flavor_data = (
            self.flavor.id,
            self.flavor.name,
            self.flavor.ram,
            self.flavor.spec_code
        )

    def test_show_flavor(self):
        arglist = [
            'test_flavor',
        ]

        verifylist = [
            ('flavor', 'test_flavor'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.app.client_manager.rds.get_flavor.side_effect = [
            self.flavor
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.app.client_manager.rds.get_flavor.assert_called()

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.flavor_data, data)
