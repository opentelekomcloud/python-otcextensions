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
# from osc_lib.cli import format_columns

from otcextensions.osclient.dws.v1 import cluster
from otcextensions.tests.unit.osclient.dws.v1 import fakes

from openstackclient.tests.unit import utils as tests_utils


_COLUMNS = (
    'action_progress',
    'availability_zone',
    'created_at',
    'endpoints',
    'enterprise_project_id',
    'flavor',
    'flavor_id',
    'floating_ip',
    'guest_agent_version',
    'id',
    'is_logical_cluster_enabled',
    'is_logical_cluster_initialed',
    'is_logical_cluster_mode',
    'maintenance_window',
    'name',
    'network_id',
    'nodes',
    'num_free_nodes',
    'num_nodes',
    'num_recent_events',
    'parameter_group',
    'port',
    'private_domain',
    'private_ip',
    'public_domain',
    'public_endpoints',
    'router_id',
    'security_group_id',
    'spec_version',
    'status',
    'sub_status',
    'tags',
    'task_status',
    'updated_at',
    'user_name',
    'version'
)


class TestListClusters(fakes.TestDws):

    objects = fakes.FakeCluster.create_multiple(3)

    column_list_headers = (
        'ID',
        'Name',
        'Num Nodes',
        'Flavor',
        'Status',
        'Version',
        'Created At'
    )

    columns = (
        'id',
        'name',
        'num_nodes',
        'flavor',
        'status',
        'version',
        'created_at'
    )

    data = []

    for s in objects:
        data.append(
            (
                s.id,
                s.name,
                s.num_nodes,
                s.flavor,
                s.status,
                s.version,
                s.created_at,
            )
        )

    def setUp(self):
        super(TestListClusters, self).setUp()

        self.cmd = cluster.ListClusters(self.app, None)

        self.client.clusters = mock.Mock()
        self.client.api_mock = self.client.clusters

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


class TestCreateCluster(fakes.TestDws):

    _cluster = fakes.FakeCluster.create_one()

    columns = _COLUMNS

    data = fakes.gen_data(_cluster, columns, cluster._formatters)

    default_timeout = 1800

    def setUp(self):
        super(TestCreateCluster, self).setUp()

        self.cmd = cluster.CreateCluster(self.app, None)

        self.client.create_cluster = mock.Mock(return_value=self._cluster)
        self.client.get_cluster = mock.Mock(return_value=self._cluster)
        self.client.wait_for_cluster = mock.Mock(return_value=True)

    def test_create(self):
        arglist = [
            'test-dws',
            '--flavor', 'dws-flavor',
            '--router-id', 'router-uuid',
            '--network-id', 'network-uuid',
            '--security-group-id', 'sg-uuid',
            '--num-nodes', '3',
            '--num-cn', '2',
            '--port', '9000',
            '--username', 'dbadmin',
            '--password', 'testtest',
            '--enterprise-project-id', 'enterprise-uuid',
            '--availability-zone', 'test-az',
            '--floating-ip', 'auto',
            '--wait'
        ]
        verifylist = [
            ('name', 'test-dws'),
            ('node_type', 'dws-flavor'),
            ('vpc_id', 'router-uuid'),
            ('subnet_id', 'network-uuid'),
            ('security_group_id', 'sg-uuid'),
            ('number_of_node', 3),
            ('number_of_cn', 2),
            ('port', 9000),
            ('user_name', 'dbadmin'),
            ('user_pwd', 'testtest'),
            ('enterprise_project_id', 'enterprise-uuid'),
            ('availability_zone', 'test-az'),
            ('floating_ip', 'auto'),
            ('wait', True),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        attrs = {
            'name': 'test-dws',
            'number_of_node': 3,
            'number_of_cn': 2,
            'node_type': 'dws-flavor',
            'vpc_id': 'router-uuid',
            'subnet_id': 'network-uuid',
            'security_group_id': 'sg-uuid',
            'user_name': 'dbadmin',
            'user_pwd': 'testtest',
            'port': 9000,
            'enterprise_project_id': 'enterprise-uuid',
            'availability_zone': 'test-az',
            'public_ip': {
                'public_bind_type': 'auto_assign',
                'eip_id': ''
            }
        }
        self.client.create_cluster.assert_called_with(**attrs)
        self.client.wait_for_cluster.assert_called_with(
            self._cluster.id, wait=self.default_timeout)
        self.client.get_cluster.assert_called_with(self._cluster.id)
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestRestartCluster(fakes.TestDws):

    _cluster = fakes.FakeCluster.create_one()

    default_timeout = 300

    def setUp(self):
        super(TestRestartCluster, self).setUp()

        self.cmd = cluster.RestartCluster(self.app, None)

        self.client.find_cluster = mock.Mock(return_value=self._cluster)
        self.client.restart_cluster = mock.Mock(return_value=None)
        self.client.wait_for_cluster = mock.Mock(return_value=True)

    def test_restart(self):
        arglist = [
            self._cluster.name,
            '--wait',
        ]

        verifylist = [
            ('cluster', self._cluster.name),
            ('wait', True),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.find_cluster.assert_called_with(self._cluster.name)
        self.client.restart_cluster.assert_called_with(self._cluster)
        self.client.wait_for_cluster.assert_called_with(
            self._cluster.id, wait=self.default_timeout)
        self.assertIsNone(result)


class TestClusterPasswordReset(fakes.TestDws):

    _cluster = fakes.FakeCluster.create_one()

    def setUp(self):
        super(TestClusterPasswordReset, self).setUp()

        self.cmd = cluster.ResetPassword(self.app, None)

        self.client.find_cluster = mock.Mock(return_value=self._cluster)
        self.client.reset_password = mock.Mock(return_value=None)

    def test_password_reset(self):
        arglist = [
            self._cluster.name,
            '--password', 'TestPasswordReset'
        ]

        verifylist = [
            ('cluster', self._cluster.name),
            ('password', 'TestPasswordReset'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.find_cluster.assert_called_with(self._cluster.name)
        self.client.reset_password.assert_called_with(self._cluster,
                                                      'TestPasswordReset')
        self.assertIsNone(result)


class TestExtendCluster(fakes.TestDws):

    _cluster = fakes.FakeCluster.create_one()

    default_timeout = 1800

    def setUp(self):
        super(TestExtendCluster, self).setUp()

        self.cmd = cluster.ExtendCluster(self.app, None)

        self.client.find_cluster = mock.Mock(return_value=self._cluster)
        self.client.extend_cluster = mock.Mock(return_value=None)
        self.client.wait_for_cluster = mock.Mock(return_value=True)

    def test_extend(self):
        arglist = [
            self._cluster.name,
            '--add-nodes', '2',
            '--wait',
        ]

        verifylist = [
            ('cluster', self._cluster.name),
            ('add_nodes', 2),
            ('wait', True),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.find_cluster.assert_called_with(self._cluster.name)
        self.client.extend_cluster.assert_called_with(self._cluster, 2)
        self.client.wait_for_cluster.assert_called_with(
            self._cluster.id, wait=self.default_timeout)

        self.assertIsNone(result)


class TestShowCluster(fakes.TestDws):

    _cluster = fakes.FakeCluster.create_one()
    columns = _COLUMNS
    data = fakes.gen_data(_cluster, columns, cluster._formatters)

    def setUp(self):
        super(TestShowCluster, self).setUp()

        self.cmd = cluster.ShowCluster(self.app, None)

        self.client.find_cluster = mock.Mock(return_value=self._cluster)
        self.client.get_cluster = mock.Mock(return_value=self._cluster)

    def test_show_no_options(self):
        arglist = []
        verifylist = []

        # Testing that a call without the required argument will fail and
        # throw a "ParserExecption"
        self.assertRaises(tests_utils.ParserException,
                          self.check_parser, self.cmd, arglist, verifylist)

    def test_show(self):
        arglist = [
            self._cluster.id,
        ]

        verifylist = [
            ('cluster', self._cluster.id),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.find_cluster.assert_called_with(self._cluster.id)

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)

    def test_show_non_existent(self):
        arglist = [
            'unexist_dws_cluster',
        ]

        verifylist = [
            ('cluster', 'unexist_dws_cluster'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_result = exceptions.CommandError('Resource Not Found')
        self.client.find_cluster = (
            mock.Mock(side_effect=find_mock_result)
        )

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual('Resource Not Found', str(e))
        self.client.find_cluster.assert_called_with('unexist_dws_cluster')


class TestDeleteCluster(fakes.TestDws):

    _cluster = fakes.FakeCluster.create_multiple(2)

    def setUp(self):
        super(TestDeleteCluster, self).setUp()

        self.client.find_cluster = mock.Mock(return_value=self._cluster[0])
        self.client.delete_cluster = mock.Mock(return_value=None)

        # Get the command object to test
        self.cmd = cluster.DeleteCluster(self.app, None)

    def test_delete(self):
        arglist = [
            self._cluster[0].name,
        ]

        verifylist = [
            ('cluster', arglist),
            ('keep_last_manual_snapshot', 0),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.find_cluster.assert_called_with(
            self._cluster[0].name, ignore_missing=False)
        self.client.delete_cluster.assert_called_with(self._cluster[0].id, 0)
        self.assertIsNone(result)

    def test_multiple_delete(self):
        arglist = []

        for dws_cluster in self._cluster:
            arglist.append(dws_cluster.name)

        verifylist = [
            ('cluster', arglist),
            ('keep_last_manual_snapshot', 0),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_results = self._cluster
        self.client.find_cluster = (
            mock.Mock(side_effect=find_mock_results)
        )

        # Trigger the action
        result = self.cmd.take_action(parsed_args)

        find_calls = []
        delete_calls = []
        for dws_cluster in self._cluster:
            find_calls.append(call(dws_cluster.name, ignore_missing=False))
            delete_calls.append(call(dws_cluster.id, 0))
        self.client.find_cluster.assert_has_calls(find_calls)
        self.client.delete_cluster.assert_has_calls(delete_calls)
        self.assertIsNone(result)

    def test_multiple_delete_with_exception(self):
        arglist = [
            self._cluster[0].id,
            'unexist_dws_cluster',
        ]
        verifylist = [
            ('cluster', arglist),
            ('keep_last_manual_snapshot', 0),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_results = [self._cluster[0], exceptions.CommandError]
        self.client.find_cluster = (
            mock.Mock(side_effect=find_mock_results)
        )

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual('1 of 2 Cluster(s) failed to delete.', str(e))

        self.client.delete_cluster.assert_any_call(self._cluster[0].id, 0)
