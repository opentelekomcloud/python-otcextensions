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
from osc_lib.command import command

from otcextensions.i18n import _


LOG = logging.getLogger(__name__)


class ListPrivateNatGateways(command.Lister):

    _description = _("List Private NAT Gateways.")
    columns = (
        'Id',
        'Name',
        'Spec',
        'Status',
        'Project Id',
        'Enterprise Project Id',
    )

    def get_parser(self, prog_name):
        parser = super(ListPrivateNatGateways, self).get_parser(prog_name)

        parser.add_argument(
            '--limit',
            metavar='<limit>',
            type=int,
            help=_("Specifies the number of records displayed on each page."),
        )
        parser.add_argument(
            '--marker',
            metavar='<marker>',
            help=_("Specifies the start resource ID of pagination query."),
        )
        parser.add_argument(
            '--page-reverse',
            action='store_true',
            default=False,
            help=_("Specifies whether to query resources"
                   " on the previous page."),
        )
        parser.add_argument(
            '--id',
            metavar='<id>',
            nargs='+',
            help=_("Specifies the private NAT gateway IDs."),
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            nargs='+',
            help=_("Specifies the private NAT gateway names."),
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            nargs='+',
            help=_("Provides supplementary information"
                   " about the private NAT gateway."),
        )
        parser.add_argument(
            '--spec',
            metavar='<spec>',
            nargs='+',
            help=_("Specifies the private NAT gateway specifications. "),
        )
        parser.add_argument(
            '--project-id',
            metavar='<project_id>',
            nargs='+',
            help=_("Specifies the project ID. Repeat for multiple values."),
        )
        parser.add_argument(
            '--status',
            metavar='<status>',
            nargs='+',
            help=_("Specifies the private NAT gateway status."),
        )
        parser.add_argument(
            '--vpc-id',
            metavar='<vpc_id>',
            nargs='+',
            help=_("Specifies the ID of the VPC."),
        )
        parser.add_argument(
            '--virsubnet-id',
            metavar='<virsubnet_id>',
            nargs='+',
            help=_("Specifies the ID of the subnet."),
        )
        parser.add_argument(
            '--enterprise-project-id',
            metavar='<enterprise_project_id>',
            nargs='+',
            help=_("Specifies the enterprise project ID "
                   "associated with the private NAT gateway."),
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.nat

        attrs = {}
        args_list = [
            'limit',
            'marker',
            'page_reverse',
            'id',
            'name',
            'description',
            'spec',
            'project_id',
            'status',
            'vpc_id',
            'virsubnet_id',
            'enterprise_project_id',
        ]
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val is not None and val != [] and val != '':
                attrs[arg] = val

        data = client.private_nat_gateways(**attrs)

        return (
            self.columns,
            (
                utils.get_item_properties(s, self.columns)
                for s in data
            )
        )
