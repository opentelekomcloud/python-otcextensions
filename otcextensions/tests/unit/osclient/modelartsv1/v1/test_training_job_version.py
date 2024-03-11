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
from otcextensions.osclient.modelartsv1.v1 import training_job_version
from otcextensions.tests.unit.osclient.modelartsv1.v1 import fakes

_COLUMNS = (
    "attributes",
    "billing",
    "core",
    "cpu",
    "created_at",
    "data_url",
    "dataset_id",
    "dataset_name",
    "dataset_version_id",
    "dataset_version_name",
    "description",
    "duration",
    "engine_id",
    "engine_name",
    "engine_type",
    "engine_version",
    "flavor_code",
    "flavor_info",
    "flavor_type",
    "gpu_memory_unit",
    "gpu_num",
    "gpu_type",
    "id",
    "is_free",
    "is_success",
    "job_desc",
    "job_id",
    "job_name",
    "job_type",
    "max_num",
    "memory_unit",
    "model_id",
    "model_metric_list",
    "name",
    "nas_type",
    "no_resource",
    "parameter",
    "pod_version",
    "pool_id",
    "pool_name",
    "pool_type",
    "resource_id",
    "spec_code",
    "spec_id",
    "started_at",
    "status",
    "system_metric_list",
    "train_url",
    "version_id",
    "version_name",
    "worker_server_num",
)


class TestListTrainingJobVersions(fakes.TestModelartsv1):
    job_id = "123"

    objects = fakes.FakeTrainingJobVersion.create_multiple(3)

    column_list_headers = (
        "Version Id",
        "Version Name",
        "Status",
        "Created At",
        "Started At",
        "Duration",
    )

    data = []

    for s in objects:
        data.append(
            (
                s.version_id,
                s.version_name,
                training_job_version.JobStatus(s.status),
                cli_utils.UnixTimestampFormatter(s.created_at),
                cli_utils.UnixTimestampFormatter(s.started_at),
                s.duration,
            )
        )

    def setUp(self):
        super(TestListTrainingJobVersions, self).setUp()

        self.cmd = training_job_version.ListTrainingJobVersions(self.app, None)

        self.client.training_job_versionss = mock.Mock()
        self.client.api_mock = self.client.training_job_versions

    def test_list(self):
        arglist = [self.job_id]

        verifylist = [
            ("jobId", self.job_id),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(self.job_id)

        self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(self.data, list(data))

    def test_list_args(self):
        arglist = [
            self.job_id,
            "--limit",
            "1",
            "--offset",
            "2",
        ]

        verifylist = [
            ("jobId", self.job_id),
            ("limit", 1),
            ("offset", 2),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(self.job_id, limit=1, offset=2)


class TestCreateTrainingJobVersion(fakes.TestModelartsv1):
    job_id = "123"

    _data = fakes.FakeTrainingJobVersion.create_one()
    columns = _COLUMNS

    data = fakes.gen_data(_data, columns, training_job_version._formatters)

    def setUp(self):
        super(TestCreateTrainingJobVersion, self).setUp()

        self.cmd = training_job_version.CreateTrainingJobVersion(
            self.app, None
        )

        self.client.create_training_job_version = mock.Mock(
            return_value=self._data
        )

    def test_create(self):
        arglist = [
            self.job_id,
            "--description",
            "1",
            "--pre-version-id",
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
        ]
        verifylist = [
            ("jobId", self.job_id),
            ("pre_version_id", 2),
            ("job_desc", "1"),
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
        ]
        # Verify cm is triggereg with default parameters
        self.check_parser(self.cmd, arglist, verifylist)
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        attrs = {
            "job_desc": "1",
            "config": {
                "worker_server_num": 3,
                "pre_version_id": 2,
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
            },
        }
        self.client.create_training_job_version.assert_called_with(
            self.job_id, **attrs
        )
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestShowTrainingJobVersion(fakes.TestModelartsv1):
    job_id = "123"
    version_id = "2"

    _data = fakes.FakeTrainingJobVersion.create_one()
    columns = _COLUMNS
    data = fakes.gen_data(_data, columns, training_job_version._formatters)

    def setUp(self):
        super(TestShowTrainingJobVersion, self).setUp()

        self.cmd = training_job_version.ShowTrainingJobVersion(self.app, None)

        self.client.get_training_job_version = mock.Mock(
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
        arglist = [self.job_id, self.version_id]

        verifylist = [
            ("jobId", self.job_id),
            ("versionId", self.version_id),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.get_training_job_version.assert_called_with(
            self.job_id, self.version_id
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)

    def test_show_non_existent(self):
        arglist = [self.job_id, "non-existing-version-id"]

        verifylist = [
            ("jobId", self.job_id),
            ("versionId", "non-existing-version-id"),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.client.get_training_job_version = mock.Mock(
            side_effect=exceptions.CommandError("Resource Not Found")
        )

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual("Resource Not Found", str(e))
        self.client.get_training_job_version.assert_called_with(
            self.job_id, "non-existing-version-id"
        )


class TestDeleteTrainingJobVersion(fakes.TestModelartsv1):

    job_id = "123"
    version_id = "2"

    def setUp(self):
        super(TestDeleteTrainingJobVersion, self).setUp()

        self.client.delete_training_job_version = mock.Mock(return_value=None)

        # Get the command object to test
        self.cmd = training_job_version.DeleteTrainingJobVersion(
            self.app, None
        )

    def test_delete(self):
        arglist = [self.job_id, self.version_id]

        verifylist = [
            ("jobId", self.job_id),
            ("versionId", self.version_id),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)

        self.client.delete_training_job_version.assert_called_with(
            self.job_id, self.version_id
        )
        self.assertIsNone(result)
