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
from unittest.mock import call

import mock
from openstackclient.tests.unit import utils as tests_utils
from osc_lib import exceptions

from otcextensions.common import cli_utils
from otcextensions.osclient.css.v1 import cluster
from otcextensions.tests.unit.osclient.css.v1 import fakes

COLUMNS = (
    'action_progress',
    'actions',
    'bandwidth_size',
    'cmk_id',
    'created_at',
    'datastore',
    'elb_whitelist',
    'endpoints',
    'enterprise_project_id',
    'floating_ip',
    'id',
    'is_authority_enabled',
    'is_backup_enabled',
    'is_billed',
    'is_disk_encrypted',
    'is_https_enabled',
    'name',
    'network_id',
    'nodes',
    'router_id',
    'security_group_id',
    'status',
    'status_code',
    'tags',
    'updated_at',
)


class TestListClusters(fakes.TestCss):

    _data = fakes.FakeCluster.create_multiple(3)

    column_list_headers = (
        'ID',
        'Name',
        'Type',
        'Version',
        'Status',
        'Created At',
    )

    columns = ('id', 'name', 'type', 'version', 'status', 'created_at')

    data = []

    for s in _data:
        data.append(
            (
                s.id,
                s.name,
                s.datastore['type'],
                s.datastore['version'],
                s.status,
                s.created_at,
            )
        )

    def setUp(self):
        super(TestListClusters, self).setUp()

        self.cmd = cluster.ListClusters(self.app, None)

        self.client.clusters = mock.Mock()

    def test_list(self):
        arglist = []

        verifylist = []

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.clusters.side_effect = [self._data]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.clusters.assert_called_with()

        self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(self.data, list(data))


class TestCreateCluster(fakes.TestCss):

    _data = fakes.FakeCluster.create_one()

    columns = COLUMNS

    data = fakes.gen_data(_data, columns)

    default_timeout = 1200

    def setUp(self):
        super(TestCreateCluster, self).setUp()

        self.cmd = cluster.CreateCluster(self.app, None)

        self.client.create_cluster = mock.Mock(return_value=self._data)
        self.client.get_cluster = mock.Mock(return_value=self._data)
        self.client.wait_for_cluster = mock.Mock(return_value=True)

    def test_create(self):
        arglist = [
            'test-css',
            '--flavor',
            'css-flavor',
            '--datastore-version',
            '7.10.2',
            '--availability-zone',
            'eu-de-01,eu-de-02',
            '--router-id',
            'router-uuid',
            '--network-id',
            'network-uuid',
            '--security-group-id',
            'sg-uuid',
            '--num-nodes',
            '2',
            '--volume-size',
            '100',
            '--volume-type',
            'COMMON',
            '--cmk-id',
            'cmk-uuid',
            '--https-enable',
            '--admin-pwd',
            'testtest',
            '--backup-policy',
            'period=00:00 GMT+08:00,keepday=7,prefix=snapshot',
            '--tag',
            'key=key1,value=value1',
            '--tag',
            'key=key2,value=value2',
            '--wait',
        ]
        verifylist = [
            ('name', 'test-css'),
            ('flavor', 'css-flavor'),
            ('datastore_version', '7.10.2'),
            ('availability_zone', 'eu-de-01,eu-de-02'),
            ('router_id', 'router-uuid'),
            ('network_id', 'network-uuid'),
            ('security_group_id', 'sg-uuid'),
            ('num_nodes', 2),
            ('volume_size', 100),
            ('volume_type', 'COMMON'),
            ('cmk_id', 'cmk-uuid'),
            ('https_enable', True),
            ('admin_pwd', 'testtest'),
            (
                'backup_policy',
                [
                    {
                        'period': '00:00 GMT+08:00',
                        'keepday': '7',
                        'prefix': 'snapshot',
                    }
                ],
            ),
            (
                'tags',
                [
                    {'key': 'key1', 'value': 'value1'},
                    {'key': 'key2', 'value': 'value2'},
                ],
            ),
            ('wait', True),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        attrs = {
            'name': 'test-css',
            'datastore': {'version': '7.10.2', 'type': 'elasticsearch'},
            'instanceNum': 2,
            'instance': {
                'availability_zone': 'eu-de-01,eu-de-02',
                'flavorRef': 'css-flavor',
                'volume': {'volume_type': 'COMMON', 'size': 100},
                'nics': {
                    'vpcId': 'router-uuid',
                    'netId': 'network-uuid',
                    'securityGroupId': 'sg-uuid',
                },
            },
            'diskEncryption': {
                'systemEncrypted': 1,
                'systemCmkid': 'cmk-uuid',
            },
            'httpsEnable': True,
            'authorityEnable': True,
            'adminPwd': 'testtest',
            'backupStrategy': {
                'period': '00:00 GMT+08:00',
                'keepday': 7,
                'prefix': 'snapshot',
            },
            'tags': [
                {'key': 'key1', 'value': 'value1'},
                {'key': 'key2', 'value': 'value2'},
            ],
        }
        self.client.create_cluster.assert_called_with(**attrs)
        self.client.wait_for_cluster.assert_called_with(
            self._data.id, self.default_timeout, print_status=True
        )
        self.client.get_cluster.assert_called_with(self._data.id)
        self.assertEqual(self.columns, columns)


class TestRestartCluster(fakes.TestCss):

    _data = fakes.FakeCluster.create_one()

    default_timeout = 300

    def setUp(self):
        super(TestRestartCluster, self).setUp()

        self.cmd = cluster.RestartCluster(self.app, None)

        self.client.find_cluster = mock.Mock(return_value=self._data)
        self.client.restart_cluster = mock.Mock(return_value=None)
        self.client.wait_for_cluster = mock.Mock(return_value=True)

    def test_restart(self):
        arglist = [
            self._data.name,
            '--wait',
        ]

        verifylist = [
            ('cluster', self._data.name),
            ('wait', True),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.find_cluster.assert_called_with(
            self._data.name, ignore_missing=False
        )
        self.client.restart_cluster.assert_called_with(self._data)
        self.client.wait_for_cluster.assert_called_with(
            self._data.id, self.default_timeout
        )
        self.assertIsNone(result)


class TestExtendCluster(fakes.TestCss):

    _data = fakes.FakeCluster.create_one()

    default_timeout = 1200

    def setUp(self):
        super(TestExtendCluster, self).setUp()

        self.cmd = cluster.ExtendCluster(self.app, None)

        self.client.find_cluster = mock.Mock(return_value=self._data)
        self.client.extend_cluster = mock.Mock(return_value=None)
        self.client.wait_for_cluster = mock.Mock(return_value=True)

    def test_extend(self):
        arglist = [
            self._data.name,
            '--add-nodes',
            '2',
            '--wait',
        ]

        verifylist = [
            ('cluster', self._data.name),
            ('add_nodes', 2),
            ('wait', True),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.find_cluster.assert_called_with(self._data.name)
        self.client.extend_cluster.assert_called_with(self._data, 2)
        self.client.wait_for_cluster.assert_called_with(
            self._data.id, self.default_timeout
        )
        self.assertIsNone(result)


class TestExtendClusterNodes(fakes.TestCss):

    _data = fakes.FakeCluster.create_one()

    default_timeout = 1200

    def setUp(self):
        super(TestExtendClusterNodes, self).setUp()

        self.cmd = cluster.ExtendClusterNodes(self.app, None)

        self.client.find_cluster = mock.Mock(return_value=self._data)
        self.client.extend_cluster_nodes = mock.Mock(return_value=None)
        self.client.wait_for_cluster = mock.Mock(return_value=True)

    def test_extend(self):
        arglist = [
            self._data.name,
            '--extend',
            'type=ess,disksize=60,nodesize=2',
            '--extend',
            'type=ess-master,disksize=0,nodesize=2',
            '--wait',
        ]

        expected_request_data = {
            'grow': [
                {'type': 'ess', 'disksize': '60', 'nodesize': '2'},
                {'type': 'ess-master', 'disksize': '0', 'nodesize': '2'},
            ]
        }

        verifylist = [
            ('cluster', self._data.name),
            ('extend', expected_request_data['grow']),
            ('wait', True),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.find_cluster.assert_called_with(self._data.name)
        self.client.extend_cluster_nodes.assert_called_with(
            self._data, **expected_request_data
        )
        self.client.wait_for_cluster.assert_called_with(
            self._data.id, self.default_timeout
        )

        self.assertIsNone(result)


class TestShowCluster(fakes.TestCss):

    _data = fakes.FakeCluster.create_one()

    columns = COLUMNS

    data = fakes.gen_data(_data, columns, cluster._formatters)

    def setUp(self):
        super(TestShowCluster, self).setUp()

        self.cmd = cluster.ShowCluster(self.app, None)

        self.client.find_cluster = mock.Mock(return_value=self._data)

    def test_show_no_options(self):
        arglist = []
        verifylist = []

        # Testing that a call without the required argument will fail and
        # throw a "ParserExecption"
        self.assertRaises(
            tests_utils.ParserException,
            self.check_parser,
            self.cmd,
            arglist,
            verifylist,
        )

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
        self.client.find_cluster.assert_called_with(self._data.id)

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)

    def test_show_non_existent(self):
        arglist = [
            'unexist_css_data',
        ]

        verifylist = [
            ('cluster', 'unexist_css_data'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_result = exceptions.CommandError('Resource Not Found')
        self.client.find_cluster = mock.Mock(side_effect=find_mock_result)

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual('Resource Not Found', str(e))
        self.client.find_cluster.assert_called_with('unexist_css_data')


class TestListClusterNodes(fakes.TestCss):

    _data = fakes.FakeCluster.create_one()

    column_list_headers = (
        'ID',
        'Name',
        'IP',
        'Type',
        'Volume',
        'Availability Zone',
        'Status',
    )

    data = []

    for s in _data.nodes:
        data.append(
            (
                s.id,
                s.name,
                s.ip,
                s.type,
                cli_utils.YamlFormat(s.volume),
                s.availability_zone,
                s.status,
            )
        )

    def setUp(self):
        super(TestListClusterNodes, self).setUp()

        self.cmd = cluster.ListClusterNodes(self.app, None)

        self.client.find_cluster = mock.Mock()

    def test_list(self):
        arglist = [
            self._data.id,
        ]

        verifylist = [
            ('cluster', self._data.id),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.find_cluster.side_effect = [self._data]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_cluster.assert_called_with(self._data.id)

        self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(self.data, list(data))


class TestDeleteCluster(fakes.TestCss):

    _data = fakes.FakeCluster.create_multiple(2)

    def setUp(self):
        super(TestDeleteCluster, self).setUp()

        self.client.delete_cluster = mock.Mock(return_value=None)

        # Get the command object to test
        self.cmd = cluster.DeleteCluster(self.app, None)

    def test_delete(self):
        arglist = [
            self._data[0].name,
        ]

        verifylist = [
            ('cluster', [self._data[0].name]),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.client.find_cluster = mock.Mock(return_value=self._data[0])

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.delete_cluster.assert_called_with(
            self._data[0], ignore_missing=False
        )
        self.assertIsNone(result)

    def test_multiple_delete(self):
        arglist = []

        for css_data in self._data:
            arglist.append(css_data.name)

        verifylist = [
            ('cluster', arglist),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.client.find_cluster = mock.Mock(side_effect=self._data)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)

        calls = []
        for css_data in self._data:
            calls.append(call(css_data, ignore_missing=False))
        self.client.delete_cluster.assert_has_calls(calls)
        self.assertIsNone(result)

    def test_multiple_delete_with_exception(self):
        arglist = [
            self._data[0].name,
            'unexist_css_data',
        ]
        verifylist = [
            ('cluster', arglist),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_results = [self._data[0], exceptions.CommandError]
        self.client.find_cluster = mock.Mock(side_effect=find_mock_results)

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual('1 of 2 Cluster(s) failed to delete.', str(e))

        self.client.find_cluster.assert_any_call(
            self._data[0].name, ignore_missing=False
        )
        self.client.find_cluster.assert_any_call(
            'unexist_css_data', ignore_missing=False
        )
        self.client.delete_cluster.assert_called_once_with(
            self._data[0], ignore_missing=False
        )
