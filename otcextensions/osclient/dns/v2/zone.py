#   Licensed under the Apache License, Version 2.0 (the 'License'); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an 'AS IS' BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#
'''DNS Zone v2 action implementations'''
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.i18n import _
from otcextensions.common import sdk_utils

LOG = logging.getLogger(__name__)

ZONE_TYPES = ['private', 'public']


_formatters = {
    # 'traffic_limited_list': sdk_utils.ListOfDictColumn,
    # 'http_limited_list': sdk_utils.ListOfDictColumn,
    # 'connection_limited_list': sdk_utils.ListOfDictColumn,
}


def _get_columns(item):
    column_map = {
    }
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


class ListZone(command.Lister):
    _description = _('List DNS zones')
    columns = (
        'id', 'name', 'zone_type', 'serial', 'status', 'action'
    )

    def get_parser(self, prog_name):
        parser = super(ListZone, self).get_parser(prog_name)
        parser.add_argument(
            '--type',
            metavar='{' + ','.join(ZONE_TYPES) + '}',
            type=lambda s: s.lower(),
            choices=ZONE_TYPES,
            help=_('Zone type.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dns

        print('client=%s' % dir(client))

        query = {}

        if parsed_args.type:
            query['type'] = parsed_args.type

        data = client.zones(**query)

        table = (self.columns,
                 (utils.get_item_properties(
                     s, self.columns, formatters=_formatters
                 ) for s in data))
        return table


class ShowZone(command.ShowOne):
    _description = _('Show the zone details')

    def get_parser(self, prog_name):
        parser = super(ShowZone, self).get_parser(prog_name)

        parser.add_argument(
            'zone',
            metavar='<zone>',
            help=_('UUID or name of the zone.')
        )

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.dns

        obj = client.find_zone(
            parsed_args.zone,
        )

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)
