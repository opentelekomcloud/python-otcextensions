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

from otcextensions.osclient.cce.v2 import cluster
from otcextensions.tests.unit.osclient.cce.v2 import fakes


class TestCluster(fakes.TestCCE):

    def setUp(self):
        super(TestCluster, self).setUp()

    def test_flatten(self):
        _obj = fakes.FakeCluster.create_one()

        flat_data = cluster._flatten_cluster(_obj)

        data = (
            flat_data['id'],
            flat_data['name'],
            flat_data['endpoint'],
            flat_data['status'],
            flat_data['version'],
            flat_data['type'],
        )

        cmp_data = (
            _obj.metadata.id,
            _obj.metadata.name,
            _obj.status.endpoints['external_otc'],
            _obj.status.status,
            _obj.spec.version,
            _obj.spec.type
        )

        self.assertEqual(data, cmp_data)


class TestClusterList(fakes.TestCCE):

    _objs = fakes.FakeCluster.create_multiple(3)

    columns = ('ID', 'name', 'status', 'flavor', 'version', 'endpoint')

    data = []

    for s in _objs:
        flat_data = cluster._flatten_cluster(s)
        data.append((
            flat_data['id'],
            flat_data['name'],
            flat_data['status'],
            flat_data['flavor'],
            flat_data['version'],
            flat_data['endpoint'],
        ))

    def setUp(self):
        super(TestClusterList, self).setUp()

        self.cmd = cluster.ListCCECluster(self.app, None)

        self.client.clusters = mock.Mock()

    def test_list_default(self):
        arglist = []

        verifylist = []

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.clusters.side_effect = [
            self._objs
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.clusters.assert_called_once_with()

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))


class TestClusterShow(fakes.TestCCE):

    _obj = fakes.FakeCluster.create_one()

    columns = ('ID', 'name', 'type', 'status', 'version', 'endpoint',
               'flavor', 'router_id', 'network_id')
    flat_data = cluster._flatten_cluster(_obj)
    data = (
        flat_data['id'],
        flat_data['name'],
        flat_data['type'],
        flat_data['status'],
        flat_data['version'],
        flat_data['endpoint'],
        flat_data['flavor'],
        flat_data['router_id'],
        flat_data['network_id'],
    )

    def setUp(self):
        super(TestClusterShow, self).setUp()

        self.cmd = cluster.ShowCCECluster(self.app, None)

        self.client.find_cluster = mock.Mock()

    def test_get(self):
        arglist = [
            'cluster_uuid'
        ]

        verifylist = [
            ('cluster', 'cluster_uuid')
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.find_cluster.side_effect = [
            self._obj
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_cluster.assert_called_once_with(
            'cluster_uuid',
            ignore_missing=False
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestClusterCreate(fakes.TestCCE):

    _obj = fakes.FakeCluster.create_one()

    columns = ('ID', 'name', 'version', 'endpoint')

    flat_data = cluster._flatten_cluster(_obj)
    data = (
        flat_data['id'],
        flat_data['name'],
        flat_data['version'],
        flat_data['endpoint'],
    )

    def setUp(self):
        super(TestClusterCreate, self).setUp()

        self.cmd = cluster.CreateCCECluster(self.app, None)

        self.sdk_client.create_cce_cluster = \
            mock.Mock(return_value=self._obj)

    def test_create(self):
        arglist = [
            'cluster_name',
            'vpc_id',
            'net_id',
            '--description', 'descr',
            '--type', 'VirtualMachine',
            '--flavor', 'flavor',
            '--container-network-mode', 'overlay_l2'
        ]

        verifylist = [
            ('name', 'cluster_name'),
            ('router', 'vpc_id'),
            ('network', 'net_id'),
            ('description', 'descr'),
            ('type', 'VirtualMachine'),
            ('flavor', 'flavor'),
            ('container_network_mode', 'overlay_l2')
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.sdk_client.create_cce_cluster.assert_called_once_with(
            container_network_mode='overlay_l2',
            description='descr',
            flavor='flavor',
            name='cluster_name',
            network='net_id',
            router='vpc_id',
            type='VirtualMachine',
            wait=False
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)

    def test_wait(self):
        arglist = [
            'cluster_name',
            'vpc_id',
            'net_id',
            '--description', 'descr',
            '--type', 'VirtualMachine',
            '--flavor', 'flavor',
            '--container-network-mode', 'overlay_l2',
            '--wait',
            '--wait-interval', '13'
        ]

        verifylist = [
            ('name', 'cluster_name'),
            ('router', 'vpc_id'),
            ('network', 'net_id'),
            ('description', 'descr'),
            ('type', 'VirtualMachine'),
            ('flavor', 'flavor'),
            ('container_network_mode', 'overlay_l2'),
            ('wait', True),
            ('wait_interval', 13)
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.sdk_client.create_cce_cluster.assert_called_once_with(
            container_network_mode='overlay_l2',
            description='descr',
            flavor='flavor',
            name='cluster_name',
            network='net_id',
            router='vpc_id',
            type='VirtualMachine',
            wait=True,
            wait_interval=13
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestClusterDelete(fakes.TestCCE):

    def setUp(self):
        super(TestClusterDelete, self).setUp()

        self.cmd = cluster.DeleteCCECluster(self.app, None)

        self.sdk_client.delete_cce_cluster = mock.Mock()

    def test_delete(self):
        arglist = [
            'cluster_uuid'
        ]

        verifylist = [
            ('cluster', 'cluster_uuid')
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.sdk_client.delete_cce_cluster.assert_called_once_with(
            cluster='cluster_uuid', wait=False)

    def test_delete_wait(self):
        arglist = [
            'cluster_uuid',
            '--wait'
        ]

        verifylist = [
            ('cluster', 'cluster_uuid'),
            ('wait', True),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.sdk_client.delete_cce_cluster.assert_called_once_with(
            cluster='cluster_uuid', wait=True)
