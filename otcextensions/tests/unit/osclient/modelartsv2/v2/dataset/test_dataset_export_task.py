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
from otcextensions.osclient.modelartsv2.v2 import dataset
from otcextensions.tests.unit.osclient.modelartsv2.v2.dataset import fakes

_COLUMNS = (
    "create_time",
    "export_format",
    "export_params",
    "export_type",
    "path",
    "progress",
    "status",
    "task_id",
)


class TestDatasetExportTask(fakes.TestModelartsv2):
    objects = fakes.FakeDatasetExportTask.create_multiple(3)

    column_list_headers = (
        "task_id",
        "path",
        "status",
        "progress",
    )

    data = []

    for s in objects:
        data.append(
            (
                s.task_id,
                s.path,
                s.status,
                s.progress,
            )
        )

    def setUp(self):
        super(TestDatasetExportTask, self).setUp()

        self.cmd = dataset.ListDatasetExportTasks(self.app, None)

        self.client.dataset_export_tasks = mock.Mock()
        self.client.api_mock = self.client.dataset_export_tasks

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

        self.client.api_mock.assert_called_with(dataset_id="dataset-uuid")

        self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(self.data, list(data))

    def test_list_args(self):
        arglist = [
            "test-id",
            "--export-type", "0",
            "--limit", "1",
            "--offset", "2",
        ]

        verifylist = [
            ("datasetId", "test-id"),
            ("export_type", 0),
            ("limit", 1),
            ("offset", 2),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(
            dataset_id="test-id", limit=1, offset=2, export_type=0
        )


class TestCreateDataExportTask(fakes.TestModelartsv2):
    _data = fakes.FakeDatasetExportTask.create_one()
    columns = _COLUMNS
    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestCreateDataExportTask, self).setUp()

        self.cmd = dataset.CreateDatasetExportTask(self.app, None)

        self.client.create_dataset_export_task = mock.Mock(
            return_value=self._data
        )

    def test_create(self):
        arglist = [
            "--dataset-id", "0",
            "--path", "1",
            "--version-id", "2",
            "--work-path", "3",
            "--work-path-type", "4",
            "--data-sources", "5",
            "--labels", "6",
            "--description", "7",
            "--import-annotations", "8",
            "--label-format", "9",
            "--workspace-id", "10",
            "--data-type", "11",
            "--data-path", "12",
            "--name", "13",
            "--type", "14",
            "--property", "15",
            "--label-type", "16",
            "--text-label-separator", "17",
            "--text-sample-separator", "18",
            "--error-code", "19",
        ]
        verifylist = [
            ("dataset_id", "0"),
            ("path", "1"),
            ("version_id", "2"),
            ("work_path", "3"),
            ("work_path_type", "4"),
            ("data_sources", "5"),
            ("labels", "6"),
            ("description", "7"),
            ("import_annotations", "8"),
            ("label_format", "9"),
            ("workspace_id", "10"),
            ("data_type", "11"),
            ("data_path", "12"),
            ("name", "13"),
            ("type", "14"),
            ("property", "15"),
            ("label_type", "16"),
            ("text_label_separator", "17"),
            ("text_sample_separator", "18"),
            ("error_code", "19"),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        attrs = {
            "work_path": "3",
            "work_path_type": "4",
            "labels": "6",
            "description": "7",
            "import_annotations": "8",
            "label_format": "9",
            "workspace_id": "10",
            "data_type": "11",
            "data_path": "12",
            "name": "13",
            "type": "14",
            "property": "15",
            "label_type": "16",
            "text_sample_separator": "18",
            "text_label_separator": "17",
            "dataset_id": "0",
            "error_code": "19",
        }
        self.client.create_dataset_export_task.assert_called_with(**attrs)
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestShowDatasetExportTask(fakes.TestModelartsv2):
    columns = (
        "create_time",
        "export_format",
        "export_params",
        "export_type",
        "path",
        "progress",
        "status",
        "task_id",
    )

    object = fakes.FakeDatasetExportTask.create_one()

    data = fakes.gen_data(object, columns)

    def setUp(self):
        super(TestShowDatasetExportTask, self).setUp()

        self.cmd = dataset.ShowDatasetExportTask(self.app, None)

        self.client.get_dataset_export_task = mock.Mock(
            return_value=self.object
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
        arglist = ["dataset-id", "task-id"]

        verifylist = [
            ("datasetId", "dataset-id"),
            ("taskId", "task-id"),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        attrs = {
            "dataset_id": "dataset-id",
            "task_id": "task-id",
        }
        self.client.get_dataset_export_task.assert_called_with(**attrs)

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)
