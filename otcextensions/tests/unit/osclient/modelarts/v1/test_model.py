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
from unittest.mock import call

from osc_lib import exceptions

from otcextensions.osclient.modelarts.v1 import model
from otcextensions.tests.unit.osclient.modelarts.v1 import fakes

from openstackclient.tests.unit import utils as tests_utils


_COLUMNS = (
    'apis',
    'config',
    'created_at',
    'dependencies',
    'execution_code',
    'id',
    'image_address',
    'input_params',
    'install_type',
    'labels_map',
    'model_id',
    'model_labels',
    'model_metrics',
    'model_size',
    'model_type',
    'name',
    'output_params',
    'owner_id',
    'project_id',
    'runtime',
    'source_location',
    'specification',
    'status',
    'tenant_id',
    'version',
    'workspace_id'
)


class TestListModels(fakes.TestModelarts):

    objects = fakes.FakeModel.create_multiple(3)

    column_list_headers = (
        'Id',
        'Name',
        'Version',
        'Model Size'
    )

    data = []

    for s in objects:
        data.append(
            (
                s.model_id,
                s.name,
                s.version,
                s.model_size,
            )
        )

    def setUp(self):
        super(TestListModels, self).setUp()

        self.cmd = model.ListModels(self.app, None)

        self.client.models = mock.Mock()
        self.client.api_mock = self.client.models

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


class TestCreateModel(fakes.TestModelarts):

    _model = fakes.FakeModel.create_one()
    columns = _COLUMNS
    data = fakes.gen_data(_model, columns, model._formatters)

    def setUp(self):
        super(TestCreateModel, self).setUp()

        self.cmd = model.CreateModel(self.app, None)

        self.client.create_model = mock.Mock(return_value=self._model)

    def test_create(self):
        arglist = [
            'test-model',
            '--model-version', '1.0.0',
            '--source-location', 'https://models.obs.xxxx.com/mnist',
            '--model-type', 'TensorFlow',
        ]
        verifylist = [
            ('name', 'test-model'),
            ('model_version', '1.0.0'),
            ('source_location', 'https://models.obs.xxxx.com/mnist'),
            ('model_type', 'TensorFlow')
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        attrs = {
            'model_name': 'test-model',
            'model_version': '1.0.0',
            'source_location': 'https://models.obs.xxxx.com/mnist',
            'model_type': 'TensorFlow'
        }
        self.client.create_model.assert_called_with(**attrs)
        # self.client.wait_for_cluster.assert_called_with(
        #    self._cluster.id, wait=self.default_timeout)
        # self.client.find_model.assert_called_with(self._model.id)
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestShowModel(fakes.TestModelarts):

    _model = fakes.FakeModel.create_one()
    columns = _COLUMNS
    data = fakes.gen_data(_model, columns, model._formatters)

    def setUp(self):
        super(TestShowModel, self).setUp()

        self.cmd = model.ShowModel(self.app, None)

        self.client.find_model = mock.Mock(return_value=self._model)
        # self.client.get_model = mock.Mock(return_value=self._model)

    def test_show_no_options(self):
        arglist = []
        verifylist = []

        # Testing that a call without the required argument will fail and
        # throw a "ParserExecption"
        self.assertRaises(tests_utils.ParserException,
                          self.check_parser, self.cmd, arglist, verifylist)

    def test_show(self):
        arglist = [
            self._model.id,
        ]

        verifylist = [
            ('model', self._model.id)
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.find_model.assert_called_with(self._model.id)

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)

    def test_show_non_existent(self):
        arglist = [
            'unexist_ma_model'
        ]

        verifylist = [
            ('model', 'unexist_ma_model')
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_result = exceptions.CommandError('Resource Not Found')
        self.client.find_model = (
            mock.Mock(side_effect=find_mock_result)
        )

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual('Resource Not Found', str(e))
        self.client.find_model.assert_called_with('unexist_ma_model')


class TestDeleteModel(fakes.TestModelarts):

    _model = fakes.FakeModel.create_multiple(2)

    def setUp(self):
        super(TestDeleteModel, self).setUp()

        self.client.find_model = mock.Mock(return_value=self._model[0])
        self.client.delete_model = mock.Mock(return_value=None)

        # Get the command object to test
        self.cmd = model.DeleteModel(self.app, None)

    def test_delete(self):
        arglist = [
            self._model[0].name,
        ]

        verifylist = [
            ('model', arglist),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.find_model.assert_called_with(
            self._model[0].name, ignore_missing=False)
        self.client.delete_model.assert_called_with(self._model[0].id)
        self.assertIsNone(result)

    def test_multiple_delete(self):
        arglist = []

        for ma_model in self._model:
            arglist.append(ma_model.name)

        verifylist = [
            ('model', arglist)]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_results = self._model
        self.client.find_model = (
            mock.Mock(side_effect=find_mock_results)
        )

        # Trigger the action
        result = self.cmd.take_action(parsed_args)

        find_calls = []
        delete_calls = []
        for ma_model in self._model:
            find_calls.append(call(ma_model.name, ignore_missing=False))
            delete_calls.append(call(ma_model.id))
        self.client.find_model.assert_has_calls(find_calls)
        self.client.delete_model.assert_has_calls(delete_calls)
        self.assertIsNone(result)

    def test_multiple_delete_with_exception(self):
        arglist = [
            self._model[0].id,
            'unexist_ma_model',
        ]
        verifylist = [
            ('model', arglist)
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_results = [self._model[0], exceptions.CommandError]
        self.client.find_model = (
            mock.Mock(side_effect=find_mock_results)
        )

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual('1 of 2 Model(s) failed to delete.', str(e))

        self.client.delete_model.assert_any_call(self._model[0].id)
