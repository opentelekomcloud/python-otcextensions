#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#
'''Anti DDoS Floating IP v1 action implementations'''
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.i18n import _
from otcextensions.common import sdk_utils

LOG = logging.getLogger(__name__)


STATUS_VALUES = ['normal', 'configging', 'notConfig',
                 'packetcleaning', 'packetdropping']


_formatters = {
}


def _get_columns(item):
    column_map = {
    }
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


class ListFloatingIP(command.Lister):
    _description = _('List Anti DDoS FloatingIP statuses')
    columns = (
        'floating_ip_address', 'floating_ip_id', 'network_type', 'status'
    )

    def get_parser(self, prog_name):
        parser = super(ListFloatingIP, self).get_parser(prog_name)

        parser.add_argument(
            '--ip',
            metavar='<IP>',
            help=_('Floating IP prefix.')
        )
        parser.add_argument(
            '--status',
            metavar='{' + ','.join(STATUS_VALUES) + '}',
            type=lambda s: s.lower(),
            choices=STATUS_VALUES,
            help=_('Policy status value.')
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.anti_ddos

        query = {}

        if parsed_args.ip:
            query['ip'] = parsed_args.ip
        if parsed_args.status:
            query['status'] = parsed_args.status

        data = client.floating_ips(**query)

        table = (self.columns,
                 (utils.get_item_properties(
                     s, self.columns
                 ) for s in data))
        return table


class ShowFloatingIP(command.ShowOne):
    _description = _('Show the policies of a single floating IP')

    def get_parser(self, prog_name):
        parser = super(ShowFloatingIP, self).get_parser(prog_name)

        parser.add_argument(
            'floating_ip_id',
            metavar='<ID>',
            help=_('UUID of the floating IP.')
        )

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.anti_ddos

        obj = client.get_floating_ip_policies(
            parsed_args.floating_ip_id,
        )

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class SetFloatingIP(command.ShowOne):
    _description = _('Update a single floating ip instance policies')

    def get_parser(self, prog_name):
        parser = super(SetFloatingIP, self).get_parser(prog_name)
        parser.add_argument(
            'floating_ip_id',
            metavar='<ID>',
            help=_('UUID of the floating IP.')
        )
        parser.add_argument(
            '--traffic_pos_id',
            type=int,
            metavar='<[1..9]>',
            choices=range(1, 10),
            required=True,
            help=_('Position ID of traffic. The value ranges from 1 to 9.')
        )
        parser.add_argument(
            '--http_request_pos_id',
            type=int,
            metavar='<[1..15]>',
            choices=range(1, 16),
            required=True,
            help=_('Position ID of number of HTTP requests. '
                   'The value ranges from 1 to 15.')
        )
        parser.add_argument(
            '--cleaning_access_pos_id',
            type=int,
            metavar='<[1..8]>',
            choices=range(1, 9),
            required=True,
            help=_('Position ID of number of access limit during cleaning. '
                   'The value ranges from 1 to 8.')
        )
        parser.add_argument(
            '--app_type_id',
            metavar='<[0..1]>',
            type=int,
            required=True,
            help=_('Application type ID.')
        )
        l7_group = parser.add_mutually_exclusive_group()
        l7_group.add_argument(
            '--enable_l7',
            action='store_true',
            default=True,
            help=_('Enable L7 defence (default).')
        )
        l7_group.add_argument(
            '--disable_l7',
            action='store_true',
            help=_('Disable L7 defence.')
        )

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.anti_ddos

        attrs = {}

        if parsed_args.enable_l7:
            attrs['is_enable_l7'] = True
        if parsed_args.disable_l7:
            attrs['is_enable_l7'] = False
        if parsed_args.traffic_pos_id:
            attrs['traffic_pos_id'] = parsed_args.traffic_pos_id
        if parsed_args.http_request_pos_id:
            attrs['http_request_pos_id'] = parsed_args.http_request_pos_id
        if parsed_args.cleaning_access_pos_id:
            attrs['cleaning_access_pos_id'] = \
                parsed_args.cleaning_access_pos_id
        if parsed_args.app_type_id:
            attrs['app_type_id'] = parsed_args.app_type_id

        obj = client.update_floating_ip_policies(
            floating_ip=parsed_args.floating_ip_id, **attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)

        return (display_columns, data)
