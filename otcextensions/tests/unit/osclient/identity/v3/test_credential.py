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

from otcextensions.osclient.identity.v3 import credential
from otcextensions.tests.unit.osclient.identity.v3 import fakes

from openstackclient.tests.unit import utils as tests_utils


class TestListIdentityCredentials(fakes.TestIdentity):

    objects = fakes.FakeIdentityCredential.create_multiple(3)

    column_list_headers = (
        'Access Key',
        'Description',
        'User ID',
        'Status',
        'Created At',
    )

    columns = (
        'access',
        'description',
        'user_id',
        'status',
        'created_at',
    )

    data = []

    for o in objects:
        data.append(
            (o.id, o.description, o.user_id, o.status, o.created_at))

    def setUp(self):
        super(TestListIdentityCredentials, self).setUp()

        self.cmd = credential.ListCredentials(self.app, None)

        self.client.credentials = mock.Mock()
        self.client.api_mock = self.client.credentials

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
            '--user-id', '1'
        ]

        verifylist = [
            ('user_id', '1'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(
            user_id='1',
        )


class TestCreateIdentityCredential(fakes.TestIdentity):

    _data = fakes.FakeIdentityCredential.create_one()

    columns = (
        'access',
        'created_at',
        'description',
        'id',
        'status',
        'user_id'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestCreateIdentityCredential, self).setUp()

        self.cmd = credential.CreateCredential(self.app, None)

        self.client.create_credential = mock.Mock(return_value=self._data)

    def test_create(self):
        arglist = [
            'user-id',
            '--description', 'description',
        ]
        verifylist = [
            ('user_id', 'user-id'),
            ('description', 'description'),
        ]
        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_credential.assert_called_with(
            user_id='user-id',
            description='description',
        )
        self.assertEqual(self.columns, columns)


class TestUpdateIdentityCredential(fakes.TestIdentity):

    _data = fakes.FakeIdentityCredential.create_one()

    columns = (
        'access',
        'created_at',
        'description',
        'id',
        'status',
        'user_id'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestUpdateIdentityCredential, self).setUp()

        self.cmd = credential.UpdateCredential(self.app, None)

        self.client.find_credential = mock.Mock(return_value=self._data)
        self.client.update_credential = mock.Mock(return_value=self._data)

    def test_update(self):
        arglist = [
            self._data.access,
            '--description', 'description2',
            '--status', 'inactive',
        ]
        verifylist = [
            ('credential', self._data.access),
            ('description', 'description2'),
            ('status', 'inactive'),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_credential.assert_called_with(self._data.access)
        self.client.update_credential.assert_called_with(
            self._data.id,
            description='description2',
            status='inactive'
        )
        self.assertEqual(self.columns, columns)


class TestShowIdentityCredential(fakes.TestIdentity):

    _data = fakes.FakeIdentityCredential.create_one()

    columns = (
        'access',
        'created_at',
        'description',
        'id',
        'status',
        'user_id'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestShowIdentityCredential, self).setUp()

        self.cmd = credential.ShowCredential(self.app, None)

        self.client.find_credential = mock.Mock(return_value=self._data)

    def test_show_no_options(self):
        arglist = []
        verifylist = []

        # Testing that a call without the required argument will fail and
        # throw a "ParserExecption"
        self.assertRaises(tests_utils.ParserException,
                          self.check_parser, self.cmd, arglist, verifylist)

    def test_show(self):
        arglist = [
            self._data.access,
        ]

        verifylist = [
            ('credential', self._data.id),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.find_credential.assert_called_with(self._data.id)

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)

    def test_show_non_existent(self):
        arglist = [
            'unexist_identity_credential',
        ]

        verifylist = [
            ('credential', 'unexist_identity_credential'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_result = exceptions.CommandError('Resource Not Found')
        self.client.find_credential = (
            mock.Mock(side_effect=find_mock_result)
        )

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual('Resource Not Found', str(e))
        self.client.find_credential.assert_called_with(
            'unexist_identity_credential')


class TestDeleteIdentityCredential(fakes.TestIdentity):

    _data = fakes.FakeIdentityCredential.create_multiple(2)

    def setUp(self):
        super(TestDeleteIdentityCredential, self).setUp()

        self.client.delete_credential = mock.Mock(return_value=None)

        # Get the command object to test
        self.cmd = credential.DeleteCredential(self.app, None)

    def test_delete(self):
        arglist = [
            self._data[0].access,
        ]

        verifylist = [
            ('credential', [self._data[0].access]),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.client.find_credential = (
            mock.Mock(return_value=self._data[0])
        )

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.delete_credential.assert_called_with(self._data[0].id)
        self.assertIsNone(result)

    def test_multiple_delete(self):
        arglist = []

        for obj in self._data:
            arglist.append(obj.id)

        verifylist = [
            ('credential', arglist),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_result = self._data
        self.client.find_credential = (
            mock.Mock(side_effect=find_mock_result)
        )

        # Trigger the action
        result = self.cmd.take_action(parsed_args)

        calls = []
        for obj in self._data:
            calls.append(call(obj.id))
        self.client.delete_credential.assert_has_calls(calls)
        self.assertIsNone(result)
