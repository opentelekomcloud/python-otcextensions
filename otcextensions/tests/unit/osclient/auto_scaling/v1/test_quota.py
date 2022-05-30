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

from otcextensions.osclient.auto_scaling.v1 import quota
from otcextensions.tests.unit.osclient.auto_scaling.v1 import fakes


class TestAutoScalingQuota(fakes.TestAutoScaling):

    def setUp(self):
        super(TestAutoScalingQuota, self).setUp()
        self.client = self.app.client_manager.auto_scaling


class TestListAutoScalingQuota(TestAutoScalingQuota):

    quotas = fakes.FakeQuota.create_multiple(3)

    columns = ('type', 'used', 'quota', 'max')

    data = []

    for s in quotas:
        data.append((
            s.type,
            s.used,
            s.quota,
            s.max
        ))

    def setUp(self):
        super(TestListAutoScalingQuota, self).setUp()

        self.cmd = quota.ListAutoScalingQuota(self.app, None)

        self.client.quotas = mock.Mock()

    def test_list_quota(self):
        arglist = [
        ]

        verifylist = [
            ('group', None),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.quotas.side_effect = [
            self.quotas
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.quotas.assert_called_once_with()

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))

    def test_list_group_quota(self):
        arglist = [
            '--group', 'grp',
        ]

        verifylist = [
            ('group', 'grp'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.quotas.side_effect = [
            self.quotas
        ]

        grp_mock = mock.Mock()
        grp_mock.id = 2

        self.client.find_group = mock.Mock(return_value=grp_mock)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.quotas.assert_called_once_with(group=2)

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))
