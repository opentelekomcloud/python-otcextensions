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

from unittest import mock

from otcextensions.osclient.privatenat.v3 import transit_ip
from otcextensions.tests.unit.osclient.privatenat.v3 import fakes


class TestListPrivateTransitIps(fakes.TestPrivateNat):
    columns = (
        "id",
        "ip_address",
        "gateway_id",
        "network_interface_id",
        "virsubnet_id",
        "status",
    )

    def setUp(self):
        super(TestListPrivateTransitIps, self).setUp()

        self.cmd = transit_ip.ListPrivateTransitIps(self.app, None)

        self.objects = fakes.FakePrivateTransitIp.create_multiple(2)
        self.data = [
            (
                obj.id,
                obj.ip_address,
                obj.gateway_id,
                obj.network_interface_id,
                obj.virsubnet_id,
                obj.status,
            )
            for obj in self.objects
        ]

        self.client.private_transit_ips = mock.Mock(return_value=self.objects)
        self.client.api_mock = self.client.private_transit_ips

    def test_list(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        columns, data = self.cmd.take_action(parsed_args)

        self.client.private_transit_ips.assert_called_once_with()
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))

    def test_list_with_supported_filters(self):
        arglist = [
            "--id",
            "transit-ip-1",
            "--id",
            "transit-ip-2",
            "--limit",
            "100",
            "--marker",
            "marker-id",
            "--page-reverse",
            "--project-id",
            "project-1",
            "--project-id",
            "project-2",
            "--network-interface-id",
            "net-1",
            "--ip-address",
            "172.20.1.10",
            "--virsubnet-id",
            "subnet-1",
            "--virsubnet-id",
            "subnet-2",
            "--transit-subnet-id",
            "transit-subnet-1",
            "--gateway-id",
            "gw-1",
            "--gateway-id",
            "gw-2",
            "--enterprise-project-id",
            "ep-1",
            "--description",
            "desc-1",
        ]
        verifylist = [
            ("id", ["transit-ip-1", "transit-ip-2"]),
            ("limit", 100),
            ("marker", "marker-id"),
            ("page_reverse", True),
            ("project_id", ["project-1", "project-2"]),
            ("network_interface_id", ["net-1"]),
            ("ip_address", ["172.20.1.10"]),
            ("virsubnet_id", ["subnet-1", "subnet-2"]),
            ("transit_subnet_id", ["transit-subnet-1"]),
            ("gateway_id", ["gw-1", "gw-2"]),
            ("enterprise_project_id", ["ep-1"]),
            ("description", ["desc-1"]),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        columns, data = self.cmd.take_action(parsed_args)

        self.client.private_transit_ips.assert_called_once_with(
            id=["transit-ip-1", "transit-ip-2"],
            limit=100,
            marker="marker-id",
            page_reverse=True,
            project_id=["project-1", "project-2"],
            network_interface_id=["net-1"],
            ip_address=["172.20.1.10"],
            virsubnet_id=["subnet-1", "subnet-2"],
            transit_subnet_id=["transit-subnet-1"],
            gateway_id=["gw-1", "gw-2"],
            enterprise_project_id=["ep-1"],
            description=["desc-1"],
        )
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))
