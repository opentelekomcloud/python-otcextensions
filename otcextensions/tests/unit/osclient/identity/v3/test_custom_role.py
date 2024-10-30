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

import mock

from otcextensions.osclient.identity.v3 import custom_role
from otcextensions.tests.unit.osclient.identity.v3 import fakes


class TestListIdentityCustomRoles(fakes.TestIdentity):

    objects = fakes.FakeIdentityCustomRole.create_multiple(3)

    column_list_headers = (
        'ID',
        'Name',
        'Description',
        'Domain ID',
        'References',
        'Catalog',
        'Display name',
        'Type',
        'Created At',
        'Updated At',
    )

    columns = (
        'id',
        'name',
        'description',
        'domain_id',
        'references',
        'catalog',
        'display_name',
        'type',
        'created_at',
        'updated_at',
    )

    data = []

    for o in objects:
        data.append(
            (o.id, o.name, o.description, o.domain_id, o.references,
             o.catalog, o.display_name, o.type, o.created_at, o.updated_at))

    def setUp(self):
        super(TestListIdentityCustomRoles, self).setUp()

        self.cmd = custom_role.ListCustomRoles(self.app, None)

        self.client.custom_roles = mock.Mock()
        self.client.api_mock = self.client.custom_roles

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
            '--page', '1',
            '--per_page', '2'
        ]

        verifylist = [
            ('page', '1'),
            ('per_page', '2'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(
            page='1', per_page='2'
        )
