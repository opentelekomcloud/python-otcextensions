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
from otcextensions.osclient.modelartsv1.v1 import builtin_model
from otcextensions.tests.unit.osclient.modelartsv1.v1 import fakes


class TestListBuiltInModels(fakes.TestModelartsv1):
    objects = fakes.FakeBuiltInModel.create_multiple(3)

    column_list_headers = (
        "Model Id",
        "Model name",
        "Model Usage",
        "Model Precision",
        "Model Size",
        "Created At",
    )

    data = []

    for s in objects:
        data.append(
            (
                s.model_id,
                s.model_name,
                s.model_usage,
                s.model_precision,
                s.model_size,
                cli_utils.UnixTimestampFormatter(s.created_at),
            )
        )

    def setUp(self):
        super(TestListBuiltInModels, self).setUp()

        self.cmd = builtin_model.ListBuiltInModels(self.app, None)

        self.client.builtin_models = mock.Mock()
        self.client.api_mock = self.client.builtin_models

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
            "create_time",
            "--order",
            "asc",
            "--search-content",
            "test-model-name",
        ]

        verifylist = [
            ("limit", 1),
            ("offset", 2),
            ("sort_by", "create_time"),
            ("order", "asc"),
            ("search_content", "test-model-name"),
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
            sort_by="create_time",
            order="asc",
            search_content="test-model-name",
        )


class TestShowBuiltInModel(fakes.TestModelartsv1):
    _model = fakes.FakeBuiltInModel.create_one()
    columns = (
        "created_at",
        "engine_id",
        "engine_name",
        "engine_version",
        "model_dataset_format",
        "model_description_url",
        "model_id",
        "model_name",
        "model_precision",
        "model_size",
        "model_train_dataset",
        "model_usage",
        "parameter",
    )
    formatters = {
        "created_at": cli_utils.UnixTimestampFormatter,
        "parameter": cli_utils.YamlFormat,
    }
    data = fakes.gen_data(_model, columns, formatters=formatters)

    def setUp(self):
        super(TestShowBuiltInModel, self).setUp()

        self.cmd = builtin_model.ShowBuiltInModel(self.app, None)

        self.client.find_builtin_model = mock.Mock(return_value=self._model)

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
            self._model.model_name,
        ]

        verifylist = [("name", self._model.model_name)]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.find_builtin_model.assert_called_with(
            self._model.model_name, ignore_missing=False
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)
