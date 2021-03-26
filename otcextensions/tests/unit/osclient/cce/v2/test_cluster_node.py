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
from otcextensions.sdk.cce.v3 import cluster_node as clusterNode
from otcextensions.osclient.cce.v2 import cluster_node
from otcextensions.tests.unit.osclient.cce.v2 import fakes


class TestCreateClusterNode(fakes.TestCCE):

    _obj = fakes.FakeClusterNode.create_one()

    columns = (
        'id',
        'name',
        'private_ip',
        'public_ip',
        'status',
        'flavor',
        'ssh_key',
        'availability_zone',
        'operating_system',
        'root_volume_type',
        'root_volume_size',
        'data_volume_type_1',
        'data_volume_size_1',
        'data_volume_type_2',
        'data_volume_size_2')

    flat_data = cluster_node._flatten_cluster_node(_obj)

    data = (
        flat_data['id'],
        flat_data['name'],
        flat_data['private_ip'],
        flat_data['public_ip'],
        flat_data['status'],
        flat_data['flavor'],
        flat_data['ssh_key'],
        flat_data['availability_zone'],
        flat_data['operating_system'],
        flat_data['root_volume_type'],
        flat_data['root_volume_size'],
        flat_data['data_volume_type_1'],
        flat_data['data_volume_size_1'],
        flat_data['data_volume_type_2'],
        flat_data['data_volume_size_2']
    )

    def setUp(self):
        super(TestCreateClusterNode, self).setUp()

        self.cmd = cluster_node.CreateCCEClusterNode(self.app, None)

        self.app.client_manager.sdk_connection = mock.Mock()

        self.cloud_client = self.app.client_manager.sdk_connection

        self.cloud_client.create_cce_cluster_node = mock.Mock()

        self.client.find_cluster = mock.Mock(
            return_value=cluster.Cluster(id='cluster_id'))

    def test_create(self):
        arglist = [
            'cluster_name',
            '--name', 'node_name',
            '--annotation', 'a1=v1',
            '--annotation', 'a2=v2',
            '--availability-zone', 'az',
            '--bandwidth', '30',
            '--count', '12',
            '--data-volume', 'volumetype=SATA,size=100',
            '--data-volume', 'volumetype=SAS,size=200',
            '--flavor', 'flvr',
            '--label', 'l1=v1',
            '--label', 'l2=v2',
            '--network-id', 'nw',
            '--root-volume-size', '230',
            '--root-volume-type', 'SATA',
            '--ssh-key', 'key',
        ]

        verifylist = [
            ('cluster', 'cluster_name'),
            ('name', 'node_name'),
            ('annotations', {'a1': 'v1', 'a2': 'v2'}),
            ('availability_zone', 'az'),
            ('bandwidth', 30),
            ('count', 12),
            ('data_volumes', [
                {'volumetype': 'SATA', 'size': '100'},
                {'volumetype': 'SAS', 'size': '200'}]),
            ('flavor', 'flvr'),
            ('labels', {'l1': 'v1', 'l2': 'v2'}),
            ('network_id', 'nw'),
            ('root_volume_size', 230),
            ('root_volume_type', 'SATA'),
            ('ssh_key', 'key'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.cloud_client.create_cce_cluster_node.side_effect = [
            self._obj
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.cloud_client.create_cce_cluster_node.assert_called_once_with(
            availability_zone='az',
            cluster='cluster_name',
            count=12,
            flavor='flvr',
            network_id='nw',
            ssh_key='key',
            annotations={'a1': 'v1', 'a2': 'v2'},
            bandwidth=30,
            data_volumes=[
                {'volumetype': 'SATA', 'size': '100'},
                {'volumetype': 'SAS', 'size': '200'}],
            labels={'l1': 'v1', 'l2': 'v2'},
            name='node_name',
            root_volume_size=230,
            root_volume_type='SATA',
            wait=False,
            wait_interval=5,
            wait_timeout=3600
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestClusterNode(fakes.TestCCE):

    def setUp(self):
        super(TestClusterNode, self).setUp()

    def test_flatten(self):
        _obj = fakes.FakeClusterNode.create_one()

        flat_data = cluster_node._flatten_cluster_node(_obj)

        data = (
            flat_data['id'],
            flat_data['name'],
            flat_data['flavor'],
            flat_data['private_ip'],
            flat_data['public_ip'],
            flat_data['availability_zone'],
            flat_data['ssh_key'],
            flat_data['status'],
        )

        cmp_data = (
            _obj.metadata.id,
            _obj.metadata.name,
            _obj.spec.flavor,
            _obj.status.private_ip,
            _obj.status.floating_ip,
            _obj.spec.availability_zone,
            _obj.spec.login.get('sshKey', None),
            _obj.status.status,
        )

        self.assertEqual(data, cmp_data)


class TestListClusterNode(fakes.TestCCE):

    _objs = fakes.FakeClusterNode.create_multiple(3)

    columns = ('ID', 'name', 'private_ip', 'public_ip',
               'status')

    data = []

    for s in _objs:
        flat_data = cluster_node._flatten_cluster_node(s)

        data.append((
            flat_data['id'],
            flat_data['name'],
            flat_data['private_ip'],
            flat_data['public_ip'],
            flat_data['status'],
        ))

    def setUp(self):
        super(TestListClusterNode, self).setUp()

        self.cmd = cluster_node.ListCCEClusterNode(self.app, None)

        self.client.cluster_nodes = mock.Mock()
        self.client.find_cluster = mock.Mock(
            return_value=cluster.Cluster(id='cluster_id'))

    def test_list_default(self):
        arglist = ['cluster_id']

        verifylist = [
            ('cluster', 'cluster_id')
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.cluster_nodes.side_effect = [
            self._objs
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.cluster_nodes.assert_called_once_with(
            'cluster_id'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))


class TestShowClusterNode(fakes.TestCCE):

    _obj = fakes.FakeClusterNode.create_one()

    columns = (
        'id',
        'name',
        'private_ip',
        'public_ip',
        'status',
        'flavor',
        'ssh_key',
        'availability_zone',
        'operating_system',
        'root_volume_type',
        'root_volume_size',
        'data_volume_type_1',
        'data_volume_size_1',
        'data_volume_type_2',
        'data_volume_size_2')

    flat_data = cluster_node._flatten_cluster_node(_obj)

    data = (
        flat_data['id'],
        flat_data['name'],
        flat_data['private_ip'],
        flat_data['public_ip'],
        flat_data['status'],
        flat_data['flavor'],
        flat_data['ssh_key'],
        flat_data['availability_zone'],
        flat_data['operating_system'],
        flat_data['root_volume_type'],
        flat_data['root_volume_size'],
        flat_data['data_volume_type_1'],
        flat_data['data_volume_size_1'],
        flat_data['data_volume_type_2'],
        flat_data['data_volume_size_2']
    )

    def setUp(self):
        super(TestShowClusterNode, self).setUp()

        self.cmd = cluster_node.ShowCCEClusterNode(self.app, None)

        self.client.find_cluster_node = mock.Mock()

        self.client.find_cluster = mock.Mock(
            return_value=cluster.Cluster(id='cluster_uuid'))

    def test_show(self):
        arglist = [
            'cluster_uuid',
            'node_id'
        ]

        verifylist = [
            ('cluster', 'cluster_uuid'),
            ('node', 'node_id')
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.find_cluster_node.side_effect = [
            self._obj
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_cluster_node.assert_called_once_with(
            cluster='cluster_uuid',
            node='node_id')

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestDeleteClusterNode(fakes.TestCCE):

    def setUp(self):
        super(TestDeleteClusterNode, self).setUp()

        self.cmd = cluster_node.DeleteCCEClusterNode(self.app, None)

        self.client.delete_cluster_node = mock.Mock()

        self.client.find_cluster = mock.Mock(
            return_value=cluster.Cluster(id='cluster_uuid'))

        self.client.find_cluster_node = mock.Mock()

    def test_delete(self):
        arglist = [
            'cluster_uuid',
            'node1',
            'node2'
        ]

        verifylist = [
            ('cluster', 'cluster_uuid'),
            ('node', ['node1', 'node2'])
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.delete_cluster_node.side_effect = [{}, {}]

        # Set the response for find_cluster
        self.client.find_cluster_node.side_effect = [
            clusterNode.ClusterNode(id='node1'),
            clusterNode.ClusterNode(id='node2')]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        delete_calls = [
            mock.call(cluster='cluster_uuid', node='node1',
                      ignore_missing=False),
            mock.call(cluster='cluster_uuid', node='node2',
                      ignore_missing=False)
        ]

        find_calls = [
            mock.call(cluster='cluster_uuid', node='node1'),
            mock.call(cluster='cluster_uuid', node='node2')
        ]

        self.client.delete_cluster_node.assert_has_calls(delete_calls)
        self.client.find_cluster_node.assert_has_calls(find_calls)
        self.assertEqual(2, self.client.delete_cluster_node.call_count)
