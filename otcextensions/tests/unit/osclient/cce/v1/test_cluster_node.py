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

from otcextensions.osclient.cce.v1 import cluster_node
from otcextensions.tests.unit.osclient.cce.v1 import fakes


class TestClusterNode(fakes.TestCCE):

    def setUp(self):
        super(TestClusterNode, self).setUp()

    def test_flatten(self):
        _obj = fakes.FakeClusterNode.create_one()

        flat_data = cluster_node._flatten_cluster_node(_obj)

        data = (
            flat_data['id'],
            flat_data['name'],
            flat_data['cluster_uuid'],
            flat_data['flavor'],
            flat_data['cpu'],
            flat_data['memory'],
            flat_data['volumes'],
            flat_data['cpu_max'],
            flat_data['mem_max'],
            flat_data['pods_max'],
            flat_data['cpu_allocatable'],
            flat_data['mem_allocatable'],
            flat_data['pods_allocatable'],
            flat_data['conditions'],
            flat_data['private_ip'],
            flat_data['public_ip'],
            flat_data['availability_zone'],
            flat_data['ssh_key'],
            flat_data['status'],
            flat_data['replica_count'],
        )

        cmp_data = (
            _obj.metadata.id,
            _obj.metadata.name,
            _obj.spec.cluster_uuid,
            _obj.spec.flavor,
            _obj.spec.cpu,
            _obj.spec.memory,
            ';'.join(
                (x.disk_type + ':' + str(x.disk_size))
                for x in _obj.spec.volume
            ) if _obj.spec.volume else '',
            _obj.spec.status.capacity.cpu,
            _obj.spec.status.capacity.memory,
            _obj.spec.status.capacity.pods,
            _obj.spec.status.allocatable.cpu,
            _obj.spec.status.allocatable.memory,
            _obj.spec.status.allocatable.pods,
            ';'.join(
                (cond['type'] + '=' + cond['status'])
                for cond in _obj.spec.status.conditions
            ) if _obj.spec.status.conditions else '',
            _obj.spec.private_ip,
            _obj.spec.public_ip,
            _obj.spec.availability_zone,
            _obj.spec.ssh_key,
            _obj.status,
            _obj.replica_count
        )

        self.assertEqual(data, cmp_data)


class TestListClusterNode(fakes.TestCCE):

    _objs = fakes.FakeClusterNode.create_multiple(3)

    columns = ('ID', 'name', 'private_ip', 'public_ip',
               'availability_zone', 'status')

    data = []

    for s in _objs:
        flat_data = cluster_node._flatten_cluster_node(s)

        data.append((
            flat_data['id'],
            flat_data['name'],
            flat_data['private_ip'],
            flat_data['public_ip'],
            flat_data['availability_zone'],
            flat_data['status'],
        ))

    def setUp(self):
        super(TestListClusterNode, self).setUp()

        self.cmd = cluster_node.ListCCEClusterNode(self.app, None)

        self.client.cluster_nodes = mock.Mock()

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

    columns = ('ID', 'name', 'cluster_uuid',
               'flavor', 'cpu', 'memory', 'volumes',
               'cpu_max', 'mem_max', 'pods_max',
               'cpu_allocatable', 'mem_allocatable', 'pods_allocatable',
               'conditions',
               'private_ip', 'public_ip', 'availability_zone', 'ssh_key',
               'status', 'replica_count')

    flat_data = cluster_node._flatten_cluster_node(_obj)

    data = (
        flat_data['id'],
        flat_data['name'],
        flat_data['cluster_uuid'],
        flat_data['flavor'],
        flat_data['cpu'],
        flat_data['memory'],
        flat_data['volumes'],
        flat_data['cpu_max'],
        flat_data['mem_max'],
        flat_data['pods_max'],
        flat_data['cpu_allocatable'],
        flat_data['mem_allocatable'],
        flat_data['pods_allocatable'],
        flat_data['conditions'],
        flat_data['private_ip'],
        flat_data['public_ip'],
        flat_data['availability_zone'],
        flat_data['ssh_key'],
        flat_data['status'],
        flat_data['replica_count'],
    )

    def setUp(self):
        super(TestShowClusterNode, self).setUp()

        self.cmd = cluster_node.ShowCCEClusterNode(self.app, None)

        self.client.find_cluster_node = mock.Mock()

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


class TestCreateClusterNode(fakes.TestCCE):

    _obj = fakes.FakeClusterNode.create_one()

    columns = ('ID', 'name', 'cluster_uuid',
               'flavor', 'cpu', 'memory', 'volumes',
               'cpu_max', 'mem_max', 'pods_max',
               'cpu_allocatable', 'mem_allocatable', 'pods_allocatable',
               'conditions',
               'private_ip', 'public_ip', 'availability_zone', 'ssh_key',
               'status', 'replica_count')

    flat_data = cluster_node._flatten_cluster_node(_obj)

    data = (
        flat_data['id'],
        flat_data['name'],
        flat_data['cluster_uuid'],
        flat_data['flavor'],
        flat_data['cpu'],
        flat_data['memory'],
        flat_data['volumes'],
        flat_data['cpu_max'],
        flat_data['mem_max'],
        flat_data['pods_max'],
        flat_data['cpu_allocatable'],
        flat_data['mem_allocatable'],
        flat_data['pods_allocatable'],
        flat_data['conditions'],
        flat_data['private_ip'],
        flat_data['public_ip'],
        flat_data['availability_zone'],
        flat_data['ssh_key'],
        flat_data['status'],
        flat_data['replica_count'],
    )

    def setUp(self):
        super(TestCreateClusterNode, self).setUp()

        self.cmd = cluster_node.CreateCCEClusterNode(self.app, None)

        self.client.add_node = mock.Mock()

    def test_create(self):
        arglist = [
            'cluster_name',
            '--flavor', 'flvr',
            '--label', 'lbl',
            '--volume', 'sys,sata,30',
            '--volume', 'data,sata,230',
            '--ssh_key', 'key',
            '--assign_floating_ip',
            '--availability_zone', 'az',
            '--tag', 'a=b',
            '--tag', 'c=d',
            '--replica_count', '12',
        ]

        verifylist = [
            ('cluster', 'cluster_name'),
            ('flavor', 'flvr'),
            ('label', 'lbl'),
            ('volume', ['sys,sata,30', 'data,sata,230']),
            ('ssh_key', 'key'),
            ('availability_zone', 'az'),
            ('assign_floating_ip', True),
            ('tag', ['a=b', 'c=d']),
            ('replica_count', 12)
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.add_node.side_effect = [
            self._obj
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.add_node.assert_called_once_with(
            cluster='cluster_name',
            replica_count=12,
            spec={
                'flavor': 'flvr',
                'ssh_key': 'key',
                'availability_zone': 'az',
                'label': 'lbl',
                'assign_floating_ip': True,
                'volume': [
                    {'disk_type': 'root', 'volume_type': 'SATA'},
                    {'disk_type': 'data', 'volume_type': 'SATA',
                        'disk_size': '230'}],
                'tags': ['a.b', 'c.d']}
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestDeleteClusterNode(fakes.TestCCE):

    def setUp(self):
        super(TestDeleteClusterNode, self).setUp()

        self.cmd = cluster_node.DeleteCCEClusterNode(self.app, None)

        self.client.delete_cluster_nodes = mock.Mock()

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
        self.client.delete_cluster_nodes.side_effect = [{}]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.delete_cluster_nodes.assert_called_once_with(
            cluster='cluster_uuid',
            node_names=['node1', 'node2']
        )
