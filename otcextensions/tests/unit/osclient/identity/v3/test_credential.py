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
# from unittest.mock import call

# from osc_lib import exceptions

from otcextensions.osclient.identity.v3 import credential
from otcextensions.tests.unit.osclient.identity.v3 import fakes

# from openstackclient.tests.unit import utils as tests_utils


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
