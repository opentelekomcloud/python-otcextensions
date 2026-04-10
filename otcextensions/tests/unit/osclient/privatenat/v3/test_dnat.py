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

from otcextensions.osclient.privatenat.v3 import dnat
from otcextensions.tests.unit.osclient.privatenat.v3 import fakes


class TestListPrivateDnatRules(fakes.TestPrivateNat):
    columns = (
        "id",
        "gateway_id",
        "transit_ip_id",
        "network_interface_id",
        "private_ip_address",
        "type",
        "protocol",
        "status",
    )

    def setUp(self):
        super(TestListPrivateDnatRules, self).setUp()

        self.cmd = dnat.ListPrivateDnatRules(self.app, None)

        self.objects = fakes.FakePrivateDnatRule.create_multiple(2)
        self.data = [
            (
                obj.id,
                obj.gateway_id,
                obj.transit_ip_id,
                obj.network_interface_id,
                obj.private_ip_address,
                obj.type,
                obj.protocol,
                obj.status,
            )
            for obj in self.objects
        ]

        self.client.private_dnat_rules = mock.Mock(return_value=self.objects)
        self.client.api_mock = self.client.private_dnat_rules

    def test_list(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        columns, data = self.cmd.take_action(parsed_args)

        self.client.private_dnat_rules.assert_called_once_with()
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))

    def test_list_with_supported_filters(self):
        arglist = [
            "--id",
            "rule-id-1",
            "--id",
            "rule-id-2",
            "--limit",
            "100",
            "--marker",
            "marker-id",
            "--page-reverse",
            "--project-id",
            "project-1",
            "--project-id",
            "project-2",
            "--enterprise-project-id",
            "ep-1",
            "--description",
            "desc-1",
            "--gateway-id",
            "gw-1",
            "--gateway-id",
            "gw-2",
            "--transit-ip-id",
            "tip-1",
            "--external-ip-address",
            "10.0.0.10",
            "--network-interface-id",
            "nic-1",
            "--type",
            "COMPUTE",
            "--private-ip-address",
            "192.168.1.10",
            "--protocol",
            "TCP",
            "--protocol",
            "udp",
            "--internal-service-port",
            "80",
            "--internal-service-port",
            "443",
            "--transit-service-port",
            "8080",
            "--created-at",
            "2019-04-29T07:10:01Z",
            "--updated-at",
            "2019-04-29T07:20:01Z",
        ]
        verifylist = [
            ("id", ["rule-id-1", "rule-id-2"]),
            ("limit", 100),
            ("marker", "marker-id"),
            ("page_reverse", True),
            ("project_id", ["project-1", "project-2"]),
            ("enterprise_project_id", ["ep-1"]),
            ("description", ["desc-1"]),
            ("gateway_id", ["gw-1", "gw-2"]),
            ("transit_ip_id", ["tip-1"]),
            ("external_ip_address", ["10.0.0.10"]),
            ("network_interface_id", ["nic-1"]),
            ("type", ["COMPUTE"]),
            ("private_ip_address", ["192.168.1.10"]),
            ("protocol", ["TCP", "udp"]),
            ("internal_service_port", ["80", "443"]),
            ("transit_service_port", ["8080"]),
            ("created_at", "2019-04-29T07:10:01Z"),
            ("updated_at", "2019-04-29T07:20:01Z"),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        columns, data = self.cmd.take_action(parsed_args)

        self.client.private_dnat_rules.assert_called_once_with(
            id=["rule-id-1", "rule-id-2"],
            limit=100,
            marker="marker-id",
            page_reverse=True,
            project_id=["project-1", "project-2"],
            enterprise_project_id=["ep-1"],
            description=["desc-1"],
            gateway_id=["gw-1", "gw-2"],
            transit_ip_id=["tip-1"],
            external_ip_address=["10.0.0.10"],
            network_interface_id=["nic-1"],
            type=["COMPUTE"],
            private_ip_address=["192.168.1.10"],
            protocol=["tcp", "udp"],
            internal_service_port=["80", "443"],
            transit_service_port=["8080"],
            created_at="2019-04-29T07:10:01Z",
            updated_at="2019-04-29T07:20:01Z",
        )
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))
