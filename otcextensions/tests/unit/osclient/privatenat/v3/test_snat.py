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

from osc_lib import exceptions

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


class TestShowPrivateSnatRule(fakes.TestPrivateNat):
    _data = fakes.FakePrivateSnatRule.create_one()

    columns = (
        "cidr",
        "created_at",
        "description",
        "enterprise_project_id",
        "gateway_id",
        "id",
        "project_id",
        "status",
        "transit_ip_associations",
        "updated_at",
        "virsubnet_id",
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestShowPrivateSnatRule, self).setUp()

        self.cmd = snat.ShowPrivateSnatRule(self.app, None)
        self.client.get_private_snat_rule = mock.Mock(return_value=self._data)

    def test_show(self):
        arglist = [self._data.id]
        verifylist = [("snat_rule", self._data.id)]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        self.client.get_private_snat_rule.assert_called_once_with(self._data.id)
        self.assertEqual(tuple(sorted(self.columns)), tuple(sorted(columns)))
        self.assertEqual(len(self.data), len(data))
        self.assertIn(self._data.id, data)


class TestCreatePrivateSnatRule(fakes.TestPrivateNat):
    _data = fakes.FakePrivateSnatRule.create_one()

    def setUp(self):
        super(TestCreatePrivateSnatRule, self).setUp()
        self.cmd = snat.CreatePrivateSnatRule(self.app, None)
        self.client.create_private_snat_rule = mock.Mock(return_value=self._data)

    def test_create_with_virsubnet(self):
        arglist = [
            "--gateway-id",
            self._data.gateway_id,
            "--virsubnet-id",
            self._data.virsubnet_id,
            "--transit-ip-id",
            "tip-1",
            "--transit-ip-id",
            "tip-2",
            "--description",
            self._data.description,
        ]
        verifylist = [
            ("gateway_id", self._data.gateway_id),
            ("virsubnet_id", self._data.virsubnet_id),
            ("transit_ip_ids", ["tip-1", "tip-2"]),
            ("description", self._data.description),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_private_snat_rule.assert_called_once_with(
            gateway_id=self._data.gateway_id,
            virsubnet_id=self._data.virsubnet_id,
            transit_ip_ids=["tip-1", "tip-2"],
            description=self._data.description,
        )
        self.assertEqual(len(columns), len(data))
        self.assertIn("id", columns)

    def test_create_with_cidr(self):
        arglist = [
            "--gateway-id",
            self._data.gateway_id,
            "--cidr",
            "10.1.1.64/30",
            "--transit-ip-id",
            "tip-1",
        ]
        verifylist = [
            ("gateway_id", self._data.gateway_id),
            ("cidr", "10.1.1.64/30"),
            ("transit_ip_ids", ["tip-1"]),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)

        self.client.create_private_snat_rule.assert_called_once_with(
            gateway_id=self._data.gateway_id,
            cidr="10.1.1.64/30",
            transit_ip_ids=["tip-1"],
        )

    def test_create_requires_cidr_or_virsubnet(self):
        arglist = [
            "--gateway-id",
            self._data.gateway_id,
            "--transit-ip-id",
            "tip-1",
        ]
        verifylist = [
            ("gateway_id", self._data.gateway_id),
            ("transit_ip_ids", ["tip-1"]),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        with self.assertRaises(exceptions.CommandError):
            self.cmd.take_action(parsed_args)

    def test_create_both_cidr_and_virsubnet(self):
        arglist = [
            "--gateway-id",
            self._data.gateway_id,
            "--cidr",
            "10.1.1.64/30",
            "--virsubnet-id",
            self._data.virsubnet_id,
            "--transit-ip-id",
            "tip-1",
        ]
        verifylist = [
            ("gateway_id", self._data.gateway_id),
            ("cidr", "10.1.1.64/30"),
            ("virsubnet_id", self._data.virsubnet_id),
            ("transit_ip_ids", ["tip-1"]),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        with self.assertRaises(exceptions.CommandError):
            self.cmd.take_action(parsed_args)

    def test_create_more_than_20_transit_ip_ids(self):
        arglist = [
            "--gateway-id",
            self._data.gateway_id,
            "--virsubnet-id",
            self._data.virsubnet_id,
        ]
        verifylist = [
            ("gateway_id", self._data.gateway_id),
            ("virsubnet_id", self._data.virsubnet_id),
        ]

        for i in range(21):
            arglist.extend(["--transit-ip-id", "tip-%s" % i])

        verifylist.append(("transit_ip_ids", ["tip-%s" % i for i in range(21)]))

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        with self.assertRaises(exceptions.CommandError):
            self.cmd.take_action(parsed_args)


class TestUpdatePrivateSnatRule(fakes.TestPrivateNat):
    _data = fakes.FakePrivateSnatRule.create_one()

    def setUp(self):
        super(TestUpdatePrivateSnatRule, self).setUp()
        self.cmd = snat.UpdatePrivateSnatRule(self.app, None)
        self.client.update_private_snat_rule = mock.Mock(return_value=self._data)

    def test_update(self):
        arglist = [
            self._data.id,
            "--description",
            "updated-description",
            "--transit-ip-id",
            "tip-1",
            "--transit-ip-id",
            "tip-2",
        ]
        verifylist = [
            ("snat_rule", self._data.id),
            ("description", "updated-description"),
            ("transit_ip_ids", ["tip-1", "tip-2"]),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        self.client.update_private_snat_rule.assert_called_once_with(
            self._data.id,
            description="updated-description",
            transit_ip_ids=["tip-1", "tip-2"],
        )
        self.assertEqual(len(columns), len(data))
        self.assertIn("id", columns)


class TestDeletePrivateSnatRule(fakes.TestPrivateNat):

    def setUp(self):
        super(TestDeletePrivateSnatRule, self).setUp()
        self.cmd = snat.DeletePrivateSnatRule(self.app, None)
        self.rule = fakes.FakePrivateSnatRule.create_one()
        self.client.get_private_snat_rule = mock.Mock(return_value=self.rule)
        self.client.delete_private_snat_rule = mock.Mock()

    def test_delete(self):
        arglist = [self.rule.id]
        verifylist = [("snat_rule", self.rule.id)]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        result = self.cmd.take_action(parsed_args)

        self.client.get_private_snat_rule.assert_called_once_with(self.rule.id)
        self.client.delete_private_snat_rule.assert_called_once_with(self.rule.id)
        self.assertIsNone(result)
