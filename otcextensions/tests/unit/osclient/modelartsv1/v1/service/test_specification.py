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


class TestSpecifications(fakes.TestModelartsv1):
    objects = fakes.FakeServiceSpecification.create_multiple(3)

    column_list_headers = (
        "Specification",
        "Billing Spec",
        "Spec Status",
        "Is Open",
        "Is Free",
        "Over Quota",
        "Display EN",
        "Extend Params",
    )

    data = []

    for s in objects:
        data.append(
            (
                s.specification,
                s.billing_spec,
                s.spec_status,
                s.is_open,
                s.is_free,
                s.over_quota,
                s.display_en,
                s.extend_params,
            )
        )

    def setUp(self):
        super(TestSpecifications, self).setUp()

        self.cmd = service.Specifications(self.app, None)

        self.client.service_deployment_specifications = mock.Mock()
        self.client.api_mock = self.client.service_deployment_specifications

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
            "--is-personal-cluster",
            "--infer-type", "real-time",
        ]

        verifylist = [
            ("is_personal_cluster", True),
            ("infer_type", "real-time"),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(
            is_personal_cluster=True,
            infer_type="real-time",
        )
