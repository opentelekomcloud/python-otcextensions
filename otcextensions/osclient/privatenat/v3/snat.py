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
"""Private SNAT v3 action implementations"""

import logging

from osc_lib import exceptions
from osc_lib import utils
from osc_lib.command import command

from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _get_columns(item):
    column_map = {}
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


def _get_transit_ip_addresses(rule):
    return ", ".join(
        association.transit_ip_address
        for association in (rule.transit_ip_associations or [])
        if getattr(association, "transit_ip_address", None)
    )


class ListPrivateSnatRules(command.Lister):

    _description = _("List private SNAT rules.")
    columns = (
        "id",
        "gateway_id",
        "virsubnet_id",
        "cidr",
        "transit_ip_addresses",
        "description",
        "status",
    )

    def get_parser(self, prog_name):
        parser = super(ListPrivateSnatRules, self).get_parser(prog_name)

        parser.add_argument(
            "--id",
            metavar="<id>",
            action="append",
            help=_("Specifies the SNAT rule ID. Repeat to filter by multiple values."),
        )
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
            help=_("Query resources on the previous page."),
        )
        parser.add_argument(
            "--project-id",
            metavar="<project_id>",
            action="append",
            help=_("Specifies the project ID. Repeat to filter by multiple values."),
        )
        parser.add_argument(
            "--description",
            metavar="<description>",
            action="append",
            help=_(
                "Provides supplementary information about the SNAT rule. "
                "Repeat to filter by multiple values."
            ),
        )
        parser.add_argument(
            "--gateway-id",
            metavar="<gateway_id>",
            action="append",
            help=_(
                "Specifies the private NAT gateway ID. "
                "Repeat to filter by multiple values."
            ),
        )
        parser.add_argument(
            "--cidr",
            metavar="<cidr>",
            action="append",
            help=_(
                "Specifies the CIDR block that matches the SNAT rule. "
                "Repeat to filter by multiple values."
            ),
        )
        parser.add_argument(
            "--virsubnet-id",
            metavar="<virsubnet_id>",
            action="append",
            help=_(
                "Specifies the subnet ID that matches the SNAT rule. "
                "Repeat to filter by multiple values."
            ),
        )
        parser.add_argument(
            "--transit-ip-id",
            metavar="<transit_ip_id>",
            action="append",
            help=_(
                "Specifies the transit IP address ID. "
                "Repeat to filter by multiple values."
            ),
        )
        parser.add_argument(
            "--transit-ip-address",
            metavar="<transit_ip_address>",
            action="append",
            help=_(
                "Specifies the transit IP address. "
                "Repeat to filter by multiple values."
            ),
        )
        parser.add_argument(
            "--enterprise-project-id",
            metavar="<enterprise_project_id>",
            action="append",
            help=_(
                "Specifies the enterprise project ID. "
                "Repeat to filter by multiple values."
            ),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.privatenat

        args_list = [
            "id",
            "limit",
            "marker",
            "page_reverse",
            "project_id",
            "description",
            "gateway_id",
            "cidr",
            "virsubnet_id",
            "transit_ip_id",
            "transit_ip_address",
            "enterprise_project_id",
        ]

        attrs = {}
        for arg in args_list:
            val = getattr(parsed_args, arg, None)

            if val is None:
                continue
            if isinstance(val, list) and not val:
                continue
            if isinstance(val, bool) and not val:
                continue

            attrs[arg] = val

        data = client.private_snat_rules(**attrs)

        return (
            self.columns,
            (
                utils.get_dict_properties(
                    {
                        "id": s.id,
                        "gateway_id": s.gateway_id,
                        "virsubnet_id": s.virsubnet_id,
                        "cidr": s.cidr,
                        "transit_ip_addresses": _get_transit_ip_addresses(s),
                        "description": s.description,
                        "status": s.status,
                    },
                    self.columns,
                )
                for s in data
            ),
        )


class CreatePrivateSnatRule(command.ShowOne):

    _description = _("Create a private SNAT rule.")

    def get_parser(self, prog_name):
        parser = super(CreatePrivateSnatRule, self).get_parser(prog_name)

        parser.add_argument(
            "--gateway-id",
            metavar="<gateway_id>",
            required=True,
            help=_("Specifies the private NAT gateway ID."),
        )
        parser.add_argument(
            "--cidr",
            metavar="<cidr>",
            help=_("Specifies the CIDR block that matches the SNAT rule."),
        )
        parser.add_argument(
            "--virsubnet-id",
            metavar="<virsubnet_id>",
            help=_("Specifies the ID of the subnet that matches the SNAT rule."),
        )
        parser.add_argument(
            "--description",
            metavar="<description>",
            help=_("Provides supplementary information about the SNAT rule."),
        )
        parser.add_argument(
            "--transit-ip-id",
            metavar="<transit_ip_id>",
            action="append",
            dest="transit_ip_ids",
            required=True,
            help=_(
                "Specifies the transit IP address ID. "
                "Repeat to associate multiple transit IPs."
            ),
        )
        return parser

    def _build_attrs(self, parsed_args):
        attrs = {
            "gateway_id": parsed_args.gateway_id,
            "transit_ip_ids": parsed_args.transit_ip_ids,
        }

        if len(parsed_args.transit_ip_ids) > 20:
            raise exceptions.CommandError(
                _("A maximum number of 20 --transit-ip-id values is allowed.")
            )

        if parsed_args.cidr and parsed_args.virsubnet_id:
            raise exceptions.CommandError(
                _("Specify either --cidr or --virsubnet-id, but not both.")
            )

        if not parsed_args.cidr and not parsed_args.virsubnet_id:
            raise exceptions.CommandError(
                _("One of --cidr or --virsubnet-id must be specified.")
            )

        if parsed_args.cidr:
            attrs["cidr"] = parsed_args.cidr
        if parsed_args.virsubnet_id:
            attrs["virsubnet_id"] = parsed_args.virsubnet_id
        if parsed_args.description is not None:
            attrs["description"] = parsed_args.description

        return attrs

    def take_action(self, parsed_args):
        client = self.app.client_manager.privatenat
        attrs = self._build_attrs(parsed_args)
        obj = client.create_private_snat_rule(**attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)
        return display_columns, data
