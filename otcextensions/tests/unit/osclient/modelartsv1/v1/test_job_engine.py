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

from otcextensions.osclient.modelartsv1.v1 import job_engine
from otcextensions.tests.unit.osclient.modelartsv1.v1 import fakes


class TestListJobEngines(fakes.TestModelartsv1):
    objects = fakes.FakeJobEngine.create_multiple(3)

    column_list_headers = (
        "Engine Id",
        "Engine Name",
        "Engine Type",
        "Engine Version",
    )

    data = []

    for s in objects:
        data.append(
            (
                s.engine_id,
                s.engine_name,
                s.engine_type,
                s.engine_version,
            )
        )

    def setUp(self):
        super(TestListJobEngines, self).setUp()

        self.cmd = job_engine.ListJobEngines(self.app, None)

        self.client.job_engines = mock.Mock()
        self.client.api_mock = self.client.job_engines

    def test_list(self):
        arglist = []

        verifylist = []

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with()

        self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(self.data, list(data))

    def test_list_args(self):
        arglist = [
            "--job-type",
            "inference",
        ]

        verifylist = [
            ("job_type", "inference"),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(
            job_type="inference",
        )
