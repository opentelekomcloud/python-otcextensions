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
from openstackclient.tests.unit import utils as tests_utils
from osc_lib import exceptions
from otcextensions.common import cli_utils
from otcextensions.osclient.modelartsv2.v2 import dataset
from otcextensions.tests.unit.osclient.modelartsv2.v2.dataset import fakes


class TestListSamples(fakes.TestModelartsv2):
    objects = fakes.FakeSample.create_multiple(3)

    column_list_headers = (
        "Id",
        "Sample Type",
        "Sample Status",
        "Sample Time",
    )

    data = []

    for s in objects:
        data.append(
            (
                s.id,
                dataset.sample.SampleType(s.sample_type),
                s.sample_status,
                cli_utils.UnixTimestampFormatter(s.sample_time),
            )
        )

    def setUp(self):
        super(TestListSamples, self).setUp()

        self.cmd = dataset.ListSamples(self.app, None)

        self.client.dataset_samples = mock.Mock()
        self.client.api_mock = self.client.dataset_samples

    def test_list(self):
        arglist = ["dataset-uuid"]

        verifylist = [
            ("datasetId", "dataset-uuid"),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with("dataset-uuid")

        self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(self.data, list(data))

    def test_list_args(self):
        arglist = [
            "dataset-uuid",
            "--email",
            "1",
            "--high-score",
            "2",
            "--label-name",
            "3",
            "--label-type",
            "4",
            "--limit",
            "5",
            "--locale",
            "6",
            "--low-score",
            "7",
            "--offset",
            "8",
            "--order",
            "asc",
            "--preview",
            "--process-parameter",
            "11",
            "--sample-state",
            "accepted",
            "--sample-type",
            "0",
            "--search-conditions",
            "13",
            "--version-id",
            "14",
        ]

        verifylist = [
            ("datasetId", "dataset-uuid"),
            ("email", "1"),
            ("high_score", "2"),
            ("label_name", "3"),
            ("label_type", "4"),
            ("limit", 5),
            ("locale", "6"),
            ("low_score", "7"),
            ("offset", 8),
            ("order", "asc"),
            ("preview", True),
            ("process_parameter", "11"),
            ("sample_state", "accepted"),
            ("sample_type", 0),
            ("search_conditions", "13"),
            ("version_id", "14"),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(
            "dataset-uuid",
            email="1",
            high_score="2",
            label_name="3",
            label_type="4",
            limit=5,
            locale="6",
            low_score="7",
            offset=8,
            order="asc",
            preview=True,
            process_parameter="11",
            sample_state="accepted",
            sample_type=0,
            search_conditions="13",
            version_id="14",
        )


class TestShowSample(fakes.TestModelartsv2):
    columns = (
        "annotated_by",
        "labels",
        "metadata",
        "preview",
        "sample_id",
        "sample_status",
        "sample_time",
        "sample_type",
        "source",
    )
    _sample = fakes.FakeSample.create_one()

    data = fakes.gen_data(_sample, columns, dataset.sample._formatters)

    def setUp(self):
        super(TestShowSample, self).setUp()

        self.cmd = dataset.ShowSample(self.app, None)

        self.client.get_dataset_sample = mock.Mock(return_value=self._sample)

    def test_show_no_options(self):
        arglist = []
        verifylist = []

        # Testing that a call without the required argument will fail and
        # throw a "ParserExecption"
        self.assertRaises(
            tests_utils.ParserException,
            self.check_parser,
            self.cmd,
            arglist,
            verifylist,
        )

    def test_show(self):
        arglist = [
            "dataset-id",
            "sample-id",
        ]

        verifylist = [
            ("datasetId", "dataset-id"),
            ("sampleId", "sample-id"),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.get_dataset_sample.assert_called_with(
            "dataset-id", "sample-id"
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)

    def test_show_non_existent(self):
        arglist = [
            "dataset-id",
            "nonexisting-sample-id",
        ]

        verifylist = [
            ("datasetId", "dataset-id"),
            ("sampleId", "nonexisting-sample-id"),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        get_mock_result = exceptions.CommandError("Resource Not Found")
        self.client.get_dataset_sample = mock.Mock(side_effect=get_mock_result)

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual("Resource Not Found", str(e))
        self.client.get_dataset_sample.assert_called_with(
            "dataset-id",
            "nonexisting-sample-id",
        )


class TestDeleteSample(fakes.TestModelartsv2):
    columns = ("results", "success")
    _data = fakes.FakeDeleteSample.create_one()
    formatters = {
        "results": cli_utils.YamlFormat,
    }
    data = fakes.gen_data(_data, columns, formatters)

    def setUp(self):
        super(TestDeleteSample, self).setUp()

        self.client.delete_dataset_samples = mock.Mock(return_value=self._data)

        # Get the command object to test
        self.cmd = dataset.DeleteSamples(self.app, None)

    def test_delete(self):
        arglist = [
            "dataset-id",
            "sample1-id",
            "sample2-id",
            "--delete-source",
        ]

        verifylist = [
            ("datasetId", "dataset-id"),
            ("sampleId", ["sample1-id", "sample2-id"]),
            ("delete_source", True),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.delete_dataset_samples.assert_called_with(
            "dataset-id", ["sample1-id", "sample2-id"], True
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)
