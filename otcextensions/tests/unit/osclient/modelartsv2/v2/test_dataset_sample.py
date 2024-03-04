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
from otcextensions.osclient.modelartsv2.v2 import dataset_sample
from otcextensions.tests.unit.osclient.modelartsv2.v2 import fakes

_COLUMNS = (
    "annotated_by",
    "id",
    "labels",
    "metadata",
    "preview",
    "sample_id",
    "sample_status",
    "sample_time",
    "sample_type",
    "source",
)


class TestAddDatasetSamples(fakes.TestModelartsv2):
    columns = (
        "Success",
        "Results",
    )
    _sample = fakes.FakeDatasetSample.create_one()
    formatters = {
        "Results": cli_utils.YamlFormat,
    }

    data = fakes.gen_data(_sample, columns, formatters)

    def setUp(self):
        super(TestAddDatasetSamples, self).setUp()

        self.cmd = dataset_sample.AddDatasetSamples(self.app, None)

        self.client.add_dataset_samples = mock.Mock(return_value=self._sample)

    def test_create(self):
        arglist = [
            "dataset-id",
            "--file-path",
            "1",
            "--directory-path",
            "2",
            "--encoding",
            "UTF-8",
            "--metadata",
            "k1=v1",
            "--metadata",
            "k2=v2",
            "--sample-type",
            "0",
            "--data-source-path",
            "3",
            "--data-source-type",
            "0",
            "--data-source-info",
            "port=1,input=2",
            "--schema-map",
            "src_name=a,dest_name=b",
            "--label",
            "name=1,type=2",
            "--data-with-column-header",
            "--to-be-confirmed",
        ]
        verifylist = [
            ("datasetId", "dataset-id"),
            ("file_path", "1"),
            ("directory_path", "2"),
            ("encoding", "UTF-8"),
            ("metadata", {"k1": "v1", "k2": "v2"}),
            ("sample_type", 0),
            ("data_source_path", "3"),
            ("data_source_type", 0),
            ("data_source_info", [{"port": "1", "input": "2"}]),
            ("schema_map", [{"src_name": "a", "dest_name": "b"}]),
            ("labels", [{"name": "1", "type": "2"}]),
            ("data_with_column_header", True),
            ("to_be_confirmed", True),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.add_dataset_samples.assert_called_with(
            "dataset-id",
            file_path="1",
            directory_path="2",
            encoding="UTF-8",
            sample_type=0,
            metadata={"k1": "v1", "k2": "v2"},
            labels=[{"name": "1", "type": "2"}],
            data_source={
                "data_path": "3",
                "schema_map": [{"src_name": "a", "dest_name": "b"}],
                "source_info": {"port": "1", "input": "2"},
                "with_column_header": True,
            },
        )
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestListDatasetSamples(fakes.TestModelartsv2):
    objects = fakes.FakeDatasetSample.create_multiple(3)

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
                dataset_sample.SampleType(s.sample_type),
                s.sample_status,
                cli_utils.UnixTimestampFormatter(s.sample_time),
            )
        )

    def setUp(self):
        super(TestListDatasetSamples, self).setUp()

        self.cmd = dataset_sample.ListDatasetSamples(self.app, None)

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
            "1",
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
            ("label_type", 1),
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
            label_type=1,
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


class TestShowDatasetSample(fakes.TestModelartsv2):
    columns = _COLUMNS
    _data = fakes.FakeDatasetSample.create_one()

    data = fakes.gen_data(_data, columns, dataset_sample._formatters)

    def setUp(self):
        super(TestShowDatasetSample, self).setUp()

        self.cmd = dataset_sample.ShowDatasetSample(self.app, None)

        self.client.get_dataset_sample = mock.Mock(return_value=self._data)

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


class TestDatasetSampleSearchCondition(fakes.TestModelartsv2):
    columns = _COLUMNS

    _data = fakes.FakeDatasetSample.create_one()

    data = fakes.gen_data(_data, columns, dataset_sample._formatters)

    def setUp(self):
        super(TestDatasetSampleSearchCondition, self).setUp()

        self.cmd = dataset_sample.DatasetSampleSearchCondition(self.app, None)

        self.client.get_dataset_sample_search_condition = mock.Mock(
            return_value=self._data
        )

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
        ]

        verifylist = [
            ("datasetId", "dataset-id"),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.get_dataset_sample_search_condition.assert_called_with(
            "dataset-id"
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestDeleteDatasetSample(fakes.TestModelartsv2):
    columns = ("results", "success")
    _data = fakes.FakeDatasetSampleResp.create_one()
    formatters = {
        "results": cli_utils.YamlFormat,
    }
    data = fakes.gen_data(_data, columns, formatters)

    def setUp(self):
        super(TestDeleteDatasetSample, self).setUp()

        self.client.delete_dataset_samples = mock.Mock(return_value=self._data)

        # Get the command object to test
        self.cmd = dataset_sample.DeleteDatasetSamples(self.app, None)

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
