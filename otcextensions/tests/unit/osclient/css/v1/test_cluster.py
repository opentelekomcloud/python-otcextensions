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
    'actions',
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

    default_timeout = 15

    def setUp(self):
        super(TestCreateCluster, self).setUp()

        self.cmd = cluster.CreateCluster(self.app, None)

        self.client.create_cluster = mock.Mock(return_value=self._data)
        self.client.get_cluster = mock.Mock(return_value=self._data)
        self.client.wait_for_cluster = mock.Mock(return_value=True)

    def test_create(self):
        arglist = [
            'test-css',
            '--flavor', 'css-flavor',
            '--datastore-version', '7.10.2',
            '--availability-zone', 'eu-de-01,eu-de-02',
            '--router-id', 'router-uuid',
            '--network-id', 'network-uuid',
            '--security-group-id', 'sg-uuid',
            '--count', '2',
            '--volume-size', '100',
            '--volume-type', 'COMMON',
            '--cmk-id', 'cmk-uuid',
            '--https-enable',
            '--admin-pwd', 'testtest',
            '--backup-policy',
            'period=00:00 GMT+08:00,keepday=7,prefix=snapshot',
            '--tag', 'key=key1,value=value1',
            '--tag', 'key=key2,value=value2',
            '--wait'
        ]
        verifylist = [
            ('name', 'test-css'),
            ('flavor', 'css-flavor'),
            ('datastore_version', '7.10.2'),
            ('availability_zone', 'eu-de-01,eu-de-02'),
            ('router_id', 'router-uuid'),
            ('network_id', 'network-uuid'),
            ('security_group_id', 'sg-uuid'),
            ('count', 2),
            ('volume_size', 100),
            ('volume_type', 'COMMON'),
            ('cmk_id', 'cmk-uuid'),
            ('https_enable', True),
            ('admin_pwd', 'testtest'),
            ('backup_policy', [{'period': '00:00 GMT+08:00',
                                'keepday': '7', 'prefix': 'snapshot'}]),
            ('tags', [{'key': 'key1', 'value': 'value1'},
                      {'key': 'key2', 'value': 'value2'}]),
            ('wait', True),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        attrs = {
            'name': 'test-css',
            'datastore': {
                'version': '7.10.2',
                'type': 'elasticsearch'
            },
            'instanceNum': 2,
            'instance': {
                'availability_zone': 'eu-de-01,eu-de-02',
                'flavorRef': 'css-flavor',
                'volume': {
                    'volume_type': 'COMMON',
                    'size': 100
                },
                'nics': {
                    'vpcId': 'router-uuid',
                    'netId': 'network-uuid',
                    'securityGroupId': 'sg-uuid'
                }
            },
            'diskEncryption': {
                'systemEncrypted': 1,
                'systemCmkid': 'cmk-uuid'
            },
            'httpsEnable': 'true',
            'authorityEnable': True,
            'adminPwd': 'testtest',
            'backupStrategy': {
                'period': '00:00 GMT+08:00',
                'keepday': 7,
                'prefix': 'snapshot'
            },
            'tags': [{'key': 'key1', 'value': 'value1'},
                     {'key': 'key2', 'value': 'value2'}]
        }
        self.client.create_cluster.assert_called_with(**attrs)
        self.client.wait_for_cluster.assert_called_with(
            self._data.id, self.default_timeout)
        self.client.get_cluster.assert_called_with(self._data.id)
        self.assertEqual(self.columns, columns)


class TestRestartCluster(fakes.TestCss):

    _data = fakes.FakeCluster.create_one()

    columns = COLUMNS

    data = fakes.gen_data(_data, columns)

    default_timeout = 10

    def setUp(self):
        super(TestRestartCluster, self).setUp()

        self.cmd = cluster.RestartCluster(self.app, None)

        self.client.find_cluster = mock.Mock(return_value=self._data)
        self.client.get_cluster = mock.Mock(return_value=self._data)
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
        columns, data = self.cmd.take_action(parsed_args)
        self.client.find_cluster.assert_called_with(self._data.name)
        self.client.restart_cluster.assert_called_with(self._data)
        self.client.wait_for_cluster.assert_called_with(
            self._data.id, self.default_timeout)
        self.client.get_cluster.assert_called_with(self._data.id)

        self.assertEqual(self.columns, columns)


class TestExtendCluster(fakes.TestCss):

    _data = fakes.FakeCluster.create_one()

    columns = COLUMNS

    data = fakes.gen_data(_data, columns)

    default_timeout = 15

    def setUp(self):
        super(TestExtendCluster, self).setUp()

        self.cmd = cluster.ExtendCluster(self.app, None)

        self.client.find_cluster = mock.Mock(return_value=self._data)
        self.client.extend_cluster = mock.Mock(return_value=None)
        self.client.get_cluster = mock.Mock(return_value=self._data)
        self.client.wait_for_cluster = mock.Mock(return_value=True)

    def test_extend(self):
        arglist = [
            self._data.name,
            '--add-nodes', '2',
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
        columns, data = self.cmd.take_action(parsed_args)
        self.client.find_cluster.assert_called_with(self._data.name)
        self.client.extend_cluster.assert_called_with(self._data, 2)
        self.client.wait_for_cluster.assert_called_with(
            self._data.id, self.default_timeout)
        self.client.get_cluster.assert_called_with(self._data.id)

        self.assertEqual(self.columns, columns)


class TestShowCluster(fakes.TestCss):

    _data = fakes.FakeCluster.create_one()

    columns = COLUMNS

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestShowCluster, self).setUp()

        self.cmd = cluster.ShowCluster(self.app, None)

        self.client.find_cluster = mock.Mock(return_value=self._data)

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
        self.client.find_cluster.assert_called_with(self._data.id)

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
        self.client.find_cluster = (
            mock.Mock(side_effect=find_mock_result)
        )

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual('Resource Not Found', str(e))
        self.client.find_cluster.assert_called_with('unexist_css_cluster')


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

        self.client.find_cluster = (
            mock.Mock(return_value=self._data[0])
        )

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.delete_cluster.assert_called_with(self._data[0].id)
        self.assertIsNone(result)

    def test_multiple_delete(self):
        arglist = []

        for css_cluster in self._data:
            arglist.append(css_cluster.name)

        verifylist = [
            ('cluster', arglist),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.client.find_cluster = (
            mock.Mock(side_effect=self._data)
        )

        # Trigger the action
        result = self.cmd.take_action(parsed_args)

        calls = []
        for css_cluster in self._data:
            calls.append(call(css_cluster.id))
        self.client.delete_cluster.assert_has_calls(calls)
        self.assertIsNone(result)

    def test_multiple_delete_with_exception(self):
        arglist = [
            self._data[0].name,
            'unexist_css_cluster',
        ]
        verifylist = [
            ('cluster', arglist),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_results = [self._data[0], exceptions.CommandError]
        self.client.find_cluster = (
            mock.Mock(side_effect=find_mock_results)
        )

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual('1 of 2 Cluster(s) failed to delete.', str(e))

        self.client.find_cluster.assert_any_call(
            self._data[0].name, ignore_missing=False)
        self.client.find_cluster.assert_any_call(
            'unexist_css_cluster', ignore_missing=False)
        self.client.delete_cluster.assert_called_once_with(self._data[0].id)
