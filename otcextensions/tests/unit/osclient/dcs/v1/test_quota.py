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

from otcextensions.osclient.dcs.v1 import quota
from otcextensions.tests.unit.osclient.dcs.v1 import fakes


class TestDCSQuota(fakes.TestDCS):

    def setUp(self):
        super(TestDCSQuota, self).setUp()
        self.client = self.app.client_manager.dcs


class TestListDCSQuota(TestDCSQuota):
    quotas = fakes.FakeQuota.create_multiple(2)
    columns = ('quota', 'used', 'type', 'min', 'max', 'unit')

    data = []

    for s in quotas:
        data.append((
            s.quota,
            s.used,
            s.type,
            s.min,
            s.max,
            s.unit
        ))

    def setUp(self):
        super(TestListDCSQuota, self).setUp()
        self.cmd = quota.ListDCSQuota(self.app, None)
        self.client.quotas = mock.Mock()

    def test_list_quota(self):
        arglist = [
        ]

        verifylist = [
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
