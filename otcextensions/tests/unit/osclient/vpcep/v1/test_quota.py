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

from otcextensions.osclient.vpcep.v1 import quota
from otcextensions.tests.unit.osclient.vpcep.v1 import fakes


class TestListQuota(fakes.TestVpcep):

    objects = fakes.FakeQuota.create_multiple(2)
    column_list_headers = ('Type', 'Quota', 'Used')

    data = []

    for s in objects:
        data.append((s.type, s.quota, s.used))

    def setUp(self):
        super(TestListQuota, self).setUp()

        self.cmd = quota.ListQuota(self.app, None)

        self.client.resource_quota = mock.Mock()
        self.client.api_mock = self.client.resource_quota

    def test_list(self):
        arglist = []

        verifylist = []

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(None)

        self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(self.data, list(data))

    def test_list_args(self):
        arglist = ['--type', 'endpoint']

        verifylist = [
            ('type', 'endpoint'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with('endpoint')
