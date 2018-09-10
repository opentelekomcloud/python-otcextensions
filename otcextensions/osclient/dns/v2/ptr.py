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
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


class ListPTR(command.Lister):
    _description = _('List PTR records')
    columns = (
        'id', 'name', 'type', 'status', 'description'
    )

    def get_parser(self, prog_name):
        parser = super(ListPTR, self).get_parser(prog_name)

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dns

        query = {}

        data = client.ptrs(**query)

        table = (self.columns,
                 (utils.get_item_properties(
                     s, self.columns, formatters=_formatters
                 ) for s in data))
        return table


class ShowPTR(command.ShowOne):
    _description = _('Show the PTR record details')

    def get_parser(self, prog_name):
        parser = super(ShowPTR, self).get_parser(prog_name)

        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            '--ptr',
            metavar='<ID>',
            help=_('PTR record ID.')
        )
        fgrp = group.add_argument_group()
        fgrp.add_argument(
            '--region',
            metavar='<region>',
            default='en-de',
            help=_('Region of the FloatingIP.')
        )
        fgrp.add_argument(
            '--floating_ip',
            metavar='<UUID>',
            help=_('FloatingIP ID.')
        )

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.dns

        query = {}

        if parsed_args.ptr:
            query['ptr'] = parsed_args.ptr
        else:
            query['region'] = parsed_args.region
            query['floating_ip_id'] = parsed_args.floating_ip

        obj = client.get_ptr(**query)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class DeletePTR(command.Command):
    _description = _('Delete (restore) PTR record')

    def get_parser(self, prog_name):
        parser = super(DeletePTR, self).get_parser(prog_name)

        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            '--ptr',
            metavar='<ID>',
            help=_('PTR record ID.')
        )
        fgrp = group.add_argument_group()
        fgrp.add_argument(
            '--region',
            metavar='<region>',
            default='en-de',
            help=_('Region of the FloatingIP.')
        )
        fgrp.add_argument(
            '--floating_ip',
            metavar='<UUID>',
            help=_('FloatingIP ID.')
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dns

        query = {}

        if parsed_args.ptr:
            query['ptr'] = parsed_args.ptr
        else:
            query['region'] = parsed_args.region
            query['floating_ip_id'] = parsed_args.floating_ip

        return client.restore_ptr(**query)


class SetPTR(command.ShowOne):
    _description = _('Set PTR record')

    def get_parser(self, prog_name):
        parser = super(SetPTR, self).get_parser(prog_name)

        fgrp = parser.add_argument_group()
        fgrp.add_argument(
            '--region',
            metavar='<region>',
            default='en-de',
            required=True,
            help=_('Region of the FloatingIP.')
        )
        fgrp.add_argument(
            '--floating_ip',
            metavar='<UUID>',
            required=True,
            help=_('FloatingIP ID.')
        )
        parser.add_argument(
            '--ptrdname',
            metavar='<ptrdomain>',
            required=True,
            help=_('Domain of the PTR record.')
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

        if parsed_args.ptrdname:
            attrs['ptrdname'] = parsed_args.ptrdname
        if parsed_args.description:
            attrs['description'] = parsed_args.description
        if parsed_args.ttl:
            attrs['ttl'] = parsed_args.ttl

        obj = client.create_ptr(
            region=parsed_args.region,
            floating_ip_id=parsed_args.floating_ip,
            **attrs
        )

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)
