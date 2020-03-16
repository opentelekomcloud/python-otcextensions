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
"""NAT Gateway v2 action implementations"""
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.i18n import _
from otcextensions.common import sdk_utils

LOG = logging.getLogger(__name__)


def _get_columns(item):
    column_map = {
    }
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


class ListNatGateways(command.Lister):

    _description = _("List Nat Gateway.")
    columns = ('Id', 'Name', 'Spec', 'Router Id', 'Status')

    def get_parser(self, prog_name):
        parser = super(ListNatGateways, self).get_parser(prog_name)

        parser.add_argument(
            '--id',
            metavar='<id>',
            help=_('Specifies the ID of the NAT Gateway.'))
        parser.add_argument(
            '--limit',
            metavar='<limit>',
            type=int,
            help=_('Limit to fetch number of records.'))
        parser.add_argument(
            '--project-id',
            metavar='<project_id>',
            help=_('Specifies the project ID.'))
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_('Specifies the Name of the NAT Gateway.'))
        parser.add_argument(
            '--spec',
            metavar='<spec>',
            help=_('Specifies the type of the NAT Gateway.'))
        parser.add_argument(
            '--router-id',
            metavar='<router_id>',
            help=_('Specifies the router ID.'))
        parser.add_argument(
            '--internal-network-id',
            metavar='<internal_network_id>',
            help=_('Specifies the network ID.'))
        parser.add_argument(
            '--status',
            metavar='<status>',
            help=_('Specifies the status of the NAT Gateway.'))
        parser.add_argument(
            '--admin-state-up',
            metavar='<admin_state_up>',
            help=_('Specifies whether the NAT Gateway is enabled '
                   'or disabled.'))
        parser.add_argument(
            '--created-at',
            metavar='<created_at>',
            help=_('Specifies when the NAT Gateway is created (UTC time). '
                   'Its valuerounds to 6 decimal places forseconds. '
                   'The format is yyyy-mm-ddhh:mm:ss.'))

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.nat
        args_list = [
            'id',
            'limit',
            'project_id',
            'name',
            'spec',
            'router_id',
            'internal_network_id',
            'status',
            'admin_state_up',
            'created_at']
        attrs = {}
        for arg in args_list:
            if getattr(parsed_args, arg):
                attrs[arg] = getattr(parsed_args, arg)

        data = client.gateways(**attrs)

        return (self.columns, (utils.get_item_properties(s, self.columns)
                               for s in data))


class ShowNatGateway(command.ShowOne):
    _description = _("Show NAT Gateway details")

    def get_parser(self, prog_name):
        parser = super(ShowNatGateway, self).get_parser(prog_name)
        parser.add_argument(
            'nat_gateway',
            metavar='<nat_gateway>',
            help=_('Specifies the ID of the NAT Gateway.'),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.nat
        obj = client.find_gateway(parsed_args.nat_gateway)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class CreateNatGateway(command.ShowOne):
    _description = _("Create new NAT Gateway")

    def get_parser(self, prog_name):
        parser = super(CreateNatGateway, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar="<name>",
            help=_("Specifies the name of the NAT Gateway."))
        parser.add_argument(
            '--description',
            metavar="<description>",
            help=_("Provides supplementary informationabout the NAT gateway."))
        parser.add_argument(
            '--spec',
            metavar="<spec>",
            required=True,
            help=_(
                "Specifies the type of the NAT gateway."
                "\n1: small type, which supports up to 10,000 "
                "SNAT connections.\n2: medium type, which supports "
                "up to 50,000 SNAT connections.\n3: large type, which "
                "supports up to 200,000 SNAT connections.\n4: extra-large "
                "type, which supports up to 1,000,000 SNAT connections."))
        parser.add_argument(
            '--router-id',
            metavar="<router_id>",
            required=True,
            help=_("Specifies the VPC ID"))
        parser.add_argument(
            '--internal-network-id',
            metavar="<internal_network_id>",
            required=True,
            help=_("Specifies the network ID of thedownstream interface "
                   "(the next hop ofthe DVR) of the NAT gateway."))

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.nat

        args_list = [
            'name',
            'description',
            'spec',
            'router_id',
            'internal_network_id']
        attrs = {}
        for arg in args_list:
            if getattr(parsed_args, arg):
                attrs[arg] = getattr(parsed_args, arg)

        obj = client.create_gateway(**attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class UpdateNatGateway(command.ShowOne):
    _description = _("Update a NAT Gateway.")

    def get_parser(self, prog_name):
        parser = super(UpdateNatGateway, self).get_parser(prog_name)
        parser.add_argument(
            'nat_gateway',
            metavar='<nat_gateway>',
            help=_('Specifies the Name or ID of the NAT Gateway.'),
        )
        parser.add_argument(
            '--name',
            metavar="<name>",
            help=_("Specifies the name of the NAT Gateway."))
        parser.add_argument(
            '--description',
            metavar="<description>",
            help=_("Provides supplementary informationabout the NAT gateway."))
        parser.add_argument(
            '--spec',
            metavar="<spec>",
            help=_("Specifies the type of the NAT gateway."))
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.nat
        args_list = [
            'name', 'description', 'spec'
        ]
        attrs = {}
        for arg in args_list:
            if getattr(parsed_args, arg):
                attrs[arg] = getattr(parsed_args, arg)
        nat_gateway = client.find_gateway(parsed_args.nat_gateway)

        obj = client.update_gateway(nat_gateway.id, **attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class DeleteNatGateway(command.Command):

    _description = _("Deletes NAT Gateway.")

    def get_parser(self, prog_name):
        parser = super(DeleteNatGateway, self).get_parser(prog_name)
        parser.add_argument(
            'nat_gateway',
            metavar='<nat_gateway>',
            help=_('Specifies the Name or ID of the NAT gateway.'),
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.nat
        nat_gateway = client.find_gateway(parsed_args.nat_gateway)
        client.delete_gateway(nat_gateway.id)
