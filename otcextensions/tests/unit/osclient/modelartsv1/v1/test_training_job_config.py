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
from otcextensions.osclient.modelartsv1.v1 import training_job_config
from otcextensions.tests.unit.osclient.modelartsv1.v1 import fakes

_COLUMNS = (
    "app_url",
    "boot_file_url",
    "config_desc",
    "config_name",
    "core",
    "cpu",
    "created_at",
    "data_source",
    "data_url",
    "dataset_id",
    "dataset_name",
    "dataset_version_id",
    "dataset_version_name",
    "engine_id",
    "engine_name",
    "engine_type",
    "engine_version",
    "gpu_num",
    "is_success",
    "log_url",
    "model_id",
    "name",
    "nas_mount_path",
    "nas_share_addr",
    "nas_type",
    "parameter",
    "pool_id",
    "pool_name",
    "spec_code",
    "spec_id",
    "train_url",
    "user_command",
    "user_image_url",
    "volumes",
    "worker_server_num",
)


class TestListTrainingJobConfigs(fakes.TestModelartsv1):
    objects = fakes.FakeTrainingJobConfig.create_multiple(3)

    column_list_headers = (
        "Config Name",
        "Created At",
        "Engine Type",
        "Engine Version",
    )

    data = []

    for s in objects:
        data.append(
            (
                s.config_name,
                cli_utils.UnixTimestampFormatter(s.created_at),
                s.engine_type,
                s.engine_version,
            )
        )

    def setUp(self):
        super(TestListTrainingJobConfigs, self).setUp()

        self.cmd = training_job_config.ListTrainingJobConfigs(self.app, None)

        self.client.training_job_configs = mock.Mock()
        self.client.api_mock = self.client.training_job_configs

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
            "--sort-by",
            "config_name",
            "--order",
            "asc",
            "--search-content",
            "test-config-name",
            "--config-type",
            "sample",
        ]

        verifylist = [
            ("limit", 1),
            ("offset", 2),
            ("sort_by", "config_name"),
            ("order", "asc"),
            ("search_content", "test-config-name"),
            ("config_type", "sample"),
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
            sort_by="config_name",
            order="asc",
            search_content="test-config-name",
            config_type="sample",
        )


class TestCreateTrainingJobConfig(fakes.TestModelartsv1):
    _data = fakes.FakeTrainingJobConfig.create_one()
    columns = _COLUMNS

    data = fakes.gen_data(
        _data, columns, formatters=training_job_config._formatters
    )

    def setUp(self):
        super(TestCreateTrainingJobConfig, self).setUp()

        self.cmd = training_job_config.CreateTrainingJobConfig(self.app, None)

        self.client.create_training_job_config = mock.Mock(
            return_value=self._data
        )

    def test_create(self):
        arglist = [
            "test-config",
            "--description",
            "1",
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
            ("name", "test-config"),
            ("config_desc", "1"),
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
            "config_name": "test-config",
            "config_desc": "1",
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
        }
        self.client.create_training_job_config.assert_called_with(**attrs)
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestShowTrainingJobConfig(fakes.TestModelartsv1):
    _data = fakes.FakeTrainingJobConfig.create_one()
    columns = _COLUMNS
    data = fakes.gen_data(_data, columns, training_job_config._formatters)

    def setUp(self):
        super(TestShowTrainingJobConfig, self).setUp()

        self.cmd = training_job_config.ShowTrainingJobConfig(self.app, None)

        self.client.get_training_job_config = mock.Mock(
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
        arglist = [
            self._data.config_name,
        ]

        verifylist = [
            ("name", self._data.config_name),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.get_training_job_config.assert_called_with(
            self._data.config_name
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)

    def test_show_non_existent(self):
        arglist = [
            "nonexisting-config",
        ]

        verifylist = [
            ("name", "nonexisting-config"),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.client.get_training_job_config = mock.Mock(
            side_effect=exceptions.CommandError("Resource Not Found")
        )

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual("Resource Not Found", str(e))
        self.client.get_training_job_config.assert_called_with(
            "nonexisting-config"
        )


class TestDeleteTrainingJobConfig(fakes.TestModelartsv1):
    def setUp(self):
        super(TestDeleteTrainingJobConfig, self).setUp()

        self.client.delete_training_job_config = mock.Mock(return_value=None)

        # Get the command object to test
        self.cmd = training_job_config.DeleteTrainingJobConfig(self.app, None)

    def test_delete(self):
        arglist = ["test-config"]

        verifylist = [
            ("name", ["test-config"]),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.delete_training_job_config.assert_called_with(
            "test-config"
        )
        self.assertIsNone(result)

    def test_multiple_delete(self):
        arglist = [
            "test-config1",
            "test-config2",
        ]

        verifylist = [
            ("name", ["test-config1", "test-config2"]),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)

        delete_calls = [call("test-config1"), call("test-config2")]
        self.client.delete_training_job_config.assert_has_calls(delete_calls)
        self.assertIsNone(result)

    def test_multiple_delete_with_exception(self):
        arglist = [
            "test-config",
            "non-existing-config",
        ]

        verifylist = [
            ("name", ["test-config", "non-existing-config"]),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        delete_mock_results = [None, exceptions.CommandError]
        self.client.delete_training_job_config = mock.Mock(
            side_effect=delete_mock_results
        )

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual(
                "1 of 2 training job config(s) failed to delete.", str(e)
            )
