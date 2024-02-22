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
from otcextensions.osclient.modelartsv1.v1 import visualization_job
from otcextensions.tests.unit.osclient.modelartsv1.v1 import fakes

# from unittest.mock import call

# from osc_lib import exceptions
# from osc_lib.cli import format_columns


_COLUMNS = (
    "created_at",
    "duration",
    "job_desc",
    "job_id",
    "job_name",
    "resource_id",
    "service_url",
    "status",
    "train_url",
)


class TestListVisualizationJobs(fakes.TestModelartsv1):
    objects = fakes.FakeVisualizationJob.create_multiple(3)
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
        super(TestListVisualizationJobs, self).setUp()

        self.cmd = visualization_job.ListVisualizationJobs(self.app, None)

        self.client.visualization_jobs = mock.Mock()
        self.client.api_mock = self.client.visualization_jobs

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


class TestCreateVisualizationJob(fakes.TestModelartsv1):
    _visualization_job = fakes.FakeVisualizationJob.create_one()
    columns = _COLUMNS
    data = fakes.gen_data(
        _visualization_job, columns, visualization_job._formatters
    )

    def setUp(self):
        super(TestCreateVisualizationJob, self).setUp()

        self.cmd = visualization_job.CreateVisualizationJob(self.app, None)

        self.client.create_visualization_job = mock.Mock(
            return_value=self._visualization_job
        )

    def test_create(self):
        arglist = [
            "--job-name",
            "test-visualizationjob",
            "--job-desc",
            "1",
            "--train-url",
            "2",
            "--job-type",
            "3",
            "--flavor",
            "4",
            "--schedule_duration",
            "5",
        ]
        verifylist = [
            ("job_name", "test-visualizationjob"),
            ("job_desc", "1"),
            ("train_url", "2"),
            ("job_type", "3"),
            ("flavor", "4"),
            ("schedule_duration", 5),
        ]
        # Verify cm is triggereg with default parameters
        self.check_parser(self.cmd, arglist, verifylist)
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.create_visualization_job.assert_called_with(
            job_name="test-visualizationjob",
            job_desc="1",
            train_url="2",
            job_type="3",
            flavor={"code": "4"},
            schedule={"type": "stop", "time_unit": "HOURS", "duration": 5},
        )
        # self.client.wait_for_cluster.assert_called_with(
        #    self._cluster.id, wait=self.default_timeout)
        # self.client.find_model.assert_called_with(self._model.id)
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestUpdateVisualizationJob(fakes.TestModelartsv1):
    _data = fakes.FakeVisualizationJob.create_one()

    columns = _COLUMNS

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestUpdateVisualizationJob, self).setUp()

        self.cmd = visualization_job.UpdateVisualizationJob(self.app, None)

        self.client.update_visualization_job = mock.Mock(
            return_value=self._data
        )

    def test_update(self):
        arglist = ["job-id", "--job-desc", "New Description"]
        verifylist = [("job_id", "job-id"), ("job_desc", "New Description")]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        attrs = {"job_desc": "This is a ModelArts job"}
        self.client.update_trainingjob.assert_called_with("job-id", **attrs)
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestDeleteVisualizationJob(fakes.TestModelartsv1):
    def setUp(self):
        super(TestDeleteVisualizationJob, self).setUp()

        self.cmd = visualization_job.DeleteVisualizationJob(self.app, None)
        self.client.delete_visualizationjob = mock.Mock(return_value=None)

    def test_delete(self):
        arglist = ["test_jobid"]

        verifylist = [
            ("jobId", "test_jobid"),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.delete_visualizationjob.assert_called_with(
            job_id="test_jobid"
        )
        self.assertIsNone(result)
