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
'''DNS PTR v2 action implementations'''
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.i18n import _
from otcextensions.common import sdk_utils

LOG = logging.getLogger(__name__)


_formatters = {
}


def _get_columns(item):
    column_map = {
    }
    hidden = ['location', 'links']
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map,
                                                           hidden)


class ListPTR(command.Lister):
    _description = _('List PTR records')
    columns = (
        'id', 'ptrdname', 'address', 'status', 'description', 'ttl'
    )

    def get_parser(self, prog_name):
        parser = super(ListPTR, self).get_parser(prog_name)

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dns

        query = {}

        data = client.floating_ips(**query)

        table = (self.columns,
                 (utils.get_item_properties(
                     s, self.columns, formatters=_formatters
                 ) for s in data))
        return table


class ShowPTR(command.ShowOne):
    _description = _('Show the PTR record details')

    def get_parser(self, prog_name):
        parser = super(ShowPTR, self).get_parser(prog_name)

        parser.add_argument(
            'floatingip_id',
            help=_('Floating IP ID in format region:floatingip_id.')
        )

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.dns

        obj = client.get_floating_ip(parsed_args.floatingip_id)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class DeletePTR(command.Command):
    _description = _('Delete (restore) PTR record')

    def get_parser(self, prog_name):
        parser = super(DeletePTR, self).get_parser(prog_name)

        parser.add_argument(
            'floatingip_id',
            help=_('FloatingIP ID.')
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dns

        client.unset_floating_ip(parsed_args.floatingip_id)


class SetPTR(command.ShowOne):
    _description = _('Set PTR record')

    def get_parser(self, prog_name):
        parser = super(SetPTR, self).get_parser(prog_name)

        parser.add_argument(
            'floatingip_id',
            help=_('Floating IP ID in format region:floatingip_id.')
        )
        parser.add_argument(
            'ptrdname',
            help=_('PTRD Name')
        )

        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_('Description for this record.')
        )
        parser.add_argument(
            '--ttl',
            metavar='<300-2147483647>',
            type=int,
            # NOTE: py2 does not support such big int, skip unless py3-only
            # choices=range(300, 2147483647),
            help=_('TTL (Time to Live) for the zone.')
        )

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.dns

        attrs = {}

        attrs['ptrdname'] = parsed_args.ptrdname
        if parsed_args.description:
            attrs['description'] = parsed_args.description
        if parsed_args.ttl:
            attrs['ttl'] = parsed_args.ttl

        obj = client.set_floating_ip(
            floating_ip=parsed_args.floatingip_id,
            **attrs
        )

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)
