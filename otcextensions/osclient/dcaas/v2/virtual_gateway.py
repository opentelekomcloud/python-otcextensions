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
"""Direct Connection Virtual Gateway v2 action implementations"""
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


class ListVirtualGateways(command.Lister):

    _description = _("List of Virtual Gateways.")
    columns = (
        'id',
        'name',
        'vpc id',
        'local ep group id',
        'type',
        'status'
    )

    def get_parser(self, prog_name):
        parser = super(ListVirtualGateways, self).get_parser(prog_name)
        parser.add_argument(
            '--id',
            metavar='<id>',
            help=_("Specifies the Virtual Gateway ID.")
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_("Specifies the Virtual Gateway name.")
        )
        parser.add_argument(
            '--vpc_id',
            metavar='<vpc_id>',
            help=_("Specifies the ID of the VPC to be accessed.")
        )
        parser.add_argument(
            '--local_ep_group_id',
            metavar='<local_ep_group_id>',
            help=_("Specifies the ID of the local endpoint group that "
                   "records CIDR blocks of the VPC subnets.")
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_("Provides supplementary information about the "
                   "Virtual Gateway.")
        )
        parser.add_argument(
            '--device_id',
            metavar='<device_id>',
            help=_("Specifies the ID of the physical device used by the "
                   "Virtual Gateway.")
        )
        parser.add_argument(
            '--redundant_device_id',
            metavar='<redundant_device_id>',
            help=_("Specifies the ID of the redundant physical device used "
                   "by the Virtual Gateway.")
        )
        parser.add_argument(
            '--type',
            metavar='<type>',
            help=_("Specifies the Virtual Gateway type. The value can be "
                   "default or double ipsec.")
        )
        parser.add_argument(
            '--bgp_asn',
            metavar='<bgp_asn>',
            type=int,
            help=_("Specifies the BGP ASN of the Virtual Gateway.")
        )
        parser.add_argument(
            '--ipsec_bandwidth',
            metavar='<ipsec_bandwidth>',
            type=int,
            help=_("Specifies the bandwidth provided for IPsec VPN in Mbit/s.")
        )
        parser.add_argument(
            '--status',
            metavar='<status>',
            help=_("Specifies the Virtual Gateway status. "
                   "The value can be ACTIVE, DOWN, BUILD, ERROR, "
                   "PENDING_CREATE, PENDING_UPDATE, or PENDING_DELETE.")
        )
        parser.add_argument(
            '--admin_state_up',
            metavar='<admin_state_up>',
            type=bool,
            help=_("Specifies the administrative status of the Virtual "
                   "Gateway. The value can be true or false.")
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dcaas

        args_list = [
            'id',
            'name',
            'vpc_id',
            'local_ep_group_id',
            'device_id',
            'redundant_device_id',
            'type',
            'bgp_asn',
            'ipsec_bandwidth',
            'status',
            'admin_state_up'
        ]

        attrs = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        data = client.virtual_gateways(**attrs)

        table = (self.columns, (utils.get_dict_properties(s, self.columns)
                                for s in data))
        return table


class ShowVirtualGateway(command.ShowOne):
    _description = _("Show Virtual Gateway details.")

    def get_parser(self, prog_name):
        parser = super(ShowVirtualGateway, self).get_parser(prog_name)
        parser.add_argument(
            'virtual_gateway',
            metavar='<virtual_gateway>',
            help=_("Specifies the Virtual Gateway ID or name.")
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dcaas
        obj = client.find_virtual_gateway(parsed_args.virtual_gateway)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class CreateVirtualGateway(command.ShowOne):
    _description = _("Create new Virtual Gateway.")

    def get_parser(self, prog_name):
        parser = super(CreateVirtualGateway, self).get_parser(prog_name)
        parser.add_argument(
            'vpc_id',
            metavar='<vpc_id>',
            help=_("Specifies the ID of the VPC to be accessed.")
        )
        parser.add_argument(
            'local_ep_group_id',
            metavar='<local_ep_group_id>',
            help=_("Specifies the ID of the local endpoint group that records "
                   "CIDR blocks of the VPC subnets.")
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_("Specifies the Virtual Gateway name.")
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_("Provides supplementary information about the "
                   "Virtual Gateway.")
        )
        parser.add_argument(
            '--device_id',
            metavar='<device_id>',
            help=_("Specifies the ID of the physical device used by the "
                   "Virtual Gateway.")
        )
        parser.add_argument(
            '--redundant_device_id',
            metavar='<redundant_device_id>',
            help=_("Specifies the ID of the redundant physical device used by "
                   "the Virtual Gateway.")
        )
        parser.add_argument(
            '--type',
            metavar='<type>',
            help=_("Specifies the Virtual Gateway type. "
                   "The value can be default or double ipsec.")
        )
        parser.add_argument(
            '--ipsec_bandwidth',
            metavar='<ipsec_bandwidth>',
            type=int,
            help=_("Specifies the bandwidth provided for IPsec VPN in Mbit/s.")
        )
        parser.add_argument(
            '--bgp_asn',
            metavar='<bgp_asn>',
            type=int,
            help=_("Specifies the BGP ASN of the Virtual Gateway.")
        )
        parser.add_argument(
            '--admin_state_up',
            metavar='<admin_state_up>',
            type=bool,
            help=_("Specifies the administrative status of the "
                   "Virtual Gateway.")
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dcaas

        args_list = [
            'vpc_id',
            'local_ep_group_id',
            'name',
            'description',
            'device_id',
            'redundant_device_id',
            'type',
            'ipsec_bandwidth',
            'bgp_asn',
            'admin_state_up'
        ]
        attrs = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        obj = client.create_virtual_gateway(**attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class UpdateVirtualGateway(command.ShowOne):
    _description = _("Update a Virtual Gateway.")

    def get_parser(self, prog_name):
        parser = super(UpdateVirtualGateway, self).get_parser(prog_name)
        parser.add_argument(
            'virtual_gateway',
            metavar='<virtual_gateway>',
            help=_("Specifies the Virual Gateway ID or name.")
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_("Specifies the Virtual Gateway name.")
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_("Provides supplementary information about the "
                   "Virtual Gateway.")
        )
        parser.add_argument(
            '--local_ep_group_id',
            metavar='<local_ep_group_id>',
            help=_("Specifies the ID of the local endpoint group that records "
                   "CIDR blocks of the VPC subnets.")
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dcaas

        args_list = [
            'name',
            'description',
            'local_ep_group_id'
        ]
        attrs = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        if parsed_args.virtual_gateway:
            virtual_gateway = client.find_virtual_gateway(
                parsed_args.virtual_gateway
            )
            obj = client.update_virtual_gateway(
                virtual_gateway.id, **attrs
            )

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class DeleteVirtualGateway(command.Command):
    _description = _("Delete the Virtual Gateway.")

    def get_parser(self, prog_name):
        parser = super(DeleteVirtualGateway, self).get_parser(prog_name)
        parser.add_argument(
            'virtual_gateway',
            metavar='<virtual_gateway>',
            help=_("Virtual Gateway to delete.")
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dcaas
        if parsed_args.virtual_gateway:
            virtual_gateway = client.find_virtual_gateway(
                parsed_args.virtual_gateway)
            client.delete_virtual_gateway(virtual_gateway.id)
