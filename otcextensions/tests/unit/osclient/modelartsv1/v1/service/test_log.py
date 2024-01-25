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
from otcextensions.common import cli_utils
from otcextensions.osclient.modelartsv1.v1 import service
from otcextensions.tests.unit.osclient.modelartsv1.v1 import fakes


class TestLogs(fakes.TestModelartsv1):
    objects = fakes.FakeServiceLog.create_multiple(3)

    column_list_headers = (
        "Update Time",
        "Result",
        "Config",
        "Result Detail",
    )

    data = []

    for s in objects:
        data.append(
            (
                cli_utils.UnixTimestampFormatter(s.update_time),
                s.result,
                cli_utils.YamlFormat(s.config),
                s.result_detail,
            )
        )

    def setUp(self):
        super(TestLogs, self).setUp()

        self.cmd = service.Logs(self.app, None)

        self.client.service_logs = mock.Mock()
        self.client.api_mock = self.client.service_logs

    def test_list(self):
        arglist = ["service-id"]

        verifylist = [
            ("serviceId", "service-id"),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with("service-id")

        self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(self.data, list(data))

    def test_list_args(self):
        arglist = [
            "service-id",
            "--update-time",
            "123",
        ]

        verifylist = [
            ("serviceId", "service-id"),
            ("update_time", 123),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(
            "service-id",
            update_time=123,
        )
