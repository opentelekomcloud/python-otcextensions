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
from otcextensions.osclient.modelartsv1.v1 import devenv
from otcextensions.tests.unit.osclient.modelartsv1.v1 import fakes

# from osc_lib.cli import format_columns


_COLUMNS = (
    "created_at",
    "description",
    "flavor",
    "flavor_details",
    "id",
    "name",
    "profile",
    "spec",
    "status",
    "updated_at",
    "user",
)


class TestListDevenvInstances(fakes.TestModelartsv1):
    objects = fakes.FakeDevenv.create_multiple(3)

    column_list_headers = ("ID", "Name", "status", "Created At")

    columns = ("id", "name", "status", "created_at")

    data = []

    for s in objects:
        data.append(
            (
                s.id,
                s.name,
                s.status,
                cli_utils.UnixTimestampFormatter(s.created_at),
            )
        )

    def setUp(self):
        super(TestListDevenvInstances, self).setUp()

        self.cmd = devenv.ListDevenvInstances(self.app, None)

        self.client.devenv_instances = mock.Mock()
        self.client.api_mock = self.client.devenv_instances

    def test_list(self):
        arglist = []

        verifylist = [
            ("de_type", "Notebook"),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(de_type="Notebook")

        self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(self.data, list(data))

    def test_list_args(self):
        arglist = [
            "--de-type",
            "1",
            "--provision-type",
            "2",
            "--status",
            "running",
            "--sort-by",
            "name",
            "--order",
            "asc",
            "--offset",
            "6",
            "--limit",
            "7",
            "--workspace-id",
            "8",
            "--ai-project-id",
            "9",
            "--pool-id",
            "10",
            "--show-self",
        ]

        verifylist = [
            ("de_type", "1"),
            ("provision_type", "2"),
            ("status", "RUNNING"),
            ("sortby", "name"),
            ("order", "asc"),
            ("offset", 6),
            ("limit", 7),
            ("workspace_id", "8"),
            ("ai_project", "9"),
            ("pool_id", "10"),
            ("show_self", True),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(
            ai_project="9",
            de_type="1",
            limit=7,
            offset=6,
            order="asc",
            pool_id="10",
            provision_type="2",
            show_self=True,
            sortby="name",
            status="RUNNING",
            workspace_id="8",
        )


class TestCreateDevenvInstance(fakes.TestModelartsv1):
    _data = fakes.FakeDevenv.create_one()
    columns = _COLUMNS
    data = fakes.gen_data(_data, columns, devenv._formatters)
    default_timeout = 1800

    def setUp(self):
        super(TestCreateDevenvInstance, self).setUp()

        self.cmd = devenv.CreateDevenvInstance(self.app, None)

        self.client.create_devenv_instance = mock.Mock(
            return_value=self._data
        )

    def test_create(self):
        arglist = [
            "test-devenv",
            "--profile-id",
            "1",
            "--description",
            "2",
            "--flavor",
            "3",
            "--ai-project-id",
            "4",
            "--workspace-id",
            "5",
            "--storage-type",
            "6",
            "--storage-path",
            "7",
            "--extended-storage-type",
            "8",
            "--extended-storage-path",
            "9",
            "--autostop-duration",
            "10",
            "--autostop-prompt",
            False,
            "--pool-id",
            "11",
            "--pool-type",
            "12",
            "--pool-name",
            "13",
            "--annotation",
            "key1=value1",
            "--annotation",
            "key2=value2",
        ]
        verifylist = [
            ("name", "test-devenv"),
            ("profile_id", 1),
            ("description", "2"),
            ("flavor", "3"),
            ("ai_project_id", "4"),
            ("workspace_id", "5"),
            ("storage_type", "6"),
            ("storage_path", "7"),
            ("extended_storage_type", "8"),
            ("extended_storage_path", "9"),
            ("autostop_duration", 10),
            ("autostop_prompt", False),
            ("pool_id", "11"),
            ("pool_type", "12"),
            ("pool_name", "13"),
            ("annotation", {"key1": "value1", "key2": "value2"}),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        attrs = {
            "name": "test-devenv",
            "flavor": "3",
            "profile_id": "Multi-Engine 1.0 (python3)-cpu",
            "spec": {
                "storage": {"location": {"path": "7"}, "type": "6"},
                "auto_stop": {"enable": True, "duration": 10},
                "extended_storage": {
                    "location": {"path": "9"},
                    "type": "8",
                },
            },
            "description": "2",
            "workspace": {"id": "5"},
            "ai_project": {"id": "4"},
            "pool": {"name": "13"},
            "annotations": {"key1": "value1", "key2": "value2"},
        }
        self.client.create_devenv_instance.assert_called_with(**attrs)
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestUpdateDevenvInstance(fakes.TestModelartsv1):
    _data = fakes.FakeDevenv.create_one()

    columns = _COLUMNS

    data = fakes.gen_data(_data, columns, devenv._formatters)

    default_timeout = 1800

    def setUp(self):
        super(TestUpdateDevenvInstance, self).setUp()

        self.cmd = devenv.UpdateDevenvInstance(self.app, None)

        self.client.update_devenv_instance = mock.Mock(
            return_value=self._data
        )

    def test_update(self):
        arglist = [
            "devenv-instance-id",
            "--description",
            "New Description",
            "--auto-stop",
            "enable",
            "--duration",
            "3600",
            "--prompt",
            "disable",
        ]
        verifylist = [
            ("instance", "devenv-instance-id"),
            ("description", "New Description"),
            ("auto_stop", "enable"),
            ("duration", 3600),
            ("prompt", "disable"),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        attrs = {
            "auto_stop": {
                "enable": True,
                "prompt": False,
                "duration": 3600,
            },
            "description": "New Description",
        }
        self.client.update_devenv_instance.assert_called_with(
            "devenv-instance-id", **attrs
        )
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestStartDevenvInstance(fakes.TestModelartsv1):
    _devenv = fakes.FakeDevenv.create_one()
    columns = _COLUMNS
    data = fakes.gen_data(_devenv, columns, devenv._formatters)

    def setUp(self):
        super(TestStartDevenvInstance, self).setUp()

        self.cmd = devenv.StartDevenvInstance(self.app, None)

        self.client.find_devenv_instance = mock.Mock(
            return_value=self._devenv
        )
        self.client.start_devenv_instance = mock.Mock(
            return_value=self._devenv
        )

    def test_start(self):
        arglist = [
            self._devenv.id,
        ]

        verifylist = [
            ("instance", self._devenv.id),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        self.cmd.take_action(parsed_args)
        self.client.find_devenv_instance.assert_called_with(
            self._devenv.id, ignore_missing=False
        )
        self.client.start_devenv_instance.assert_called_with(
            self._devenv.id
        )


class TestStopDevenvInstance(fakes.TestModelartsv1):
    _devenv = fakes.FakeDevenv.create_one()
    columns = _COLUMNS
    data = fakes.gen_data(_devenv, columns, devenv._formatters)

    def setUp(self):
        super(TestStopDevenvInstance, self).setUp()

        self.cmd = devenv.StopDevenvInstance(self.app, None)

        self.client.find_devenv_instance = mock.Mock(
            return_value=self._devenv
        )
        self.client.stop_devenv_instance = mock.Mock(
            return_value=self._devenv
        )

    def test_start(self):
        arglist = [
            self._devenv.id,
        ]

        verifylist = [
            ("instance", self._devenv.id),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        self.cmd.take_action(parsed_args)
        self.client.find_devenv_instance.assert_called_with(
            self._devenv.id, ignore_missing=False
        )
        self.client.stop_devenv_instance.assert_called_with(
            self._devenv.id
        )


class TestShowDevenvInstance(fakes.TestModelartsv1):
    _devenv = fakes.FakeDevenv.create_one()
    columns = _COLUMNS
    data = fakes.gen_data(_devenv, columns, devenv._formatters)

    def setUp(self):
        super(TestShowDevenvInstance, self).setUp()

        self.cmd = devenv.ShowDevenvInstance(self.app, None)

        self.client.find_devenv_instance = mock.Mock(
            return_value=self._devenv
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
            self._devenv.id,
        ]

        verifylist = [
            ("instance", self._devenv.id),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.find_devenv_instance.assert_called_with(
            self._devenv.id
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)

    def test_show_non_existent(self):
        arglist = [
            "unexist_devenv_instance",
        ]

        verifylist = [
            ("instance", "unexist_devenv_instance"),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_result = exceptions.CommandError(
            "Resource Not Found"
        )
        self.client.find_devenv_instance = mock.Mock(
            side_effect=find_mock_result
        )

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual("Resource Not Found", str(e))
        self.client.find_devenv_instance.assert_called_with(
            "unexist_devenv_instance"
        )


class TestDeleteDevenvInstance(fakes.TestModelartsv1):
    _devenv = fakes.FakeDevenv.create_multiple(2)

    def setUp(self):
        super(TestDeleteDevenvInstance, self).setUp()

        self.client.find_devenv_instance = mock.Mock(
            return_value=self._devenv[0]
        )
        self.client.delete_devenv_instance = mock.Mock(
            return_value=None
        )

        # Get the command object to test
        self.cmd = devenv.DeleteDevenvInstance(self.app, None)

    def test_delete(self):
        arglist = [
            self._devenv[0].name,
        ]

        verifylist = [
            ("instance", arglist),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.find_devenv_instance.assert_called_with(
            self._devenv[0].name, ignore_missing=False
        )
        self.client.delete_devenv_instance.assert_called_with(
            self._devenv[0].id
        )
        self.assertIsNone(result)

    def test_multiple_delete(self):
        arglist = []

        for instance in self._devenv:
            arglist.append(instance.name)

        verifylist = [
            ("instance", arglist),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_results = self._devenv
        self.client.find_devenv_instance = mock.Mock(
            side_effect=find_mock_results
        )

        # Trigger the action
        result = self.cmd.take_action(parsed_args)

        find_calls = []
        delete_calls = []
        for instance in self._devenv:
            find_calls.append(
                call(instance.name, ignore_missing=False)
            )
            delete_calls.append(call(instance.id))
        self.client.find_devenv_instance.assert_has_calls(find_calls)
        self.client.delete_devenv_instance.assert_has_calls(
            delete_calls
        )
        self.assertIsNone(result)

    def test_multiple_delete_with_exception(self):
        arglist = [
            self._devenv[0].id,
            "unexist_devenv_instance",
        ]
        verifylist = [
            ("instance", arglist),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_results = [self._devenv[0], exceptions.CommandError]
        self.client.find_devenv_instance = mock.Mock(
            side_effect=find_mock_results
        )

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual(
                "1 of 2 Devenv Instance(s) failed to delete.", str(e)
            )

        self.client.delete_devenv_instance.assert_any_call(
            self._devenv[0].id
        )
