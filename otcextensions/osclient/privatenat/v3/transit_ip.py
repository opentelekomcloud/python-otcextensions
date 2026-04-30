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
"""Private transit IP v3 action implementations"""

import logging

from osc_lib import exceptions
from osc_lib import utils
from osc_lib.command import command

from otcextensions.common import sdk_utils
from otcextensions.common.utils import normalize_tags
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _get_columns(item):
    column_map = {}
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


class ListPrivateTransitIps(command.Lister):

    _description = _("List private transit IP addresses.")
    columns = (
        "id",
        "ip_address",
        "gateway_id",
        "network_interface_id",
        "virsubnet_id",
        "status",
    )

    def get_parser(self, prog_name):
        parser = super(ListPrivateTransitIps, self).get_parser(prog_name)

        parser.add_argument(
            "--id",
            metavar="<id>",
            action="append",
            help=_(
                "Specifies the transit IP address ID. "
                "Repeat to filter by multiple values."
            ),
        )
        parser.add_argument(
            "--project-id",
            metavar="<project_id>",
            action="append",
            help=_("Specifies the project ID. Repeat to filter by multiple values."),
        )
        parser.add_argument(
            "--network-interface-id",
            metavar="<network_interface_id>",
            action="append",
            help=_(
                "Specifies the network interface ID of the transit IP address. "
                "Repeat to filter by multiple values."
            ),
        )
        parser.add_argument(
            "--ip-address",
            metavar="<ip_address>",
            action="append",
            help=_(
                "Specifies the transit IP address. "
                "Repeat to filter by multiple values."
            ),
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
            "--virsubnet-id",
            metavar="<virsubnet_id>",
            action="append",
            help=_(
                "Specifies the subnet ID of the current VPC. "
                "Repeat to filter by multiple values."
            ),
        )
        parser.add_argument(
            "--transit-subnet-id",
            metavar="<transit_subnet_id>",
            action="append",
            help=_(
                "Specifies the subnet ID of the transit VPC. "
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
            "--enterprise-project-id",
            metavar="<enterprise_project_id>",
            action="append",
            help=_(
                "Specifies the enterprise project ID. "
                "Repeat to filter by multiple values."
            ),
        )
        parser.add_argument(
            "--description",
            metavar="<description>",
            action="append",
            help=_(
                "Provides supplementary information about the transit IP address. "
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
            "network_interface_id",
            "ip_address",
            "virsubnet_id",
            "transit_subnet_id",
            "gateway_id",
            "enterprise_project_id",
            "description",
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

        data = client.private_transit_ips(**attrs)

        return (
            self.columns,
            (
                utils.get_item_properties(
                    t,
                    self.columns,
                )
                for t in data
            ),
        )


class ShowPrivateTransitIp(command.ShowOne):
    _description = _("Show private transit IP address details.")

    def get_parser(self, prog_name):
        parser = super(ShowPrivateTransitIp, self).get_parser(prog_name)
        parser.add_argument(
            "transit_ip",
            metavar="<transit_ip>",
            help=_("Specifies the transit IP address ID."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.privatenat
        obj = client.get_private_transit_ip(parsed_args.transit_ip)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return display_columns, data


class CreatePrivateTransitIp(command.ShowOne):
    _description = _("Assign a private transit IP address.")

    def get_parser(self, prog_name):
        parser = super(CreatePrivateTransitIp, self).get_parser(prog_name)
        parser.add_argument(
            "--virsubnet-id",
            metavar="<virsubnet_id>",
            required=True,
            help=_("Specifies the subnet ID of the current project."),
        )
        parser.add_argument(
            "--ip-address",
            metavar="<ip_address>",
            help=_("Specifies the transit IP address."),
        )
        parser.add_argument(
            "--enterprise-project-id",
            metavar="<enterprise_project_id>",
            help=_(
                "Specifies the enterprise project ID associated with the "
                "transit IP address."
            ),
        )
        parser.add_argument(
            "--tags",
            metavar="<tags>",
            action="append",
            help=_(
                "Specifies the tag list in KEY=VALUE format. "
                "Repeat for multiple values."
            ),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.privatenat

        attrs = {
            "virsubnet_id": parsed_args.virsubnet_id,
        }

        if parsed_args.ip_address:
            attrs["ip_address"] = parsed_args.ip_address
        if parsed_args.enterprise_project_id:
            attrs["enterprise_project_id"] = parsed_args.enterprise_project_id
        if parsed_args.tags:
            attrs["tags"] = normalize_tags(parsed_args.tags)

        obj = client.create_private_transit_ip(**attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return display_columns, data


class DeletePrivateTransitIp(command.Command):
    _description = _("Delete a private transit IP address.")

    def get_parser(self, prog_name):
        parser = super(DeletePrivateTransitIp, self).get_parser(prog_name)
        parser.add_argument(
            "transit_ip",
            metavar="<transit_ip>",
            help=_("Specifies the transit IP address ID."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.privatenat

        try:
            client.delete_private_transit_ip(parsed_args.transit_ip)
        except Exception as e:
            msg = _(
                "Failed to delete private transit IP address with ID '%(id)s': %(e)s"
            ) % {"id": parsed_args.transit_ip, "e": e}
            raise exceptions.CommandError(msg)
