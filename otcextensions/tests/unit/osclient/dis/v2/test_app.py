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

from otcextensions.osclient.dis.v2 import app
from otcextensions.sdk.dis.v2 import app as sdk_app
from otcextensions.common import cli_utils
from otcextensions.tests.unit.osclient.dis.v2 import fakes

from openstackclient.tests.unit import utils as tests_utils


class TestListApps(fakes.TestDis):

    objects = fakes.FakeApp.create_multiple(3)

    column_list_headers = (
        'App Name',
        'Id',
        'Created At',
    )

    columns = (
        'name',
        'id',
        'created_at',
    )

    data = []

    for s in objects:
        data.append((
            s.name,
            s.id,
            cli_utils.UnixTimestampFormatter(s.created_at),
        ))

    def setUp(self):
        super(TestListApps, self).setUp()

        self.cmd = app.ListApps(self.app, None)

        self.client.apps = mock.Mock()
        self.client.api_mock = self.client.apps

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
            '--limit', '1',
            '--start-app-name', '2',
            '--stream-name', '3',
        ]

        verifylist = [
            ('limit', 1),
            ('start_app_name', '2'),
            ('stream_name', '3'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(
            limit=1,
            start_app_name='2',
            stream_name='3',
        )


class TestCreateApp(fakes.TestDis):

    columns = (
        'name',
    )

    def setUp(self):
        super(TestCreateApp, self).setUp()

        self.cmd = app.CreateApp(self.app, None)

    def test_create(self):
        arglist = [
            'test-app',
        ]
        verifylist = [
            ('appName', 'test-app'),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        attrs = {}
        attrs.update(
            app_name='test-app',
        )

        self.client.create_app = mock.Mock(
            return_value=sdk_app.App(**attrs))

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_app.assert_called_with(**attrs)
        self.assertEqual(self.columns, columns)


class TestShowApp(fakes.TestDis):

    _data = fakes.FakeApp.create_one()
    columns = (
        'commit_checkpoint_stream_names',
        'created_at',
        'id',
        'name',
    )

    data = fakes.gen_data(_data, columns, app._formatters)

    def setUp(self):
        super(TestShowApp, self).setUp()

        self.cmd = app.ShowApp(self.app, None)

        self.client.get_app = mock.Mock(return_value=self._data)

    def test_show_no_options(self):
        arglist = []
        verifylist = []

        # Testing that a call without the required argument will fail and
        # throw a "ParserExecption"
        self.assertRaises(tests_utils.ParserException,
                          self.check_parser, self.cmd, arglist, verifylist)

    def test_show(self):
        arglist = [
            self._data.name,
        ]

        verifylist = [
            ('appName', self._data.name),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.get_app.assert_called_with(self._data.name)

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)

    def test_show_non_existent(self):
        arglist = [
            'unexist_dis_app',
        ]

        verifylist = [
            ('appName', 'unexist_dis_app'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        get_mock_result = exceptions.CommandError('Resource Not Found')
        self.client.find_app = (
            mock.Mock(side_effect=get_mock_result)
        )

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual('Resource Not Found', str(e))
        self.client.get_app.assert_called_with('unexist_dis_app')


class TestDeleteApp(fakes.TestDis):

    _data = fakes.FakeApp.create_multiple(2)

    def setUp(self):
        super(TestDeleteApp, self).setUp()

        self.client.delete_app = mock.Mock(return_value=None)

        # Get the command object to test
        self.cmd = app.DeleteApp(self.app, None)

    def test_delete(self):
        arglist = [
            self._data[0].name,
        ]

        verifylist = [
            ('appName', [self._data[0].name]),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.delete_app.assert_called_with(self._data[0].name)
        self.assertIsNone(result)

    def test_multiple_delete(self):
        arglist = []

        for dis_app in self._data:
            arglist.append(dis_app.name)

        verifylist = [
            ('appName', arglist),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)

        calls = []
        for dis_app in self._data:
            calls.append(call(dis_app.name))
        self.client.delete_app.assert_has_calls(calls)
        self.assertIsNone(result)

    def test_multiple_delete_with_exception(self):
        arglist = [
            self._data[0].name,
            'unexist_dis_app',
        ]
        verifylist = [
            ('appName', arglist),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # delete_mock_result = [None, exceptions.CommandError]

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual('1 of 2 DIS App(s) failed to delete.', str(e))

        calls = [call(self._data[0].name), call('unexist_dis_app')]
        self.client.delete_app.assert_has_calls(calls)
