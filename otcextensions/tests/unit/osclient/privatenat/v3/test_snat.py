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

from otcextensions.osclient.privatenat.v3 import snat
from otcextensions.tests.unit.osclient.privatenat.v3 import fakes


class TestListPrivateSnatRules(fakes.TestPrivateNat):
    columns = (
        "id",
        "gateway_id",
        "virsubnet_id",
        "cidr",
        "transit_ip_addresses",
        "description",
        "status",
    )

    def setUp(self):
        super(TestListPrivateSnatRules, self).setUp()

        self.cmd = snat.ListPrivateSnatRules(self.app, None)

        self.objects = fakes.FakePrivateSnatRule.create_multiple(2)
        self.data = [
            (
                obj.id,
                obj.gateway_id,
                obj.virsubnet_id,
                obj.cidr,
                obj.transit_ip_associations[0].transit_ip_address,
                obj.description,
                obj.status,
            )
            for obj in self.objects
        ]

        self.client.private_snat_rules = mock.Mock(return_value=self.objects)
        self.client.api_mock = self.client.private_snat_rules

    def test_list(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        columns, data = self.cmd.take_action(parsed_args)

        self.client.private_snat_rules.assert_called_once_with()
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
            "--description",
            "desc-1",
            "--gateway-id",
            "gw-1",
            "--gateway-id",
            "gw-2",
            "--cidr",
            "10.0.0.0/24",
            "--virsubnet-id",
            "subnet-1",
            "--transit-ip-id",
            "tip-1",
            "--transit-ip-address",
            "172.20.1.10",
            "--enterprise-project-id",
            "ep-1",
        ]
        verifylist = [
            ("id", ["rule-id-1", "rule-id-2"]),
            ("limit", 100),
            ("marker", "marker-id"),
            ("page_reverse", True),
            ("project_id", ["project-1", "project-2"]),
            ("description", ["desc-1"]),
            ("gateway_id", ["gw-1", "gw-2"]),
            ("cidr", ["10.0.0.0/24"]),
            ("virsubnet_id", ["subnet-1"]),
            ("transit_ip_id", ["tip-1"]),
            ("transit_ip_address", ["172.20.1.10"]),
            ("enterprise_project_id", ["ep-1"]),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        columns, data = self.cmd.take_action(parsed_args)

        self.client.private_snat_rules.assert_called_once_with(
            id=["rule-id-1", "rule-id-2"],
            limit=100,
            marker="marker-id",
            page_reverse=True,
            project_id=["project-1", "project-2"],
            description=["desc-1"],
            gateway_id=["gw-1", "gw-2"],
            cidr=["10.0.0.0/24"],
            virsubnet_id=["subnet-1"],
            transit_ip_id=["tip-1"],
            transit_ip_address=["172.20.1.10"],
            enterprise_project_id=["ep-1"],
        )
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))
