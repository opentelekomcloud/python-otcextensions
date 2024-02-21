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
    "annotated_sample_count",
    "create_time",
    "elapsed_time",
    "finished_file_count",
    "finished_file_size",
    "import_path",
    "import_type",
    "imported_sample_count",
    "imported_sub_sample_count",
    "status",
    "task_id",
    "total_file_count",
    "total_file_size",
    "total_sample_count",
    "total_sub_sample_count",
    "update_ms",
)


class TestDatasetImportTask(fakes.TestModelartsv2):
    objects = fakes.FakeDatasetImportTask.create_multiple(3)

    column_list_headers = (
        "task_id",
        "dataset_id",
        "import_path",
    )

    data = []

    for s in objects:
        data.append(
            (
                s.task_id,
                s.dataset_id,
                s.import_path,
            )
        )

    def setUp(self):
        super(TestDatasetImportTask, self).setUp()

        self.cmd = dataset.ListDatasetImportTasks(self.app, None)

        self.client.dataset_import_tasks = mock.Mock()
        self.client.api_mock = self.client.dataset_import_tasks

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
            "dataset-uuid",
            "--limit", "1",
            "--offset", "2",
        ]

        verifylist = [
            ("datasetId", "dataset-uuid"),
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
            dataset_id="dataset-uuid", limit=1, offset=2
        )


class TestCreateDataImportTask(fakes.TestModelartsv2):
    _data = fakes.FakeDatasetImportTask.create_one()
    columns = _COLUMNS
    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestCreateDataImportTask, self).setUp()

        self.cmd = dataset.CreateDatasetImportTask(self.app, None)

        self.client.create_dataset_import_task = mock.Mock(
            return_value=self._data
        )

    def test_create(self):
        arglist = [
            "--dataset-id", "0",
            "--import-path", "1",
            "--import-annotations", "2",
            "--import-type", "3",
            "--import-folder", "4",
            "--final-annotation", "5",
            "--difficult-only", "6",
            "--included-labels", "7",
            "--included-tags", "8",
            "--type", "9",
            "--label-property", "key=1,value=2",
            "--label-type", "11",
            "--text-label-separator", "12",
            "--text-sample-separator", "13",
        ]
        verifylist = [
            ("dataset_id", "0"),
            ("import_path", "1"),
            ("import_annotations", "2"),
            ("import_type", "3"),
            ("import_folder", "4"),
            ("final_annotation", "5"),
            ("difficult_only", "6"),
            ("included_labels", "7"),
            ("included_tags", "8"),
            ("type", "9"),
            ("label_properties", [{"key": "1", "value": "2"}]),
            ("label_type", "11"),
            ("text_label_separator", "12"),
            ("text_sample_separator", "13"),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        attrs = {
            "dataset_id": "0",
            "import_path": "1",
            "import_annotations": "2",
            "import_type": "3",
            "import_folder": "4",
            "final_annotation": "5",
            "difficult_only": "6",
            "included_labels": "7",
            "included_tags": "8",
            "type": "9",
            "label_properties": {"1": "2"},
        }
        self.client.create_dataset_import_task.assert_called_with(**attrs)
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestShowDatasetImportTask(fakes.TestModelartsv2):
    columns = _COLUMNS

    object = fakes.FakeDatasetImportTask.create_one()

    data = fakes.gen_data(object, columns)

    def setUp(self):
        super(TestShowDatasetImportTask, self).setUp()

        self.cmd = dataset.ShowDatasetImportTask(self.app, None)

        self.client.get_dataset_import_task = mock.Mock(
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
        arglist = [
            "dataset-id",
            "task-id"
        ]

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
        self.client.get_dataset_import_task.assert_called_with(**attrs)

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)
