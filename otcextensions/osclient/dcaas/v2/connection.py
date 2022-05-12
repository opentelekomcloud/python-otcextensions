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
"""Direct Connection v2 action implementations"""
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


class ListDirectConnections(command.Lister):

    _description = _("List of Direct Connections.")
    columns = (
        'id',
        'name',
        'port type',
        'provider',
        'bandwidth',
        'location',
        'status'
    )

    def get_parser(self, prog_name):
        parser = super(ListDirectConnections, self).get_parser(prog_name)
        parser.add_argument(
            '--id',
            metavar='<id>',
            help=_("Specifies the ID of the Direct Connection.")
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_("Specified the name of Direct Connection.")
        )
        parser.add_argument(
            '--port_type',
            metavar='<port_type>',
            help=_("Specified the port type of Direct Connection. The value "
                   "can be 1G or 10G.")
        )
        parser.add_argument(
            '--bandwidth',
            metavar='<bandwidth>',
            type=int,
            help=_("Specified the bandwidth of Direct Connection in Mbit/s.")
        )
        parser.add_argument(
            '--location',
            metavar='<location>',
            help=_("Specified the access location of Direct Connection.")
        )
        parser.add_argument(
            '--peer_location',
            metavar='<peer_location>',
            help=_("Specifies the location of the on-premises facility at "
                   "the other end of the connection, specific to the street "
                   "or data center name.")
        )
        parser.add_argument(
            '--device_id',
            metavar='<device_id>',
            help=_("Specifies the gateway device ID of the Direct Connection.")
        )
        parser.add_argument(
            '--interface_name',
            metavar='<interface_name>',
            help=_("Specifies the name of the interface accessed by the "
                   "Direct Connection.")
        )
        parser.add_argument(
            '--redundant_id',
            metavar='<redundant_id>',
            help=_("Specifies the ID of the redundant connection using "
                   "the same gateway.")
        )
        parser.add_argument(
            '--provider',
            metavar='<provider>',
            help=_("Specifies the carrier who provides the leased line.")
        )
        parser.add_argument(
            '--provider_status',
            metavar='<provider_status>',
            help=_("Specifies the status of the carrier's leased line."
                   " The value can be ACTIVE or DOWN.")
        )
        parser.add_argument(
            '--type',
            metavar='<type>',
            help=_("Specifies the connection type. The value can be hosted.")
        )
        parser.add_argument(
            '--hosting_id',
            metavar='<hosting_id>',
            help=_("Specifies the ID of the operations connection on which"
                   " the hosted connection is created.")
        )
        parser.add_argument(
            '--vlan',
            metavar='<vlan>',
            help=_("Specifies the VLAN pre-allocated to the hosted"
                   " connection.")
        )
        parser.add_argument(
            '--charge_mode',
            metavar='<charge_mode>',
            help=_("Specifies the billing mode. The value can be prepayment,"
                   " bandwidth, or traffic.")
        )
        parser.add_argument(
            '--apply_time',
            metavar='<apply_time>',
            help=_("Specifies the time when the connection is requested.")
        )
        parser.add_argument(
            '--create_time',
            metavar='<create_time>',
            help=_("Specifies the time when the connection is created.")
        )
        parser.add_argument(
            '--delete_time',
            metavar='<delete_time>',
            help=_("Specifies the time when the connection is deleted.")
        )
        parser.add_argument(
            '--order_id',
            metavar='<order_id>',
            help=_("Specifies the order number of the connection.")
        )
        parser.add_argument(
            '--product_id',
            metavar='<product_id>',
            help=_("Specifies the product ID corresponding to the "
                   "connection's order.")
        )
        parser.add_argument(
            '--status',
            metavar='<status>',
            help=_("Specifies the connection status. The value can be ACTIVE, "
                   "DOWN, BUILD, ERROR, PENDING_DELETE, DELETED, APPLY, DENY, "
                   "PENDING_PAY, PAID, ORDERING, ACCEPT, or REJECTED.")
        )
        parser.add_argument(
            '--admin_state_up',
            metavar='<admin_state_up>',
            help=_("Specifies the administrative status of the connection."
                   "The value can be true or false.")
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dcaas

        args_list = [
            'id',
            'name',
            'port_type',
            'bandwidth',
            'location',
            'peer_location',
            'device_id',
            'interface_name',
            'redundant_id',
            'provider',
            'provider_status',
            'type',
            'hosting_id',
            'vlan',
            'charge_mode',
            'apply_time',
            'create_time',
            'delete_time',
            'order_id',
            'product_id',
            'status',
            'admin_state_up'
        ]

        attrs = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        data = client.connections(**attrs)

        table = (self.columns, (utils.get_dict_properties(s, self.columns)
                                for s in data))
        return table


class ShowDirectConnection(command.ShowOne):
    _description = _("Show Direct Connection details.")

    def get_parser(self, prog_name):
        parser = super(ShowDirectConnection, self).get_parser(prog_name)
        parser.add_argument(
            'direct_connection',
            metavar='<direct_connection>',
            help=_("Specifies the connection ID or name.")
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dcaas
        obj = client.find_connection(parsed_args.direct_connection)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class CreateDirectConnection(command.ShowOne):
    _description = _("Create new Direct Connection")

    def get_parser(self, prog_name):
        parser = super(CreateDirectConnection, self).get_parser(prog_name)
        parser.add_argument(
            'port_type',
            metavar='<port_type>',
            help=_("Specified the port type of Direct Connection. The value "
                   "can be 1G or 10G.")
        )
        parser.add_argument(
            'bandwidth',
            metavar='<bandwidth>',
            type=int,
            help=_("Specified the bandwidth of Direct Connection in Mbit/s.")
        )
        parser.add_argument(
            'location',
            metavar='<location>',
            help=_("Specified the access location of Direct Connection.")
        )
        parser.add_argument(
            'provider',
            metavar='<provider>',
            help=_("Specifies the carrier who provides the leased line.")
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_("Specified the name of Direct Connection.")
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_("Provides supplementary information about the connection.")
        )
        parser.add_argument(
            '--peer_location',
            metavar='<peer_location>',
            help=_("Specifies the location of the on-premises facility at "
                   "the other end of the connection, specific to the street "
                   "or data center name.")
        )
        parser.add_argument(
            '--device_id',
            metavar='<device_id>',
            help=_("Specifies the gateway device ID of the Direct Connection.")
        )
        parser.add_argument(
            '--interface_name',
            metavar='<interface_name>',
            help=_("Specifies the name of the interface accessed by the "
                   "Direct Connection.")
        )
        parser.add_argument(
            '--redundant_id',
            metavar='<redundant_id>',
            help=_("Specifies the ID of the redundant connection using "
                   "the same gateway.")
        )
        parser.add_argument(
            '--provider_status',
            metavar='<provider_status>',
            help=_("Specifies the status of the carrier's leased line. "
                   "The value can be ACTIVE or DOWN.")
        )
        parser.add_argument(
            '--type',
            metavar='<type>',
            help=_("Specifies the connection type. The value can be hosted.")
        )
        parser.add_argument(
            '--hosting_id',
            metavar='<hosting_id>',
            help=_("Specifies the ID of the operations connection on which "
                   "the hosted connection is created.")
        )
        parser.add_argument(
            '--vlan',
            metavar='<vlan>',
            type=int,
            help=_("Specifies the VLAN pre-allocated to the hosted "
                   "connection.")
        )
        parser.add_argument(
            '--charge_mode',
            metavar='<charge_mode>',
            help=_("Specifies the billing mode. The value can be prepayment, "
                   "bandwidth, or traffic.")
        )
        parser.add_argument(
            '--order_id',
            metavar='<order_id>',
            help=_("Specifies the order number of the connection.")
        )
        parser.add_argument(
            '--product_id',
            metavar='<product_id>',
            help=_("Specifies the product ID corresponding to the "
                   "connection's order.")
        )
        parser.add_argument(
            '--status',
            metavar='<status>',
            help=_("Specifies the connection status. The value can be ACTIVE, "
                   "DOWN, BUILD, ERROR, PENDING_DELETE, DELETED, APPLY, DENY, "
                   "PENDING_PAY, PAID, ORDERING, ACCEPT, or REJECTED.")
        )
        parser.add_argument(
            '--admin_state_up',
            metavar='<admin_state_up>',
            type=bool,
            help=_("Specifies the administrative status of the connection. "
                   "The value can be true or false.")
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dcaas

        args_list = [
            'name',
            'description',
            'port_type',
            'bandwidth',
            'location',
            'peer_location',
            'device_id',
            'interface_name',
            'redundant_id',
            'provider',
            'provider_status',
            'type',
            'hosting_id',
            'vlan',
            'charge_mode',
            'order_id',
            'product_id',
            'status',
            'admin_state_up'
        ]
        attrs = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        obj = client.create_connection(**attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class UpdateDirectConnection(command.ShowOne):
    _description = _("Update a Direct Connection")

    def get_parser(self, prog_name):
        parser = super(UpdateDirectConnection, self).get_parser(prog_name)
        parser.add_argument(
            'direct_connection',
            metavar='<direct_connection>',
            help=_("Specifies the connection ID or name.")
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_("Specifies the connection name.")
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_("Provides supplementary information about the connection.")
        )
        parser.add_argument(
            '--bandwidth',
            metavar='<bandwidth>',
            type=int,
            help=_("Specifies the bandwidth of the connection in Mbit/s. "
                   "The value can be 1G or 10G.")
        )
        parser.add_argument(
            '--provider_status',
            metavar='<provider_status>',
            help=_("Specifies the status of the carrier's leased line. "
                   "The value can be ACTIVE or DOWN.")
        )
        parser.add_argument(
            '--order_id',
            metavar='<order_id>',
            help=_("Specifies the order number of the connection.")
        )
        parser.add_argument(
            '--product_id',
            metavar='<product_id>',
            help=_("Specifies the product ID corresponding to the "
                   "connection's order.")
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dcaas

        args_list = [
            'name',
            'description',
            'bandwidth',
            'provider_status',
            'order_id',
            'product_id'
        ]
        attrs = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        if parsed_args.direct_connection:
            direct_connection = client.find_connection(
                parsed_args.direct_connection
            )
            obj = client.update_connection(
                direct_connection=direct_connection.id, **attrs
            )

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class DeleteDirectConnection(command.Command):
    _description = _("Delete the Direct Connection.")

    def get_parser(self, prog_name):
        parser = super(DeleteDirectConnection, self).get_parser(prog_name)
        parser.add_argument(
            'direct_connection',
            metavar='<direct_connection>',
            help=_("Direct Connection to delete.")
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dcaas
        if parsed_args.direct_connection:
            direct_connection = client.find_connection(
                parsed_args.direct_connection)
            client.delete_connection(direct_connection.id)
