# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
import mock

from otcextensions.osclient.css.v1 import flavor
from otcextensions.tests.unit.osclient.css.v1 import fakes


class TestListFlavors(fakes.TestCss):

    objects = fakes.FakeFlavor.create_multiple(3)

    column_list_headers = (
        'Id',
        'Name',
        'Version',
        'Type',
        'Availability Zones',
        'Disk Range',
        'vCPUs',
        'RAM',
    )

    columns = (
        'id',
        'name',
        'version',
        'type',
        'availability_zones',
        'disk_range',
        'vcpus',
        'ram'
    )

    data = []

    for s in objects:
        data.append(
            (
                s.id,
                s.name,
                s.version,
                s.type,
                s.availability_zones,
                s.disk_range,
                s.vcpus,
                s.ram,
            )
        )

    def setUp(self):
        super(TestListFlavors, self).setUp()

        self.cmd = flavor.ListFlavors(self.app, None)

        self.client.flavors = mock.Mock()
        self.client.api_mock = self.client.flavors

    def test_list(self):
        arglist = []

        verifylist = []

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with()

        self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(self.data, list(data))

    def test_list_args(self):
        arglist = [
            '--datastore-version', '7.6.2',
            '--node-type', 'ess',
        ]

        verifylist = [
            ('datastore_version', '7.6.2'),
            ('node_type', 'ess'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with()

        self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(self.data, list(data))
