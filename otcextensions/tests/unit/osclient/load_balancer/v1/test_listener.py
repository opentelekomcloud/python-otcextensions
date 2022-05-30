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
from otcextensions.osclient.load_balancer.v1 import listener
from otcextensions.tests.unit.osclient.load_balancer.v1 import fakes


class TestListListener(fakes.TestLoadBalancer):

    _objects = fakes.FakeListener.create_multiple(3)

    columns = (
        'id', 'default_pool_id', 'name', 'project_id',
        'protocol', 'protocol_port', 'admin_state_up')

    data = []

    for s in _objects:
        data.append((
            s.id,
            s.default_pool_id,
            s.name,
            s.project_id,
            s.protocol,
            s.protocol_port,
            # sdk_utils.ListOfIdsColumn(s.load_balancer_ids),
            s.is_admin_state_up,
        ))

    def setUp(self):
        super(TestListListener, self).setUp()

        self.cmd = listener.ListListener(self.app, None)

        self.client.listeners = mock.Mock()

    def test_list_default(self):
        arglist = [
        ]

        verifylist = [
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.listeners.side_effect = [
            self._objects
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.listeners.assert_called_once_with()

        self.assertEqual(self.columns, columns)
        self.assertListItemEqual(self.data, list(data))

    def test_list_filters(self):
        arglist = [
            '--protocol', 'TCP',
            '--protocol_port', '12',
            '--name', 'some_name',
            '--load_balancer', 'lb'
        ]

        verifylist = [
            ('protocol', 'TCP'),
            ('protocol_port', 12),
            ('name', 'some_name'),
            ('load_balancer', 'lb')
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.listeners.side_effect = [
            self._objects
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.listeners.assert_called_once_with(
            protocol='TCP',
            protocol_port=12,
            name='some_name',
            load_balancer_id='lb'
        )

        self.assertEqual(self.columns, columns)
        self.assertListItemEqual(self.data, list(data))

    def test_list_filters_exceptions_proto(self):
        arglist = [
            '--protocol', 'SMTP',
            '--protocol_port', '12'
        ]

        verifylist = [
            ('protocol', 'SMTP'),
            ('protocol_port', 12)
        ]

        self.assertRaises(
            utils.ParserException,
            self.check_parser, self.cmd, arglist, verifylist)

    def test_list_filters_exceptions_port(self):
        arglist = [
            '--protocol_port', '12x'
        ]

        verifylist = [
            ('protocol_port', 12)
        ]

        # Ensure exception is raised
        self.assertRaises(
            utils.ParserException,
            self.check_parser, self.cmd, arglist, verifylist)


class TestShowListener(fakes.TestLoadBalancer):

    _object = fakes.FakeListener.create_one()

    columns = (
        'admin_state_up', 'connection_limit', 'default_pool_id',
        'description', 'id', 'loadbalancers', 'name', 'protocol',
        'protocol_port')

    data = (
        _object.is_admin_state_up,
        _object.connection_limit,
        _object.default_pool_id,
        _object.description,
        _object.id,
        sdk_utils.ListOfIdsColumnBR(_object.load_balancer_ids),
        _object.name,
        _object.protocol,
        _object.protocol_port,
    )

    def setUp(self):
        super(TestShowListener, self).setUp()

        self.cmd = listener.ShowListener(self.app, None)

        self.client.find_listener = mock.Mock()

    def test_show_default(self):
        arglist = [
            'lb'
        ]

        verifylist = [
            ('listener', 'lb')
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.find_listener.side_effect = [
            self._object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_listener.assert_called_once_with(
            name_or_id='lb',
            ignore_missing=False
        )

        self.assertEqual(self.columns, columns)
        self.assertItemEqual(self.data, data)


class TestCreateListener(fakes.TestLoadBalancer):

    _object = fakes.FakeListener.create_one()

    columns = (
        'admin_state_up', 'connection_limit', 'default_pool_id',
        'description', 'id', 'loadbalancers', 'name', 'protocol',
        'protocol_port')

    data = (
        _object.is_admin_state_up,
        _object.connection_limit,
        _object.default_pool_id,
        _object.description,
        _object.id,
        sdk_utils.ListOfIdsColumnBR(_object.load_balancer_ids),
        _object.name,
        _object.protocol,
        _object.protocol_port,
    )

    def setUp(self):
        super(TestCreateListener, self).setUp()

        self.cmd = listener.CreateListener(self.app, None)

        self.client.create_listener = mock.Mock()

    def test_create_default(self):
        arglist = [
            'lb',
            '--protocol', 'tcp',
            '--protocol_port', '134',
            '--disable',
            '--connection_limit', '-1',
            '--default_pool', 'pool',
            '--default_tls_container_ref', 'default_tls_container_ref',
            '--description', 'description',
            '--name', 'name'
        ]

        verifylist = [
            ('protocol', 'TCP'),
            ('protocol_port', 134),
            ('load_balancer', 'lb'),
            ('disable', True),
            ('connection_limit', -1),
            ('default_pool', 'pool'),
            ('default_tls_container_ref', 'default_tls_container_ref'),
            ('description', 'description'),
            ('name', 'name')
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.create_listener.side_effect = [
            self._object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_listener.assert_called_once_with(
            connection_limit=-1,
            default_pool_id='pool',
            default_tls_container_ref='default_tls_container_ref',
            description='description',
            is_admin_state_up=False,
            load_balancer_id='lb',
            name='name',
            protocol='TCP',
            protocol_port=134
        )

        self.assertEqual(self.columns, columns)
        self.assertItemEqual(self.data, data)


class TestUpdateListener(fakes.TestLoadBalancer):

    _object = fakes.FakeListener.create_one()

    columns = (
        'ID', 'Name', 'description',
        'is_admin_state_up', 'protocol', 'protocol_port',
        'load_balancer_ids', 'default_pool_id',
        'connection_limit')

    data = (
        _object.id,
        _object.name,
        _object.description,
        _object.is_admin_state_up,
        _object.protocol,
        _object.protocol_port,
        sdk_utils.ListOfIdsColumn(_object.load_balancer_ids),
        _object.default_pool_id,
        _object.connection_limit,
    )

    def setUp(self):
        super(TestUpdateListener, self).setUp()

        self.cmd = listener.SetListener(self.app, None)

        self.client.update_listener = mock.Mock()

    def test_update_default(self):
        arglist = [
            'lsnr',
            '--disable',
            '--connection_limit', '-1',
            '--default_pool', 'pool',
            '--default_tls_container_ref', 'default_tls_container_ref',
            '--description', 'description',
            '--name', 'name'
        ]

        verifylist = [
            ('listener', 'lsnr'),
            ('disable', True),
            ('connection_limit', -1),
            ('default_pool', 'pool'),
            ('default_tls_container_ref', 'default_tls_container_ref'),
            ('description', 'description'),
            ('name', 'name')
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.update_listener.side_effect = [
            self._object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.update_listener.assert_called_once_with(
            is_admin_state_up=False,
            listener='lsnr',
            connection_limit=-1,
            default_pool_id='pool',
            default_tls_container_ref='default_tls_container_ref',
            description='description',
            name='name',
        )


class TestDeleteListener(fakes.TestLoadBalancer):

    _object = fakes.FakeListener.create_one()

    def setUp(self):
        super(TestDeleteListener, self).setUp()

        self.cmd = listener.DeleteListener(self.app, None)

        self.client.delete_listener = mock.Mock()
        self.client.find_listener = mock.Mock()

    def test_delete_default(self):
        arglist = [
            'lsnr',
        ]

        verifylist = [
            ('listener', ['lsnr']),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.delete_listener.side_effect = [
            {}
        ]
        self.client.find_listener.side_effect = [
            self._object
        ]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.delete_listener.assert_called_once_with(
            listener=self._object.id,
            ignore_missing=False
        )
