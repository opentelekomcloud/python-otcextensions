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
from unittest.mock import call

import mock
from openstackclient.tests.unit import utils as tests_utils
from osc_lib import exceptions
from otcextensions.common import cli_utils
from otcextensions.osclient.modelartsv2.v2 import dataset
from otcextensions.tests.unit.osclient.modelartsv2.v2.dataset import fakes


class TestDatasetExportTask(fakes.TestModelartsv2):
    objects = fakes.FakeDatasetExportTask.create_multiple(3)

    column_list_headers = (
        "Dataset Id",
        "Task Id",
    )

    data = []

    for s in objects:
        data.append(
            (
                s.dataset_id,
                s.task_id,
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

        self.client.api_mock.assert_called_with("dataset-uuid")

        self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(self.data, list(data))

    def test_list_args(self):
        arglist = [
            "--check-running-task",
            "--contain-versions",
            "--dataset-type", "0",
            "--file-preview",
            "--limit", "1",
            "--offset", "2",
            "--order", "asc",
            "--running-task-type", "0",
            "--search-content", "123",
            "--sort-by", "create_time",
            "--support-export",
            "--train-evaluate-ratio", "2,3",
            "--version-format", "0",
            "--with-labels",
            "--workspace-id", "0",
        ]

        verifylist = [
            ("check_running_task", True),
            ("contain_versions", True),
            ("dataset_type", 0),
            ("file_preview", True),
            ("limit", 1),
            ("offset", 2),
            ("order", "asc"),
            ("running_task_type", 0),
            ("search_content", "123"),
            ("sort_by", "create_time"),
            ("support_export", True),
            ("train_evaluate_ratio", "2,3"),
            ("version_format", 0),
            ("with_labels", True),
            ("workspace_id", "0"),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(
            check_running_task=True,
            contain_versions=True,
            dataset_type=0,
            file_preview=True,
            limit=1,
            offset=2,
            order="asc",
            running_task_type=0,
            search_content="123",
            sort_by="create_time",
            support_export=True,
            train_evaluate_ratio="2,3",
            version_format=0,
            with_labels=True,
            workspace_id="0",
        )


class TestShowDatasetExportTask(fakes.TestModelartsv2):
    columns = (
        "ai_project",
        "annotated_sample_count",
        "content_labeling",
        "create_time",
        "data_format",
        "data_sources",
        "data_update_time",
        "dataset_format",
        "dataset_id",
        "dataset_name",
        "dataset_type",
        "dataset_version",
        "dataset_version_count",
        "description",
        "enterprise_project_id",
        "feature_supports",
        "id",
        "import_data",
        "inner_annotation_path",
        "inner_data_path",
        "inner_log_path",
        "inner_task_path",
        "inner_temp_path",
        "inner_work_path",
        "label_task_count",
        "labels",
        "managed",
        "name",
        "next_version_num",
        "status",
        "total_sample_count",
        "unconfirmed_sample_count",
        "update_time",
        "work_path",
        "work_path_type",
        "workforce_task_count",
        "workspace_id",
    )

    object = fakes.FakeDatasetExportTask.create_one()

    data = fakes.gen_data(object, columns)

    def setUp(self):
        super(TestShowDatasetExportTask, self).setUp()

        self.cmd = dataset.ShowDatasetExportTask(self.app, None)

        self.client.get_dataset_export_task = mock.Mock(return_value=self.object)

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
            "--dataset_id",
            "--task_id"
        ]

        verifylist = [
            ("datasetId", "--dataset_id"),
            ("task_id", "--task_id")
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.get_dataset_export_task.assert_called_with("--dataset_id", "--task_id")

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)

    def test_show_non_existent(self):
        arglist = [
            "--dataset-id",
            "nonexisting-task-id",
        ]

        verifylist = [
            ("datasetId", "--dataset-id"),
            ("task_id", "nonexisting-task-id"),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        get_mock_result = exceptions.CommandError("Resource Not Found")
        self.client.get_dataset_export_task = mock.Mock(side_effect=get_mock_result)

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual("Resource Not Found", str(e))
        self.client.get_dataset_export_task.assert_called_with("--dataset-id", "nonexisting-task-id")


