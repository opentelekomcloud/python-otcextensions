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

from otcextensions.osclient.smn.v2 import topic
from otcextensions.tests.unit.osclient.smn.v2 import fakes

from openstackclient.tests.unit import utils as tests_utils


class TestListTopic(fakes.TestSmn):

    objects = fakes.FakeTopic.create_multiple(3)

    column_list_headers = ('Topic Urn', 'Name', 'Display Name', 'Push Policy')

    columns = ('topic_urn', 'name', 'display_name', 'push_policy')

    data = []

    for s in objects:
        data.append(
            (s.topic_urn, s.name, s.display_name, s.push_policy))

    def setUp(self):
        super(TestListTopic, self).setUp()

        self.cmd = topic.ListTopic(self.app, None)

        self.client.topics = mock.Mock()
        self.client.api_mock = self.client.topics

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
            '--offset', '2'
        ]

        verifylist = [
            ('limit', 1),
            ('offset', 2),
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
        )


class TestCreateTopic(fakes.TestSmn):

    _data = fakes.FakeTopic.create_one()

    columns = (
        'request_id',
        'topic_urn'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestCreateTopic, self).setUp()

        self.cmd = topic.CreateTopic(self.app, None)

        self.client.create_topic = mock.Mock(return_value=self._data)

    def test_create(self):
        arglist = [
            'test-topic',
            '--display-name', 'topic_display_name',
        ]
        verifylist = [
            ('name', 'test-topic'),
            ('display_name', 'topic_display_name'),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_topic.assert_called_with(
            name='test-topic',
            display_name='topic_display_name',
        )
        self.assertEqual(self.columns, columns)


class TestUpdateTopic(fakes.TestSmn):

    _data = fakes.FakeTopic.create_one()

    columns = (
        'create_time',
        'display_name',
        'name',
        'push_policy',
        'request_id',
        'topic_urn',
        'update_time'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestUpdateTopic, self).setUp()

        self.cmd = topic.UpdateTopic(self.app, None)

        self.client.find_topic = mock.Mock(return_value=self._data)
        self.client.update_topic = mock.Mock(return_value=self._data)

    def test_update(self):
        arglist = [
            self._data.name,
            '--display-name', 'topic display name updated',
        ]
        verifylist = [
            ('topic', self._data.name),
            ('display_name', 'topic display name updated'),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_topic.assert_called_with(self._data.name)
        self.client.update_topic.assert_called_with(
            self._data,
            display_name='topic display name updated',
        )
        self.assertEqual(self.columns, columns)


class TestShowTopic(fakes.TestSmn):

    _data = fakes.FakeTopic.create_one()

    columns = (
        'create_time',
        'display_name',
        'name',
        'push_policy',
        'request_id',
        'topic_urn',
        'update_time'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestShowTopic, self).setUp()

        self.cmd = topic.ShowTopic(self.app, None)

        self.client.find_topic = mock.Mock(return_value=self._data)

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
            ('topic', self._data.id),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.find_topic.assert_called_with(self._data.id)

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)

    def test_show_non_existent(self):
        arglist = [
            'unexist_topic',
        ]

        verifylist = [
            ('topic', 'unexist_topic'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_result = exceptions.CommandError('Resource Not Found')
        self.client.find_topic = (
            mock.Mock(side_effect=find_mock_result)
        )

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual('Resource Not Found', str(e))
        self.client.find_topic.assert_called_with('unexist_topic')


class TestDeleteTopic(fakes.TestSmn):

    _data = fakes.FakeTopic.create_multiple(2)

    def setUp(self):
        super(TestDeleteTopic, self).setUp()

        self.client.delete_topic = mock.Mock(return_value=None)

        # Get the command object to test
        self.cmd = topic.DeleteTopic(self.app, None)

    def test_delete(self):
        arglist = [
            self._data[0].name,
        ]

        verifylist = [
            ('topic', [self._data[0].name]),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.client.find_topic = (
            mock.Mock(return_value=self._data[0])
        )

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.delete_topic.assert_called_with(self._data[0])
        self.assertIsNone(result)

    def test_multiple_delete(self):
        arglist = []

        for data in self._data:
            arglist.append(data.name)

        verifylist = [
            ('topic', arglist),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_result = self._data
        self.client.find_topic = (
            mock.Mock(side_effect=find_mock_result)
        )

        # Trigger the action
        result = self.cmd.take_action(parsed_args)

        calls = []
        for data in self._data:
            calls.append(call(data))
        self.client.delete_topic.assert_has_calls(calls)
        self.assertIsNone(result)

    def test_multiple_delete_with_exception(self):
        arglist = [
            self._data[0].name,
            'unexist_topic',
        ]
        verifylist = [
            ('topic', arglist),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_result = [self._data[0], exceptions.CommandError]
        self.client.find_topic = (
            mock.Mock(side_effect=find_mock_result)
        )

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual('1 of 2 SMN Topic(s) failed to delete.', str(e))

        self.client.find_topic.assert_any_call(self._data[0].name)
        self.client.find_topic.assert_any_call('unexist_topic')
        self.client.delete_topic.assert_called_once_with(self._data[0])
