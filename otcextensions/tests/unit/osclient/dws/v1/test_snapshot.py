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
from unittest.mock import call

from osc_lib import exceptions

from otcextensions.osclient.dws.v1 import snapshot
from otcextensions.osclient.dws.v1 import cluster
from otcextensions.tests.unit.osclient.dws.v1 import fakes

from openstackclient.tests.unit import utils as tests_utils


class TestListSnapshots(fakes.TestDws):

    objects = fakes.FakeSnapshot.create_multiple(3)

    column_list_headers = ('ID', 'Name', 'Cluster Id',)

    columns = ('id', 'name', 'cluster_id',)

    data = []

    for s in objects:
        data.append((s.id, s.name, s.cluster_id,))

    def setUp(self):
        super(TestListSnapshots, self).setUp()

        self.cmd = snapshot.ListSnapshots(self.app, None)

        self.client.snapshots = mock.Mock()
        self.client.api_mock = self.client.snapshots

    def test_list(self):
        arglist = [
        ]
        verifylist = [
        ]
        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with()

        self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(self.data, list(data))


class TestCreateSnapshot(fakes.TestDws):

    _cluster = fakes.FakeCluster.create_one()
    _data = fakes.FakeSnapshot.create_one()

    columns = (
        'id',
        'name',
        'cluster_id',
        'status',
        'size',
        'type',
        'created_at',
        'updated_at',
    )

    data = fakes.gen_data(_data, columns)

    default_timeout = 900

    def setUp(self):
        super(TestCreateSnapshot, self).setUp()

        self.cmd = snapshot.CreateSnapshot(self.app, None)

        self.client.find_cluster = mock.Mock(return_value=self._cluster)
        self.client.create_snapshot = mock.Mock(return_value=self._data)
        self.client.wait_for_snapshot = mock.Mock(return_value=True)

    def test_create(self):
        arglist = [
            self._cluster.name,
            'test-snapshot',
            '--description', 'test description',
            '--wait',
        ]
        verifylist = [
            ('cluster', self._cluster.name),
            ('name', 'test-snapshot'),
            ('description', 'test description'),
            ('wait', True),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        attrs = {
            'name': 'test-snapshot',
            'cluster_id': self._cluster.id,
            'description': 'test description',
        }
        self.client.create_snapshot.assert_called_with(**attrs)
        self.client.wait_for_cluster.assert_called_with(
            self._cluster.id, wait=self.default_timeout)
        self.assertEqual(self.columns, columns)


class TestShowSnapshot(fakes.TestDws):

    _snapshot = fakes.FakeSnapshot.create_one()

    columns = (
        'id',
        'name',
        'cluster_id',
        'status',
        'size',
        'type',
        'created_at',
        'updated_at',
    )

    data = fakes.gen_data(_snapshot, columns)

    def setUp(self):
        super(TestShowSnapshot, self).setUp()

        self.cmd = snapshot.ShowSnapshot(self.app, None)

        self.client.find_snapshot = mock.Mock(return_value=self._snapshot)

    def test_show_no_options(self):
        arglist = []
        verifylist = []

        # Testing that a call without the required argument will fail and
        # throw a "ParserExecption"
        self.assertRaises(tests_utils.ParserException,
                          self.check_parser, self.cmd, arglist, verifylist)

    def test_show(self):
        arglist = [
            self._snapshot.id,
        ]

        verifylist = [
            ('snapshot', self._snapshot.id),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.find_snapshot.assert_called_with(self._snapshot.id)

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)

    def test_show_non_existent(self):
        arglist = [
            'unexist_dws_snapshot',
        ]

        verifylist = [
            ('snapshot', 'unexist_dws_snapshot'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_result = exceptions.CommandError('Resource Not Found')
        self.client.find_snapshot = (
            mock.Mock(side_effect=find_mock_result)
        )

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual('Resource Not Found', str(e))
        self.client.find_snapshot.assert_called_with('unexist_dws_snapshot')


class TestRestoreSnapshot(fakes.TestDws):

    _cluster = cluster.format_response(
        fakes.FakeCluster.create_one())
    _snapshot = fakes.FakeSnapshot.create_one()

    columns = (
        'id',
        'name',
        'flavor',
        'availability_zone',
        'version',
        'num_nodes',
        'num_free_nodes',
        'user_name',
        'port',
        'private_domain',
        'private_ip',
        'floating_ip_address',
        'public_domain',
        'router_id',
        'network_id',
        'security_group_id',
        'recent_event',
        'spec_version',
        'status',
        'task_status',
        'sub_status',
        'action_progress',
        'created_at',
        'updated_at',
        'is_logical_cluster_initialed',
        'is_logical_cluster_mode',
        'is_logical_cluster_enabled',
        'maintenance_window',
        'enterprise_project_id',
    )

    data = fakes.gen_data(_cluster, columns, cluster._formatters)

    default_timeout = 1800

    def setUp(self):
        super(TestRestoreSnapshot, self).setUp()

        self.cmd = snapshot.RestoreSnapshot(self.app, None)

        self.client.restore_snapshot = mock.Mock(return_value=self._cluster)
        self.client.wait_for_cluster = mock.Mock(return_value=True)
        self.client.get_cluster = mock.Mock(return_value=self._cluster)

    def test_restore(self):
        arglist = [
            'restored-cluster',
            '--snapshot-id', self._snapshot.id,
            '--router-id', 'router-uuid',
            '--network-id', 'network-uuid',
            '--security-group-id', 'sg-uuid',
            '--port', '9000',
            '--availability-zone', 'test-az',
            '--enterprise-project-id', 'eps-uuid',
            '--floating-ip', 'auto',
            '--wait'
        ]
        verifylist = [
            ('name', 'restored-cluster'),
            ('snapshot_id', self._snapshot.id),
            ('vpc_id', 'router-uuid'),
            ('subnet_id', 'network-uuid'),
            ('security_group_id', 'sg-uuid'),
            ('port', 9000),
            ('availability_zone', 'test-az'),
            ('enterprise_project_id', 'eps-uuid'),
            ('floating_ip', 'auto'),
            ('wait', True),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        attrs = {
            'name': 'restored-cluster',
            'vpc_id': 'router-uuid',
            'subnet_id': 'network-uuid',
            'security_group_id': 'sg-uuid',
            'port': 9000,
            'availability_zone': 'test-az',
            'enterprise_project_id': 'eps-uuid',
            'public_ip': {
                'public_bind_type': 'auto_assign',
                'eip_id': ''
            }
        }
        self.client.restore_snapshot.assert_called_with(
            self._snapshot.id, **attrs)
        self.client.wait_for_cluster.assert_called_with(
            self._cluster.id, self.default_timeout)
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestDeleteSnapshot(fakes.TestDws):

    _snapshot = fakes.FakeSnapshot.create_multiple(2)

    def setUp(self):
        super(TestDeleteSnapshot, self).setUp()

        self.client.find_snapshot = mock.Mock(return_value=self._snapshot[0])
        self.client.delete_snapshot = mock.Mock(return_value=None)

        # Get the command object to test
        self.cmd = snapshot.DeleteSnapshot(self.app, None)

    def test_delete(self):
        arglist = [
            self._snapshot[0].id,
        ]

        verifylist = [
            ('snapshot', [self._snapshot[0].id]),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.find_snapshot.assert_called_with(
            self._snapshot[0].id, ignore_missing=False)
        self.client.delete_snapshot.assert_called_with(self._snapshot[0].id)
        self.assertIsNone(result)

    def test_multiple_delete(self):
        arglist = []
        snapshot_list = []

        for dws_snapshot in self._snapshot:
            snapshot_list.append(dws_snapshot.name)
            arglist.append(dws_snapshot.name)

        verifylist = [
            ('snapshot', snapshot_list),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)

        calls = []
        for dws_snapshot in self._snapshot:
            calls.append(call(dws_snapshot.name, ignore_missing=False))
        self.client.find_snapshot.assert_has_calls(calls)
        self.client.delete_snapshot.assert_any_call(self._snapshot[0].id)
        self.assertIsNone(result)

    def test_multiple_delete_with_exception(self):
        arglist = [
            self._snapshot[0].id,
            'unexist_dws_snapshot',
        ]
        verifylist = [
            ('snapshot', [self._snapshot[0].id, 'unexist_dws_snapshot']),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        delete_mock_results = [None, exceptions.CommandError]
        self.client.delete_snapshot = (
            mock.Mock(side_effect=delete_mock_results)
        )

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual('1 of 2 Snapshot(s) failed to delete.', str(e))

        self.client.delete_snapshot.assert_any_call(self._snapshot[0].id)
