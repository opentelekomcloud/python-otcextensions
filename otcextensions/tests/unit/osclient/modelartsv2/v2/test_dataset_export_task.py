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

from otcextensions.common import cli_utils
from otcextensions.osclient.modelartsv2.v2 import dataset_export_task
from otcextensions.tests.unit.osclient.modelartsv2.v2 import fakes

_COLUMNS = (
    'created_at',
    'export_format',
    'export_params',
    'export_type',
    'id',
    'path',
    'progress',
    'status',
    'task_id',
    'updated_at',
    'version_format',
)


class TestListDatasetExportTask(fakes.TestModelartsv2):
    _dataset = fakes.FakeDataset.create_one()
    objects = fakes.FakeDatasetExportTask.create_multiple(3)

    column_list_headers = (
        "Task Id",
        "Created At",
        "Status",
    )

    data = []

    for s in objects:
        data.append(
            (
                s.task_id,
                cli_utils.UnixTimestampFormatter(s.created_at),
                s.status,
            )
        )

    def setUp(self):
        super(TestListDatasetExportTask, self).setUp()

        self.cmd = dataset_export_task.ListDatasetExportTasks(self.app, None)

        self.client.find_dataset = mock.Mock(return_value=self._dataset)
        self.client.dataset_export_tasks = mock.Mock()
        self.client.api_mock = self.client.dataset_export_tasks

    def test_list(self):
        arglist = ["dataset-id"]

        verifylist = [
            ("dataset", "dataset-id"),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_dataset.assert_called_with(
            "dataset-id", ignore_missing=False
        )
        self.client.api_mock.assert_called_with(self._dataset)

        self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(self.data, list(data))

    def test_list_args(self):
        arglist = [
            "dataset-id",
            "--export-type",
            "0",
            "--limit",
            "1",
            "--offset",
            "2",
        ]

        verifylist = [
            ("dataset", "dataset-id"),
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

        self.client.find_dataset.assert_called_with(
            "dataset-id", ignore_missing=False
        )
        self.client.api_mock.assert_called_with(
            self._dataset, limit=1, offset=2, export_type=0
        )


class TestShowDatasetExportTask(fakes.TestModelartsv2):
    _dataset = fakes.FakeDataset.create_one()
    columns = _COLUMNS

    object = fakes.FakeDatasetExportTask.create_one()

    formatters = {
        "created_at": cli_utils.UnixTimestampFormatter,
        "updated_at": cli_utils.UnixTimestampFormatter,
        "export_params": cli_utils.YamlFormat,
    }
    data = fakes.gen_data(object, columns, formatters)

    def setUp(self):
        super(TestShowDatasetExportTask, self).setUp()

        self.cmd = dataset_export_task.ShowDatasetExportTask(self.app, None)

        self.client.find_dataset = mock.Mock(return_value=self._dataset)
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
            ("dataset", "dataset-id"),
            ("taskId", "task-id"),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_dataset.assert_called_with(
            "dataset-id", ignore_missing=False
        )
        self.client.get_dataset_export_task.assert_called_with(
            self._dataset, "task-id"
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)
