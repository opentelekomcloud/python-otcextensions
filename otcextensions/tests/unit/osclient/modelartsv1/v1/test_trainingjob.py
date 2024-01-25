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

# from openstackclient.tests.unit import utils as tests_utils
from otcextensions.common import cli_utils
from otcextensions.osclient.modelartsv1.v1 import trainingjob
from otcextensions.tests.unit.osclient.modelartsv1.v1 import fakes

# from unittest.mock import call

# from osc_lib import exceptions
# from osc_lib.cli import format_columns


_COLUMNS = (
    "access_address",
    "additional_properties",
    "cluster_id",
    "config",
    "failed_times",
    "infer_type",
    "invocation_times",
    "is_free",
    "is_shared",
    "operation_time",
    "owner",
    "progress",
    "project",
    "publish_at",
    "schedule",
    "service_id",
    "service_name",
    "shared_count",
    "status",
    "tenant",
    "transition_at",
    "update_time",
    "workspace_id",
)


class TestListTrainingJobs(fakes.TestModelartsv1):
    objects = fakes.FakeTrainingJob.create_multiple(3)

    column_list_headers = ("Job Id", "Job Name", "Created At")

    data = []

    for s in objects:
        data.append(
            (
                s.job_id,
                s.job_name,
                cli_utils.UnixTimestampFormatter(s.created_at),
            )
        )

    def setUp(self):
        super(TestListTrainingJobs, self).setUp()

        self.cmd = trainingjob.ListTrainingJobs(self.app, None)

        self.client.trainingjobs = mock.Mock()
        self.client.api_mock = self.client.trainingjobs

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


class TestCreateTrainingJob(fakes.TestModelartsv1):
    _trainingjob = fakes.FakeTrainingJob.create_one()
    columns = _COLUMNS
    data = fakes.gen_data(_trainingjob, columns, trainingjob._formatters)

    def setUp(self):
        super(TestCreateTrainingJob, self).setUp()

        self.cmd = trainingjob.CreateTrainingJob(self.app, None)

        self.client.create_trainingjob = mock.Mock(
            return_value=self._trainingjob
        )

    def test_create(self):
        arglist = [
            "--job-name",
            "test-trainingjob",
            "--job-desc",
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
            "--dataset-version-id",
            "9",
            "--data-source",
            "10",
            "--spec-id",
            "11",
            "--engine-id",
            "12",
            "--model-id",
            "13",
        ]
        verifylist = [
            ("job_name", "test-trainingjob"),
            ("job_desc", "1"),
            ("workspace_id", "2"),
            ("worker_server_num", 3),
            ("app_url", "4"),
            ("boot_file_url", "5"),
            ("log_url", "6"),
            ("data_url", "7"),
            ("dataset_id", "8"),
            ("dataset_version_id", "9"),
            ("data_source", "10"),
            ("spec_id", 11),
            ("engine_id", 12),
            ("model_id", 13),
        ]
        # Verify cm is triggereg with default parameters
        self.check_parser(self.cmd, arglist, verifylist)
        # parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        # columns, data = self.cmd.take_action(parsed_args)
        # attrs = {}
        # self.client.create_trainingjob.assert_called_with(**attrs)
        # self.client.wait_for_cluster.assert_called_with(
        #    self._cluster.id, wait=self.default_timeout)
        # self.client.find_model.assert_called_with(self._model.id)
        # self.assertEqual(self.columns, columns)
        # self.assertEqual(self.data, data)


class TestDeleteTrainingJob(fakes.TestModelartsv1):
    def setUp(self):
        super(TestDeleteTrainingJob, self).setUp()

        self.cmd = trainingjob.DeleteTrainingJob(self.app, None)
        self.client.delete_trainingjob = mock.Mock(return_value=None)

    def test_delete(self):
        arglist = ["test_jobid"]

        verifylist = [
            ("jobId", "test_jobid"),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.delete_trainingjob.assert_called_with(job_id="test_jobid")
        self.assertIsNone(result)
