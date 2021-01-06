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

from otcextensions.sdk.cce.v3 import cluster
from otcextensions.sdk.cce.v3 import node_pool as nodePool
from otcextensions.osclient.cce.v2 import node_pool
from otcextensions.tests.unit.osclient.cce.v2 import fakes


class TestNodePool(fakes.TestCCE):

    def setUp(self):
        super(TestNodePool, self).setUp()

    def test_flatten(self):
        obj = fakes.FakeNodePool.create_one()

        flat_data = node_pool._flatten_node_pool(obj)

        data = (
            flat_data['id'],
            flat_data['name'],
            flat_data['flavor'],
            flat_data['os'],
            flat_data['current_node'],
            flat_data['network_id'],
            flat_data['root_volume_type'],
            flat_data['root_volume_size'],
            flat_data['data_volume_type'],
            flat_data['data_volume_size'],
            flat_data['autoscaling'],
            flat_data['min_node_count'],
            flat_data['max_node_count'],
            flat_data['scale_down_cooldown_time'],
            flat_data['priority'],

        )

        cmp_data = (
            obj.id,
            obj.name,
            obj.spec.node_template_spec.flavor,
            obj.spec.node_template_spec.os,
            obj.status.current_node,
            obj.spec.node_template_spec.node_nic_spec.primary_nic.network_id,
            obj.spec.node_template_spec.root_volume.type,
            obj.spec.node_template_spec.root_volume.size,
            obj.spec.node_template_spec.data_volumes[0].type,
            obj.spec.node_template_spec.data_volumes[0].size,
            obj.spec.autoscaling.enable,
            obj.spec.autoscaling.min_node_count,
            obj.spec.autoscaling.max_node_count,
            obj.spec.autoscaling.scale_down_cooldown_time,
            obj.spec.autoscaling.priority
        )

        self.assertEqual(data, cmp_data)


class TestListNodePool(fakes.TestCCE):

    _objs = fakes.FakeNodePool.create_multiple(3)

    columns = ('ID', 'name', 'flavor', 'os', 'autoscaling', 'current_node')

    data = []

    for s in _objs:
        flat_data = node_pool._flatten_node_pool(s)

        data.append((
            flat_data['id'],
            flat_data['name'],
            flat_data['flavor'],
            flat_data['os'],
            flat_data['autoscaling'],
            flat_data['current_node'],
        ))

    def setUp(self):
        super(TestListNodePool, self).setUp()

        self.cmd = node_pool.ListCCENodePools(self.app, None)

        self.client.node_pools = mock.Mock()
        self.client.find_cluster = mock.Mock(
            return_value=cluster.Cluster(id='cluster_id'))

    def test_list_default(self):
        arglist = ['cluster_id']

        verifylist = [
            ('cluster', 'cluster_id')
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.node_pools.side_effect = [
            self._objs
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.node_pools.assert_called_once_with(
            'cluster_id'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))


class TestShowNodePool(fakes.TestCCE):

    _obj = fakes.FakeNodePool.create_one()

    columns = (
        'ID',
        'name',
        'flavor',
        'os',
        'current_node',
        'network_id',
        'root_volume_type',
        'root_volume_size',
        'data_volume_type',
        'data_volume_size',
        'autoscaling',
        'min_node_count',
        'max_node_count',
        'scale_down_cooldown_time',
        'priority',)

    flat_data = node_pool._flatten_node_pool(_obj)

    data = (
        flat_data['id'],
        flat_data['name'],
        flat_data['flavor'],
        flat_data['os'],
        flat_data['current_node'],
        flat_data['network_id'],
        flat_data['root_volume_type'],
        flat_data['root_volume_size'],
        flat_data['data_volume_type'],
        flat_data['data_volume_size'],
        flat_data['autoscaling'],
        flat_data['min_node_count'],
        flat_data['max_node_count'],
        flat_data['scale_down_cooldown_time'],
        flat_data['priority'],
    )

    def setUp(self):
        super(TestShowNodePool, self).setUp()

        self.cmd = node_pool.ShowCCENodePool(self.app, None)

        self.client.find_node_pool = mock.Mock()

        self.client.find_cluster = mock.Mock(
            return_value=cluster.Cluster(id='cluster_uuid'))

    def test_show(self):
        arglist = [
            'cluster_uuid',
            'pool_id'
        ]

        verifylist = [
            ('cluster', 'cluster_uuid'),
            ('nodepool', 'pool_id')
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.find_node_pool.side_effect = [
            self._obj
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_node_pool.assert_called_once_with(
            cluster='cluster_uuid',
            node_pool='pool_id')

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestDeleteNodePool(fakes.TestCCE):

    def setUp(self):
        super(TestDeleteNodePool, self).setUp()

        self.cmd = node_pool.DeleteCCENodePool(self.app, None)

        self.client.delete_node_pool = mock.Mock()

        self.client.find_cluster = mock.Mock(
            return_value=cluster.Cluster(id='cluster_uuid'))

        self.client.find_node_pool = mock.Mock()

    def test_delete(self):
        arglist = [
            'cluster_uuid',
            'pool1',
            'pool2'
        ]

        verifylist = [
            ('cluster', 'cluster_uuid'),
            ('nodepool', ['pool1', 'pool2'])
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.delete_node_pool.side_effect = [{}, {}]

        # Set the response for find_cluster
        self.client.find_node_pool.side_effect = [
            nodePool.NodePool(id='pool1'),
            nodePool.NodePool(id='pool2')]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        delete_calls = [
            mock.call(cluster='cluster_uuid', node_pool='pool1',
                      ignore_missing=False),
            mock.call(cluster='cluster_uuid', node_pool='pool2',
                      ignore_missing=False)
        ]

        find_calls = [
            mock.call(cluster='cluster_uuid', node_pool='pool1'),
            mock.call(cluster='cluster_uuid', node_pool='pool2')
        ]

        self.client.delete_node_pool.assert_has_calls(delete_calls)
        self.client.find_node_pool.assert_has_calls(find_calls)
        self.assertEqual(2, self.client.delete_node_pool.call_count)


class TestCreateNodePool(fakes.TestCCE):

    _obj = fakes.FakeNodePool.create_one()

    columns = (
        'ID',
        'name',
        'flavor',
        'os',
        'current_node',
        'network_id',
        'root_volume_type',
        'root_volume_size',
        'data_volume_type',
        'data_volume_size',
        'autoscaling',
        'min_node_count',
        'max_node_count',
        'scale_down_cooldown_time',
        'priority',)

    flat_data = node_pool._flatten_node_pool(_obj)

    data = (
        flat_data['id'],
        flat_data['name'],
        flat_data['flavor'],
        flat_data['os'],
        flat_data['current_node'],
        flat_data['network_id'],
        flat_data['root_volume_type'],
        flat_data['root_volume_size'],
        flat_data['data_volume_type'],
        flat_data['data_volume_size'],
        flat_data['autoscaling'],
        flat_data['min_node_count'],
        flat_data['max_node_count'],
        flat_data['scale_down_cooldown_time'],
        flat_data['priority'],
    )

    def setUp(self):
        super(TestCreateNodePool, self).setUp()

        self.cmd = node_pool.CreateCCENodePool(self.app, None)

        self.client.create_node_pool = mock.Mock()

        self.client.find_cluster = mock.Mock(
            return_value=cluster.Cluster(id='cluster_id'))

    def test_create(self):
        arglist = [
            'cluster_name',
            'pool_name',
            '--flavor', 'flav',
            '--os', 'CentOS',
            '--network-id', 'nw',
            '--ssh-key', 'sshkey'
        ]

        verifylist = [
            ('cluster', 'cluster_name'),
            ('name', 'pool_name'),
            ('flavor', 'flav'),
            ('os', 'CentOS'),
            ('network_id', 'nw'),
            ('ssh_key', 'sshkey'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.create_node_pool.side_effect = [
            self._obj
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_node_pool.assert_called_once_with(
            cluster='cluster_id',
            metadata={
                'name': 'pool_name',
            },
            spec={
                'nodeTemplate': {
                    'flavor': 'flav',
                    'os': 'CentOS',
                    'nodeNicSpec': {
                        'primaryNic': {
                            'subnetId': 'nw'
                        }
                    },
                    'login': {
                        'sshKey': 'sshkey'
                    }
                }
            }
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)
