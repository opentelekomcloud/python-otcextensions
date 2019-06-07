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

from otcextensions.osclient.auto_scaling.v1 import group
from otcextensions.tests.unit.osclient.auto_scaling.v1 import fakes


class TestAutoScalingGroup(fakes.TestAutoScaling):

    def setUp(self):
        super(TestAutoScalingGroup, self).setUp()
        self.client = self.app.client_manager.auto_scaling


class TestListAutoScalingGroup(TestAutoScalingGroup):

    groups = fakes.FakeGroup.create_multiple(3)

    columns = ('ID', 'Name', 'status', 'detail')

    data = []

    for s in groups:
        data.append((
            s.id,
            s.name,
            s.status,
            s.detail
        ))

    def setUp(self):
        super(TestListAutoScalingGroup, self).setUp()

        self.cmd = group.ListAutoScalingGroup(self.app, None)

        self.client.groups = mock.Mock()

    def test_list_default(self):
        arglist = [
        ]

        verifylist = [
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.groups.side_effect = [
            self.groups
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.groups.assert_called_once_with()

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))


class TestShowAutoScalingGroup(TestAutoScalingGroup):

    columns = ('create_time', 'detail', 'id', 'name', 'network_id', 'status')

    _group = fakes.FakeGroup.create_one()

    data = (
        _group.create_time,
        _group.detail,
        _group.id,
        _group.name,
        _group.network_id,
        _group.status,
    )

    def setUp(self):
        super(TestShowAutoScalingGroup, self).setUp()

        self.cmd = group.ShowAutoScalingGroup(self.app, None)

        self.client.find_group = mock.Mock()

    def test_show_default(self):
        arglist = [
            'test_group'
        ]
        verifylist = [
            ('group', 'test_group')
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.find_group.side_effect = [
            self._group
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_group.assert_called()

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestCreateAutoScalingGroup(TestAutoScalingGroup):

    columns = ('create_time', 'detail', 'id', 'name', 'network_id', 'status')

    _group = fakes.FakeGroup.create_one()

    data = (
        _group.create_time,
        _group.detail,
        _group.id,
        _group.name,
        _group.network_id,
        _group.status,
    )

    def setUp(self):
        super(TestCreateAutoScalingGroup, self).setUp()

        self.cmd = group.CreateAutoScalingGroup(self.app, None)

        self.client.create_group = mock.Mock()

    def test_create(self):
        arglist = [
            '--desire_instance_number', '10',
            '--min_instance_number', '1',
            '--max_instance_number', '15',
            '--cool_down_time', '1',
            '--availability_zone', 'eu-1',
            '--availability_zone', 'eu-2',
            '--subnet', 'sub1',
            '--subnet', 'sub2',
            '--router', 'vpc-1',
            '--security_group', 'sg1',
            '--security_group', 'sg2',
            '--lb_listener_id', 'lb1',
            '--lbaas_listener', 'lbas1:14',
            '--lbaas_listener', 'lbas2:15:10',
            '--audit_method', 'some_method',
            '--audit_time', '15',
            '--terminate_policy', 'pol',
            '--notification', 'EMAIL',
            '--notification', 'SMS',

            'test_name'
        ]
        verifylist = [
            ('desire_instance_number', 10),
            ('min_instance_number', 1),
            ('max_instance_number', 15),
            ('cool_down_time', 1),
            ('availability_zone', ['eu-1', 'eu-2']),
            ('subnet', ['sub1', 'sub2']),
            ('security_group', ['sg1', 'sg2']),
            ('router', 'vpc-1'),
            ('lb_listener_id', 'lb1'),
            ('lbaas_listener', ['lbas1:14', 'lbas2:15:10']),
            ('audit_method', 'some_method'),
            ('audit_time', 15),
            ('terminate_policy', 'pol'),
            ('notification', ['EMAIL', 'SMS']),
            ('name', 'test_name')
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.create_group.side_effect = [
            self._group
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_group.assert_called_with(
            available_zones=['eu-1', 'eu-2'],
            cool_down_time=1,
            desire_instance_number=10,
            health_periodic_audit_method='some_method',
            health_periodic_audit_time=15,
            instance_terminate_policy='pol',
            lb_listener_id='lb1',
            lbaas_listeners=[
                {'id': 'lbas1', 'protocol_port': '14'},
                {'id': 'lbas2', 'protocol_port': '15', 'weight': '10'}],
            max_instance_number=15,
            min_instance_number=1,
            name='test_name',
            networks=[{'id': 'sub1'}, {'id': 'sub2'}],
            notifications=['EMAIL', 'SMS'],
            security_groups=[{'id': 'sg1'}, {'id': 'sg2'}],
            vpc_id='vpc-1'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestDeleteAutoScalingGroup(TestAutoScalingGroup):

    def setUp(self):
        super(TestDeleteAutoScalingGroup, self).setUp()

        self.cmd = group.DeleteAutoScalingGroup(self.app, None)

        self.client.delete_group = mock.Mock()

    def test_sdelete(self):
        arglist = [
            'group1'
        ]
        verifylist = [
            ('group', 'group1')
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.delete_group.side_effect = [{}]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.delete_group.assert_called()


class TestUpdateAutoScalingGroup(TestAutoScalingGroup):

    columns = ('create_time', 'detail', 'id', 'name', 'network_id', 'status')

    _group = fakes.FakeGroup.create_one()

    data = (
        _group.create_time,
        _group.detail,
        _group.id,
        _group.name,
        _group.network_id,
        _group.status,
    )

    def setUp(self):
        super(TestUpdateAutoScalingGroup, self).setUp()

        self.cmd = group.UpdateAutoScalingGroup(self.app, None)

        self.client.update_group = mock.Mock()

    def test_create(self):
        arglist = [
            '--desire_instance_number', '10',
            '--min_instance_number', '1',
            '--max_instance_number', '15',
            '--cool_down_time', '1',
            '--availability_zone', 'eu-1',
            '--availability_zone', 'eu-2',
            '--subnetwork', 'sub1',
            '--subnetwork', 'sub2',
            '--network_id', 'vpc-1',
            '--security_group', 'sg1',
            '--security_group', 'sg2',
            '--lb_listener_id', 'lb1',
            '--lbaas_listener', 'lbas1:14',
            '--lbaas_listener', 'lbas2:15:10',
            '--audit_method', 'some_method',
            '--audit_time', '15',
            '--terminate_policy', 'pol',
            '--notification', 'EMAIL',
            '--notification', 'SMS',

            'test_name'
        ]
        verifylist = [
            ('desire_instance_number', 10),
            ('min_instance_number', 1),
            ('max_instance_number', 15),
            ('cool_down_time', 1),
            ('availability_zone', ['eu-1', 'eu-2']),
            ('subnetwork', ['sub1', 'sub2']),
            ('security_group', ['sg1', 'sg2']),
            ('network_id', 'vpc-1'),
            ('lb_listener_id', 'lb1'),
            ('lbaas_listener', ['lbas1:14', 'lbas2:15:10']),
            ('audit_method', 'some_method'),
            ('audit_time', 15),
            ('terminate_policy', 'pol'),
            ('notification', ['EMAIL', 'SMS']),
            ('group', 'test_name')
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.update_group.side_effect = [
            self._group
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.update_group.assert_called_with(
            available_zones=['eu-1', 'eu-2'],
            cool_down_time=1,
            desire_instance_number=10,
            health_periodic_audit_method='some_method',
            health_periodic_audit_time=15,
            instance_terminate_policy='pol',
            lb_listener_id='lb1',
            lbaas_listeners=[
                {'id': 'lbas1', 'protocol_port': '14'},
                {'id': 'lbas2', 'protocol_port': '15', 'weight': '10'}],
            max_instance_number=15,
            min_instance_number=1,
            group='test_name',
            networks=[{'id': 'sub1'}, {'id': 'sub2'}],
            notifications=['EMAIL', 'SMS'],
            security_groups=[{'id': 'sg1'}, {'id': 'sg2'}],
            vpc_id='vpc-1'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestEnableAutoScalingGroup(TestAutoScalingGroup):

    _group = fakes.FakeGroup.create_one()

    def setUp(self):
        super(TestEnableAutoScalingGroup, self).setUp()

        self.cmd = group.EnableAutoScalingGroup(self.app, None)

        self.client.find_group = mock.Mock()
        self.client.resume_group = mock.Mock()

    def test_enable(self):
        arglist = [
            'group1'
        ]
        verifylist = [
            ('group', 'group1')
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.find_group.side_effect = [
            self._group
        ]
        self.client.resume_group.side_effect = [{}]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.find_group.assert_called()
        self.client.resume_group.assert_called()


class TestDisableAutoScalingGroup(TestAutoScalingGroup):

    _group = fakes.FakeGroup.create_one()

    def setUp(self):
        super(TestDisableAutoScalingGroup, self).setUp()

        self.cmd = group.DisableAutoScalingGroup(self.app, None)

        self.client.find_group = mock.Mock()
        self.client.pause_group = mock.Mock()

    def test_disable(self):
        arglist = [
            'group1'
        ]
        verifylist = [
            ('group', 'group1')
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.find_group.side_effect = [
            self._group
        ]
        self.client.pause_group.side_effect = [{}]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.find_group.assert_called()
        self.client.pause_group.assert_called()
