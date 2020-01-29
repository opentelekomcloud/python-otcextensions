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

LOG = logging.getLogger(__name__)


class ListNatGateway(command.Lister):

    _description = _("List Nat Gateway.")
    columns = ('Id', 'Name', 'Spec', 'Router Id', 'Status')

    def get_parser(self, prog_name):
        parser = super(ListNatGateway, self).get_parser(prog_name)

        parser.add_argument(
            '--id',
            metavar='<id>',
            help=_('Specifies the ID of the NAT Gateway.'))
        parser.add_argument(
            '--limit',
            metavar='<limit>',
            help=_('Limit to fetch number of records.'))
        parser.add_argument(
            '--project-id',
            metavar='<tenant_id>',
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
            help=_('Specifies whether the NAT Gateway is enabled or disabled.'))
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
            'id', 'limit', 'tenant_id', 'name', 'description', 'spec', 'router_id', 'internal_network_id', 'status', 'admin_state_up', 'created_at'
        ]
        attrs = {}
        for arg in args_list:
            if getattr(parsed_args, arg):
                attrs[arg] = getattr(parsed_args, arg)

        data = client.gateways(**args)

        return (
            self.columns,
            (utils.get_item_properties(
                s,
                self.columns,
            ) for s in data)
        )


class ShowNatGateway(command.ShowOne):
    _description = _("Show NAT Gateway details")

    def get_parser(self, prog_name):
        parser = super(ShowNatGateway, self).get_parser(prog_name)
        parser.add_argument(
            'nat_gateway_id',
            metavar='<nat_gateway_id>',
            help=_('Specifies the ID of the NAT Gateway.'),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.nat
        obj = client.get_gateway(parsed_args.nat_gateway_id)

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
            help=_("Specifies the type of the NAT gateway."))
        parser.add_argument(
            '--router-id',
            metavar="<router_id>",
            help=_("Specifies the VPC ID"))
        parser.add_argument(
            '--internal-network-id',
            metavar="<internal_network_id>",
            help=_("Specifies the network ID of thedownstream interface "
                   "(the next hop ofthe DVR) of the NAT gateway."))

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.nat

        args_list = ['name', 'description', 'spec', 'router_id', 'internal_network_id']
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
        nat_gateway = client.get_gateway(parsed_args.nat_gateway)

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
        nat_gateway = client.get_gateway(parsed_args.nat_gateway)
        return client.delete_gateway(nat_gateway.id)
