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
import mock

from otcextensions.common import sdk_utils
from otcextensions.osclient.anti_ddos.v1 import config
from otcextensions.tests.unit.osclient.anti_ddos.v1 import fakes


class TestListConfig(fakes.TestAntiDDoS):

    objects = fakes.FakeConfig.create_multiple(3)

    columns = (
        'traffic_limited_list', 'http_limited_list', 'connection_limited_list'
    )

    data = []

    for s in objects:
        data.append((
            sdk_utils.ListOfDictColumn(s.traffic_limited_list),
            sdk_utils.ListOfDictColumn(s.http_limited_list),
            sdk_utils.ListOfDictColumn(s.connection_limited_list),
        ))

    def setUp(self):
        super(TestListConfig, self).setUp()

        self.cmd = config.ListConfig(self.app, None)

        self.client.configs = mock.Mock()

    def test_list(self):
        arglist = [
        ]

        verifylist = [
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.configs.side_effect = [
            self.objects
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.configs.assert_called_once_with(
        )

        self.assertEqual(self.columns, columns)
        self.assertListItemEqual(self.data, list(data))
