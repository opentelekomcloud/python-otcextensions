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

from otcextensions.osclient.mrs.v1 import datasource
from otcextensions.tests.unit.osclient.mrs.v1 import fakes


class TestListDatasource(fakes.TestMrs):
    objects = fakes.FakeCluster.create_multiple(3)

    columns = (
        'id', 'name', 'type', 'url', 'description',
        'is_public', 'is_protected'
    )

    data = []

    for s in objects:
        data.append(fakes.gen_data(s, columns))

    def setUp(self):
        super(TestListDatasource, self).setUp()

        self.cmd = datasource.ListDatasource(self.app, None)

        self.client.datasources = mock.Mock()
        self.client.api_mock = self.client.datasources

    def test_default(self):
        arglist = [
            '--type', 'hdfs',
        ]
        verifylist = [
            ('type', 'hdfs'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [
            self.objects
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_once_with(
            type='hdfs'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))


class TestShowDatasource(fakes.TestMrs):
    object = fakes.FakeDatasource.create_one()

    columns = (
        'description',
        'id',
        'is_protected',
        'is_public',
        'name',
        'type',
        'url'
    )

    data = fakes.gen_data(object, columns)

    def setUp(self):
        super(TestShowDatasource, self).setUp()

        self.cmd = datasource.ShowDatasource(self.app, None)

        self.client.find_datasource = mock.Mock()

    def test_default(self):
        arglist = [
            'datasource'
        ]
        verifylist = [
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.find_datasource.side_effect = [
            self.object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_datasource.assert_called_once_with(
            'datasource',
            ignore_missing=False
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestDeleteDatasource(fakes.TestMrs):

    def setUp(self):
        super(TestDeleteDatasource, self).setUp()

        self.cmd = datasource.DeleteDatasource(self.app, None)

        self.client.delete_datasource = mock.Mock()

    def test_delete(self):
        arglist = [
            'datasource'
        ]
        verifylist = []
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.delete_datasource.side_effect = [{}]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        delete_calls = [
            mock.call(
                'datasource',
                ignore_missing=False),
        ]

        self.client.delete_datasource.assert_has_calls(delete_calls)
        self.assertEqual(1, self.client.delete_datasource.call_count)


class TestCreateDatasource(fakes.TestMrs):
    object = fakes.FakeDatasource.create_one()

    columns = ('description', 'id', 'is_protected', 'is_public', 'name',
               'type', 'url')

    data = fakes.gen_data(object, columns)

    def setUp(self):
        super(TestCreateDatasource, self).setUp()

        self.cmd = datasource.CreateDatasource(self.app, None)
        self.app.client_manager.sdk_connection = mock.Mock()

        self.client.create_datasource = mock.Mock()

    def test_default(self):
        arglist = [
            '--name', 'test_ds',
            '--type', 'hdfs',
            '--url', '/simple/mapreduce/input',
            '--description', 'test',
        ]
        verifylist = [
            ('name', 'test_ds'),
            ('type', 'hdfs'),
            ('url', '/simple/mapreduce/input'),
            ('description', 'test'),
        ]

        # Verify cmd is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.create_datasource.side_effect = [
            self.object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_datasource.assert_called_once_with(
            type='hdfs',
            name='test_ds',
            url='/simple/mapreduce/input',
            description='test',
            is_public='false',
            is_protected='false'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestUpdateDatasource(fakes.TestMrs):
    object = fakes.FakeDatasource.create_one()

    columns = ('description', 'id', 'is_protected', 'is_public', 'name',
               'type', 'url')

    data = fakes.gen_data(object, columns)

    def setUp(self):
        super(TestUpdateDatasource, self).setUp()

        self.cmd = datasource.UpdateDatasource(self.app, None)
        self.app.client_manager.sdk_connection = mock.Mock()

        self.client.update_datasource = mock.Mock()

    def test_default(self):
        arglist = [
            'datasource_id',
            '--name', 'test_ds',
            '--type', 'obs',
            '--url', '/simple/mapreduce/updated',
            '--description', 'updated',
        ]
        verifylist = [
            ('datasource', 'datasource_id'),
            ('name', 'test_ds'),
            ('type', 'obs'),
            ('url', '/simple/mapreduce/updated'),
            ('description', 'updated'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.update_datasource.side_effect = [
            self.object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_datasource.assert_called_with(
            'datasource_id',
            ignore_missing=False)

        self.client.update_datasource.assert_called_once_with(
            datasource=mock.ANY,
            name='test_ds',
            type='obs',
            url='/simple/mapreduce/updated',
            description='updated',
            is_public='false'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)
