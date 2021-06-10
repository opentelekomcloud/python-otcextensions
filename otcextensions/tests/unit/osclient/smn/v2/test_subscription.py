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

from otcextensions.osclient.smn.v2 import subscription
from otcextensions.tests.unit.osclient.smn.v2 import fakes


class TestListSubscription(fakes.TestSmn):

    objects = fakes.FakeSubscription.create_multiple(3)
    _topic = fakes.FakeTopic.create_one()

    column_list_headers = (
        'ID',
        'Protocol',
        'Topic URN',
        'Owner',
        'Endpoint',
        'Status'
    )

    columns = (
        'id',
        'protocol',
        'topic_urn',
        'owner',
        'endpoint',
        'status'
    )

    data = []

    for s in objects:
        data.append(
            (s.id,
             s.protocol,
             s.topic_urn,
             s.owner,
             s.endpoint,
             s.status))

    def setUp(self):
        super(TestListSubscription, self).setUp()

        self.cmd = subscription.ListSubscription(self.app, None)

        self.client.get_topic = mock.Mock(return_value=self._topic)
        self.client.subscriptions = mock.Mock()
        self.client.api_mock = self.client.subscriptions

    def test_list(self):
        arglist = []

        verifylist = []

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(None)

        self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(self.data, list(data))

    def test_list_args(self):
        arglist = [
            '--topic', '1',
            '--limit', '2',
            '--offset', '3'
        ]

        verifylist = [
            ('topic', '1'),
            ('limit', 2),
            ('offset', 3),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(
            self._topic,
            limit=2,
            offset=3,
        )


class TestCreateSubscription(fakes.TestSmn):

    _data = fakes.FakeSubscription.create_one()
    _topic = fakes.FakeTopic.create_one()

    columns = ('endpoint', 'id', 'owner', 'protocol', 'remark', 'status')

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestCreateSubscription, self).setUp()

        self.client.get_topic = mock.Mock(return_value=self._topic)
        self.cmd = subscription.CreateSubscription(self.app, None)

        self.client.create_subscription = mock.Mock(return_value=self._data)

    def test_create(self):
        arglist = [
            'test-topic',
            '--endpoint', 'test@otce.com',
            '--protocol', 'email',
            '--remark', 'test subscription',
        ]
        verifylist = [
            ('topic', 'test-topic'),
            ('endpoint', 'test@otce.com'),
            ('protocol', 'email'),
            ('remark', 'test subscription'),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_subscription.assert_called_with(
            self._topic,
            endpoint='test@otce.com',
            protocol='email',
            remark='test subscription',
        )
        self.assertEqual(self.columns, columns)


class TestDeleteSubscription(fakes.TestSmn):

    _data = fakes.FakeSubscription.create_multiple(2)

    def setUp(self):
        super(TestDeleteSubscription, self).setUp()

        self.client.delete_subscription = mock.Mock(return_value=None)

        # Get the command object to test
        self.cmd = subscription.DeleteSubscription(self.app, None)

    def test_delete(self):
        arglist = ['subscription-urn']

        verifylist = [
            ('subscription', arglist),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.delete_subscription.assert_called_with(
            'subscription-urn', ignore_missing=False)
        self.assertIsNone(result)

    def test_multiple_delete(self):
        arglist = []

        for data in self._data:
            arglist.append(data.id)

        verifylist = [
            ('subscription', arglist),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)

        calls = []
        for data in self._data:
            calls.append(call(data.id, ignore_missing=False))
        self.client.delete_subscription.assert_has_calls(calls)
        self.assertIsNone(result)

    def test_multiple_delete_with_exception(self):
        arglist = [
            self._data[0].id,
            'unexist_subscription',
        ]
        verifylist = [
            ('subscription', arglist),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_result = [None, exceptions.CommandError]
        self.client.delete_subscription = (
            mock.Mock(side_effect=find_mock_result)
        )

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual(
                '1 of 2 SMN Subscription(s) failed to delete.', str(e))

        self.client.delete_subscription.assert_any_call(
            self._data[0].id, ignore_missing=False)
        self.client.delete_subscription.assert_any_call(
            'unexist_subscription', ignore_missing=False)
