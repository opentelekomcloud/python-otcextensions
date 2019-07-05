#   Copyright 2013 Nebula Inc.
#
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
from otcextensions.osclient.cce.v2 import cluster_node
from otcextensions.tests.unit.osclient.cce.v2 import fakes


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

    columns = ('ID', 'name', 'flavor',
               'private_ip', 'public_ip', 'availability_zone', 'ssh_key',
               'status')

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


class TestCreateClusterNode(fakes.TestCCE):

    _obj = fakes.FakeClusterNode.create_one()

    columns = ('ID', 'name', 'flavor',
               'private_ip', 'public_ip', 'availability_zone', 'ssh_key',
               'status')

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

    def setUp(self):
        super(TestCreateClusterNode, self).setUp()

        self.cmd = cluster_node.CreateCCEClusterNode(self.app, None)

        self.client.create_cluster_node = mock.Mock()

        self.client.find_cluster = mock.Mock(
            return_value=cluster.Cluster(id='cluster_id'))

    def test_create(self):
        arglist = [
            'cluster_name',
            '--flavor', 'flvr',
            '--label', 'l1=v1',
            '--label', 'l2=v2',
            '--annotation', 'a1=v1',
            '--annotation', 'a2=v2',
            '--volume', 'sata,30',
            '--root_volume', 'sata,230',
            '--ssh_key', 'key',
            '--availability_zone', 'az',
            '--count', '12'
        ]

        verifylist = [
            ('cluster', 'cluster_name'),
            ('flavor', 'flvr'),
            ('label', ['l1=v1', 'l2=v2']),
            ('annotation', ['a1=v1', 'a2=v2']),
            ('volume', 'sata,30'),
            ('root_volume', 'sata,230'),
            ('ssh_key', 'key'),
            ('availability_zone', 'az'),
            ('count', 12)
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.create_cluster_node.side_effect = [
            self._obj
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_cluster_node.assert_called_once_with(
            cluster='cluster_id',
            metadata={
                'annotations': {'a1': 'v1', 'a2': 'v2'},
                'labels': {'l1': 'v1', 'l2': 'v2'}
            },
            spec={
                'flavor': 'flvr',
                'login': {'sshKey': 'key'},
                'az': 'az',
                'count': 12,
                'rootVolume': {'volumetype': 'SATA', 'size': 230},
                'dataVolumes': [{'volumetype': 'SATA', 'size': 30}]
            }
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestDeleteClusterNode(fakes.TestCCE):

    def setUp(self):
        super(TestDeleteClusterNode, self).setUp()

        self.cmd = cluster_node.DeleteCCEClusterNode(self.app, None)

        self.client.delete_cluster_node = mock.Mock()

        self.client.find_cluster = mock.Mock(
            return_value=cluster.Cluster(id='cluster_uuid'))

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

        # Trigger the action
        self.cmd.take_action(parsed_args)

        calls = [
            mock.call(cluster='cluster_uuid', node='node1',
                      ignore_missing=False),
            mock.call(cluster='cluster_uuid', node='node2',
                      ignore_missing=False)
        ]

        self.client.delete_cluster_node.assert_has_calls(calls)
        self.assertEqual(2, self.client.delete_cluster_node.call_count)
