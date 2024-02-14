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
from otcextensions.osclient.modelartsv1.v1 import service
from otcextensions.tests.unit.osclient.modelartsv1.v1 import fakes

_COLUMNS = (
    "access_address",
    "additional_properties",
    "config",
    "description",
    "failed_times",
    "id",
    "infer_type",
    "invocation_times",
    "is_free",
    "is_shared",
    "operation_time",
    "owner",
    "progress",
    "project",
    "publish_at",
    "service_id",
    "service_name",
    "shared_count",
    "status",
    "tenant",
    "transition_at",
    "update_time",
    "workspace_id",
)


class TestListServices(fakes.TestModelartsv1):
    objects = fakes.FakeService.create_multiple(3)

    column_list_headers = (
        "Service Id",
        "Service Name",
        "Infer Type",
        "Status",
    )

    data = []

    for s in objects:
        data.append((s.service_id, s.service_name, s.infer_type, s.status))

    def setUp(self):
        super(TestListServices, self).setUp()

        self.cmd = service.ListServices(self.app, None)

        self.client.services = mock.Mock()
        self.client.api_mock = self.client.services

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
            "--cluster-id",
            "4",
            "--infer-type",
            "real-time",
            "--limit",
            "7",
            "--model-id",
            "3",
            "--offset",
            "6",
            "--order",
            "asc",
            "--service-id",
            "1",
            "--service-name",
            "2",
            "--sort-by",
            "service_name",
            "--status",
            "running",
            "--workspace-id",
            "5",
        ]

        verifylist = [
            ("cluster_id", "4"),
            ("infer_type", "real-time"),
            ("limit", 7),
            ("model_id", "3"),
            ("offset", 6),
            ("order", "asc"),
            ("service_id", "1"),
            ("service_name", "2"),
            ("sort_by", "service_name"),
            ("status", "running"),
            ("workspace_id", "5"),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(
            cluster_id="4",
            infer_type="real-time",
            limit=7,
            model_id="3",
            offset=6,
            order="asc",
            service_id="1",
            service_name="2",
            sort_by="service_name",
            status="running",
            workspace_id="5",
        )


# class TestCreateService(fakes.TestModelartsv1):
#     _service = fakes.FakeService.create_one()
#     columns = _COLUMNS
#     data = fakes.gen_data(_service, columns, service._formatters)

#     def setUp(self):
#         super(TestCreateService, self).setUp()

#         self.cmd = service.CreateService(self.app, None)

#         self.client.create_service = mock.Mock(return_value=self._service)

#     def test_create(self):
#         arglist = [
#             "test-service",
#             "--infer-type",
#             "https://models.obs.xxxx.com/mnist",
#             "--config",
#             "TensorFlow",
#         ]
#         verifylist = [
#             ("name", "test-service"),
#             ("infer_type", "https://models.obs.xxxx.com/mnist"),
#             ("config", "TensorFlow"),
#         ]
#         # Verify cm is triggereg with default parameters
#         parsed_args = self.check_parser(self.cmd, arglist, verifylist)

#         # Trigger the action
#         columns, data = self.cmd.take_action(parsed_args)
#         attrs = {
#             "service_name": "test-service",
#             "infer_type": "https://models.obs.xxxx.com/mnist",
#             "config": "TensorFlow",
#         }
#         self.client.create_service.assert_called_with(**attrs)
#         # self.client.wait_for_cluster.assert_called_with(
#         #    self._cluster.id, wait=self.default_timeout)
#         # self.client.find_model.assert_called_with(self._model.id)
#         self.assertEqual(self.columns, columns)
#         self.assertEqual(self.data, data)


class TestShowService(fakes.TestModelartsv1):
    _service = fakes.FakeService.create_one()
    columns = _COLUMNS
    data = fakes.gen_data(_service, columns, service.service._formatters)

    def setUp(self):
        super(TestShowService, self).setUp()

        self.cmd = service.ShowService(self.app, None)

        self.client.find_service = mock.Mock(return_value=self._service)
        # self.client.get_model = mock.Mock(return_value=self._model)

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
            self._service.id,
        ]

        verifylist = [("service", self._service.id)]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.find_service.assert_called_with(self._service.id)

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)

    def test_show_non_existent(self):
        arglist = ["unexist_ma_service"]

        verifylist = [("service", "unexist_ma_service")]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_result = exceptions.CommandError("Resource Not Found")
        self.client.find_service = mock.Mock(side_effect=find_mock_result)

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual("Resource Not Found", str(e))
        self.client.find_service.assert_called_with("unexist_ma_service")


class TestDeleteService(fakes.TestModelartsv1):
    _service = fakes.FakeService.create_multiple(2)

    def setUp(self):
        super(TestDeleteService, self).setUp()

        self.client.find_service = mock.Mock(return_value=self._service[0])
        self.client.delete_service = mock.Mock(return_value=None)

        # Get the command object to test
        self.cmd = service.DeleteService(self.app, None)

    def test_delete(self):
        arglist = [
            self._service[0].name,
        ]

        verifylist = [
            ("service", arglist),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.find_service.assert_called_with(
            self._service[0].name, ignore_missing=False
        )
        self.client.delete_service.assert_called_with(self._service[0].id)
        self.assertIsNone(result)

    def test_multiple_delete(self):
        arglist = []

        for ma_service in self._service:
            arglist.append(ma_service.name)

        verifylist = [("service", arglist)]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_results = self._service
        self.client.find_service = mock.Mock(side_effect=find_mock_results)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)

        find_calls = []
        delete_calls = []
        for ma_service in self._service:
            find_calls.append(call(ma_service.name, ignore_missing=False))
            delete_calls.append(call(ma_service.id))
        self.client.find_service.assert_has_calls(find_calls)
        self.client.delete_service.assert_has_calls(delete_calls)
        self.assertIsNone(result)

    def test_multiple_delete_with_exception(self):
        arglist = [
            self._service[0].id,
            "unexist_ma_service",
        ]
        verifylist = [("service", arglist)]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_results = [self._service[0], exceptions.CommandError]
        self.client.find_service = mock.Mock(side_effect=find_mock_results)

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual("1 of 2 Service(s) failed to delete.", str(e))

        self.client.delete_service.assert_any_call(self._service[0].id)
