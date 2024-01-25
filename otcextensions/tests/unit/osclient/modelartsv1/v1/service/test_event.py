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


class TestEvents(fakes.TestModelartsv1):
    objects = fakes.FakeServiceEvent.create_multiple(3)

    column_list_headers = (
        "Occur Time",
        "Event Type",
        "Event Info",
    )

    data = []

    for s in objects:
        data.append(
            (
                cli_utils.UnixTimestampFormatter(s.occur_time),
                s.event_type,
                s.event_info,
            )
        )

    def setUp(self):
        super(TestEvents, self).setUp()

        self.cmd = service.Events(self.app, None)

        self.client.service_events = mock.Mock()
        self.client.api_mock = self.client.service_events

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
            "--event-type",
            "normal",
            "--limit",
            "10",
            "--offset",
            "2",
            "--order",
            "asc",
            "--sort-by",
            "occur_time",
            "--start-time",
            "123",
            "--end-time",
            "567",
        ]

        verifylist = [
            ("serviceId", "service-id"),
            ("event_type", "normal"),
            ("limit", 10),
            ("offset", 2),
            ("order", "asc"),
            ("sort_by", "occur_time"),
            ("start_time", 123),
            ("end_time", 567),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(
            "service-id",
            end_time=567,
            event_type="normal",
            limit=10,
            offset=2,
            order="asc",
            sort_by="occur_time",
            start_time=123,
        )
