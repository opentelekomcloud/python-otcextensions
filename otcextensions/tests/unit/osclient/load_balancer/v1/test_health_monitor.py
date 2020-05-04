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

from openstackclient.tests.unit import utils

from otcextensions.common import sdk_utils
from otcextensions.osclient.load_balancer.v1 import health_monitor
from otcextensions.tests.unit.osclient.load_balancer.v1 import fakes


class TestListHealthMonitor(fakes.TestLoadBalancer):

    _objects = fakes.FakeHealthMonitor.create_multiple(3)

    columns = ('id', 'name', 'project_id', 'type', 'admin_state_up')

    data = []

    for s in _objects:
        data.append((
            s.id,
            s.name,
            s.project_id,
            s.type,
            s.is_admin_state_up,
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
            # '--delay', '1',
            # '--expected_codes', 'codes',
            # '--http_method', 'GET',
            # '--max_retries', '2',
            # '--timeout', '3',
            # '--url_path', 'url_path',
            '--type', 'HTTP',
        ]

        verifylist = [
            # ('delay', 1),
            # ('max_retries', 2),
            # ('timeout', 3),
            # ('expected_codes', 'codes'),
            # ('http_method', 'GET'),
            # ('url_path', 'url_path'),
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
            # delay=1,
            # max_retries=2,
            # timeout=3,
            # expected_codes='codes',
            # http_method='GET',
            # url_path='url_path',
            type='HTTP'
        )

    def test_list_filter_exceptions_method(self):
        arglist = [
            '--http_method', 'bad',
        ]

        verifylist = [
            ('http_method', 'bad')
        ]

        # Ensure exception is raised
        self.assertRaises(
            utils.ParserException,
            self.check_parser, self.cmd, arglist, verifylist)

    def test_list_filter_exceptions_type(self):
        arglist = [
            '--type', 'bad',
        ]

        verifylist = [
            ('type', 'bad')
        ]

        # Ensure exception is raised
        self.assertRaises(
            utils.ParserException,
            self.check_parser, self.cmd, arglist, verifylist)


class TestShowHealthMonitor(fakes.TestLoadBalancer):

    _object = fakes.FakeHealthMonitor.create_one()

    columns = (
        'admin_state_up', 'expected_codes', 'http_method',
        'id', 'max_retries', 'name', 'pool_ids', 'timeout',
        'type', 'url_path')

    data = (
        _object.is_admin_state_up,
        _object.expected_codes,
        _object.http_method,
        _object.id,
        _object.max_retries,
        _object.name,
        sdk_utils.ListOfIdsColumnBR(_object.pool_ids),
        _object.timeout,
        _object.type,
        _object.url_path,
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
            ignore_missing=False
        )

        self.assertEqual(self.columns, columns)
        self.assertItemEqual(self.data, data)


class TestCreateHealthMonitor(fakes.TestLoadBalancer):

    _object = fakes.FakeHealthMonitor.create_one()
    _pool = fakes.FakePool.create_one()

    columns = (
        'admin_state_up', 'expected_codes', 'http_method',
        'id', 'max_retries', 'name', 'pool_ids', 'timeout',
        'type', 'url_path')

    data = (
        _object.is_admin_state_up,
        _object.expected_codes,
        _object.http_method,
        _object.id,
        _object.max_retries,
        _object.name,
        sdk_utils.ListOfIdsColumnBR(_object.pool_ids),
        _object.timeout,
        _object.type,
        _object.url_path,
    )

    def setUp(self):
        super(TestCreateHealthMonitor, self).setUp()

        self.cmd = health_monitor.CreateHealthMonitor(self.app, None)

        self.client.create_health_monitor = mock.Mock()
        self.client.find_pool = mock.Mock()

    def test_create_default(self):
        arglist = [
            'pool_id',
            '--disable',
            '--delay', '1',
            '--expected_codes', '100',
            '--http_method', 'CONNECT',
            '--name', 'name',
            '--max_retries', '2',
            '--timeout', '3',
            '--type', 'PING',
            '--url_path', 'url'
        ]

        verifylist = [
            ('disable', True),
            ('delay', 1),
            ('expected_codes', '100'),
            ('http_method', 'CONNECT'),
            ('name', 'name'),
            ('max_retries', 2),
            ('pool', 'pool_id'),
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
        self.client.find_pool.side_effect = [
            self._pool
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_health_monitor.assert_called_once_with(
            is_admin_state_up=False,
            delay=1,
            expected_codes='100',
            http_method='CONNECT',
            max_retries=2,
            name='name',
            pool_id=self._pool.id,
            timeout=3,
            type='PING',
            url_path='url'
        )

        self.assertEqual(self.columns, columns)
        self.assertItemEqual(self.data, data)


class TestUpdateHealthMonitor(fakes.TestLoadBalancer):

    _object = fakes.FakeHealthMonitor.create_one()

    columns = (
        'admin_state_up', 'expected_codes', 'http_method',
        'id', 'max_retries', 'name', 'pool_ids', 'timeout',
        'type', 'url_path')

    data = (
        _object.is_admin_state_up,
        _object.expected_codes,
        _object.http_method,
        _object.id,
        _object.max_retries,
        _object.name,
        sdk_utils.ListOfIdsColumnBR(_object.pool_ids),
        _object.timeout,
        _object.type,
        _object.url_path,
    )

    def setUp(self):
        super(TestUpdateHealthMonitor, self).setUp()

        self.cmd = health_monitor.SetHealthMonitor(self.app, None)

        self.client.update_health_monitor = mock.Mock()
        self.client.find_health_monitor = mock.Mock()

    def test_update_default(self):
        arglist = [
            'hm',
            '--disable',
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
            ('disable', True),
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
        self.client.find_health_monitor.side_effect = [
            self._object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.update_health_monitor.assert_called_once_with(
            health_monitor=self._object.id,
            is_admin_state_up=False,
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
        self.client.find_health_monitor = mock.Mock()

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
        self.client.find_health_monitor.side_effect = [
            self._object
        ]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.delete_health_monitor.assert_called_once_with(
            health_monitor=self._object.id,
            ignore_missing=False
        )
