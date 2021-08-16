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

from otcextensions.osclient.css.v1 import cluster
from otcextensions.tests.unit.osclient.css.v1 import fakes

from openstackclient.tests.unit import utils as tests_utils
from collections import defaultdict


COLUMNS = (
    'id',
    'name',
    'type',
    'version',
    'endpoint',
    'disk_encryption',
    'cmk_id',
    'error',
    'instance',
    'instance_count',
    'node_count',
    'is_disk_encrypted',
    'is_https_enabled',
    'progress',
    'router_id',
    'subnet_id',
    'security_group_id',
    'status',
    'created_at',
    'updated_at'
)


class TestListClusters(fakes.TestCss):

    objects = fakes.FakeCluster.create_multiple(3)

    column_list_headers = (
        'ID',
        'Name',
        'Type',
        'Version',
        'Status',
        'Created At'
    )

    columns = ('id', 'name', 'type', 'version', 'status', 'created_at')

    data = []

    for s in objects:
        data.append(
            (
                s.id,
                s.name,
                s.datastore['type'],
                s.datastore['version'],
                s.status,
                s.created_at
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


class TestCreateCluster(fakes.TestCss):

    _data = fakes.FakeCluster.create_one()

    columns = COLUMNS

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestCreateCluster, self).setUp()

        self.cmd = cluster.CreateCluster(self.app, None)

        self.client.create_cluster = mock.Mock(return_value=self._data)
        self.client.get_cluster = mock.Mock(return_value=self._data)

    def test_create(self):
        arglist = [
            '--name', 'test-css',
            '--flavor', 'css-flavor',
            '--router-id', 'router-uuid',
            '--network-id', 'network-uuid',
            '--security-group-id', 'sg-uuid',
            '--instanceNum', '2',
            '--volume-type', 'COMMON',
            '--volume-size', '60'
        ]
        verifylist = [
            ('name', 'test-css'),
            ('flavor', 'css-flavor'),
            ('router_id', 'router-uuid'),
            ('network_id', 'network-uuid'),
            ('security_group_id', 'sg-uuid'),
            ('volume_type', 'COMMON'),
            ('volume_size', 60),
            ('instanceNum', 2),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        attrs = {
            'name': 'test-css',
            'instanceNum': 2,
            'instance': {
                'flavorRef': 'css-flavor',
                'volume': {
                    'volume_type': 'COMMON',
                    'size': 60
                },
                'nics': {
                    'vpcId': 'router-uuid',
                    'netId': 'network-uuid',
                    'securityGroupId': 'sg-uuid'
                }
            }
        }
        self.client.create_cluster.assert_called_with(**attrs)
        self.client.get_cluster.assert_called_with(self._data.id)
        self.assertEqual(self.columns, columns)


class TestRestartCluster(fakes.TestCss):

    _data = fakes.FakeCluster.create_one()

    columns = COLUMNS

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestRestartCluster, self).setUp()

        self.cmd = cluster.RestartCluster(self.app, None)

        self.client.restart_cluster = mock.Mock(return_value=None)
        self.client.get_cluster = mock.Mock(return_value=self._data)

    def test_restart(self):
        arglist = [
            self._data.id,
        ]

        verifylist = [
            ('cluster', self._data.id),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.restart_cluster.assert_called_with(self._data.id)
        self.client.get_cluster.assert_called_with(self._data.id)

        self.assertEqual(self.columns, columns)


class TestExtendCluster(fakes.TestCss):

    _data = fakes.FakeCluster.create_one()

    columns = COLUMNS

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestExtendCluster, self).setUp()

        self.cmd = cluster.ExtendCluster(self.app, None)

        self.client.extend_cluster = mock.Mock(return_value=None)
        self.client.get_cluster = mock.Mock(return_value=self._data)

    def test_restart(self):
        arglist = [
            self._data.id, '2',
        ]

        verifylist = [
            ('cluster', self._data.id),
            ('modifySize', 2),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.extend_cluster.assert_called_with(self._data.id, 2)
        self.client.get_cluster.assert_called_with(self._data.id)

        self.assertEqual(self.columns, columns)


class TestShowCluster(fakes.TestCss):

    _data = fakes.FakeCluster.create_one()
    setattr(_data, 'version', _data.datastore.version)
    setattr(_data, 'type', _data.datastore.type)
    node_count = defaultdict(int)
    for node in _data.nodes:
        node_count[node['type']] += 1
    setattr(_data, 'node_count', dict(node_count))

    columns = COLUMNS

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestShowCluster, self).setUp()

        self.cmd = cluster.ShowCluster(self.app, None)

        self.client.get_cluster = mock.Mock(return_value=self._data)

    def test_show_no_options(self):
        arglist = []
        verifylist = []

        # Testing that a call without the required argument will fail and
        # throw a "ParserExecption"
        self.assertRaises(tests_utils.ParserException,
                          self.check_parser, self.cmd, arglist, verifylist)

    def test_show(self):
        arglist = [
            self._data.id,
        ]

        verifylist = [
            ('cluster', self._data.id),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.get_cluster.assert_called_with(self._data.id)

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)

    def test_show_non_existent(self):
        arglist = [
            'unexist_css_cluster',
        ]

        verifylist = [
            ('cluster', 'unexist_css_cluster'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_result = exceptions.CommandError('Resource Not Found')
        self.client.get_cluster = (
            mock.Mock(side_effect=find_mock_result)
        )

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual('Resource Not Found', str(e))
        self.client.get_cluster.assert_called_with('unexist_css_cluster')


class TestDeleteCluster(fakes.TestCss):

    _data = fakes.FakeCluster.create_multiple(2)

    def setUp(self):
        super(TestDeleteCluster, self).setUp()

        self.client.delete_cluster = mock.Mock(return_value=None)

        # Get the command object to test
        self.cmd = cluster.DeleteCluster(self.app, None)

    def test_delete(self):
        arglist = [
            self._data[0].id,
        ]

        verifylist = [
            ('cluster', [self._data[0].id]),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.delete_cluster.assert_called_with(
            self._data[0].id, ignore_missing=False)
        self.assertIsNone(result)

    def test_multiple_delete(self):
        arglist = []

        for data in self._data:
            arglist.append(data.id)

        verifylist = [
            ('cluster', arglist),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)

        calls = []
        for data in self._data:
            calls.append(call(data.id, ignore_missing=False))
        self.client.delete_cluster.assert_has_calls(calls)
        self.assertIsNone(result)

    def test_multiple_delete_with_exception(self):
        arglist = [
            self._data[0].id,
            'unexist_css_cluster',
        ]
        verifylist = [
            ('cluster', arglist),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        delete_mock_result = [None, exceptions.CommandError]
        self.client.delete_cluster = (
            mock.Mock(side_effect=delete_mock_result)
        )

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual('1 of 2 Cluster(s) failed to delete.', str(e))

        self.client.delete_cluster.assert_any_call(
            self._data[0].id, ignore_missing=False)
        self.client.delete_cluster.assert_any_call(
            'unexist_css_cluster', ignore_missing=False)
