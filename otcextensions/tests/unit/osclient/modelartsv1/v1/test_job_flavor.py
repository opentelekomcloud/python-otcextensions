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

from otcextensions.osclient.modelartsv1.v1 import job_flavor
from otcextensions.tests.unit.osclient.modelartsv1.v1 import fakes


class TestListJobFlavors(fakes.TestModelartsv1):
    objects = fakes.FakeJobFlavor.create_multiple(3)

    column_list_headers = (
        "Spec Id",
        "Spec Code",
        "Core",
        "CPU",
        "GPU Num",
        "GPU Type",
    )

    data = []

    for s in objects:
        data.append(
            (
                s.spec_id,
                s.spec_code,
                s.core,
                s.cpu,
                s.gpu_num,
                s.gpu_type,
            )
        )

    def setUp(self):
        super(TestListJobFlavors, self).setUp()

        self.cmd = job_flavor.ListJobFlavors(self.app, None)

        self.client.job_flavors = mock.Mock()
        self.client.api_mock = self.client.job_flavors

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
            "--engine-id",
            "1",
            "--project-type",
            "2",
        ]

        verifylist = [
            ("job_type", "inference"),
            ("engine_id", 1),
            ("project_type", 2),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(
            job_type="inference",
            engine_id=1,
            project_type=2,
        )
