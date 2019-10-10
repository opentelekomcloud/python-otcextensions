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

from otcextensions.osclient.rds.v3 import configuration
from otcextensions.tests.unit.osclient.rds.v3 import fakes


class TestListConfiguration(fakes.TestRds):

    objects = fakes.FakeConfiguration.create_multiple(3)

    column_list_headers = [
        'ID',
        'Name',
        'Description',
        'Datastore Name',
        'Datastore Version Name',
        'User Defined'
    ]

    columns = ('id', 'name', 'description', 'datastore_name',
               'datastore_version_name', 'is_user_defined')

    data = []

    for s in objects:
        data.append(fakes.gen_data(s, columns))

    def setUp(self):
        super(TestListConfiguration, self).setUp()

        self.cmd = configuration.ListConfigurations(self.app, None)

        self.client.configurations = mock.Mock()
        self.client.api_mock = self.client.configurations

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


class TestShowConfiguration(fakes.TestRds):

    _data = fakes.FakeConfiguration.create_one()

    columns = (
        'datastore_name', 'datastore_version_name',
        'description', 'id', 'is_user_defined', 'name'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestShowConfiguration, self).setUp()

        self.cmd = configuration.ShowConfiguration(self.app, None)

        self.client.find_configuration = mock.Mock(return_value=self._data)

    def test_show(self):
        arglist = [
            'test',
        ]

        verifylist = [
            ('configuration', 'test'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.find_configuration.assert_called_with('test',
                                                          ignore_missing=False)

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestListConfigurationParameters(fakes.TestRds):

    config = fakes.FakeConfiguration.create_one()

    objects = config.configuration_parameters

    column_list_headers = (
        'Name', 'Value', 'Type', 'Description',
        'Restart Required', 'Readonly', 'Value Range'
    )

    columns = (
        'name', 'value', 'type', 'description',
        'restart_required', 'readonly', 'value_range'
    )

    data = []

    for s in objects:
        # NOTE: please fix this. For some reason comprehension doesn't work
        # here
        values = []
        for attr in columns:
            values.append(s.get(attr, ''))
        data.append(tuple(values))

    def setUp(self):
        super(TestListConfigurationParameters, self).setUp()

        self.cmd = configuration.ListConfigurationParameters(self.app, None)

        self.client.find_configuration = mock.Mock(return_value=self.config)
        self.client.api_mock = self.client.find_configuration

    def test_list(self):
        arglist = ['test_config']

        verifylist = [
            ('configuration', 'test_config')
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with('test_config',
                                                ignore_missing=False)

        self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(self.data, list(data))


class TestCreateConfiguration(fakes.TestRds):

    _data = fakes.FakeConfiguration.create_one()

    columns = (
        'datastore_name', 'datastore_version_name',
        'description', 'id', 'is_user_defined', 'name'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestCreateConfiguration, self).setUp()

        self.cmd = configuration.CreateConfiguration(self.app, None)

        self.client.create_configuration = mock.Mock()
        self.client.api_mock = self.client.create_configuration

    def test_create(self):
        arglist = [
            'cfg',
            '--datastore-type', 'postgresql',
            '--datastore-version', '-9.6',
            '--description', 'descr',
            '--value', 'a=b',
            '--value', 'c=d'
        ]

        verifylist = [
            ('name', 'cfg'),
            ('datastore_type', 'postgresql'),
            ('datastore_version', '-9.6'),
            ('description', 'descr'),
            ('values', {'a': 'b', 'c': 'd'})
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [
            self._data
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_once_with(
            datastore={'type': 'postgresql', 'version': '-9.6'},
            description='descr',
            name='cfg',
            values={'a': 'b', 'c': 'd'}
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)

    def test_create2(self):
        arglist = [
            'cfg',
            '--datastore-type', 'MySQL',
            '--datastore-version', '-9.6',
        ]

        verifylist = [
            ('name', 'cfg'),
            ('datastore_type', 'mysql'),
            ('datastore_version', '-9.6'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [
            self._data
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_once_with(
            datastore={'type': 'mysql', 'version': '-9.6'},
            name='cfg'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestSetConfiguration(fakes.TestRds):

    def setUp(self):
        super(TestSetConfiguration, self).setUp()

        self.cmd = configuration.SetConfiguration(self.app, None)

        self.client.update_configuration = mock.Mock()
        self.client.api_mock = self.client.update_configuration
        self.client.find_configuration = mock.Mock()

    def test_action(self):
        arglist = [
            't1',
            '--name', 'new_name',
            '--description', 'new_descr',
            '--value', 'q=z',
            '--value', 'w=u'
        ]
        verifylist = [
            ('configuration', 't1'),
            ('name', 'new_name'),
            ('description', 'new_descr'),
            ('values', {'q': 'z', 'w': 'u'})
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.find_configuration.return_value = 't1'

        # Trigger the action
        resp = self.cmd.take_action(parsed_args)

        self.client.find_configuration.assert_called_with('t1',
                                                          ignore_missing=False)
        self.client.api_mock.assert_called_with(
            't1',
            description='new_descr',
            name='new_name',
            values={'q': 'z', 'w': 'u'}
        )
        self.assertIsNone(resp)


class TestDeleteConfiguration(fakes.TestRds):

    def setUp(self):
        super(TestDeleteConfiguration, self).setUp()

        self.cmd = configuration.DeleteConfiguration(self.app, None)

        self.client.delete_configuration = mock.Mock()
        self.client.api_mock = self.client.delete_configuration
        self.client.find_configuration = mock.Mock()

    def test_delete_multiple(self):
        arglist = [
            't1',
            't2',
        ]
        verifylist = [
            ('configuration', ['t1', 't2'])
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [{}, {}]
        self.client.find_configuration.side_effect = ['t1', 't2']

        # Trigger the action
        self.cmd.take_action(parsed_args)

        find_calls = [
            mock.call('t1', ignore_missing=False),
            mock.call('t2', ignore_missing=False)
        ]

        delete_calls = [
            mock.call('t1'),
            mock.call('t2')
        ]

        self.client.find_configuration.assert_has_calls(find_calls)
        self.client.api_mock.assert_has_calls(delete_calls)


class TestApplyConfiguration(fakes.TestRds):

    _data = fakes.FakeConfiguration.create_one()

    columns = (
        'datastore_name', 'datastore_version_name',
        'description', 'id', 'is_user_defined', 'name'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestApplyConfiguration, self).setUp()

        self.cmd = configuration.ApplyConfiguration(self.app, None)

        self.client.find_configuration = mock.Mock()
        self.client.apply_configuration = mock.Mock()
        self.client.get_instance = mock.Mock()

    def test_apply(self):
        arglist = [
            'cfg',
            '--instance', 'i1',
            '--instance', 'i2',
        ]

        verifylist = [
            ('configuration', 'cfg'),
            ('instances', ['i1', 'i2']),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.find_configuration.return_value = self._data
        self.client.apply_configuration.return_value = self._data

        class Inst(object):
            def __init__(self, id):
                self.id = id

        self.client.get_instance.side_effect = lambda s: Inst(s)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        get_calls = [
            mock.call('i1'),
            mock.call('i2')
        ]

        self.client.get_instance.assert_has_calls(get_calls)
        self.client.find_configuration.assert_called_with('cfg',
                                                          ignore_missing=False)

        self.client.apply_configuration.assert_called_once_with(
            self._data.id,
            instances=['i1', 'i2']
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)
