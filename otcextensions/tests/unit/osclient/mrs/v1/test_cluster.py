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
from collections import namedtuple

import mock

from otcextensions.osclient.mrs.v1 import cluster
from otcextensions.tests.unit.osclient.mrs.v1 import fakes


class TestCluster(fakes.TestMrs):

    def setUp(self):
        super(TestCluster, self).setUp()

    def test_flatten(self):
        obj = fakes.FakeCluster.create_one()

        flat_data = cluster._flatten_cluster(obj)

        data = (
            flat_data['id'],
            flat_data['name'],
            flat_data['status'],
            flat_data['region'],
            flat_data['cluster_type'],
            flat_data['availability_zone'],
            flat_data['version'],
            flat_data['tags'],
            flat_data['created_at'],
            flat_data['updated_at'],
            flat_data['billing_type'],
            flat_data['vpc'],
            flat_data['master_node_size'],
            flat_data['core_node_size'],
            flat_data['external_ip'],
            flat_data['internal_ip'],
            flat_data['master_num'],
            flat_data['core_num'],
            flat_data['core_node_size'],
            flat_data['component_list'],
            flat_data['deployment_id'],
            flat_data['instance_id'],
            flat_data['vnc'],
            flat_data['project_id'],
            flat_data['volume_size'],
            flat_data['volume_type'],
            flat_data['subnet_id'],
            flat_data['subnet_name'],
            flat_data['security_group_id'],
            flat_data['non_master_security_group_id'],
            flat_data['safe_mode'],
            flat_data['key'],
            flat_data['master_ip'],
            flat_data['preffered_private_ip'],
            flat_data['charging_start_time'],
            flat_data['task_node_groups'],
            flat_data['node_groups'],
            flat_data['bootstrap_scripts'],
            flat_data['scale'],
        )

        cmp_data = (
            obj.id,
            obj.name,
            obj.status,
            obj.region,
            obj.cluster_type,
            obj.az_id,
            obj.cluster_version,
            obj.tags,
            cluster._utc_to_timestamp(obj.created_at),
            cluster._utc_to_timestamp(obj.updated_at),
            obj.billing_type,
            obj.vpc,
            obj.master_node_size,
            obj.core_node_size,
            obj.external_ip,
            obj.internal_ip,
            obj.master_num,
            obj.core_num,
            obj.core_node_size,
            obj.component_list,
            obj.deployment_id,
            obj.instance_id,
            obj.vnc,
            obj.project_id,
            obj.volume_size,
            obj.volume_type,
            obj.subnet_id,
            obj.subnet_name,
            obj.security_group_id,
            obj.non_master_security_group_id,
            obj.safe_mode,
            obj.key,
            obj.master_ip,
            obj.preffered_private_ip,
            obj.charging_start_time,
            obj.task_node_groups,
            obj.node_groups,
            obj.bootstrap_scripts,
            obj.scale
        )

        self.assertEqual(data, cmp_data)

    def test_normalize_tags(self):
        tags = ['k1=v1', 'k2', 'k3=']

        verify_result = 'k1*v1,k2,k3'

        result = cluster._normalize_tags(tags)

        self.assertEqual(result, verify_result)

    def test_add_tags_to_cluster_output(self):
        Obj = namedtuple('obj', 'tags')
        obj = Obj(['an=,1=2'])

        column = ()
        data = ()
        verify_column = (
            'tags',
        )
        verify_data = ('key=an, value=\nkey=1, value=2\n'),

        data, column = cluster._add_tags_to_cluster_obj(
            obj, data, column
        )

        self.assertEqual(data, verify_data)
        self.assertEqual(column, verify_column)


class TestListCluster(fakes.TestMrs):
    objects = fakes.FakeCluster.create_multiple(3)

    columns = ('id', 'name', 'status', 'region',
               'cluster_type', 'availability_zone', 'version')

    data = []

    for s in objects:
        flat_data = cluster._flatten_cluster(s)
        data.append((
            flat_data['id'],
            flat_data['name'],
            flat_data['status'],
            flat_data['region'],
            flat_data['cluster_type'],
            flat_data['availability_zone'],
            flat_data['version'],
        ))

    def setUp(self):
        super(TestListCluster, self).setUp()

        self.cmd = cluster.ListCluster(self.app, None)

        self.client.clusters = mock.Mock()
        self.client.api_mock = self.client.clusters

    def test_default(self):
        arglist = []

        verifylist = []

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [
            self.objects
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_once_with()

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))


class TestShowCluster(fakes.TestMrs):
    object = fakes.FakeCluster.create_one()

    columns = (
        'ID',
        'name',
        'status',
        'region',
        'cluster_type',
        'availability_zone',
        'version',
        'created_at',
        'updated_at',
        'billing_type',
        'vpc',
        'core_node_flavor',
        'external_ip',
        'internal_ip',
        'master_num',
        'core_num',
        'master_node_size',
        'core_node_size',
        'deployment_id',
        'component_list',
        'instance_id',
        'vnc',
        'project_id',
        'volume_size',
        'volume_type',
        'subnet_id',
        'subnet_name',
        'security_group_id',
        'non_master_security_group_id',
        'safe_mode',
        'key',
        'master_ip',
        'preffered_private_ip',
        'charging_start_time',
        'task_node_groups',
        'node_groups',
        'bootstrap_scripts',
        'scale'
    )

    flat_data = cluster._flatten_cluster(object)

    data = (
        flat_data['id'],
        flat_data['name'],
        flat_data['status'],
        flat_data['region'],
        flat_data['cluster_type'],
        flat_data['availability_zone'],
        flat_data['version'],
        flat_data['created_at'],
        flat_data['updated_at'],
        flat_data['billing_type'],
        flat_data['vpc'],
        flat_data['core_node_flavor'],
        flat_data['external_ip'],
        flat_data['internal_ip'],
        flat_data['master_num'],
        flat_data['core_num'],
        flat_data['master_node_size'],
        flat_data['core_node_size'],
        flat_data['deployment_id'],
        flat_data['component_list'],
        flat_data['instance_id'],
        flat_data['vnc'],
        flat_data['project_id'],
        flat_data['volume_size'],
        flat_data['volume_type'],
        flat_data['subnet_id'],
        flat_data['subnet_name'],
        flat_data['security_group_id'],
        flat_data['non_master_security_group_id'],
        flat_data['safe_mode'],
        flat_data['key'],
        flat_data['master_ip'],
        flat_data['preffered_private_ip'],
        flat_data['charging_start_time'],
        flat_data['task_node_groups'],
        flat_data['node_groups'],
        flat_data['bootstrap_scripts'],
        flat_data['scale'],
    )

    def setUp(self):
        super(TestShowCluster, self).setUp()

        self.cmd = cluster.ShowCluster(self.app, None)

        self.client.find_cluster = mock.Mock()

    def test_default(self):
        arglist = [
            'cluster'
        ]
        verifylist = [
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.find_cluster.side_effect = [
            self.object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_cluster.assert_called_once_with(
            name_or_id='cluster',
            ignore_missing=False, )

        self.data, self.columns = cluster._add_tags_to_cluster_obj(
            self.object,
            self.data,
            self.columns,
        )
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestDeleteCluster(fakes.TestMrs):

    def setUp(self):
        super(TestDeleteCluster, self).setUp()

        self.cmd = cluster.DeleteCluster(self.app, None)

        self.client.delete_cluster = mock.Mock()

    def test_delete(self):
        arglist = [
            'cluster'
        ]
        verifylist = []
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.delete_cluster.side_effect = [{}]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        delete_calls = [
            mock.call(
                cluster='cluster',
                ignore_missing=False),
        ]

        self.client.delete_cluster.assert_has_calls(delete_calls)
        self.assertEqual(1, self.client.delete_cluster.call_count)


class TestUpdateVault(fakes.TestMrs):
    object = fakes.FakeCluster.create_one()

    columns = (
        'ID',
        'name',
        'status',
        'region',
        'cluster_type',
        'availability_zone',
        'version',
        'created_at',
        'updated_at',
        'billing_type',
        'vpc',
        'core_node_flavor',
        'external_ip',
        'internal_ip',
        'master_num',
        'core_num',
        'master_node_size',
        'core_node_size',
        'deployment_id',
        'component_list',
        'instance_id',
        'vnc',
        'project_id',
        'volume_size',
        'volume_type',
        'subnet_id',
        'subnet_name',
        'security_group_id',
        'non_master_security_group_id',
        'safe_mode',
        'key',
        'master_ip',
        'preffered_private_ip',
        'charging_start_time',
        'task_node_groups',
        'node_groups',
        'bootstrap_scripts',
        'scale'
    )

    flat_data = cluster._flatten_cluster(object)

    data = (
        flat_data['id'],
        flat_data['name'],
        flat_data['status'],
        flat_data['region'],
        flat_data['cluster_type'],
        flat_data['availability_zone'],
        flat_data['version'],
        flat_data['created_at'],
        flat_data['updated_at'],
        flat_data['billing_type'],
        flat_data['vpc'],
        flat_data['core_node_flavor'],
        flat_data['external_ip'],
        flat_data['internal_ip'],
        flat_data['master_num'],
        flat_data['core_num'],
        flat_data['master_node_size'],
        flat_data['core_node_size'],
        flat_data['deployment_id'],
        flat_data['component_list'],
        flat_data['instance_id'],
        flat_data['vnc'],
        flat_data['project_id'],
        flat_data['volume_size'],
        flat_data['volume_type'],
        flat_data['subnet_id'],
        flat_data['subnet_name'],
        flat_data['security_group_id'],
        flat_data['non_master_security_group_id'],
        flat_data['safe_mode'],
        flat_data['key'],
        flat_data['master_ip'],
        flat_data['preffered_private_ip'],
        flat_data['charging_start_time'],
        flat_data['task_node_groups'],
        flat_data['node_groups'],
        flat_data['bootstrap_scripts'],
        flat_data['scale'],
    )

    def setUp(self):
        super(TestUpdateVault, self).setUp()

        self.cmd = cluster.UpdateCluster(self.app, None)
        self.app.client_manager.sdk_connection = mock.Mock()

        self.client.update_cluster = mock.Mock()

    def test_default(self):
        arglist = [
            'cluster_id',
            '--scale_type', 'scale_in',
            '--instances', '3',
        ]
        verifylist = [
            ('cluster', 'cluster_id'),
            ('scale_type', 'scale_in'),
            ('instances', 3),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.update_cluster.side_effect = [
            self.object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_cluster.assert_called_with(
            name_or_id='cluster_id',
            ignore_missing=False)

        self.client.update_cluster.assert_called_once_with(
            cluster=mock.ANY,
            parameters={
                'scale_type': 'scale_in',
                'node_id': 'node_orderadd',
                'instances': 3
            }
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)
