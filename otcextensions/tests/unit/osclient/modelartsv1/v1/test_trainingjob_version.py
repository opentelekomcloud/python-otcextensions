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
from otcextensions.osclient.modelartsv1.v1 import trainingjob_version
from otcextensions.tests.unit.osclient.modelartsv1.v1 import fakes

_COLUMNS = (
    "is_success",
    "job_id",
    "job_name",
    "job_desc",
    "version_id",
    "version_name",
    "pre_version_id",
    "engine_type",
    "engine_name",
    "engine_id",
    "engine_version",
    "status",
    "app_url",
    "boot_file_url",
    "create_time",
    "parameter",
    "duration",
    "spec_id",
    "core",
    "cpu",
    "gpu_num",
    "gpu_type",
    "worker_server_num",
    "data_url",
    "train_url",
    "log_url",
    "dataset_version_id",
    "dataset_id",
    "data_source",
    "user_image_url",
    "user_command",
    "model_id",
    "model_metric_list",
    "dataset_name",
    "dataset_version_name",
    "spec_code",
    "start_time",
    "volumes",
    "pool_id",
    "pool_name",
    "nas_mount_path",
    "nas_share_addr",
    "nas_type",
)


class TestListTrainingJobVersions(fakes.TestModelartsv1):
    objects = fakes.FakeTrainingJobVersion.create_multiple(3)
    column_list_headers = ("Version Id", "Version Name")

    data = []

    for s in objects:
        data.append((s.version_id, s.version_name))

    def setUp(self):
        super(TestListTrainingJobVersions, self).setUp()

        self.cmd = trainingjob_version.ListTrainingJobVersions(self.app, None)

        self.client.trainingjob_versions = mock.Mock()
        self.client.api_mock = self.client.trainingjob_versions

    def test_list_args(self):
        arglist = ["--job-id", "1"]

        verifylist = [
            ("job_id", "1"),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(job_id="1")

        self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(self.data, list(data))



class TestCreateTrainingJobVersion(fakes.TestModelartsv1):

    _trainingjob_version = fakes.FakeTrainingJobVersion.create_one()
    columns = _COLUMNS
    data = fakes.gen_data(_trainingjob_version, columns,
                          trainingjob_version._formatters)

    def setUp(self):
        super(TestCreateTrainingJobVersion, self).setUp()

        self.cmd = trainingjob_version.CreateTrainingJobVersion(self.app, None)

        self.client.create_trainingjob_version = \
            mock.Mock(return_value=self._trainingjob_version)

    def test_create(self):
        arglist = [
            'test-trainingjobversion',
            '--infer-type', 'https://models.obs.xxxx.com/mnist',
            '--config', 'TensorFlow',
        ]
        verifylist = [
            ('name', 'test-service'),
            ('infer_type', 'https://models.obs.xxxx.com/mnist'),
            ('config', 'TensorFlow')
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        attrs = {
            'trainingjob_version_name': 'test-trainingjob_version',
            'infer_type': 'https://models.obs.xxxx.com/mnist',
            'config': 'TensorFlow'
        }
        self.client.create_trainingjob_version.assert_called_with(**attrs)
        # self.client.wait_for_cluster.assert_called_with(
        #    self._cluster.id, wait=self.default_timeout)
        # self.client.find_model.assert_called_with(self._model.id)
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestShowTrainingJobVersion(fakes.TestModelartsv1):

    _trainingjob_version = fakes.FakeTrainingJobVersion.create_one()
    columns = _COLUMNS
    data = fakes.gen_data(_trainingjob_version, columns,
                          trainingjob_version._formatters)

    def setUp(self):
        super(TestShowTrainingJobVersion, self).setUp()

        self.cmd = trainingjob_version.ShowTrainingJobVersion(self.app, None)

        self.client.find_trainingjob_version = \
            mock.Mock(return_value=self._trainingjob_version)
        #self.client.get_model = mock.Mock(return_value=self._model)

    def test_show_no_options(self):
        arglist = []
        verifylist = []

        # Testing that a call without the required argument will fail and
        # throw a "ParserExecption"
        self.assertRaises(tests_utils.ParserException,
                          self.check_parser, self.cmd, arglist, verifylist)

    def test_show(self):
        arglist = [
            self._trainingjob_version.id,
        ]

        verifylist = [
            ('trainingjob_version', self._trainingjob_version.id)
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.find_trainingjob_version.assert_called_with(self._trainingjob_version.id)

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)

    def test_show_non_existent(self):
        arglist = [
            'unexist_ma_trainingjob_version'
        ]

        verifylist = [
            ('trainingjob_version', 'unexist_ma_trainingjob_version')
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_result = exceptions.CommandError('Resource Not Found')
        self.client.find_trainingjob_version = (
            mock.Mock(side_effect=find_mock_result)
        )

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual('Resource Not Found', str(e))
        self.client.find_trainingjob_version.assert_called_with('unexist_ma_trainingjob_version')


class TestDeleteTrainingJobVersion(fakes.TestModelartsv1):

    _trainingjobversion = fakes.FakeTrainingJobVersion.create_multiple(2)

    def setUp(self):
        super(TestDeleteTrainingJobVersion, self).setUp()

        self.client.find_trainingjobversion = \
            mock.Mock(return_value=self._trainingjobversion[0])
        self.client.delete_trainingjobversion = mock.Mock(return_value=None)

        # Get the command object to test
        self.cmd = trainingjob_version.DeleteTrainingJobVersion(self.app, None)

    def test_delete(self):
        arglist = [
            self._trainingjobversion[0].name,
        ]

        verifylist = [
            ('trainingjobversion', arglist),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.find_trainingjobversion.assert_called_with(
            self._trainingjobversion[0].name, ignore_missing=False)
        self.client.delete_trainingjobversion.assert_called_with(self._trainingjobversion[0].id)
        self.assertIsNone(result)

    def test_multiple_delete(self):
        arglist = []

        for ma_trainingjobversion in self._trainingjobversion:
            arglist.append(ma_trainingjobversion.name)

        verifylist = [
            ('trainingjobversion', arglist)]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_results = self._trainingjobversion
        self.client.find_trainingjobversion = (
            mock.Mock(side_effect=find_mock_results)
        )

        # Trigger the action
        result = self.cmd.take_action(parsed_args)

        find_calls = []
        delete_calls = []
        for ma_trainingjobversion in self._trainingjobversion:
            find_calls.append(
                call(ma_trainingjobversion.name, ignore_missing=False))
            delete_calls.append(call(ma_trainingjobversion.id))
        self.client.find_trainingjobversion.assert_has_calls(find_calls)
        self.client.delete_trainingjobversion.assert_has_calls(delete_calls)
        self.assertIsNone(result)

    def test_multiple_delete_with_exception(self):
        arglist = [
            self._trainingjobversion[0].id,
            'unexist_ma_trainingjobversion',
        ]
        verifylist = [
            ('trainingjobversion', arglist)
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_results = [self._trainingjobversion[0],
                             exceptions.CommandError]
        self.client.find_trainingjobversion = (
            mock.Mock(side_effect=find_mock_results)
        )

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual(
                '1 of 2 Training Job Version(s) failed to delete.',
                str(e)
            )

        self.client.delete_trainingjobversion.assert_any_call(self._trainingjobversion[0].id)

