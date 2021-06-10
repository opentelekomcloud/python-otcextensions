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

from otcextensions.osclient.smn.v2 import template
from otcextensions.tests.unit.osclient.smn.v2 import fakes

from openstackclient.tests.unit import utils as tests_utils


class TestListTemplate(fakes.TestSmn):

    objects = fakes.FakeTemplate.create_multiple(3)

    column_list_headers = (
        'ID',
        'Name',
        'Protocol'
    )

    columns = (
        'id',
        'name',
        'protocol'
    )

    data = []

    for s in objects:
        data.append(
            (s.id, s.name, s.protocol))

    def setUp(self):
        super(TestListTemplate, self).setUp()

        self.cmd = template.ListTemplate(self.app, None)

        self.client.templates = mock.Mock()
        self.client.api_mock = self.client.templates

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
            '--offset', '2',
            '--name', '3',
            '--protocol', 'email'
        ]

        verifylist = [
            ('limit', 1),
            ('offset', 2),
            ('name', '3'),
            ('protocol', 'email'),
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
            name='3',
            protocol='email',
        )


class TestCreateTemplate(fakes.TestSmn):

    _data = fakes.FakeTemplate.create_one()

    columns = (
        'content',
        'create_time',
        'id',
        'name',
        'protocol',
        'request_id',
        'tag_names',
        'update_time')

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestCreateTemplate, self).setUp()

        self.cmd = template.CreateTemplate(self.app, None)

        self.client.create_template = mock.Mock(return_value=self._data)

    def test_create(self):
        arglist = [
            'test-template',
            '--protocol', 'email',
            '--content', 'test-content',
        ]
        verifylist = [
            ('name', 'test-template'),
            ('protocol', 'email'),
            ('content', 'test-content'),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_template.assert_called_with(
            name='test-template',
            protocol='email',
            content='test-content',
        )
        self.assertEqual(self.columns, columns)


class TestUpdateTemplate(fakes.TestSmn):

    _data = fakes.FakeTemplate.create_one()

    columns = (
        'content',
        'create_time',
        'id',
        'name',
        'protocol',
        'request_id',
        'tag_names',
        'update_time'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestUpdateTemplate, self).setUp()

        self.cmd = template.UpdateTemplate(self.app, None)

        self.client.find_template = mock.Mock(return_value=self._data)
        self.client.update_template = mock.Mock(return_value=self._data)

    def test_update(self):
        arglist = [
            self._data.name,
            '--content', 'test content updated',
        ]
        verifylist = [
            ('template', self._data.name),
            ('content', 'test content updated'),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_template.assert_called_with(self._data.name)
        self.client.update_template.assert_called_with(
            self._data,
            content='test content updated',
        )
        self.assertEqual(self.columns, columns)


class TestShowTemplate(fakes.TestSmn):

    _data = fakes.FakeTemplate.create_one()

    columns = (
        'content',
        'create_time',
        'id',
        'name',
        'protocol',
        'request_id',
        'tag_names',
        'update_time'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestShowTemplate, self).setUp()

        self.cmd = template.ShowTemplate(self.app, None)

        self.client.find_template = mock.Mock(return_value=self._data)

    def test_show_no_options(self):
        arglist = []
        verifylist = []

        # Testing that a call without the required argument will fail and
        # throw a "ParserExecption"
        self.assertRaises(tests_utils.ParserException,
                          self.check_parser, self.cmd, arglist, verifylist)

    def test_show(self):
        arglist = [
            self._data.id,
        ]

        verifylist = [
            ('template', self._data.id),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.find_template.assert_called_with(self._data.id)

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)

    def test_show_non_existent(self):
        arglist = [
            'unexist_template',
        ]

        verifylist = [
            ('template', 'unexist_template'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_result = exceptions.CommandError('Resource Not Found')
        self.client.find_template = (
            mock.Mock(side_effect=find_mock_result)
        )

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual('Resource Not Found', str(e))
        self.client.find_template.assert_called_with('unexist_template')


class TestDeleteTemplate(fakes.TestSmn):

    _data = fakes.FakeTemplate.create_multiple(2)

    def setUp(self):
        super(TestDeleteTemplate, self).setUp()

        self.client.delete_template = mock.Mock(return_value=None)

        # Get the command object to test
        self.cmd = template.DeleteTemplate(self.app, None)

    def test_delete(self):
        arglist = [
            self._data[0].name,
        ]

        verifylist = [
            ('template', [self._data[0].name]),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.client.find_template = (
            mock.Mock(return_value=self._data[0])
        )

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.delete_template.assert_called_with(self._data[0])
        self.assertIsNone(result)

    def test_multiple_delete(self):
        arglist = []

        for data in self._data:
            arglist.append(data.name)

        verifylist = [
            ('template', arglist),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_result = self._data
        self.client.find_template = (
            mock.Mock(side_effect=find_mock_result)
        )

        # Trigger the action
        result = self.cmd.take_action(parsed_args)

        calls = []
        for data in self._data:
            calls.append(call(data))
        self.client.delete_template.assert_has_calls(calls)
        self.assertIsNone(result)

    def test_multiple_delete_with_exception(self):
        arglist = [
            self._data[0].name,
            'unexist_template',
        ]
        verifylist = [
            ('template', arglist),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_result = [self._data[0], exceptions.CommandError]
        self.client.find_template = (
            mock.Mock(side_effect=find_mock_result)
        )

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual(
                '1 of 2 message template(s) failed to delete.', str(e))

        self.client.find_template.assert_any_call(self._data[0].name)
        self.client.find_template.assert_any_call('unexist_template')
        self.client.delete_template.assert_called_once_with(self._data[0])
