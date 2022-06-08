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

from otcextensions.osclient.dcaas.v2 import endpoint_group
from otcextensions.tests.unit.osclient.dcaas.v2 import fakes

from osc_lib import exceptions

from openstackclient.tests.unit import utils as tests_utils


class TestListEndpointGroups(fakes.TestDcaas):

    objects = fakes.FakeEndpointGroup.create_multiple(3)
    column_list_headers = (
        'id',
        'name',
        'description',
        'project id',
        'type',
        'endpoints',
    )
    columns = (
        'id',
        'name',
        'description',
        'project id',
        'type',
        'endpoints'
    )
    data = []
    for s in objects:
        data.append((
            s.id,
            s.name,
            s.description,
            s.project_id,
            s.type,
            s.endpoints,
        ))

    def setUp(self):
        super(TestListEndpointGroups, self).setUp()
        self.cmd = endpoint_group.ListEndpointGroups(self.app, None)
        self.client.endpoint_groups = mock.Mock()
        self.client.api_mock = self.client.endpoint_groups

    def test_list(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.client.api_mock.side_effect = [self.objects]
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with()
        self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(self.data, list(data))

    def test_list_args(self):
        arglist = [
            '--id', '1',
            '--name', 'test',
            '--description', 'test description',
            '--project_id', 'tid1',
            '--type', 'cidr',
            '--endpoints', '10.2.0.0/24', '10.3.0.0/24',
        ]
        verifylist = [
            ('id', '1'),
            ('name', 'test'),
            ('description', 'test description'),
            ('project_id', 'tid1'),
            ('type', 'cidr'),
            ('endpoints', ["10.2.0.0/24", "10.3.0.0/24"]),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.client.api_mock.side_effect = [self.objects]
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(
            id='1',
            name='test',
            description='test description',
            project_id='tid1',
            type='cidr',
            endpoints=["10.2.0.0/24", "10.3.0.0/24"],
        )


class TestCreateEndpointGroup(fakes.TestDcaas):

    _data = fakes.FakeEndpointGroup.create_one()

    columns = (
        'description',
        'endpoints',
        'id',
        'name',
        'project_id',
        'type'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestCreateEndpointGroup, self).setUp()
        self.cmd = endpoint_group.CreateEndpointGroup(self.app, None)
        self.client.create_endpoint_group = mock.Mock(return_value=self._data)

    def test_create(self):
        arglist = [
            '--name', 'test',
            '--description', 'test description',
            'tid1',
            'cidr',
            '10.2.0.0/24', '10.3.0.0/24'
        ]
        verifylist = [
            ('name', 'test'),
            ('description', 'test description'),
            ('project_id', 'tid1'),
            ('type', 'cidr'),
            ('endpoints', ["10.2.0.0/24", "10.3.0.0/24"])
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)
        self.client.create_endpoint_group.assert_called_with(
            project_id='tid1',
            endpoints=["10.2.0.0/24", "10.3.0.0/24"],
            type='cidr',
            name='test',
            description='test description'
        )
        self.assertEqual(self.columns, columns)


class TestShowEndpointGroup(fakes.TestDcaas):

    _data = fakes.FakeEndpointGroup.create_one()

    columns = (
        'description',
        'endpoints',
        'id',
        'name',
        'project_id',
        'type'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestShowEndpointGroup, self).setUp()
        self.cmd = endpoint_group.ShowEndpointGroup(self.app, None)
        self.client.find_endpoint_group = mock.Mock(return_value=self._data)

    def test_show_no_options(self):
        arglist = []
        verifylist = []
        self.assertRaises(tests_utils.ParserException, self.check_parser,
                          self.cmd, arglist, verifylist)

    def test_show(self):
        arglist = [
            self._data.id,
        ]
        verifylist = [
            ('endpoint_group', self._data.id)
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)
        self.client.find_endpoint_group.assert_called_with(self._data.id)
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)

    def test_show_non_existing(self):
        arglist = [
            'unexisted_endpoint_group'
        ]
        verifylist = [
            ('endpoint_group', 'unexisted_endpoint_group')
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        find_mock_result = exceptions.CommandError('Resource Not Found')
        self.client.find_endpoint_group = (
            mock.Mock(side_effect=find_mock_result)
        )
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual('Resource Not Found', str(e))
        self.client.find_endpoint_group.assert_called_with(
            'unexisted_endpoint_group'
        )


class TestUpdateEndpointGroup(fakes.TestDcaas):

    _data = fakes.FakeEndpointGroup.create_one()

    columns = (
        'description',
        'endpoints',
        'id',
        'name',
        'project_id',
        'type'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestUpdateEndpointGroup, self).setUp()
        self.cmd = endpoint_group.UpdateEndpointGroup(self.app, None)
        self.client.find_endpoint_group = mock.Mock(return_value=self._data)
        self.client.update_endpoint_group = mock.Mock(return_value=self._data)
        self.client.api_mock = self.client.update_endpoint_group

    def test_update(self):
        arglist = [
            self._data.id,
            '--name', 'updated_name',
            '--description', 'updated description'
        ]
        verifylist = [
            ('endpoint_group', self._data.id),
            ('name', 'updated_name'),
            ('description', 'updated description')
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)
        self.client.api_mock.side_effect = [
            self._data
        ]
        self.client.api_mock.assert_called_with(
            self._data.id,
            name='updated_name',
            description='updated description'
        )
        self.assertEqual(self.columns, columns)


class TestDeleteEndpointGroup(fakes.TestDcaas):
    _data = fakes.FakeEndpointGroup.create_one()

    def setUp(self):
        super(TestDeleteEndpointGroup, self).setUp()
        self.client.delete_endpoint_group = mock.Mock(return_value=None)
        self.cmd = endpoint_group.DeleteEndpointGroup(self.app, None)

    def test_delete_by_name(self):
        arglist = [
            self._data.name,
        ]
        verifylist = [
            ('endpoint_group', self._data.name),
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.client.find_endpoint_group = (
            mock.Mock(return_value=self._data)
        )
        result = self.cmd.take_action(parsed_args)
        self.client.delete_endpoint_group.assert_called_with(self._data.id)
        self.assertIsNone(result)
