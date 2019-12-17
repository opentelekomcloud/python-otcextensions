#   Copyright 2013 Nebula Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
import mock

from otcextensions.osclient.mrs.v1 import host
from otcextensions.tests.unit.osclient.mrs.v1 import fakes


class TestListHost(fakes.TestMrs):

    objects = fakes.FakeHost.create_multiple(3)

    columns = (
        'id', 'name', 'auto_placement', 'availability_zone',
        'available_vcpus', 'available_memory'
    )

    data = []

    for s in objects:
        data.append(fakes.gen_data(s, columns))

    def setUp(self):
        super(TestListHost, self).setUp()

        self.cmd = host.ListHost(self.app, None)

        self.client.hosts = mock.Mock()
        self.client.api_mock = self.client.hosts

    def test_default(self):
        arglist = [
        ]

        verifylist = [
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
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))

    def test_default_query(self):
        arglist = [
            '--id', 'some_id',
            '--name', 'some_name',
            '--host_type', 'some_type',
            '--host_type_name', 'some_type_name',
            '--flavor', 'some_flavor',
            '--state', 'available',
            '--tenant', 'all',
            '--availability_zone', 'some_az',
            '--limit', '1',
            '--marker', 'some_marker',
            '--changes_since', '2200-01-01T00:00:00+00:00'
        ]

        verifylist = [
            ('id', 'some_id'),
            ('name', 'some_name'),
            ('host_type', 'some_type'),
            ('host_type_name', 'some_type_name'),
            ('flavor', 'some_flavor'),
            ('state', 'available'),
            ('tenant', 'all'),
            ('availability_zone', 'some_az'),
            ('limit', 1),
            ('marker', 'some_marker'),
            ('changes_since', '2200-01-01T00:00:00+00:00')
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
            availability_zone='some_az',
            changes_since='2200-01-01T00:00:00+00:00',
            flavor='some_flavor',
            host_type='some_type',
            host_type_name='some_type_name',
            id='some_id',
            limit=1,
            marker='some_marker',
            name='some_name',
            state='available',
            tenant='all'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))


class TestShowHost(fakes.TestMrs):

    _data = fakes.FakeHost.create_one()

    columns = (
        'allocated_at', 'auto_placement', 'availability_zone',
        'available_memory', 'available_vcpus', 'host_properties', 'id',
        'instance_total', 'name', 'project_id', 'released_at', 'state'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestShowHost, self).setUp()

        self.cmd = host.ShowHost(self.app, None)

        self.client.find_host = mock.Mock()
        self.client.api_mock = self.client.find_host

    def test_default(self):
        arglist = [
            'host'
        ]

        verifylist = [
            ('host', 'host')
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
            'host'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestCreateHost(fakes.TestMrs):

    _data = fakes.FakeHost.create_one()

    columns = (
        'id'
    )

    _data.dedicated_host_ids = [_data.id]

    data = []

    for s in _data.dedicated_host_ids:
        data.append(fakes.gen_data(s, columns))

    def setUp(self):
        super(TestCreateHost, self).setUp()

        self.cmd = host.CreateHost(self.app, None)

        self.client.create_host = mock.Mock()
        self.client.api_mock = self.client.create_host

    def test_create(self):
        arglist = [
            '--name', 'name',
            '--auto_placement',
            '--availability_zone', 'az1',
            '--host_type', 'type',
            '--quantity', '1',
        ]

        verifylist = [
            ('name', 'name'),
            ('auto_placement', 'on'),
            ('availability_zone', 'az1'),
            ('host_type', 'type'),
            ('quantity', 1),
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
            auto_placement='on', availability_zone='az1',
            host_type='type', name='name', quantity=1
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))

    def test_create_default_placement(self):
        arglist = [
            '--name', 'name',
            '--availability_zone', 'az1',
        ]

        verifylist = [
            ('name', 'name'),
            ('auto_placement', 'on'),
            ('availability_zone', 'az1'),
            ('quantity', 1),
        ]

        # Verify cm is triggereg with default parameters
        self.check_parser(self.cmd, arglist, verifylist)

    def test_create_no_placement(self):
        arglist = [
            '--name', 'name',
            '--no-auto_placement',
            '--availability_zone', 'az1',
        ]

        verifylist = [
            ('name', 'name'),
            ('auto_placement', 'off'),
            ('availability_zone', 'az1'),
            ('quantity', 1),
        ]

        # Verify cm is triggereg with default parameters
        self.check_parser(self.cmd, arglist, verifylist)


class TestSetHost(fakes.TestMrs):

    _data = fakes.FakeHost.create_one()

    columns = (
        'allocated_at', 'auto_placement', 'availability_zone',
        'available_memory', 'available_vcpus', 'host_properties', 'id',
        'instance_total', 'name', 'project_id', 'released_at', 'state'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestSetHost, self).setUp()

        self.cmd = host.SetHost(self.app, None)

        self.client.update_host = mock.Mock()
        self.client.find_host = mock.Mock()
        self.client.api_mock = self.client.update_host

    def test_update(self):
        arglist = [
            'zn',
            '--name', 'name',
            '--auto_placement'
        ]

        verifylist = [
            ('host', 'zn'),
            ('name', 'name'),
            ('auto_placement', 'on'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [
            self._data
        ]
        self.client.find_host.side_effect = [
            self._data
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_host.assert_called_once_with(
            'zn',
            ignore_missing=False
        )

        self.client.api_mock.assert_called_once_with(
            host=self._data,
            name='name',
            auto_placement='on',
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)

    def test_update_disable_placement(self):
        arglist = [
            'zn',
            '--name', 'name',
            '--no-auto_placement'
        ]

        verifylist = [
            ('host', 'zn'),
            ('name', 'name'),
            ('auto_placement', 'off'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [
            self._data
        ]
        self.client.find_host.side_effect = [
            self._data
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_host.assert_called_once_with(
            'zn',
            ignore_missing=False
        )

        self.client.api_mock.assert_called_once_with(
            host=self._data,
            name='name',
            auto_placement='off',
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestDeleteHost(fakes.TestMrs):

    def setUp(self):
        super(TestDeleteHost, self).setUp()

        self.cmd = host.DeleteHost(self.app, None)

        self.client.delete_host = mock.Mock()
        self.client.api_mock = self.client.delete_host

    def test_delete_multiple(self):
        arglist = [
            't1',
            't2',
        ]
        verifylist = [
            ('host', ['t1', 't2'])
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [{}, {}]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        calls = [
            mock.call(host='t1', ignore_missing=False),
            mock.call(host='t2', ignore_missing=False)
        ]

        self.client.api_mock.assert_has_calls(calls)
        self.assertEqual(2, self.client.api_mock.call_count)


class TestListServer(fakes.TestMrs):

    _host = fakes.FakeHost.create_one()
    objects = fakes.FakeServer.create_multiple(3)

    columns = (
        'addresses', 'id', 'name', 'metadata', 'status', 'user_id'
    )

    data = []

    for s in objects:
        data.append(fakes.gen_data(s, columns))

    def setUp(self):
        super(TestListServer, self).setUp()

        self.cmd = host.ListServer(self.app, None)

        self.client.servers = mock.Mock()
        self.client.find_host = mock.Mock()
        self.client.api_mock = self.client.servers

    def test_default(self):
        arglist = [
            'zn',
        ]

        verifylist = [
            ('host', 'zn'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [
            self.objects
        ]
        self.client.find_host.side_effect = [
            self.data
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_host.assert_called_once_with(
            'zn',
            ignore_missing=False
        )

        self.client.api_mock.assert_called_once_with(
            host=self.data,
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))


class TestListHostType(fakes.TestMrs):

    objects = fakes.FakeHostType.create_multiple(3)

    columns = (
        'host_type', 'host_type_name'
    )

    data = []

    for s in objects:
        data.append(fakes.gen_data(s, columns))

    def setUp(self):
        super(TestListHostType, self).setUp()

        self.cmd = host.ListHostType(self.app, None)

        self.client.host_types = mock.Mock()
        self.client.api_mock = self.client.host_types

    def test_default(self):
        arglist = [
            'az',
        ]

        verifylist = [
            ('az', 'az'),
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
            'az'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))
