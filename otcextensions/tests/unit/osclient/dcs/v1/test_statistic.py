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
import mock

from openstackclient.tests.unit import utils

from otcextensions.osclient.dcs.v1 import statistic
from otcextensions.tests.unit.osclient.dcs.v1 import fakes


class TestListStatistic(fakes.TestDCS):

    objects = fakes.FakeStatistic.create_multiple(3)

    columns = ('instance_id', 'max_memory', 'used_memory',
               'cmd_get_count', 'cmd_set_count', 'used_cpu',
               'input_kbps', 'output_kbps')

    data = []

    for s in objects:
        data.append((
            s.instance_id,
            s.max_memory,
            s.used_memory,
            s.cmd_get_count,
            s.cmd_set_count,
            s.used_cpu,
            s.input_kbps,
            s.output_kbps
        ))

    def setUp(self):
        super(TestListStatistic, self).setUp()

        self.cmd = statistic.ListStatistic(self.app, None)

        self.client.statistics = mock.Mock()

    def test_list(self):
        arglist = [
        ]

        verifylist = [
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.statistics.side_effect = [
            self.objects
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.statistics.assert_called_once_with(
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))
