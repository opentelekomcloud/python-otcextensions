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

from otcextensions.osclient.dms.v1 import quota
from otcextensions.tests.unit.osclient.dms.v1 import fakes


class TestDMSQuota(fakes.TestDMS):

    def setUp(self):
        super(TestDMSQuota, self).setUp()
        self.client = self.app.client_manager.dms


class TestListDMSQuota(TestDMSQuota):

    objects = fakes.FakeQuota.create_multiple(3)

    columns = ('type', 'quota', 'used', 'min', 'max')

    data = []

    for s in objects:
        data.append((
            s.type,
            s.quota,
            s.used,
            s.min,
            s.max,
        ))

    def setUp(self):
        super(TestListDMSQuota, self).setUp()

        self.cmd = quota.ListQuota(self.app, None)

        self.client.quotas = mock.Mock()

    def test_list_queue(self):
        arglist = [
        ]

        verifylist = [
            # ('group', None),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.quotas.side_effect = [
            self.objects
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.quotas.assert_called_once_with()

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))
