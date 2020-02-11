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
'''DNS Recordset v2 action implementations'''
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.i18n import _
from otcextensions.common import sdk_utils

LOG = logging.getLogger(__name__)

RS_TYPES = ['A', 'AAAA', 'MX', 'TXT', 'CNAME', 'NS', 'SRV', 'PTR', 'CAA']


_formatters = {
}


def _get_columns(item):
    column_map = {
    }
    hidden = ['location', 'links']
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map,
                                                           hidden)


class ListRS(command.Lister):
    _description = _('List recordsets.')
    columns = (
        'id', 'name', 'type', 'status', 'description', 'records'
    )

    def get_parser(self, prog_name):
        parser = super(ListRS, self).get_parser(prog_name)
        parser.add_argument(
            'zone',
            metavar='<zone>',
            help=_('UUID or name of the zone. Recordsets of all zones '
                   'will be returned if not given.')
        )
        parser.add_argument(
            '--zone-type',
            help=_('DNS Zone type (private/public)')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dns

        zone = None
        attrs = {}
        if parsed_args.zone_type:
            attrs['zone_type'] = parsed_args.zone_type

        if parsed_args.zone:

            zone = client.find_zone(parsed_args.zone, ignore_missing=False,
                                    **attrs)

        data = client.recordsets(zone=zone)

        table = (self.columns,
                 (utils.get_item_properties(
                     s, self.columns, formatters=_formatters
                 ) for s in data))
        return table


class ShowRS(command.ShowOne):
    _description = _('Show the recordset details')

    def get_parser(self, prog_name):
        parser = super(ShowRS, self).get_parser(prog_name)

        parser.add_argument(
            'zone',
            metavar='<zone>',
            help=_('UUID or name of the zone.')
        )
        parser.add_argument(
            '--zone-type',
            help=_('DNS Zone type (private/public)')
        )

        parser.add_argument(
            'recordset',
            metavar='<rs>',
            help=_('UUID or name of the recordset.')
        )

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.dns

        zone = client.find_zone(
            parsed_args.zone,
            ignore_missing=False,
            zone_type=parsed_args.zone_type
        )

        obj = client.find_recordset(zone=zone,
                                    name_or_id=parsed_args.recordset)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class DeleteRS(command.Command):
    _description = _('Delete Recordset')

    def get_parser(self, prog_name):
        parser = super(DeleteRS, self).get_parser(prog_name)

        parser.add_argument(
            'zone',
            metavar='<zone>',
            help=_('UUID or name of the zone.')
        )
        parser.add_argument(
            '--zone-type',
            help=_('DNS Zone type (private/public)')
        )

        parser.add_argument(
            'recordset',
            metavar='<rs>',
            nargs='+',
            help=_('UUID or Name of the recordset.')
        )

        return parser

    def take_action(self, parsed_args):
        if parsed_args.zone:
            client = self.app.client_manager.dns
            zone = client.find_zone(parsed_args.zone, ignore_missing=False,
                                    zone_type=parsed_args.zone_type)
            for rs in parsed_args.recordset:
                rs = client.find_recordset(zone=zone, name_or_id=rs,
                                           ignore_missing=False)
                client.delete_recordset(
                    recordset=rs, zone=zone, ignore_missing=False)


class CreateRS(command.ShowOne):
    _description = _('Create recordset')

    def get_parser(self, prog_name):
        parser = super(CreateRS, self).get_parser(prog_name)

        parser.add_argument(
            'zone',
            metavar='<zone>',
            help=_('UUID or name of the zone.')
        )
        parser.add_argument(
            '--zone-type',
            help=_('DNS Zone type (private/public)')
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            required=True,
            help=_('DNS Name for the zone.')
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_('Description for this zone.')
        )
        parser.add_argument(
            '--type',
            metavar='{' + ','.join(RS_TYPES) + '}',
            type=lambda s: s.upper(),
            choices=RS_TYPES,
            help=_('Recordset type.')
        )
        parser.add_argument(
            '--ttl',
            metavar='<300-2147483647>',
            type=int,
            # NOTE: py2 does not support such big int, skip unless py3-only
            # choices=range(300, 2147483647),
            help=_('TTL (Time to Live) for the zone.')
        )
        parser.add_argument(
            '--record',
            metavar='<value>',
            action='append',
            help=_('Record set value, which varies depending on the record '
                   'set type. For example, the value of an `AAAA` record set '
                   'is the IPv6 address list mapped to the domain name. ')
        )

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.dns

        attrs = {'records': []}

        zone = client.find_zone(parsed_args.zone, ignore_missing=False,
                                zone_type=parsed_args.zone_type)

        if parsed_args.name:
            attrs['name'] = parsed_args.name
        if parsed_args.description:
            attrs['description'] = parsed_args.description
        if parsed_args.type:
            attrs['type'] = parsed_args.type
        if parsed_args.ttl:
            attrs['ttl'] = parsed_args.ttl
        for rec in parsed_args.record:
            attrs['records'].append(rec)

        obj = client.create_recordset(
            zone=zone,
            **attrs
        )

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class SetRS(command.ShowOne):
    _description = _('Update a Recordset')

    def get_parser(self, prog_name):
        parser = super(SetRS, self).get_parser(prog_name)

        parser.add_argument(
            'zone',
            metavar='<zone>',
            help=_('UUID or name of the zone.')
        )
        parser.add_argument(
            '--zone-type',
            help=_('DNS Zone type (private/public)')
        )
        parser.add_argument(
            'recordset',
            metavar='<rs>',
            help=_('UUID or name of the recordset.')
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_('Description for this zone.')
        )
        parser.add_argument(
            '--ttl',
            metavar='<300-2147483647>',
            type=int,
            # NOTE: py2 does not support such big int, skip unless py3-only
            # choices=range(300, 2147483647),
            help=_('TTL (Time to Live) for the zone.')
        )
        parser.add_argument(
            '--record',
            metavar='<value>',
            action='append',
            help=_('Record set value, which varies depending on the record '
                   'set type. For example, the value of an `AAAA` record set '
                   'is the IPv6 address list mapped to the domain name. ')
        )

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.dns

        attrs = {'records': []}

        if parsed_args.description:
            attrs['description'] = parsed_args.description
        if parsed_args.ttl:
            attrs['ttl'] = parsed_args.ttl

        zone = client.find_zone(parsed_args.zone, ignore_missing=False,
                                zone_type=parsed_args.zone_type)

        if parsed_args.ttl:
            attrs['zone_id'] = zone.id

        for rec in parsed_args.record:
            attrs['records'].append(rec)

        recordset = client.find_recordset(zone=zone,
                                          name_or_id=parsed_args.recordset)

        obj = client.update_recordset(
            recordset=recordset,
            **attrs
        )

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)
