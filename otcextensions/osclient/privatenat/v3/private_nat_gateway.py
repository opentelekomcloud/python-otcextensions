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
"""Private NAT Gateway v3 action implementations"""

import logging

from osc_lib import utils
from osc_lib.cli import parseractions
from osc_lib.command import command

from otcextensions.common import sdk_utils
from otcextensions.common.utils import normalize_tags
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _get_columns(item):
    column_map = {}
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


def _flatten_private_nat_gateway(obj):
    return {
        "id": obj.id,
        "name": obj.name,
        "description": obj.description,
        "spec": obj.spec,
        "project_id": obj.project_id,
        "enterprise_project_id": obj.enterprise_project_id,
        "status": obj.status,
        "created_at": obj.created_at,
        "updated_at": obj.updated_at,
        "rule_max": obj.rule_max,
        "transit_ip_pool_size_max": obj.transit_ip_pool_size_max,
    }


def _add_downlink_vpcs_to_obj(obj, data, columns):
    for index, downlink_vpc in enumerate(obj.downlink_vpcs or [], start=1):
        data += (downlink_vpc.get("vpc_id", ""),)
        columns += ("downlink_vpc_id_%s" % index,)

        data += (downlink_vpc.get("virsubnet_id", ""),)
        columns += ("downlink_virsubnet_id_%s" % index,)

        data += (downlink_vpc.get("ngport_ip_address", ""),)
        columns += ("downlink_ngport_ip_address_%s" % index,)

    return data, columns


def _add_tags_to_obj(obj, data, columns):
    data += (
        "\n".join(
            "key=%s, value=%s"
            % (
                tag.get("key", ""),
                tag.get("value", ""),
            )
            for tag in obj.tags
        ),
    )
    columns += ("tags",)
    return data, columns


class ListPrivateNatGateways(command.Lister):

    _description = _("List Private NAT Gateways.")
    columns = (
        "Id",
        "Name",
        "Spec",
        "Status",
        "Project Id",
        "Enterprise Project Id",
    )

    def get_parser(self, prog_name):
        parser = super(ListPrivateNatGateways, self).get_parser(prog_name)

        parser.add_argument(
            "--limit",
            metavar="<limit>",
            type=int,
            help=_("Specifies the number of records displayed on each page."),
        )
        parser.add_argument(
            "--marker",
            metavar="<marker>",
            help=_("Specifies the start resource ID of pagination query."),
        )
        parser.add_argument(
            "--page-reverse",
            action="store_true",
            default=False,
            help=_("Specifies whether to query resources" " on the previous page."),
        )
        parser.add_argument(
            "--id",
            metavar="<id>",
            nargs="+",
            help=_("Specifies the private NAT gateway IDs."),
        )
        parser.add_argument(
            "--name",
            metavar="<name>",
            nargs="+",
            help=_("Specifies the private NAT gateway names."),
        )
        parser.add_argument(
            "--description",
            metavar="<description>",
            nargs="+",
            help=_(
                "Provides supplementary information" " about the private NAT gateway."
            ),
        )
        parser.add_argument(
            "--spec",
            metavar="<spec>",
            nargs="+",
            help=_("Specifies the private NAT gateway specifications. "),
        )
        parser.add_argument(
            "--project-id",
            metavar="<project_id>",
            nargs="+",
            help=_("Specifies the project ID. Repeat for multiple values."),
        )
        parser.add_argument(
            "--status",
            metavar="<status>",
            nargs="+",
            help=_("Specifies the private NAT gateway status."),
        )
        parser.add_argument(
            "--vpc-id",
            metavar="<vpc_id>",
            nargs="+",
            help=_("Specifies the ID of the VPC."),
        )
        parser.add_argument(
            "--virsubnet-id",
            metavar="<virsubnet_id>",
            nargs="+",
            help=_("Specifies the ID of the subnet."),
        )
        parser.add_argument(
            "--enterprise-project-id",
            metavar="<enterprise_project_id>",
            nargs="+",
            help=_(
                "Specifies the enterprise project ID "
                "associated with the private NAT gateway."
            ),
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.privatenat

        attrs = {}
        args_list = [
            "limit",
            "marker",
            "page_reverse",
            "id",
            "name",
            "description",
            "spec",
            "project_id",
            "status",
            "vpc_id",
            "virsubnet_id",
            "enterprise_project_id",
        ]
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if arg == "page_reverse":
                # Only send flag if explicitly requested
                if val:
                    attrs[arg] = val
            elif val is not None and val != [] and val != "":
                attrs[arg] = val

        data = client.private_nat_gateways(**attrs)

        return (
            self.columns,
            (utils.get_item_properties(s, self.columns) for s in data),
        )


class ShowPrivateNatGateway(command.ShowOne):
    _description = _("Show Private NAT Gateway details")

    def get_parser(self, prog_name):
        parser = super(ShowPrivateNatGateway, self).get_parser(prog_name)
        parser.add_argument(
            "gateway",
            metavar="<gateway>",
            help=_("Specifies the private NAT gateway ID."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.privatenat
        obj = client.get_private_nat_gateway(parsed_args.gateway)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return display_columns, data


class CreatePrivateNatGateway(command.ShowOne):
    _description = _("Create new Private NAT Gateway")
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

    def get_parser(self, prog_name):
        parser = super(CreatePrivateNatGateway, self).get_parser(prog_name)
        parser.add_argument(
            "--name",
            metavar="<name>",
            required=True,
            help=_("Specifies the name of the Private NAT Gateway."),
        )
        parser.add_argument(
            "--description",
            metavar="<description>",
            help=_(
                "Provides supplementary information about " "the Private NAT Gateway."
            ),
        )
        parser.add_argument(
            "--spec",
            metavar="<spec>",
            default="Small",
            help=_(
                "Specifies the type of the Private NAT Gateway. "
                "The value can be:\n"
                "1: small type, which supports up to 10,000 "
                "SNAT connections.\n"
                "2: medium type, which supports up to 50,000 "
                "SNAT connections.\n"
                "3: large type, which supports up to 200,000 "
                "SNAT connections.\n"
                "4: extra-large type, which supports up to "
                "1,000,000 SNAT connections."
            ),
        )
        parser.add_argument(
            "--enterprise-project-id",
            metavar="<enterprise_project_id>",
            default=0,
            help=_(
                "Specifies the ID of the enterprise project"
                " that is associated with the private NAT gateway"
                " when the private NAT gateway is created."
            ),
        )
        parser.add_argument(
            "--downlink-vpc",
            metavar="<virsubnet_id=virsubnet_id[,ngport_ip_address=ip]>",
            action=parseractions.MultiKeyValueAction,
            dest="downlink_vpcs",
            required_keys=["virsubnet_id"],
            optional_keys=["ngport_ip_address"],
            help=_("Specifies the VPC where the private NAT gateway works."),
        )
        parser.add_argument(
            "--tags",
            metavar="<tags>",
            action="append",
            help=_(
                "Specifies the tag list in KEY=VALUE format."
                "Repeat for multiple values."
            ),
        )

        return parser

    def _build_attrs(self, parsed_args):
        attrs = {
            "name": parsed_args.name,
            "downlink_vpcs": parsed_args.downlink_vpcs,
        }

        optional_attrs = (
            "description",
            "spec",
            "enterprise_project_id",
        )
        for key in optional_attrs:
            value = getattr(parsed_args, key, None)
            if value is not None:
                attrs[key] = value

        if parsed_args.tags:
            attrs["tags"] = normalize_tags(parsed_args.tags)

        return attrs

    def take_action(self, parsed_args):
        client = self.app.client_manager.privatenat

        attrs = self._build_attrs(parsed_args)
        obj = client.create_private_nat_gateway(**attrs)

        columns = self.columns
        data = utils.get_dict_properties(
            _flatten_private_nat_gateway(obj),
            columns,
        )

        if obj.downlink_vpcs:
            data, columns = _add_downlink_vpcs_to_obj(obj, data, columns)
        if obj.tags:
            data, columns = _add_tags_to_obj(obj, data, columns)

        return columns, data
