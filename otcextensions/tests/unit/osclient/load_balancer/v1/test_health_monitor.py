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
#
import mock

from osc_lib import exceptions

from otcextensions.common import sdk_utils

from otcextensions.tests.unit.osclient.load_balancer.v1 import fakes

from otcextensions.osclient.load_balancer.v1 import health_monitor


class TestListHealthMonitor(fakes.TestLoadBalancer):

    _objects = fakes.FakeHealthMonitor.create_multiple(3)

    columns = ('ID', 'Name', 'type', 'is_admin_state_up',
               'url_path', 'expected_codes',
               'delay', 'max_retries', 'timeout', 'pool_ids')

    data = []

    for s in _objects:
        data.append((
            s.id,
            s.name,
            s.type,
            s.is_admin_state_up,
            s.url_path,
            s.expected_codes,
            s.delay,
            s.max_retries,
            s.timeout,
            sdk_utils.ListOfIdsColumn(s.pool_ids),
        ))

    def setUp(self):
        super(TestListHealthMonitor, self).setUp()

        self.cmd = health_monitor.ListHealthMonitor(self.app, None)

        self.client.health_monitors = mock.Mock()

    def test_list_default(self):
        arglist = [
        ]

        verifylist = [
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.health_monitors.side_effect = [
            self._objects
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.health_monitors.assert_called_once_with()

        self.assertEqual(self.columns, columns)
        self.assertListItemEqual(self.data, list(data))

    def test_list_filter_values(self):
        arglist = [
            '--delay', '1',
            '--expected_codes', 'codes',
            '--http_method', 'GET',
            '--max_retries', '2',
            '--timeout', '3',
            '--url_path', 'url_path',
            '--type', 'HTTP',
        ]

        verifylist = [
            ('delay', 1),
            ('max_retries', 2),
            ('timeout', 3),
            ('expected_codes', 'codes'),
            ('http_method', 'GET'),
            ('url_path', 'url_path'),
            ('type', 'HTTP'),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.health_monitors.side_effect = [
            {}
        ]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.health_monitors.assert_called_once_with(
            delay=1,
            max_retries=2,
            timeout=3,
            expected_codes='codes',
            http_method='GET',
            url_path='url_path',
            type='HTTP'
        )

    def test_list_filter_exceptions_method(self):
        arglist = [
            '--http_method', 'bad',
        ]

        verifylist = [
            ('http_method', 'bad')
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Ensure exception is raised
        self.assertRaises(
            exceptions.CommandError,
            self.cmd.take_action, parsed_args)

    def test_list_filter_exceptions_type(self):
        arglist = [
            '--type', 'bad',
        ]

        verifylist = [
            ('type', 'bad')
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Ensure exception is raised
        self.assertRaises(
            exceptions.CommandError,
            self.cmd.take_action, parsed_args)


class TestShowHealthMonitor(fakes.TestLoadBalancer):

    _object = fakes.FakeHealthMonitor.create_one()

    columns = ('ID', 'Name', 'type', 'is_admin_state_up',
               'http_method', 'url_path', 'expected_codes',
               'delay', 'max_retries', 'timeout', 'pool_ids')

    data = (
        _object.id,
        _object.name,
        _object.type,
        _object.is_admin_state_up,
        _object.http_method,
        _object.url_path,
        _object.expected_codes,
        _object.delay,
        _object.max_retries,
        _object.timeout,
        sdk_utils.ListOfIdsColumn(_object.pool_ids),
    )

    def setUp(self):
        super(TestShowHealthMonitor, self).setUp()

        self.cmd = health_monitor.ShowHealthMonitor(self.app, None)

        self.client.find_health_monitor = mock.Mock()

    def test_show_default(self):
        arglist = [
            'hm'
        ]

        verifylist = [
            ('health_monitor', 'hm'),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.find_health_monitor.side_effect = [
            self._object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_health_monitor.assert_called_once_with(
            name_or_id='hm',
        )

        self.assertEqual(self.columns, columns)
        self.assertItemEqual(self.data, data)


class TestCreateHealthMonitor(fakes.TestLoadBalancer):

    _object = fakes.FakeHealthMonitor.create_one()

    columns = ('ID', 'Name', 'type', 'is_admin_state_up',
               'http_method', 'url_path', 'expected_codes',
               'delay', 'max_retries', 'timeout', 'pool_ids')

    data = (
        _object.id,
        _object.name,
        _object.type,
        _object.is_admin_state_up,
        _object.http_method,
        _object.url_path,
        _object.expected_codes,
        _object.delay,
        _object.max_retries,
        _object.timeout,
        sdk_utils.ListOfIdsColumn(_object.pool_ids),
    )

    def setUp(self):
        super(TestCreateHealthMonitor, self).setUp()

        self.cmd = health_monitor.CreateHealthMonitor(self.app, None)

        self.client.create_health_monitor = mock.Mock()

    def test_create_default(self):
        arglist = [
            '--admin_state_up', 'true',
            '--delay', '1',
            '--expected_codes', '100',
            '--http_method', 'CONNECT',
            '--name', 'name',
            '--max_retries', '2',
            '--pool_id', 'pool',
            '--timeout', '3',
            '--type', 'PING',
            '--url_path', 'url'
        ]

        verifylist = [
            ('admin_state_up', True),
            ('delay', 1),
            ('expected_codes', '100'),
            ('http_method', 'CONNECT'),
            ('name', 'name'),
            ('max_retries', 2),
            ('pool_id', 'pool'),
            ('timeout', 3),
            ('type', 'PING'),
            ('url_path', 'url')
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.create_health_monitor.side_effect = [
            self._object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_health_monitor.assert_called_once_with(
            admin_state_up=True,
            delay=1,
            expected_codes='100',
            http_method='CONNECT',
            max_retries=2,
            name='name',
            pool_id='pool',
            timeout=3,
            type='PING',
            url_path='url'
        )

        self.assertEqual(self.columns, columns)
        self.assertItemEqual(self.data, data)


class TestUpdateHealthMonitor(fakes.TestLoadBalancer):

    _object = fakes.FakeHealthMonitor.create_one()

    columns = ('ID', 'Name', 'type', 'is_admin_state_up',
               'http_method', 'url_path', 'expected_codes',
               'delay', 'max_retries', 'timeout', 'pool_ids')

    data = (
        _object.id,
        _object.name,
        _object.type,
        _object.is_admin_state_up,
        _object.http_method,
        _object.url_path,
        _object.expected_codes,
        _object.delay,
        _object.max_retries,
        _object.timeout,
        sdk_utils.ListOfIdsColumn(_object.pool_ids),
    )

    def setUp(self):
        super(TestUpdateHealthMonitor, self).setUp()

        self.cmd = health_monitor.UpdateHealthMonitor(self.app, None)

        self.client.update_health_monitor = mock.Mock()

    def test_update_default(self):
        arglist = [
            'hm',
            '--admin_state_up', 'true',
            '--delay', '1',
            '--expected_codes', '100',
            '--http_method', 'CONNECT',
            '--name', 'name',
            '--max_retries', '2',
            '--timeout', '3',
            '--url_path', 'url'
        ]

        verifylist = [
            ('health_monitor', 'hm'),
            ('admin_state_up', True),
            ('delay', 1),
            ('expected_codes', '100'),
            ('http_method', 'CONNECT'),
            ('name', 'name'),
            ('max_retries', 2),
            ('timeout', 3),
            ('url_path', 'url')
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.update_health_monitor.side_effect = [
            self._object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.update_health_monitor.assert_called_once_with(
            health_monitor='hm',
            admin_state_up=True,
            delay=1,
            expected_codes='100',
            http_method='CONNECT',
            max_retries=2,
            name='name',
            timeout=3,
            url_path='url'
        )

        self.assertEqual(self.columns, columns)
        self.assertItemEqual(self.data, data)


class TestDeleteHealthMonitor(fakes.TestLoadBalancer):

    _object = fakes.FakeHealthMonitor.create_one()

    def setUp(self):
        super(TestDeleteHealthMonitor, self).setUp()

        self.cmd = health_monitor.DeleteHealthMonitor(self.app, None)

        self.client.delete_health_monitor = mock.Mock()

    def test_delete_default(self):
        arglist = [
            'hm',
        ]

        verifylist = [
            ('health_monitor', ['hm']),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.delete_health_monitor.side_effect = [
            {}
        ]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.delete_health_monitor.assert_called_once_with(
            health_monitor='hm',
            ignore_missing=False
        )
