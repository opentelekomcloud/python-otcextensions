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
from otcextensions.osclient.modelartsv1.v1 import trainingjob_configuration
from otcextensions.tests.unit.osclient.modelartsv1.v1 import fakes

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

    column_list_headers = ("is_success", "config_total_count", "configs")

    data = []

    for s in objects:
        data.append(
            (
                s.is_success,
                s.config_total_count,
                s.configs,
            )
        )

    def setUp(self):
        super(TestListTrainingJobConfigurations, self).setUp()

        self.cmd = trainingjob_configuration.ListTrainingJobConfigurations(
            self.app, None
        )

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
    _trainingjob_configuration = (
        fakes.FakeTrainingJobConfiguration.create_one()
    )
    columns = _COLUMNS
    data = fakes.gen_data(
        _trainingjob_configuration,
        columns,
        trainingjob_configuration._formatters,
    )

    def setUp(self):
        super(TestCreateTrainingJobConfiguration, self).setUp()

        self.cmd = trainingjob_configuration.CreateTrainingJobConfiguration(
            self.app, None
        )

        self.client.create_trainingjob_configuration = mock.Mock(
            return_value=self._trainingjob_configuration
        )

    def test_create(self):
        arglist = [
            "--config-name", "test-trainingjob-configuration",
            "--config-desc", "1",
            "--worker-server-num", "2",
            "--app-url", "3",
            "--boot-file-url", "4",
            "--log-url", "5",
            "--data-url", "6",
            "--train-url", "7",
            "--dataset-id", "8",
            "--dataset-version-id", "9",
            "--data-source", "10",
            "--spec-id", "11",
            "--engine-id", "12",
            "--model-id", "13",
            "--parameter", "14",
            "--user-image-url", "15",
            "--user-command", "16",
            "--dataset-version", "17",
            "--type", "18",
        ]
        verifylist = [
            ("config_name", "test-trainingjob-configuration"),
            ("config_desc", "1"),
            ("worker_server_num", "2"),
            ("app_url", "3"),
            ("boot_file_url", "4"),
            ("log_url", "5"),
            ("data_url", "6"),
            ("train_url", "7"),
            ("dataset_id", "8"),
            ("dataset_version_id", "9"),
            ("data_source", "10"),
            ("spec_id", "11"),
            ("engine_id", "12"),
            ("model_id", "13"),
            ("parameter", "14"),
            ("user_image_url", "15"),
            ("user_command", "16"),
            ("dataset_version", "17"),
            ("type", "18"),
        ]
        # Verify cm is triggereg with default parameters
        self.check_parser(self.cmd, arglist, verifylist)
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        attrs = {
        
        "config_name": "testConfig",
        "config_desc": "This is config",
        "worker_server_num": 1,
        "app_url": "/usr/app/",
        "boot_file_url": "/usr/app/boot.py",
        "parameter": [
            {
                "label": "learning_rate",
                "value": "0.01"
            },
            {
                "label": "batch_size",
                "value": "32"
            }
        ],
        "spec_id": 1,
        "dataset_id": "38277e62-9e59-48f4-8d89-c8cf41622c24",
        "dataset_version_id": "2ff0d6ba-c480-45ae-be41-09a8369bfc90",
        "engine_id": 1,
        "train_url": "/usr/train/",
        "log_url": "/usr/log/"
        }
        self.client.create_trainingjob_configuration.assert_called_with(**attrs)
        # self.client.wait_for_cluster.assert_called_with(
        #    self._cluster.id, wait=self.default_timeout)
        # self.client.find_model.assert_called_with(self._model.id)
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestDeleteTrainingJobConfiguration(fakes.TestModelartsv1):
    def setUp(self):
        super(TestDeleteTrainingJobConfiguration, self).setUp()

        self.cmd = trainingjob_configuration.DeleteTrainingJobConfiguration(
            self.app, None
        )
        self.client.delete_trainingjob_configuration = mock.Mock(
            return_value=None
        )

    def test_delete(self):
        arglist = ["test_config_name"]

        verifylist = [
            ("configName", "test_config_name"),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.delete_trainingjob_configuration.assert_called_with(
            config_name="test_config_name"
        )
        self.assertIsNone(result)
