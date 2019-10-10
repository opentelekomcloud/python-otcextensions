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
import mock

from otcextensions.osclient.rds.v3 import flavor
from otcextensions.tests.unit.osclient.rds.v3 import fakes


class TestListDatabaseFlavors(fakes.TestRds):

    objects = fakes.FakeFlavor.create_multiple(3)

    columns = (
        'name', 'instance_mode', 'vcpus', 'ram',
    )

    data = []

    for s in objects:
        data.append(fakes.gen_data(s, columns))

    def setUp(self):
        super(TestListDatabaseFlavors, self).setUp()

        self.cmd = flavor.ListDatabaseFlavors(self.app, None)

        self.client.flavors = mock.Mock(return_value=self.objects)

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

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.flavors.assert_called_with(
            datastore_name='mysql',
            version_name='5.7'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))
