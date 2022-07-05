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
import mock

from otcextensions.osclient.mrs.v1 import cluster
from otcextensions.tests.unit.osclient.mrs.v1 import fakes


class TestListClusterHost(fakes.TestMrs):
    objects = fakes.FakeHost.create_multiple(3)

    columns = (
        'id', 'name', 'status', 'flavor', 'type',
        'ip', 'mem', 'cpu', 'data_volume_size'
    )

    data = []

    for s in objects:
        data.append(fakes.gen_data(s, columns))

    def setUp(self):
        super(TestListClusterHost, self).setUp()

        self.cmd = cluster.ListClusterHost(self.app, None)

        self.client.hosts = mock.Mock()
        self.client.api_mock = self.client.hosts

    def test_default(self):
        arglist = [
            'cluster_id'
        ]
        verifylist = [
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [
            self.objects
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_once_with(
            cluster_id='cluster_id'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))
