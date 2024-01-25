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
from otcextensions.osclient.modelartsv1.v1 import service
from otcextensions.tests.unit.osclient.modelartsv1.v1 import fakes


class TestMonitors(fakes.TestModelartsv1):
    objects = fakes.FakeServiceMonitor.create_multiple(3)

    column_list_headers = (
        "Model Id",
        "Model Name",
        "Model Version",
        "Invocation Times",
        "Failed Times",
        "CPU Core",
        "CPU Memory",
        "GPU",
    )

    data = []

    for s in objects:
        data.append(
            (
                s.model_id,
                s.model_name,
                s.model_version,
                s.invocation_times,
                s.failed_times,
                s.cpu_core,
                s.cpu_memory,
                s.gpu,
            )
        )

    def setUp(self):
        super(TestMonitors, self).setUp()

        self.cmd = service.Monitors(self.app, None)

        self.client.service_monitors = mock.Mock()
        self.client.api_mock = self.client.service_monitors

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
            "--node-id",
            "123",
        ]

        verifylist = [
            ("serviceId", "service-id"),
            ("node_id", "123"),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(
            "service-id",
            node_id="123",
        )
