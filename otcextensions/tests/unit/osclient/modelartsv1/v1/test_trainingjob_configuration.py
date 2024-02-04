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
from otcextensions.osclient.modelartsv1.v1 import trainingjob_configuration
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


class TestListTrainingJobConfigurations(fakes.TestModelartsv1):
    objects = fakes.FakeTrainingJobConfiguration.create_multiple(3)

    column_list_headers = ("Job Name", "Created At")

    data = []

    for s in objects:
        data.append(
            (
                s.config_name,
                cli_utils.UnixTimestampFormatter(s.created_at),
            )
        )

    def setUp(self):
        super(TestListTrainingJobConfigurations, self).setUp()

        self.cmd = trainingjob_configuration.ListTrainingJobConfigurations(self.app, None)

        self.client.trainingjob_configurations = mock.Mock()
        self.client.api_mock = self.client.trainingjob_configurations

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


class TestCreateTrainingJobConfiguration(fakes.TestModelartsv1):
    _trainingjob_configuration = fakes.FakeTrainingJobConfiguration.create_one()
    columns = _COLUMNS
    data = fakes.gen_data(_trainingjob_configuration, columns, trainingjob_configuration._formatters)

    def setUp(self):
        super(TestCreateTrainingJobConfiguration, self).setUp()

        self.cmd = trainingjob_configuration.CreateTrainingJobConfiguration(self.app, None)

        self.client.create_trainingjob_configuration = mock.Mock(
            return_value=self._trainingjob_configuration
        )

    def test_create(self):
        arglist = [
            "--config-name",
            "test-trainingjob-configuration",
            "--config-desc",
            "1",
            "--worker-server-num",
            "2",
            "--app-url",
            "3",
            "--boot-file-url",
            "4",
            "--log-url",
            "5",
            "--data-url",
            "6",
            "--train-url",
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
            "--parameter",
            "14",
            "--user-image-url",
             "15",
            "--user-command"
            "16"
        ]
        verifylist = [
            ("config_name", "test-trainingjob-configuration"),
            ("config_desc", "1"),
            ("worker_server_num", 2),
            ("app_url", "3"),
            ("boot_file_url", "4"),
            ("log_url", "5"),
            ("data_url", "6")
            ("train_url", "7"),
            ("dataset_id", "8"),
            ("dataset_version_id", "9"),
            ("data_source", "10"),
            ("spec_id", 11),
            ("engine_id", 12),
            ("model_id", 13),
            ("parameter", 14),
            ("user_image_url", 15),
            ("user_command", 16) 
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


class TestDeleteTrainingJobConfiguration(fakes.TestModelartsv1):
    def setUp(self):
        super(TestDeleteTrainingJobConfiguration, self).setUp()

        self.cmd = trainingjob_configuration.DeleteTrainingJobConfiguration(self.app, None)
        self.client.delete_trainingjob_configuration = mock.Mock(return_value=None)

    def test_delete(self):
        arglist = ["test_config_name"]

        verifylist = [
            ("config_name", "test_config_name"),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.delete_trainingjob_configuration.assert_called_with(job_id="test_config_name")
        self.assertIsNone(result)
