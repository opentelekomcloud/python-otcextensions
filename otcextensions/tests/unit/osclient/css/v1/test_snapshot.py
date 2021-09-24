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

from otcextensions.osclient.css.v1 import snapshot
from otcextensions.tests.unit.osclient.css.v1 import fakes

# from openstackclient.tests.unit import utils as tests_utils


COLUMNS = (
    'agency',
    'backup_keep_days',
    'backup_path',
    'backup_period',
    'backup_prefix',
    'bucket_name',
    'cmk_id',
    'enable',
)


class TestListSnapshots(fakes.TestCss):

    _cluster = fakes.FakeCluster.create_one()
    objects = fakes.FakeSnapshot.create_multiple(3)

    column_list_headers = (
        'ID',
        'Name',
        'Status',
        'Backup Method',
        'Bucket Name',
        'Created At',
        'Backup Keep Days',
    )

    columns = (
        'id',
        'name',
        'status',
        'backup_method',
        'bucket_name',
        'created_at',
        'backup_keep_days'
    )

    data = []

    for s in objects:
        data.append(
            (
                s.id,
                s.name,
                s.status,
                s.backup_method,
                s.bucket_name,
                s.created_at,
                s.backup_keep_days,
            )
        )

    def setUp(self):
        super(TestListSnapshots, self).setUp()

        self.cmd = snapshot.ListSnapshots(self.app, None)

        self.client.find_cluster = mock.Mock(return_value=self._cluster)
        self.client.snapshots = mock.Mock()
        self.client.api_mock = self.client.snapshots

    def test_list(self):
        arglist = [
            self._cluster.name,
        ]
        verifylist = [
            ('cluster', self._cluster.name),
        ]
        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(self._cluster)

        self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(self.data, list(data))


class TestCreateSnapshot(fakes.TestCss):

    _cluster = fakes.FakeCluster.create_one()
    _data = fakes.FakeSnapshot.create_one()

    columns = ('id', 'name')

    data = fakes.gen_data(_data, columns)

    default_timeout = 15

    def setUp(self):
        super(TestCreateSnapshot, self).setUp()

        self.cmd = snapshot.CreateSnapshot(self.app, None)

        self.client.find_cluster = mock.Mock(return_value=self._cluster)
        self.client.create_snapshot = mock.Mock(return_value=self._data)
        self.client.wait_for_cluster = mock.Mock(return_value=True)

    def test_create(self):
        arglist = [
            self._cluster.name,
            'test-snapshot',
            '--indices', '1',
            '--description', '2',
            '--wait'
        ]
        verifylist = [
            ('cluster', self._cluster.name),
            ('name', 'test-snapshot'),
            ('indices', '1'),
            ('description', '2'),
            ('wait', True),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        attrs = {
            'name': 'test-snapshot',
            'indices': '1',
            'description': '2',
        }
        self.client.create_snapshot.assert_called_with(self._cluster, **attrs)
        self.client.wait_for_cluster.assert_called_with(
            self._cluster.id, self.default_timeout)
        self.assertEqual(self.columns, columns)


class TestRestoreSnapshot(fakes.TestCss):

    _cluster = fakes.FakeCluster.create_one()

    columns = (
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

    data = fakes.gen_data(_cluster, columns)

    default_timeout = 15

    def setUp(self):
        super(TestRestoreSnapshot, self).setUp()

        self.cmd = snapshot.RestoreSnapshot(self.app, None)

        self.client.find_cluster = mock.Mock(return_value=self._cluster)
        self.client.restore_snapshot = mock.Mock(return_value=None)
        self.client.wait_for_cluster = mock.Mock(return_value=True)
        self.client.get_cluster = mock.Mock(return_value=self._cluster)

    def test_restore(self):
        arglist = [
            self._cluster.name,
            'snapshot-uuid',
            '--target-cluster', self._cluster.name,
            '--indices', '1',
            '--rename-replacement', '2',
            '--rename-pattern', '3',
            '--wait'
        ]
        verifylist = [
            ('cluster', self._cluster.name),
            ('snapshotId', 'snapshot-uuid'),
            ('target_cluster', self._cluster.name),
            ('indices', '1'),
            ('rename_replacement', '2'),
            ('rename_pattern', '3'),
            ('wait', True),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        attrs = {
            'targetCluster': self._cluster.id,
            'indices': '1',
            'renameReplacement': '2',
            'renamePattern': '3',
        }
        self.client.restore_snapshot.assert_called_with(
            self._cluster, 'snapshot-uuid', **attrs)
        self.client.wait_for_cluster.assert_called_with(
            self._cluster.id, self.default_timeout)
        self.assertEqual(self.columns, columns)


class TestDeleteSnapshot(fakes.TestCss):

    _cluster = fakes.FakeCluster.create_one()
    _data = fakes.FakeSnapshot.create_multiple(2)

    def setUp(self):
        super(TestDeleteSnapshot, self).setUp()

        self.client.find_cluster = mock.Mock(return_value=self._cluster)
        self.client.delete_snapshot = mock.Mock(return_value=None)

        # Get the command object to test
        self.cmd = snapshot.DeleteSnapshot(self.app, None)

    def test_delete(self):
        arglist = [
            self._cluster.name,
            self._data[0].id,
        ]

        verifylist = [
            ('cluster', self._cluster.name),
            ('snapshot', [self._data[0].id]),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.delete_snapshot.assert_called_with(
            self._cluster, self._data[0].id, ignore_missing=False)
        self.assertIsNone(result)

    def test_multiple_delete(self):
        arglist = [self._cluster.name]

        snapshot_list = []
        for css_snapshot in self._data:
            snapshot_list.append(css_snapshot.id)
            arglist.append(css_snapshot.id)

        verifylist = [
            ('cluster', self._cluster.name),
            ('snapshot', snapshot_list),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)

        calls = []
        for css_snapshot in self._data:
            calls.append(call(self._cluster, css_snapshot.id,
                              ignore_missing=False))
        self.client.delete_snapshot.assert_has_calls(calls)
        self.assertIsNone(result)

    def test_multiple_delete_with_exception(self):
        arglist = [
            self._cluster.name,
            self._data[0].id,
            'unexist_css_snapshot',
        ]
        verifylist = [
            ('cluster', self._cluster.name),
            ('snapshot', [self._data[0].id, 'unexist_css_snapshot']),
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

        self.client.delete_snapshot.assert_any_call(
            self._cluster, self._data[0].id, ignore_missing=False)


class TestSetSnapshotPolicy(fakes.TestCss):

    _cluster = fakes.FakeCluster.create_one()
    _data = fakes.FakeSnapshotPolicy.create_one()

    columns = COLUMNS

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestSetSnapshotPolicy, self).setUp()

        self.cmd = snapshot.SetSnapshotPolicy(self.app, None)

        self.client.find_cluster = mock.Mock(return_value=self._cluster)
        self.client.set_snapshot_policy = mock.Mock(return_value=None)
        self.client.get_snapshot_policy = mock.Mock(return_value=self._data)

    def test_setpolicy(self):
        arglist = [
            self._cluster.name,
            '--name-prefix', '1',
            '--keep-days', '2',
            '--period', '3',
            '--disable',
            '--delete-auto'
        ]
        verifylist = [
            ('cluster', self._cluster.name),
            ('name_prefix', '1'),
            ('keep_days', 2),
            ('period', '3'),
            ('disable', True),
            ('delete_auto', True),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        attrs = {
            "prefix": "1",
            "keepday": 2,
            "period": "3",
            "enable": 'false',
            "deleteAuto": 'true',
        }
        self.client.set_snapshot_policy.assert_called_with(
            self._cluster, **attrs)
        self.client.get_snapshot_policy.assert_called_with(self._cluster)

        self.assertEqual(self.columns, columns)


class TestShowSnapshotPolicy(fakes.TestCss):

    _cluster = fakes.FakeCluster.create_one()
    _data = fakes.FakeSnapshotPolicy.create_one()

    columns = COLUMNS

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestShowSnapshotPolicy, self).setUp()

        self.cmd = snapshot.ShowSnapshotPolicy(self.app, None)

        self.client.find_cluster = mock.Mock(return_value=self._cluster)
        self.client.get_snapshot_policy = mock.Mock(return_value=self._data)

    def test_showpolicy(self):
        arglist = [
            self._cluster.name,
        ]
        verifylist = [
            ('cluster', self._cluster.name),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.get_snapshot_policy.assert_called_with(self._cluster)

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestSetSnapshotConfiguration(fakes.TestCss):

    _cluster = fakes.FakeCluster.create_one()
    _data = fakes.FakeSnapshotPolicy.create_one()

    columns = COLUMNS

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestSetSnapshotConfiguration, self).setUp()

        self.cmd = snapshot.SetSnapshotConfiguration(self.app, None)

        self.client.find_cluster = mock.Mock(return_value=self._cluster)
        self.client.get_snapshot_policy = mock.Mock(return_value=self._data)

    def test_setconfiguration_auto(self):
        arglist = [
            self._cluster.name,
            '--auto'
        ]
        verifylist = [
            ('cluster', self._cluster.name),
            ('auto', True)
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.set_snapshot_configuration.assert_called_with(
            self._cluster, True)

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)
