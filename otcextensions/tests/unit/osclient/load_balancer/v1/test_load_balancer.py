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

from otcextensions.common import sdk_utils
from otcextensions.osclient.load_balancer.v1 import load_balancer
from otcextensions.tests.unit.osclient.load_balancer.v1 import fakes


class TestListLoadBalancer(fakes.TestLoadBalancer):

    _objects = fakes.FakeLoadBalancer.create_multiple(3)

    columns = ('id', 'name', 'project_id', 'vip_address',
               'provisioning_status', 'provider')

    data = []

    for s in _objects:
        data.append((
            s.id,
            s.name,
            s.project_id,
            s.vip_address,
            s.provisioning_status,
            s.provider,
        ))

    def setUp(self):
        super(TestListLoadBalancer, self).setUp()

        self.cmd = load_balancer.ListLoadBalancer(self.app, None)

        self.client.load_balancers = mock.Mock()

    def test_list_default(self):
        arglist = [
        ]

        verifylist = [
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.load_balancers.side_effect = [
            self._objects
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.load_balancers.assert_called_once_with()

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))


class TestShowLoadBalancer(fakes.TestLoadBalancer):

    _object = fakes.FakeLoadBalancer.create_one()

    columns = ('admin_state_up', 'description', 'id',
               'listener_ids', 'name', 'operating_status', 'pool_ids',
               'project_id', 'provider', 'provisioning_status', 'vip_address',
               'vip_port_id', 'vip_subnet_id')

    data = (
        _object.is_admin_state_up,
        _object.description,
        _object.id,
        sdk_utils.ListOfIdsColumnBR(_object.listener_ids),
        _object.name,
        _object.operating_status,
        sdk_utils.ListOfIdsColumnBR(_object.pool_ids),
        _object.project_id,
        _object.provider,
        _object.provisioning_status,
        _object.vip_address,
        _object.vip_port_id,
        _object.vip_subnet_id,
    )

    def setUp(self):
        super(TestShowLoadBalancer, self).setUp()

        self.cmd = load_balancer.ShowLoadBalancer(self.app, None)

        self.client.find_load_balancer = mock.Mock()

    def test_show_default(self):
        arglist = [
            'lb'
        ]

        verifylist = [
            ('load_balancer', 'lb')
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.find_load_balancer.side_effect = [
            self._object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_load_balancer.assert_called_once_with(
            name_or_id='lb',
            ignore_missing=False
        )

        self.assertEqual(self.columns, columns)
        self.assertItemEqual(self.data, data)


class TestCreateLoadBalancer(fakes.TestLoadBalancer):

    _object = fakes.FakeLoadBalancer.create_one()

    columns = (
        'admin_state_up',
        'description',
        'id',
        'listener_ids',
        'name',
        'operating_status',
        'pool_ids',
        'project_id',
        'provider',
        'provisioning_status',
        'vip_address',
        'vip_port_id',
        'vip_subnet_id')

    data = (
        _object.is_admin_state_up,
        _object.description,
        _object.id,
        sdk_utils.ListOfIdsColumnBR(_object.listener_ids),
        _object.name,
        _object.operating_status,
        sdk_utils.ListOfIdsColumnBR(_object.pool_ids),
        _object.project_id,
        _object.provider,
        _object.provisioning_status,
        _object.vip_address,
        _object.vip_port_id,
        _object.vip_subnet_id,
    )

    def setUp(self):
        super(TestCreateLoadBalancer, self).setUp()

        self.cmd = load_balancer.CreateLoadBalancer(self.app, None)

        self.client.create_load_balancer = mock.Mock()

    def test_create_default(self):
        arglist = [
            '--disable',
            '--description', 'descr',
            '--name', 'nm',
            '--vip_address', 'vip_addr',
            '--vip_network_id', 'vip_network_id',
            '--vip_qos_policy_id', 'vip_qos_policy_id'
        ]

        verifylist = [
            ('disable', True),
            ('description', 'descr'),
            ('name', 'nm'),
            ('vip_address', 'vip_addr'),
            ('vip_network_id', 'vip_network_id'),
            ('vip_qos_policy_id', 'vip_qos_policy_id'),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.create_load_balancer.side_effect = [
            self._object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_load_balancer.assert_called_once_with(
            is_admin_state_up=False,
            description='descr',
            name='nm',
            vip_address='vip_addr',
            vip_network_id='vip_network_id',
            vip_qos_policy_id='vip_qos_policy_id'
        )

        self.assertEqual(self.columns, columns)
        self.assertItemEqual(self.data, data)

    def test_create_subnet(self):
        arglist = [
            '--vip_subnet_id', 'vip_subnet_id',
        ]

        verifylist = [
            ('vip_subnet_id', 'vip_subnet_id'),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.create_load_balancer.side_effect = [
            self._object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_load_balancer.assert_called_once_with(
            vip_subnet_id='vip_subnet_id',
        )

        self.assertEqual(self.columns, columns)
        self.assertItemEqual(self.data, data)

    def test_create_port(self):
        arglist = [
            '--vip_port_id', 'vip_port_id',
        ]

        verifylist = [
            ('vip_port_id', 'vip_port_id'),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.create_load_balancer.side_effect = [
            self._object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_load_balancer.assert_called_once_with(
            vip_port_id='vip_port_id',
        )

        self.assertEqual(self.columns, columns)
        self.assertItemEqual(self.data, data)


class TestUpdateLoadBalancer(fakes.TestLoadBalancer):

    _object = fakes.FakeLoadBalancer.create_one()

    columns = (
        'admin_state_up', 'description', 'id',
        'listener_ids', 'name', 'operating_status',
        'pool_ids', 'project_id', 'provider',
        'provisioning_status', 'vip_address',
        'vip_port_id', 'vip_subnet_id')

    data = (
        _object.is_admin_state_up,
        _object.description,
        _object.id,
        sdk_utils.ListOfIdsColumnBR(_object.listener_ids),
        _object.name,
        _object.operating_status,
        sdk_utils.ListOfIdsColumnBR(_object.pool_ids),
        _object.project_id,
        _object.provider,
        _object.provisioning_status,
        _object.vip_address,
        _object.vip_port_id,
        _object.vip_subnet_id,
    )

    def setUp(self):
        super(TestUpdateLoadBalancer, self).setUp()

        self.cmd = load_balancer.SetLoadBalancer(self.app, None)

        self.client.update_load_balancer = mock.Mock()

    def test_update_default(self):
        arglist = [
            'lb',
            '--disable',
            '--description', 'descr',
            '--name', 'nm',
            '--vip_qos_policy_id', 'vip_qos_policy_id'
        ]

        verifylist = [
            ('load_balancer', 'lb'),
            ('disable', True),
            ('description', 'descr'),
            ('name', 'nm'),
            ('vip_qos_policy_id', 'vip_qos_policy_id'),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.update_load_balancer.side_effect = [
            self._object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.update_load_balancer.assert_called_once_with(
            load_balancer='lb',
            # is_admin_state_up=False,
            description='descr',
            name='nm',
            vip_qos_policy_id='vip_qos_policy_id'
        )

        self.assertEqual(self.columns, columns)
        self.assertItemEqual(self.data, data)


class TestDeleteLoadBalancer(fakes.TestLoadBalancer):

    def setUp(self):
        super(TestDeleteLoadBalancer, self).setUp()

        self.cmd = load_balancer.DeleteLoadBalancer(self.app, None)

        self.client.delete_load_balancer = mock.Mock()

    def test_create_default(self):
        arglist = [
            'lb',
        ]

        verifylist = [
            ('load_balancer', ['lb']),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.delete_load_balancer.side_effect = [
            {}
        ]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.delete_load_balancer.assert_called_once_with(
            load_balancer='lb',
            ignore_missing=False
        )
