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
from otcextensions.common import cli_utils
from otcextensions.osclient.modelartsv1.v1 import service
from otcextensions.tests.unit.osclient.modelartsv1.v1 import fakes


class TestClusters(fakes.TestModelartsv1):
    objects = fakes.FakeServiceCluster.create_multiple(3)

    column_list_headers = (
        "Cluster Id",
        "Cluster Name",
        "Created At",
        "Status",
        "Allocatable Resources",
        "Charging Mode",
        "Max Node Count",
        "Nodes",
        "Services Count",
    )

    data = []

    for s in objects:
        data.append(
            (
                s.cluster_id,
                s.cluster_name,
                cli_utils.UnixTimestampFormatter(s.created_at),
                s.status,
                cli_utils.YamlFormat(s.allocatable_resources),
                s.charging_mode,
                s.max_node_count,
                cli_utils.YamlFormat(s.nodes),
                cli_utils.YamlFormat(s.services_count),
            )
        )

    def setUp(self):
        super(TestClusters, self).setUp()

        self.cmd = service.Clusters(self.app, None)

        self.client.service_resource_pools = mock.Mock()
        self.client.api_mock = self.client.service_resource_pools

    def test_list(self):
        arglist = []

        verifylist = []

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with()

        self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(self.data, list(data))

    def test_list_args(self):
        arglist = [
            "--cluster-name",
            "1",
            "--limit",
            "2",
            "--offset",
            "3",
            "--order",
            "asc",
            "--sort-by",
            "cluster_name",
            "--status",
            "6",
        ]

        verifylist = [
            ("cluster_name", "1"),
            ("limit", 2),
            ("offset", 3),
            ("order", "asc"),
            ("sort_by", "cluster_name"),
            ("status", "6"),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(
            cluster_name="1",
            limit=2,
            offset=3,
            order="asc",
            sort_by="cluster_name",
            status="6",
        )
