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
from otcextensions.osclient.modelartsv1.v1 import visualization_job
from otcextensions.tests.unit.osclient.modelartsv1.v1 import fakes

_COLUMNS = (
    "created_at",
    "duration",
    "id",
    "job_desc",
    "job_id",
    "job_name",
    "name",
    "resource_id",
    "schedule",
    "service_url",
    "status",
    "train_url",
)


class TestListVisualizationJobs(fakes.TestModelartsv1):
    objects = fakes.FakeVisualizationJob.create_multiple(3)

    column_list_headers = (
        "Job Id",
        "Job Name",
        "Created At",
    )

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


class TestCreateVisualizationJob(fakes.TestModelartsv1):
    _data = fakes.FakeVisualizationJob.create_one()
    columns = _COLUMNS

    data = fakes.gen_data(_data, columns, visualization_job._formatters)

    def setUp(self):
        super(TestCreateVisualizationJob, self).setUp()

        self.cmd = visualization_job.CreateVisualizationJob(self.app, None)

        self.client.create_visualization_job = mock.Mock(
            return_value=self._data
        )

    def test_create(self):
        arglist = [
            "test-visualizationjob",
            "--description",
            "1",
            "--train-url",
            "2",
            "--job-type",
            "3",
            "--flavor",
            "4",
            "--auto-stop-duration",
            "5",
        ]
        verifylist = [
            ("name", "test-visualizationjob"),
            ("job_desc", "1"),
            ("train_url", "2"),
            ("job_type", "3"),
            ("flavor", "4"),
            ("auto_stop_duration", 5),
        ]
        # Verify cm is triggereg with default parameters
        self.check_parser(self.cmd, arglist, verifylist)
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        attrs = {
            "job_name": "test-visualizationjob",
            "train_url": "2",
            "job_type": "3",
            "flavor": {"code": "4"},
            "job_desc": "1",
            "schedule": {
                "type": "stop",
                "time_unit": "HOURS",
                "duration": 5,
            },
        }
        self.client.create_visualization_job.assert_called_with(**attrs)
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
        arglist = [
            "1234",
            "--description",
            "New Description",
        ]
        verifylist = [
            ("jobId", "1234"),
            ("description", "New Description"),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.update_visualization_job.assert_called_with(
            "1234", "New Description"
        )
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestDeleteVisualizationJob(fakes.TestModelartsv1):
    def setUp(self):
        super(TestDeleteVisualizationJob, self).setUp()

        self.client.delete_visualization_job = mock.Mock(return_value=None)

        # Get the command object to test
        self.cmd = visualization_job.DeleteVisualizationJob(self.app, None)

    def test_delete(self):
        arglist = ["123"]

        verifylist = [
            ("jobId", [123]),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.delete_visualization_job.assert_called_with(123)
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
        self.client.delete_visualization_job.assert_has_calls(delete_calls)
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
        self.client.delete_visualization_job = mock.Mock(
            side_effect=delete_mock_results
        )

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual(
                "1 of 2 visualization job(s) failed to delete.", str(e)
            )
