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
from otcextensions.osclient.load_balancer.v1 import pool
from otcextensions.tests.unit.osclient.load_balancer.v1 import fakes


class TestListPool(fakes.TestLoadBalancer):

    _objects = fakes.FakePool.create_multiple(3)

    columns = (
        'id', 'name', 'project_id', 'provisioning_status',
        'protocol', 'lb_algorithm', 'admin_state_up')

    data = []

    for s in _objects:
        data.append((
            s.id,
            s.name,
            s.project_id,
            '',
            s.protocol,
            s.lb_algorithm,
            s.is_admin_state_up,
        ))

    def setUp(self):
        super(TestListPool, self).setUp()

        self.cmd = pool.ListPool(self.app, None)

        self.client.pools = mock.Mock()

    def test_list_default(self):
        arglist = [
        ]

        verifylist = [
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.pools.side_effect = [
            self._objects
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.pools.assert_called_once_with()

        self.assertEqual(self.columns, columns)
        self.assertListItemEqual(self.data, list(data))

    def test_list_filter_values(self):
        arglist = [
            '--name', 'name',
            '--protocol', 'TCP',
            '--lb_algorithm', 'ROUND_ROBIN',
            '--description', 'descr',
            '--load_balancer', 'lb',
        ]

        verifylist = [
            ('name', 'name'),
            ('protocol', 'TCP'),
            ('lb_algorithm', 'ROUND_ROBIN'),
            ('description', 'descr'),
            ('load_balancer', 'lb')
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.pools.side_effect = [
            {}
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.pools.assert_called_once_with(
            name='name',
            protocol='TCP',
            lb_algorithm='ROUND_ROBIN',
            description='descr',
            load_balancer_id='lb'
        )

    def test_list_filter_exceptions_proto(self):
        arglist = [
            '--protocol', 'bad',
        ]

        verifylist = [
            ('protocol', 'bad'),
        ]

        # Ensure exception is raised
        self.assertRaises(
            utils.ParserException,
            self.check_parser, self.cmd, arglist, verifylist)

    def test_list_filter_exceptions_algo(self):
        arglist = [
            '--lb_algorithm', 'bad',
        ]

        verifylist = [
            ('lb_algorithm', 'bad'),
        ]

        # Ensure exception is raised
        self.assertRaises(
            utils.ParserException,
            self.check_parser, self.cmd, arglist, verifylist)


class TestShowPool(fakes.TestLoadBalancer):

    _object = fakes.FakePool.create_one()

    columns = (
        'admin_state_up', 'description',
        'healthmonitor_id', 'id', 'lb_algorithm', 'listeners',
        'loadbalancers', 'member_ids', 'name', 'protocol',
        'provisioning_status', 'session_persistence')

    data = (
        _object.is_admin_state_up,
        _object.description,
        # sdk_utils.ListOfIdsColumnBR(_object.health_monitor_ids),
        _object.health_monitor_id,
        _object.id,
        _object.lb_algorithm,
        sdk_utils.ListOfIdsColumnBR(_object.listener_ids),
        sdk_utils.ListOfIdsColumnBR(_object.load_balancer_ids),
        sdk_utils.ListOfIdsColumnBR(_object.member_ids),
        _object.name,
        _object.protocol,
        _object.status,
        _object.session_persistence,
    )

    def setUp(self):
        super(TestShowPool, self).setUp()

        self.cmd = pool.ShowPool(self.app, None)

        self.client.find_pool = mock.Mock()

    def test_show_default(self):
        arglist = [
            'pool_id'
        ]

        verifylist = [
            ('pool', 'pool_id')
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.find_pool.side_effect = [
            self._object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_pool.assert_called_once_with(
            name_or_id='pool_id',
            ignore_missing=False
        )

        self.assertEqual(self.columns, columns)
        self.assertItemEqual(self.data, data)


class TestCreatePool(fakes.TestLoadBalancer):

    _object = fakes.FakePool.create_one()

    columns = (
        'admin_state_up', 'description',
        'healthmonitor_id', 'id', 'lb_algorithm', 'listeners',
        'loadbalancers', 'member_ids', 'name', 'protocol',
        'provisioning_status', 'session_persistence')

    data = (
        _object.is_admin_state_up,
        _object.description,
        _object.health_monitor_id,
        _object.id,
        _object.lb_algorithm,
        sdk_utils.ListOfIdsColumnBR(_object.listener_ids),
        sdk_utils.ListOfIdsColumnBR(_object.load_balancer_ids),
        sdk_utils.ListOfIdsColumnBR(_object.member_ids),
        _object.name,
        _object.protocol,
        _object.status,
        _object.session_persistence,
    )

    def setUp(self):
        super(TestCreatePool, self).setUp()

        self.cmd = pool.CreatePool(self.app, None)

        self.client.create_pool = mock.Mock()

    def test_create_default(self):
        arglist = [
            '--protocol', 'HTTP',
            '--lb_algorithm', 'ROUND_ROBIN',
            '--listener_id', 'listener',
            '--name', 'name',
            '--description', 'descr',
            '--session_persistence', '{"a": "b"}',
            '--disable'
        ]

        verifylist = [
            ('protocol', 'HTTP'),
            ('lb_algorithm', 'ROUND_ROBIN'),
            ('listener_id', 'listener'),
            ('disable', True),
            ('name', 'name'),
            ('description', 'descr'),
            ('session_persistence', '{"a": "b"}'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.create_pool.side_effect = [
            self._object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_pool.assert_called_once_with(
            lb_algorithm='ROUND_ROBIN',
            listener_id='listener',
            name='name',
            protocol='HTTP',
            session_persistence={'a': 'b'},
            is_admin_state_up=False,
            description='descr'
        )

        self.assertEqual(self.columns, columns)
        self.assertItemEqual(self.data, data)

    def test_create_with_lb(self):
        arglist = [
            '--protocol', 'HTTP',
            '--lb_algorithm', 'ROUND_ROBIN',
            '--loadbalancer_id', 'lb',
        ]

        verifylist = [
            ('protocol', 'HTTP'),
            ('lb_algorithm', 'ROUND_ROBIN'),
            ('loadbalancer_id', 'lb'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.create_pool.side_effect = [
            self._object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_pool.assert_called_once_with(
            lb_algorithm='ROUND_ROBIN',
            loadbalancer_id='lb',
            protocol='HTTP',
        )

        self.assertEqual(self.columns, columns)
        self.assertItemEqual(self.data, data)

    def test_create_exclusive_group(self):
        arglist = [
            'HTTP',
            'ROUND_ROBIN',
            '--listener_id', 'listener',
            '--loadbalancer_id', 'loadbalancer_id',
            '--name', 'name',
            '--session_persistence', "{'a': 'b'}"
        ]

        verifylist = [
            ('protocol', 'HTTP'),
            ('lb_algorithm', 'ROUND_ROBIN'),
            ('listener_id', 'listener'),
            ('loadbalancer_id', 'loadbalancer_id'),
            ('name', 'name'),
            ('session_persistence', "{'a': 'b'}"),
        ]

        # Verify cm is raising exception due to the exclusive group
        self.assertRaises(
            utils.ParserException,
            self.check_parser,
            self.cmd, arglist, verifylist
        )


class TestUpdatePool(fakes.TestLoadBalancer):

    _object = fakes.FakePool.create_one()

    columns = (
        'admin_state_up', 'description',
        'healthmonitor_id', 'id', 'lb_algorithm', 'listeners',
        'loadbalancers', 'member_ids', 'name', 'protocol',
        'provisioning_status', 'session_persistence')

    data = (
        _object.is_admin_state_up,
        _object.description,
        _object.health_monitor_id,
        _object.id,
        _object.lb_algorithm,
        sdk_utils.ListOfIdsColumnBR(_object.listener_ids),
        sdk_utils.ListOfIdsColumnBR(_object.load_balancer_ids),
        sdk_utils.ListOfIdsColumnBR(_object.member_ids),
        _object.name,
        _object.protocol,
        _object.status,
        _object.session_persistence,
    )

    def setUp(self):
        super(TestUpdatePool, self).setUp()

        self.cmd = pool.SetPool(self.app, None)

        self.client.update_pool = mock.Mock()

    def test_update_default(self):
        arglist = [
            'pool',
            '--lb_algorithm', 'ROUND_ROBIN',
            '--name', 'name',
            '--description', 'descr',
            '--session_persistence', '{"a": "b"}',
            '--disable'
        ]

        verifylist = [
            ('pool', 'pool'),
            ('lb_algorithm', 'ROUND_ROBIN'),
            ('disable', True),
            ('name', 'name'),
            ('description', 'descr'),
            ('session_persistence', '{"a": "b"}'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.update_pool.side_effect = [
            self._object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.update_pool.assert_called_once_with(
            lb_algorithm='ROUND_ROBIN',
            pool='pool',
            name='name',
            session_persistence={'a': 'b'},
            is_admin_state_up=False,
            description='descr'
        )

        self.assertEqual(self.columns, columns)
        self.assertItemEqual(self.data, data)


class TestDeletePool(fakes.TestLoadBalancer):

    _object = fakes.FakePool.create_one()

    def setUp(self):
        super(TestDeletePool, self).setUp()

        self.cmd = pool.DeletePool(self.app, None)

        self.client.delete_pool = mock.Mock()
        self.client.find_pool = mock.Mock()

    def test_delete_default(self):
        arglist = [
            'pool',
        ]

        verifylist = [
            ('pool', ['pool']),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.delete_pool.side_effect = [
            {}
        ]
        self.client.find_pool.side_effect = [
            self._object
        ]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.delete_pool.assert_called_once_with(
            pool=self._object.id,
            ignore_missing=False
        )
