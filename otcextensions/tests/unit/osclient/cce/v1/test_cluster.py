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

from osc_lib import exceptions

from otcextensions.tests.unit.osclient.cce.v1 import fakes

from otcextensions.osclient.cce.v1 import cluster


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

        self.client.get_cluster = mock.Mock()

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
        self.client.get_cluster.side_effect = [
            self._obj
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.get_cluster.assert_called_once_with('cluster_uuid')

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)
