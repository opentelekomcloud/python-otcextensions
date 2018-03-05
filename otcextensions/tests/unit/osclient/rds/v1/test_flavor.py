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

from otcextensions.osclient.rds.v1 import flavor
from otcextensions.tests.unit.osclient.rds.v1 import fakes as rds_fakes


class TestRdsListFlavors(rds_fakes.TestRds):

    column_list_headers = (
        'Name',
        'Ram',
        'ID',
        # 'Str_ID',
        'Flavor details'
    )

    def setUp(self):
        super(TestRdsListFlavors, self).setUp()

        self.cmd = flavor.ListFlavor(self.app, None)

        self.app.client_manager.rds.flavors = mock.Mock()

        self.flavors = self.flavor_mock.create_flavors(3)
        self.flavor_data = []
        for s in self.flavors:
            self.flavor_data.append((
                s.name,
                s.ram,
                s.id,
                s.flavor_detail,
            ))

    def test_list_flavors(self):
        arglist = [
        ]

        verifylist = [
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


class TestRdsShowFlavors(rds_fakes.TestRds):

    columns = (
        'name',
        'ram',
        'str_id',
        'flavor_detail',
        'price_detail'
    )

    def setUp(self):
        super(TestRdsShowFlavors, self).setUp()

        self.cmd = flavor.ShowFlavor(self.app, None)

        self.app.client_manager.rds.get_flavor = mock.Mock()

        self.flavor = self.flavor_mock.create_one_flavor()

        self.flavor_data = (
            self.flavor.name,
            self.flavor.ram,
            self.flavor.str_id,
            # s.flavor,
            self.flavor.flavor_detail,
            self.flavor.price_detail
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
