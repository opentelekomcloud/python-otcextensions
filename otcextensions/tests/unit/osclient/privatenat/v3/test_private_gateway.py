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
from openstackclient.tests.unit import utils as tests_utils
from osc_lib import exceptions

from otcextensions.osclient.privatenat.v3 import private_nat_gateway
from otcextensions.tests.unit.osclient.privatenat.v3 import fakes


class TestListPrivateNatGateways(fakes.TestPrivateNat):

    objects = fakes.FakePrivateNatGateway.create_multiple(3)

    column_list_headers = (
        "Id",
        "Name",
        "Spec",
        "Status",
        "Project Id",
        "Enterprise Project Id",
    )

    columns = (
        "id",
        "name",
        "spec",
        "status",
        "project_id",
        "enterprise_project_id",
    )

    data = []

    for s in objects:
        data.append(
            (
                s.id,
                s.name,
                s.spec,
                s.status,
                s.project_id,
                s.enterprise_project_id,
            )
        )

    def setUp(self):
        super(TestListPrivateNatGateways, self).setUp()

        self.cmd = private_nat_gateway.ListPrivateNatGateways(self.app, None)

        self.client.private_nat_gateways = mock.Mock()
        self.client.api_mock = self.client.private_nat_gateways

    def test_list(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.client.api_mock.side_effect = [self.objects]

        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with()

        self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(self.data, list(data))

    def test_list_args(self):
        arglist = [
            "--limit",
            "1",
            "--marker",
            "m1",
            "--page-reverse",
            "--id",
            "id1",
            "id2",
            "--name",
            "n1",
            "--description",
            "d1",
            "--spec",
            "Small",
            "--project-id",
            "p1",
            "--status",
            "ACTIVE",
            "--vpc-id",
            "v1",
            "--virsubnet-id",
            "s1",
            "--enterprise-project-id",
            "ep1",
        ]

        verifylist = [
            ("limit", 1),
            ("marker", "m1"),
            ("page_reverse", True),
            ("id", ["id1", "id2"]),
            ("name", ["n1"]),
            ("description", ["d1"]),
            ("spec", ["Small"]),
            ("project_id", ["p1"]),
            ("status", ["ACTIVE"]),
            ("vpc_id", ["v1"]),
            ("virsubnet_id", ["s1"]),
            ("enterprise_project_id", ["ep1"]),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.client.api_mock.side_effect = [self.objects]

        self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(
            limit=1,
            marker="m1",
            page_reverse=True,
            id=["id1", "id2"],
            name=["n1"],
            description=["d1"],
            spec=["Small"],
            project_id=["p1"],
            status=["ACTIVE"],
            vpc_id=["v1"],
            virsubnet_id=["s1"],
            enterprise_project_id=["ep1"],
        )


class TestGetPrivateNatGateway(fakes.TestPrivateNat):

    _data = fakes.FakePrivateNatGateway.create_one()

    columns = (
        "id",
        "name",
        "spec",
        "status",
        "project_id",
        "enterprise_project_id",
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestGetPrivateNatGateway, self).setUp()

        self.cmd = private_nat_gateway.ShowPrivateNatGateway(self.app, None)

        self.client.get_private_nat_gateway = mock.Mock(return_value=self._data)

    def test_get_no_options(self):
        arglist = []
        verifylist = []

        # Testing that a call without the required argument will fail and
        # throw a "ParserExecption"
        self.assertRaises(
            tests_utils.ParserException,
            self.check_parser,
            self.cmd,
            arglist,
            verifylist,
        )

    def test_get(self):
        arglist = [
            self._data.id,
        ]

        verifylist = [
            ("gateway", self._data.id),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.get_private_nat_gateway.assert_called_with(self._data.id)

        self.assertEqual(tuple(sorted(self.columns)), tuple(sorted(columns)))
        self.assertEqual(tuple(sorted(self.data)), tuple(sorted(data)))

    def test_get_non_existing(self):
        arglist = ["unexist_nat_gateway"]
        verifylist = [("gateway", "unexist_nat_gateway")]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.client.get_private_nat_gateway.side_effect = exceptions.CommandError(
            "Resource Not Found"
        )

        with self.assertRaises(exceptions.CommandError):
            self.cmd.take_action(parsed_args)

        self.client.get_private_nat_gateway.assert_called_once_with(
            "unexist_nat_gateway"
        )


class TestCreatePrivateNatGateway(fakes.TestPrivateNat):

    object = fakes.FakePrivateNatGateway.create_one()

    columns = (
        "id",
        "name",
        "description",
        "spec",
        "project_id",
        "enterprise_project_id",
        "status",
        "created_at",
        "updated_at",
        "rule_max",
        "transit_ip_pool_size_max",
    )

    flat_data = private_nat_gateway._flatten_private_nat_gateway(object)

    data = (
        flat_data["id"],
        flat_data["name"],
        flat_data["description"],
        flat_data["spec"],
        flat_data["project_id"],
        flat_data["enterprise_project_id"],
        flat_data["status"],
        flat_data["created_at"],
        flat_data["updated_at"],
        flat_data["rule_max"],
        flat_data["transit_ip_pool_size_max"],
    )

    def setUp(self):
        super(TestCreatePrivateNatGateway, self).setUp()

        self.cmd = private_nat_gateway.CreatePrivateNatGateway(self.app, None)
        self.client.create_gateway = mock.Mock()
        self.client.create_gateway.side_effect = [self.object]

    def test_create(self):
        arglist = [
            "--name",
            "test-private-gateway",
            "--description",
            "test description",
            "--spec",
            "Small",
            "--enterprise-project-id",
            "test-eps-id",
            "--downlink-vpc",
            "virsubnet_id=test-subnet-id,ngport_ip_address=192.168.10.10",
            "--tags",
            "key1=value1",
        ]
        verifylist = [
            ("name", "test-private-gateway"),
            ("description", "test description"),
            ("spec", "Small"),
            ("enterprise_project_id", "test-eps-id"),
            (
                "downlink_vpcs",
                [
                    {
                        "virsubnet_id": "test-subnet-id",
                        "ngport_ip_address": "192.168.10.10",
                    }
                ],
            ),
            ("tags", ["key1=value1"]),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.client.create_private_nat_gateway.side_effect = [self.object]

        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_private_nat_gateway.assert_called_once_with(
            name="test-private-gateway",
            description="test description",
            spec="Small",
            enterprise_project_id="test-eps-id",
            downlink_vpcs=[
                {
                    "virsubnet_id": "test-subnet-id",
                    "ngport_ip_address": "192.168.10.10",
                }
            ],
            tags=[
                {
                    "key": "key1",
                    "value": "value1",
                }
            ],
        )

        self.data, self.columns = private_nat_gateway._add_downlink_vpcs_to_obj(
            self.object, self.data, self.columns
        )

        self.data, self.columns = private_nat_gateway._add_tags_to_obj(
            self.object, self.data, self.columns
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)
