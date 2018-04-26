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

from otcextensions.osclient.cce.v1 import cluster
from otcextensions.tests.unit.osclient.cce.v1 import fakes


class TestCluster(fakes.TestCCE):

    def setUp(self):
        super(TestCluster, self).setUp()


class TestListCluster(TestCluster):

    _objs = fakes.FakeCluster.create_multiple(3)

    columns = ('ID', 'name', 'cpu', 'memory', 'endpoint')

    data = []

    for s in _objs:
        data.append((
            s.metadata.id,
            s.metadata.name,
            s.spec.cpu,
            s.spec.memory,
            s.spec.endpoint,
        ))

    def setUp(self):
        super(TestListCluster, self).setUp()

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


class TestShowCluster(TestCluster):

    _obj = fakes.FakeCluster.create_one()

    columns = ('ID', 'name', 'status', 'cpu', 'memory', 'endpoint',
               'availability_zone',
               'vpc', 'nodes')

    data = (
        _obj.metadata.id,
        _obj.metadata.name,
        _obj.status['status'],
        _obj.spec.cpu,
        _obj.spec.memory,
        _obj.spec.endpoint,
        _obj.spec.availability_zone,
        _obj.spec.vpc,
        len(_obj.spec.host_list.spec.host_list)
    )

    def setUp(self):
        super(TestShowCluster, self).setUp()

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

        self.client.find_cluster.assert_called_once_with('cluster_uuid')

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestCreateCluster(TestCluster):

    _obj = fakes.FakeCluster.create_one()

    columns = ('ID', 'name', 'status', 'cpu', 'memory', 'endpoint',
               'availability_zone',
               'vpc', 'nodes')

    data = (
        _obj.metadata.id,
        _obj.metadata.name,
        _obj.status['status'],
        _obj.spec.cpu,
        _obj.spec.memory,
        _obj.spec.endpoint,
        _obj.spec.availability_zone,
        _obj.spec.vpc,
        len(_obj.spec.host_list.spec.host_list)
    )

    def setUp(self):
        super(TestCreateCluster, self).setUp()

        self.cmd = cluster.CreateCCECluster(self.app, None)

        self.client.create_cluster = mock.Mock()

    def test_create(self):
        arglist = [
            'cluster_name',
            'vpc_id',
            'subnet_id',
            '--description', 'descr',
            '--region', 'regio',
            '--security_group', 'sg',
            '--type', 'HA'
        ]

        verifylist = [
            ('name', 'cluster_name'),
            ('vpc', 'vpc_id'),
            ('subnet', 'subnet_id'),
            ('description', 'descr'),
            ('region', 'regio'),
            ('security_group', 'sg'),
            ('type', 'HA')
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.create_cluster.side_effect = [
            self._obj
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_cluster.assert_called_once_with(
            name='cluster_name',
            spec={
                'vpc': 'vpc_id',
                'subnet': 'subnet_id',
                'region': 'regio',
                'description': 'descr',
                'security_group_id': 'sg',
                'cluster_type': 'HA'
            }
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestDeleteCluster(TestCluster):

    def setUp(self):
        super(TestDeleteCluster, self).setUp()

        self.cmd = cluster.DeleteCCECluster(self.app, None)

        self.client.delete_cluster = mock.Mock()

    def test_delete(self):
        arglist = [
            'cluster_uuid'
        ]

        verifylist = [
            ('cluster', 'cluster_uuid')
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.delete_cluster.side_effect = [{}]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.delete_cluster.assert_called_once_with('cluster_uuid')
