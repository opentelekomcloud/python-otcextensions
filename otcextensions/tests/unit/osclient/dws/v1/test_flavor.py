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

from otcextensions.osclient.dws.v1 import flavor
from otcextensions.tests.unit.osclient.dws.v1 import fakes


class TestListFlavors(fakes.TestDws):

    objects = fakes.FakeFlavor.create_multiple(3)

    column_list_headers = ('ID', 'Name', 'Availability Zones', 'vCPU',
                           'RAM', 'Disk Size', 'Disk Type',)

    columns = ('id', 'name', 'availability_zones', 'vcpu',
               'ram', 'disk_size', 'disk_type',)

    data = []

    for s in objects:
        data.append((s.id, s.name, s.availability_zones, s.vcpu,
                     s.ram, s.disk_size, s.disk_type))

    def setUp(self):
        super(TestListFlavors, self).setUp()

        self.cmd = flavor.ListFlavors(self.app, None)

        self.client.snapshots = mock.Mock()
        self.client.api_mock = self.client.flavors

    def test_list(self):
        arglist = [
        ]
        verifylist = [
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
