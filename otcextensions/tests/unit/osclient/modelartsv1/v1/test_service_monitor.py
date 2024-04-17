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

from otcextensions.osclient.modelartsv1.v1 import service_monitor
from otcextensions.tests.unit.osclient.modelartsv1.v1 import fakes


class TestServiceMonitor(fakes.TestModelartsv1):
    _service = fakes.FakeService.create_one()
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
        super(TestServiceMonitor, self).setUp()

        self.cmd = service_monitor.ServiceMonitor(self.app, None)

        self.client.find_service = mock.Mock(return_value=self._service)
        self.client.service_monitor = mock.Mock()
        self.client.api_mock = self.client.service_monitor

    def test_list(self):
        arglist = [self._service.name]

        verifylist = [
            ("service", self._service.name),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_service.assert_called_with(
            self._service.name, ignore_missing=False
        )
        self.client.api_mock.assert_called_with(self._service.id)

        self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(self.data, list(data))

    def test_list_args(self):
        arglist = [
            self._service.name,
            "--node-id",
            "123",
        ]

        verifylist = [
            ("service", self._service.name),
            ("node_id", "123"),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(
            self._service.id,
            node_id="123",
        )
