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
from osc_lib import exceptions

from otcextensions.common import cli_utils
from otcextensions.osclient.modelartsv1.v1 import training_job
from otcextensions.tests.unit.osclient.modelartsv1.v1 import fakes

_COLUMNS = (
    "created_at",
    "duration",
    "id",
    "job_description",
    "job_id",
    "job_name",
    "name",
    "status",
    "user",
    "version_count",
    "version_id",
)


class TestListTrainingJobs(fakes.TestModelartsv1):
    objects = fakes.FakeTrainingJob.create_multiple(3)

    column_list_headers = (
        "Job Id",
        "Job Name",
        "Status",
        "Version Id",
        "Version Count",
        "Created At",
        "Duration",
    )

    data = []

    for s in objects:
        data.append(
            (
                s.job_id,
                s.job_name,
                training_job.JobStatus(s.status),
                s.version_id,
                s.version_count,
                cli_utils.UnixTimestampFormatter(s.created_at),
                s.duration,
            )
        )

    def setUp(self):
        super(TestListTrainingJobs, self).setUp()

        self.cmd = training_job.ListTrainingJobs(self.app, None)

        self.client.training_jobs = mock.Mock()
        self.client.api_mock = self.client.training_jobs

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
            "--limit",
            "1",
            "--offset",
            "2",
            "--status",
            "10",
            "--sort-by",
            "job_name",
            "--order",
            "asc",
            "--search-content",
            "test-job-name",
            "--workspace-id",
            "0",
        ]

        verifylist = [
            ("limit", 1),
            ("offset", 2),
            ("status", 10),
            ("sort_by", "job_name"),
            ("order", "asc"),
            ("search_content", "test-job-name"),
            ("workspace_id", "0"),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(
            limit=1,
            offset=2,
            status=10,
            sort_by="job_name",
            order="asc",
            search_content="test-job-name",
            workspace_id="0",
        )


class TestCreateTrainingJob(fakes.TestModelartsv1):
    _data = fakes.FakeTrainingJob.create_one()
    columns = _COLUMNS

    data = fakes.gen_data(_data, columns, training_job._formatters)

    def setUp(self):
        super(TestCreateTrainingJob, self).setUp()

        self.cmd = training_job.CreateTrainingJob(self.app, None)

        self.client.create_training_job = mock.Mock(return_value=self._data)

    def test_create(self):
        arglist = [
            "test-trainingjob",
            "--description",
            "1",
            "--workspace-id",
            "2",
            "--worker-server-num",
            "3",
            "--app-url",
            "4",
            "--boot-file-url",
            "5",
            "--log-url",
            "6",
            "--data-url",
            "7",
            "--dataset-id",
            "8",
            "--dataset-version",
            "9",
            "--spec-id",
            "11",
            "--engine-id",
            "12",
            "--model-id",
            "13",
            "--train-url",
            "14",
            "--parameter",
            "label=k1,value=v1",
            "--parameter",
            "label=k2,value=v2",
            "--nfs",
            "id=123,src_path=a,dest_path=b,read_only=false",
            "--host-path",
            "src_path=x,dest_path=y,read_only=false",
            "--no-create-version",
        ]
        verifylist = [
            ("name", "test-trainingjob"),
            ("job_desc", "1"),
            ("workspace_id", "2"),
            ("worker_server_num", 3),
            ("app_url", "4"),
            ("boot_file_url", "5"),
            ("log_url", "6"),
            ("data_url", "7"),
            ("dataset_id", "8"),
            ("dataset_version_id", "9"),
            ("spec_id", 11),
            ("engine_id", 12),
            ("model_id", 13),
            ("train_url", "14"),
            (
                "parameter",
                [
                    {"label": "k1", "value": "v1"},
                    {"label": "k2", "value": "v2"},
                ],
            ),
            (
                "nfs",
                [
                    {
                        "id": "123",
                        "src_path": "a",
                        "dest_path": "b",
                        "read_only": "false",
                    }
                ],
            ),
            (
                "host_path",
                [
                    {
                        "src_path": "x",
                        "dest_path": "y",
                        "read_only": "false",
                    }
                ],
            ),
            ("no_create_version", True),
        ]
        # Verify cm is triggereg with default parameters
        self.check_parser(self.cmd, arglist, verifylist)
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        attrs = {
            "job_name": "test-trainingjob",
            "config": {
                "worker_server_num": 3,
                "app_url": "4",
                "boot_file_url": "5",
                "parameter": [
                    {"label": "k1", "value": "v1"},
                    {"label": "k2", "value": "v2"},
                ],
                "data_url": "7",
                "dataset_id": "8",
                "dataset_version_id": "9",
                "spec_id": 11,
                "engine_id": 12,
                "model_id": 13,
                "train_url": "14",
                "log_url": "6",
                "create_version": False,
                "volumes": [
                    {
                        "nfs": {
                            "id": "123",
                            "src_path": "a",
                            "dest_path": "b",
                            "read_only": "false",
                        }
                    },
                    {
                        "host_path": {
                            "src_path": "x",
                            "dest_path": "y",
                            "read_only": "false",
                        }
                    },
                ],
            },
            "job_desc": "1",
            "workspace_id": "2",
        }
        self.client.create_training_job.assert_called_with(**attrs)
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestUpdateTrainingJob(fakes.TestModelartsv1):
    _data = fakes.FakeTrainingJob.create_one()

    columns = _COLUMNS

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestUpdateTrainingJob, self).setUp()

        self.cmd = training_job.UpdateTrainingJob(self.app, None)

        self.client.update_training_job = mock.Mock(return_value=self._data)

    def test_update(self):
        arglist = [
            "1234",
            "--description",
            "New Description",
        ]
        verifylist = [
            ("jobId", 1234),
            ("description", "New Description"),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.update_training_job.assert_called_with(
            1234, "New Description"
        )
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestDeleteTrainingJob(fakes.TestModelartsv1):
    def setUp(self):
        super(TestDeleteTrainingJob, self).setUp()

        self.client.delete_training_job = mock.Mock(return_value=None)

        # Get the command object to test
        self.cmd = training_job.DeleteTrainingJob(self.app, None)

    def test_delete(self):
        arglist = ["123"]

        verifylist = [
            ("jobId", [123]),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.delete_training_job.assert_called_with(123)
        self.assertIsNone(result)

    def test_multiple_delete(self):
        arglist = [
            "1234",
            "9876",
        ]

        verifylist = [
            ("jobId", [1234, 9876]),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)

        delete_calls = [call(1234), call(9876)]
        self.client.delete_training_job.assert_has_calls(delete_calls)
        self.assertIsNone(result)

    def test_multiple_delete_with_exception(self):
        arglist = [
            "1234",
            "5544",  # non-existing-job-id
        ]

        verifylist = [
            ("jobId", [1234, 5544]),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        delete_mock_results = [None, exceptions.CommandError]
        self.client.delete_training_job = mock.Mock(
            side_effect=delete_mock_results
        )

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual(
                "1 of 2 training job(s) failed to delete.", str(e)
            )
