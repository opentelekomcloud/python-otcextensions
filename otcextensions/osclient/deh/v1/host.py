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
'''DeH Host v1 action implementations'''
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.i18n import _
from otcextensions.common import sdk_utils

LOG = logging.getLogger(__name__)

HOST_STATES = ['available', 'fault', 'released']


_formatters = {
}


def _get_columns(item):
    column_map = {
    }
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


class ListHost(command.Lister):
    _description = _('List DeH hosts')
    columns = (
        'id', 'name', 'auto_placement', 'availability_zone',
        'available_vcpus', 'available_memory'
    )

    def get_parser(self, prog_name):
        parser = super(ListHost, self).get_parser(prog_name)
        parser.add_argument(
            '--id',
            metavar='<id>',
            help=_('Host id.')
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_('Host name.')
        )
        parser.add_argument(
            '--host_type',
            metavar='<host_type>',
            help=_('Host type.')
        )
        parser.add_argument(
            '--host_type_name',
            metavar='<host_type_name>',
            help=_('Host type name.')
        )
        parser.add_argument(
            '--flavor',
            metavar='<flavor>',
            help=_('Flavor ID.')
        )
        parser.add_argument(
            '--state',
            metavar='{' + ','.join(HOST_STATES) + '}',
            type=lambda s: s.lower(),
            choices=HOST_STATES,
            help=_('Host state filter.')
        )
        parser.add_argument(
            '--tenant',
            metavar='<tenant>',
            help=_('Tenant ID or "all".')
        )
        parser.add_argument(
            '--availability_zone',
            metavar='<availability_zone>',
            help=_('Availability zone.')
        )
        parser.add_argument(
            '--limit',
            metavar='<limit>',
            type=int,
            help=_('Number of entries to display.')
        )
        parser.add_argument(
            '--marker',
            metavar='<marker>',
            help=_('ID of the last record on the previous page.')
        )
        parser.add_argument(
            '--changes_since',
            metavar='<changes_since>',
            help=_('Filters the response by a date and time stamp when the '
                   'DeH last changed status. Format: '
                   'CCYY-MM-DDThh:mm:ss+hh:mm')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.deh

        query = {}

        if parsed_args.id:
            query['id'] = parsed_args.id
        if parsed_args.name:
            query['name'] = parsed_args.name
        if parsed_args.host_type:
            query['host_type'] = parsed_args.host_type
        if parsed_args.host_type_name:
            query['host_type_name'] = parsed_args.host_type_name
        if parsed_args.flavor:
            query['flavor'] = parsed_args.flavor
        if parsed_args.state:
            query['state'] = parsed_args.state
        if parsed_args.tenant:
            query['tenant'] = parsed_args.tenant
        if parsed_args.availability_zone:
            query['availability_zone'] = parsed_args.availability_zone
        if parsed_args.limit:
            query['limit'] = parsed_args.limit
        if parsed_args.marker:
            query['marker'] = parsed_args.marker
        if parsed_args.changes_since:
            query['changes_since'] = parsed_args.changes_since

        data = client.hosts(**query)

        table = (self.columns,
                 (utils.get_item_properties(
                     s, self.columns, formatters=_formatters
                 ) for s in data))
        return table


class ShowHost(command.ShowOne):
    _description = _('Show the DeH Host details')

    def get_parser(self, prog_name):
        parser = super(ShowHost, self).get_parser(prog_name)

        parser.add_argument(
            'host',
            metavar='<host>',
            help=_('UUID of the host.')
        )

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.deh

        obj = client.find_host(
            parsed_args.host,
        )

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class DeleteHost(command.Command):
    _description = _('Delete host')

    def get_parser(self, prog_name):
        parser = super(DeleteHost, self).get_parser(prog_name)

        parser.add_argument(
            'host',
            metavar='<host>',
            nargs='+',
            help=_('UUID or name of the host.')
        )

        return parser

    def take_action(self, parsed_args):
        if parsed_args.host:
            client = self.app.client_manager.deh
            for host in parsed_args.host:
                client.delete_host(host=host, ignore_missing=False)


class CreateHost(command.ShowOne):
    _description = _('Create/allocate host')

    columns = ('id')

    def get_parser(self, prog_name):
        parser = super(CreateHost, self).get_parser(prog_name)

        parser.add_argument(
            '--name',
            metavar='<name>',
            required=True,
            help=_('DNS Name for the host.')
        )
        parser.add_argument('--auto_placement',
                            action='store_const',
                            default='on',
                            const='on',
                            dest='auto_placement')
        parser.add_argument('--no-auto_placement',
                            action='store_const',
                            const='off',
                            dest='auto_placement')
        parser.add_argument(
            '--availability_zone',
            metavar='<az>',
            required=True,
            help=_('The AZ the host belongs to.')
        )
        parser.add_argument(
            '--host_type',
            metavar='<type>',
            help=_('DeH type.')
        )
        parser.add_argument(
            '--quantity',
            metavar='[0..]',
            type=int,
            default=1,
            help=_('Number of DeHs to allocate.')
        )

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.deh

        attrs = {}

        if parsed_args.name:
            attrs['name'] = parsed_args.name
        if parsed_args.auto_placement:
            attrs['auto_placement'] = parsed_args.auto_placement
        if parsed_args.availability_zone:
            attrs['availability_zone'] = parsed_args.availability_zone
        if parsed_args.host_type:
            attrs['host_type'] = parsed_args.host_type
        if parsed_args.quantity:
            attrs['quantity'] = parsed_args.quantity

        obj = client.create_host(
            **attrs
        )

        table = (self.columns,
                 (utils.get_item_properties(
                     s, self.columns, formatters=_formatters
                 ) for s in obj.dedicated_host_ids))
        return table

        #
        # display_columns, columns = _get_columns(obj)
        # data = utils.get_item_properties(obj, columns)
        #
        # return (display_columns, data)


class SetHost(command.ShowOne):
    _description = _('Update a Host')

    def get_parser(self, prog_name):
        parser = super(SetHost, self).get_parser(prog_name)

        parser.add_argument(
            'host',
            metavar='<host>',
            help=_('UUID or name of the host.')
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_('DNS Name for the host.')
        )
        parser.add_argument('--auto_placement',
                            action='store_const',
                            default='on',
                            const='on',
                            dest='auto_placement')
        parser.add_argument('--no-auto_placement',
                            action='store_const',
                            const='off',
                            dest='auto_placement')

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.deh

        attrs = {}

        if parsed_args.name:
            attrs['name'] = parsed_args.name
        if parsed_args.auto_placement:
            attrs['auto_placement'] = parsed_args.auto_placement

        host = client.find_host(parsed_args.host, ignore_missing=False)

        if host:
            obj = client.update_host(
                host=host,
                **attrs
            )

            display_columns, columns = _get_columns(obj)
            data = utils.get_item_properties(obj, columns)

            return (display_columns, data)


class ListServer(command.Lister):
    _description = _('List Servers on a DeH')
    columns = (
        'addresses', 'id', 'name', 'metadata', 'status', 'user_id'
    )

    def get_parser(self, prog_name):
        parser = super(ListServer, self).get_parser(prog_name)

        parser.add_argument(
            'host',
            metavar='<host>',
            help=_('UUID of the DeH host.')
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.deh

        host = client.find_host(parsed_args.host, ignore_missing=False)

        if host:
            data = client.servers(host=host)

            table = (self.columns,
                     (utils.get_item_properties(
                         s, self.columns, formatters=_formatters
                     ) for s in data))
            return table


class ListHostType(command.Lister):
    _description = _('List DeH host types')
    columns = (
        'host_type', 'host_type_name'
    )

    def get_parser(self, prog_name):
        parser = super(ListHostType, self).get_parser(prog_name)

        parser.add_argument(
            'az',
            metavar='<az>',
            help=_('Availability zone.')
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.deh

        data = client.host_types(parsed_args.az)

        table = (self.columns,
                 (utils.get_item_properties(
                     s, self.columns, formatters=_formatters
                 ) for s in data))
        return table
