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
"""Private DNAT v3 action implementations"""

import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


class ListPrivateDnatRules(command.Lister):

    _description = _("List private DNAT rules.")
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

    def get_parser(self, prog_name):
        parser = super(ListPrivateDnatRules, self).get_parser(prog_name)

        parser.add_argument(
            "--id",
            metavar="<id>",
            action="append",
            help=_("Specifies the DNAT rule ID. Repeat to filter by multiple values."),
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
                "Provides supplementary information about the DNAT rule. "
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
            "--transit-ip-id",
            metavar="<transit_ip_id>",
            action="append",
            help=_(
                "Specifies the transit IP address ID. "
                "Repeat to filter by multiple values."
            ),
        )
        parser.add_argument(
            "--external-ip-address",
            metavar="<external_ip_address>",
            action="append",
            help=_(
                "Specifies the transit IP address. "
                "Repeat to filter by multiple values."
            ),
        )
        parser.add_argument(
            "--network-interface-id",
            metavar="<network_interface_id>",
            action="append",
            help=_(
                "Specifies the port ID of the backend resource. "
                "Repeat to filter by multiple values."
            ),
        )
        parser.add_argument(
            "--type",
            metavar="<type>",
            action="append",
            choices=["COMPUTE", "VIP", "ELB", "ELBv3", "CUSTOMIZE"],
            help=_(
                "Specifies the backend resource type. "
                "Supported values: COMPUTE, VIP, ELB, ELBv3, CUSTOMIZE. "
                "Repeat to filter by multiple values."
            ),
        )
        parser.add_argument(
            "--private-ip-address",
            metavar="<private_ip_address>",
            action="append",
            help=_(
                "Specifies the port IP address that the NAT gateway uses. "
                "Repeat to filter by multiple values."
            ),
        )
        parser.add_argument(
            "--protocol",
            metavar="<protocol>",
            action="append",
            choices=["tcp", "udp", "any", "TCP", "UDP", "ANY"],
            help=_(
                "Specifies the protocol type. "
                "Supported values: tcp, udp, any. "
                "Repeat to filter by multiple values."
            ),
        )
        parser.add_argument(
            "--internal-service-port",
            metavar="<internal_service_port>",
            action="append",
            help=_(
                "Specifies the port number of the backend resource. "
                "Repeat to filter by multiple values."
            ),
        )
        parser.add_argument(
            "--transit-service-port",
            metavar="<transit_service_port>",
            action="append",
            help=_(
                "Specifies the port number of the transit IP address. "
                "Repeat to filter by multiple values."
            ),
        )
        parser.add_argument(
            "--created-at",
            metavar="<created_at>",
            help=_(
                "Specifies the time when the DNAT rule was created. "
                "UTC time in yyyy-mm-ddThh:mm:ssZ format."
            ),
        )
        parser.add_argument(
            "--updated-at",
            metavar="<updated_at>",
            help=_(
                "Specifies the time when the DNAT rule was updated. "
                "UTC time in yyyy-mm-ddThh:mm:ssZ format."
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
            "enterprise_project_id",
            "description",
            "gateway_id",
            "transit_ip_id",
            "external_ip_address",
            "network_interface_id",
            "type",
            "private_ip_address",
            "protocol",
            "internal_service_port",
            "transit_service_port",
            "created_at",
            "updated_at",
        ]

        attrs = {}
        for arg in args_list:
            val = getattr(parsed_args, arg, None)

            if val is None:  # skip missing args
                continue
            if isinstance(val, list) and not val:  # skip empty lists
                continue
            if isinstance(val, bool) and not val:  # skip false bool values
                continue

            if arg == "protocol" and isinstance(val, list):
                attrs[arg] = [p.lower() for p in val]
            else:
                attrs[arg] = val

        data = client.private_dnat_rules(**attrs)

        return (
            self.columns,
            (
                utils.get_item_properties(
                    s,
                    self.columns,
                )
                for s in data
            ),
        )
