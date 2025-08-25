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
            'HIGH',
            '--cmk-id',
            'cmk-uuid',
            '--https-enable',
            '--admin-pwd',
            'testtest',
            '--backup-policy',
            (
                'period=00:00 GMT+08:00,keepday=7,prefix=snapshot,'
                'bucket=css-backup-bucket,agency=obs_css_agency,'
                'basepath=obs_path'
            ),
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
            ('volume_type', 'HIGH'),
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
                        'bucket': 'css-backup-bucket',
                        'agency': 'obs_css_agency',
                        'basepath': 'obs_path',
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
                'volume': {'volume_type': 'HIGH', 'size': 100},
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
                'bucket': 'css-backup-bucket',
                'agency': 'obs_css_agency',
                'basePath': 'obs_path',
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


class TestUpdateClusterName(fakes.TestCss):
    _data = fakes.FakeCluster.create_one()

    columns = COLUMNS

    data = fakes.gen_data(_data, columns, cluster._formatters)

    def setUp(self):
        super(TestUpdateClusterName, self).setUp()

        self.cmd = cluster.UpdateClusterName(self.app, None)

        self.client.find_cluster = mock.Mock(return_value=self._data)
        self.client.get_cluster = mock.Mock(return_value=self._data)
        self.client.update_cluster_name = mock.Mock(return_value=None)

    def test_update_name(self):
        new_name = 'new_cluster_name'
        arglist = [
            self._data.name,
            '--new-name',
            new_name,
        ]

        verifylist = [
            ('cluster', self._data.name),
            ('new_name', new_name),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.find_cluster.assert_called_with(
            self._data.name, ignore_missing=False
        )
        self.client.update_cluster_name.assert_called_with(
            self._data, new_name
        )
        self.client.get_cluster.assert_called_with(self._data)

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestUpdateClusterPassword(fakes.TestCss):
    _data = fakes.FakeCluster.create_one()

    def setUp(self):
        super(TestUpdateClusterPassword, self).setUp()

        self.cmd = cluster.UpdateClusterPassword(self.app, None)

        self.client.find_cluster = mock.Mock(return_value=self._data)
        self.client.update_cluster_password = mock.Mock(return_value=None)

    def test_update_password(self):
        new_password = 'new_cluster_password'
        arglist = [
            self._data.name,
            '--new-password',
            new_password,
        ]

        verifylist = [
            ('cluster', self._data.name),
            ('new_password', new_password),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.find_cluster.assert_called_with(
            self._data.name, ignore_missing=False
        )
        self.client.update_cluster_password.assert_called_with(
            self._data, new_password
        )
        self.assertIsNone(result)


class TestUpdateSecurityGroup(fakes.TestCss):
    _data = fakes.FakeCluster.create_one()

    def setUp(self):
        super(TestUpdateSecurityGroup, self).setUp()

        self.cmd = cluster.UpdateClusterSecurityGroup(self.app, None)

        self.client.find_cluster = mock.Mock(return_value=self._data)

        self.app.client_manager.network = mock.Mock()

        self.app.client_manager.network.find_security_group = mock.Mock(
            return_value=self._data
        )

        self.client.update_cluster_security_group = mock.Mock(
            return_value=None
        )

    def test_update_security_group(self):
        new_security_group = 'new_security_group'
        arglist = [
            self._data.name,
            '--security-group',
            new_security_group,
        ]

        verifylist = [
            ('cluster', self._data.name),
            ('security_group', new_security_group),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.find_cluster.assert_called_with(
            self._data.name, ignore_missing=False
        )

        self.app.client_manager.network.find_security_group.assert_called_with(
            new_security_group, ignore_missing=False
        )
        self.client.update_cluster_security_group.assert_called_with(
            self._data, self._data.id
        )
        self.assertIsNone(result)

    def test_missing_security_group(self):
        arglist = [
            self._data.name,
        ]
        verifylist = [('cluster', self._data.name)]

        # Testing that a call without the required argument will fail and
        # throw a "ParserExecption"
        ex = self.assertRaises(
            tests_utils.ParserException,
            self.check_parser,
            self.cmd,
            arglist,
            verifylist,
        )
        self.assertIn('arguments are required: --security-group', str(ex))


class TestUpdateSecurityMode(fakes.TestCss):
    _data = fakes.FakeCluster.create_one()

    def setUp(self):
        super(TestUpdateSecurityMode, self).setUp()

        self.cmd = cluster.UpdateClusterSecurityMode(self.app, None)

        self.client.find_cluster = mock.Mock(return_value=self._data)

        self.client.update_cluster_security_mode = mock.Mock(return_value=None)

    def test_update_security_mode(self):
        authority_enable = True
        https_enable = True
        arglist = [
            self._data.name,
            '--authority-enable',
            '--https-enable',
        ]

        verifylist = [
            ('cluster', self._data.name),
            ('authority_enable', authority_enable),
            ('https_enable', https_enable),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.find_cluster.assert_called_with(
            self._data.name, ignore_missing=False
        )

        self.client.update_cluster_security_mode.assert_called_with(
            self._data,
            authority_enable=authority_enable,
            https_enable=https_enable,
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
        self.client.find_cluster.assert_called_with(
            self._data.name, ignore_missing=False
        )
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
        self.client.find_cluster.assert_called_with(
            self._data.name, ignore_missing=False
        )
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
        self.client.find_cluster.assert_called_with(
            self._data.id, ignore_missing=False
        )

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
        self.client.find_cluster.assert_called_with(
            'unexist_css_data', ignore_missing=False
        )


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

        self.client.find_cluster.assert_called_with(
            self._data.id, ignore_missing=False
        )

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


class TestUpdateClusterFlavor(fakes.TestCss):
    _data = fakes.FakeCluster.create_one()

    default_timeout = 1200

    def setUp(self):
        super(TestUpdateClusterFlavor, self).setUp()

        self.cmd = cluster.UpdateClusterFlavor(self.app, None)

        self.client.find_cluster = mock.Mock(return_value=self._data)
        self.client.update_cluster_flavor = mock.Mock(return_value=None)
        self.client.wait_for_cluster = mock.Mock(return_value=True)

    def test_update_flavor(self):
        new_flavor = 'new_flavor'
        arglist = [self._data.name, '--flavor', new_flavor, '--wait']

        verifylist = [
            ('cluster', self._data.name),
            ('flavor', new_flavor),
            ('wait', True),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.find_cluster.assert_called_with(
            self._data.name, ignore_missing=False
        )
        self.client.update_cluster_flavor.assert_called_with(
            self._data, new_flavor=new_flavor
        )
        self.client.wait_for_cluster.assert_called_with(
            self._data.id, self.default_timeout
        )
        self.assertIsNone(result)

    def test_update_flavor_with_node_type(self):
        node_type = 'ess'
        new_flavor = 'new_flavor'
        arglist = [
            self._data.name,
            '--node-type',
            node_type,
            '--flavor',
            new_flavor,
        ]

        verifylist = [
            ('cluster', self._data.name),
            ('node_type', node_type),
            ('flavor', new_flavor),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.find_cluster.assert_called_with(
            self._data.name, ignore_missing=False
        )
        self.client.update_cluster_flavor.assert_called_with(
            self._data, node_type=node_type, new_flavor=new_flavor
        )
        self.assertIsNone(result)


class TestScaleInCluster(fakes.TestCss):
    _data = fakes.FakeCluster.create_one()

    default_timeout = 1200

    def setUp(self):
        super(TestScaleInCluster, self).setUp()

        self.cmd = cluster.ScaleInCluster(self.app, None)

        self.client.find_cluster = mock.Mock(return_value=self._data)
        self.client.scale_in_cluster = mock.Mock(return_value=None)
        self.client.wait_for_cluster = mock.Mock(return_value=True)

    def test_scale_in(self):
        arglist = [
            self._data.name,
            '--nodes',
            'id1',
            'id2',
            '--wait',
        ]

        verifylist = [
            ('cluster', self._data.name),
            ('nodes', ['id1', 'id2']),
            ('wait', True),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.find_cluster.assert_called_with(
            self._data.name, ignore_missing=False
        )
        self.client.scale_in_cluster.assert_called_with(
            self._data, ['id1', 'id2']
        )
        self.client.wait_for_cluster.assert_called_with(
            self._data.id, self.default_timeout
        )
        self.assertIsNone(result)


class TestScaleInClusterByNodeType(fakes.TestCss):
    _data = fakes.FakeCluster.create_one()

    default_timeout = 1200

    def setUp(self):
        super(TestScaleInClusterByNodeType, self).setUp()

        self.cmd = cluster.ScaleInClusterByNodeType(self.app, None)

        self.client.find_cluster = mock.Mock(return_value=self._data)
        self.client.scale_in_cluster_by_node_type = mock.Mock(
            return_value=None
        )
        self.client.wait_for_cluster = mock.Mock(return_value=True)

    def test_scale_in_ess(self):
        arglist = [
            self._data.name,
            '--ess',
            '2',
            '--wait',
        ]

        verifylist = [
            ('cluster', self._data.name),
            ('ess', 2),
            ('wait', True),
        ]

        expected_data = [{'type': 'ess', 'reducedNodeNum': 2}]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.find_cluster.assert_called_with(
            self._data.name, ignore_missing=False
        )
        self.client.scale_in_cluster_by_node_type.assert_called_with(
            self._data, expected_data
        )
        self.client.wait_for_cluster.assert_called_with(
            self._data.id, self.default_timeout
        )
        self.assertIsNone(result)

    def test_scale_in_all_type(self):
        arglist = [
            self._data.name,
            '--ess',
            '2',
            '--ess-master',
            '3',
            '--ess-client',
            '1',
            '--ess-cold',
            '5',
            '--wait',
        ]

        verifylist = [
            ('cluster', self._data.name),
            ('ess', 2),
            ('ess-master', 3),
            ('ess-client', 1),
            ('ess-cold', 5),
            ('wait', True),
        ]

        expected_data = [
            {'type': 'ess', 'reducedNodeNum': 2},
            {'type': 'ess-master', 'reducedNodeNum': 3},
            {'type': 'ess-client', 'reducedNodeNum': 1},
            {'type': 'ess-cold', 'reducedNodeNum': 5},
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.find_cluster.assert_called_with(
            self._data.name, ignore_missing=False
        )
        self.client.scale_in_cluster_by_node_type.assert_called_with(
            self._data, expected_data
        )
        self.client.wait_for_cluster.assert_called_with(
            self._data.id, self.default_timeout
        )
        self.assertIsNone(result)


class TestRetryClusterUpgradeJob(fakes.TestCss):
    _data = fakes.FakeCluster.create_one()

    default_timeout = 1200

    def setUp(self):
        super(TestRetryClusterUpgradeJob, self).setUp()

        self.cmd = cluster.RetryClusterUpgradeJob(self.app, None)

        self.client.find_cluster = mock.Mock(return_value=self._data)
        self.client.retry_cluster_upgrade_task = mock.Mock(return_value=None)
        self.client.wait_for_cluster = mock.Mock(return_value=True)

    def test_retry_mode(self):
        arglist = [self._data.name, '--job-id', 'job_id', '--wait']

        verifylist = [
            ('cluster', self._data.name),
            ('job_id', 'job_id'),
            ('retry_mode', 'abort'),
            ('wait', True),
        ]

        expected_data = {'job_id': 'job_id', 'retry_mode': 'abort'}

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.find_cluster.assert_called_with(
            self._data.name, ignore_missing=False
        )
        self.client.retry_cluster_upgrade_job.assert_called_with(
            self._data, **expected_data
        )
        self.client.wait_for_cluster.assert_called_with(
            self._data.id, self.default_timeout
        )
        self.assertIsNone(result)


class TestUpdateClusterKernel(fakes.TestCss):
    _data = fakes.FakeCluster.create_one()

    def setUp(self):
        super(TestUpdateClusterKernel, self).setUp()

        self.cmd = cluster.UpdateClusterKernel(self.app, None)

        self.client.find_cluster = mock.Mock(return_value=self._data)
        self.client.update_cluster_kernel = mock.Mock(return_value=None)

    def test_upgrade_cluster_all_checks(self):
        arglist = [
            self._data.name,
            '--target-image-id',
            'target_image_id',
            '--upgrade-type',
            'cross',
            '--agency',
            'css_agency',
            '--check-backup-indices',
            '--check-cluster-load',
        ]

        verifylist = [
            ('cluster', self._data.name),
            ('target_image_id', 'target_image_id'),
            ('upgrade_type', 'cross'),
            ('agency', 'css_agency'),
            ('check_backup_indices', True),
            ('check_cluster_load', True),
        ]

        expected_data = {
            'target_image_id': 'target_image_id',
            'upgrade_type': 'cross',
            'agency': 'css_agency',
            'indices_backup_check': True,
            'cluster_load_check': True,
        }

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.find_cluster.assert_called_with(
            self._data.name, ignore_missing=False
        )
        self.client.update_cluster_kernel.assert_called_with(
            self._data, **expected_data
        )
        self.assertIsNone(result)


class TestReplaceClusterNode(fakes.TestCss):
    _data = fakes.FakeCluster.create_one()

    default_timeout = 1200

    def setUp(self):
        super(TestReplaceClusterNode, self).setUp()

        self.cmd = cluster.ReplaceClusterNode(self.app, None)

        self.client.find_cluster = mock.Mock(return_value=self._data)
        self.client.replace_cluster_node = mock.Mock(return_value=None)
        self.client.wait_for_cluster = mock.Mock(return_value=True)

    def test_replace_node(self):
        arglist = [
            self._data.name,
            '--node-id',
            'id1',
            '--wait',
        ]

        verifylist = [
            ('cluster', self._data.name),
            ('node_id', 'id1'),
            ('wait', True),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.find_cluster.assert_called_with(
            self._data.name, ignore_missing=False
        )
        self.client.replace_cluster_node.assert_called_with(self._data, 'id1')
        self.client.wait_for_cluster.assert_called_with(
            self._data.id, self.default_timeout
        )
        self.assertIsNone(result)


class TestAddClusterNodes(fakes.TestCss):
    _data = fakes.FakeCluster.create_one()

    default_timeout = 1200

    def setUp(self):
        super(TestAddClusterNodes, self).setUp()

        self.cmd = cluster.AddClusterNodes(self.app, None)

        self.client.find_cluster = mock.Mock(return_value=self._data)
        self.client.add_cluster_nodes = mock.Mock(return_value=None)
        self.client.wait_for_cluster = mock.Mock(return_value=True)

    def test_add_nodes(self):
        arglist = [
            self._data.name,
            '--node-type',
            'ess',
            '--flavor',
            'node_flavor',
            '--node-size',
            '3',
            '--volume-type',
            'HIGH',
            '--wait',
        ]

        verifylist = [
            ('cluster', self._data.name),
            ('node_type', 'ess'),
            ('flavor', 'node_flavor'),
            ('node_size', 3),
            ('volume_type', 'HIGH'),
            ('wait', True),
        ]

        expected_data = {
            'node_type': 'ess',
            'flavor': 'node_flavor',
            'node_size': 3,
            'volume_type': 'HIGH',
        }

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.find_cluster.assert_called_with(
            self._data.name, ignore_missing=False
        )
        self.client.add_cluster_nodes.assert_called_with(
            self._data, **expected_data
        )
        self.client.wait_for_cluster.assert_called_with(
            self._data.id, self.default_timeout
        )
        self.assertIsNone(result)


class TestListClusterVersionUpgrades(fakes.TestCss):
    _data = fakes.FakeClusterImage.create_one()
    _cluster = fakes.FakeCluster.create_one()

    column_list_headers = [
        'Datastore Type',
        'Datastore Version',
        'Image Name',
        'Id',
        'Description',
        'Priority',
    ]

    columns = (
        'datastore_type',
        'datastore_version',
        'dsiplay_name',
        'id',
        'image_desc',
        'priority',
    )

    data = []

    for s in _data.image_info_list:
        data.append(
            (
                s.datastore_type,
                s.datastore_version,
                s.display_name,
                s.id,
                s.image_desc,
                s.priority,
            )
        )

    def setUp(self):
        super(TestListClusterVersionUpgrades, self).setUp()

        self.client.find_cluster = mock.Mock(return_value=self._cluster)

        self.cmd = cluster.ListClusterVersionUpgrades(self.app, None)

        self.client.clusters = mock.Mock()

    def test_list_version_upgrades(self):
        arglist = [self._cluster.name, '--upgrade-type', 'same']

        verifylist = [
            ('cluster', self._cluster.name),
            ('upgrade_type', 'same'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.get_cluster_version_upgrades.side_effect = [self._data]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.get_cluster_version_upgrades.assert_called_with(
            self._cluster, 'same'
        )

        self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(self.data, list(data))


class TestShowClusterUpgradeStatus(fakes.TestCss):
    _data = fakes.FakeClusterUpgradeStatus.create_multiple(3)
    _cluster = fakes.FakeCluster.create_one()

    column_list_headers = (
        'ID',
        'Image Info',
        'Execute Times',
        'Start Time',
        'End Time',
        'Status',
    )

    columns = (
        'id',
        'image_info',
        'execute_times',
        'start_time',
        'end_time',
        'status',
    )

    data = []

    for s in _data:
        data.append(
            (
                s.id,
                cli_utils.YamlFormat(s.image_info),
                s.execute_times,
                s.start_time,
                s.end_time,
                s.status,
            )
        )

    def setUp(self):
        super(TestShowClusterUpgradeStatus, self).setUp()

        self.cmd = cluster.ShowClusterUpgradeStatus(self.app, None)

        self.client.find_cluster = mock.Mock(return_value=self._cluster)

        self.client.get_cluster_upgrade_status = mock.Mock()

    def test_status_show(self):
        arglist = [self._cluster.name]

        verifylist = [
            ('cluster', self._cluster.name),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.get_cluster_upgrade_status.side_effect = [self._data]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.get_cluster_upgrade_status.assert_called_with(
            self._cluster
        )

        self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(self.data, list(data))
