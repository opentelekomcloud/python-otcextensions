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
'''LoadBalancer Health Monitor v1 action implementations'''
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


_formatters = {
    'pool_ids': sdk_utils.ListOfIdsColumnBR,
}


def _get_columns(item):
    column_map = {
        'is_admin_state_up': 'admin_state_up',
    }
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE',
                'TRACE', 'OPTIONS', 'CONNECT', 'PATCH']
TYPE_VALUES = ['HTTP', 'HTTPS', 'PING', 'TCP', 'TLS-HELLO']


class ListHealthMonitor(command.Lister):
    _description = _('List health monitors')
    column_headers = ('id', 'name', 'project_id', 'type', 'admin_state_up')
    columns = ('id', 'name', 'project_id', 'type', 'is_admin_state_up')

    def get_parser(self, prog_name):
        parser = super(ListHealthMonitor, self).get_parser(prog_name)

        parser.add_argument(
            '--type',
            metavar='{' + ','.join(TYPE_VALUES) + '}',
            type=lambda s: s.upper(),
            choices=TYPE_VALUES,
            help=_('Health monitor type to use as a filter\n'
                   'one of [`HTTP`, `HTTPS`, `PING`, `TCP`, `TLS-HELLO`]')
        )

        return parser

    def take_action(self, parsed_args):

        args = {}
        if parsed_args.type:
            args['type'] = parsed_args.type

        client = self.app.client_manager.network

        data = client.health_monitors(**args)

        return (
            self.column_headers,
            (utils.get_item_properties(
                s, self.columns, formatters=_formatters
            ) for s in data))


class ShowHealthMonitor(command.ShowOne):
    _description = _('Show the details of a single health monitor')

    def get_parser(self, prog_name):
        parser = super(ShowHealthMonitor, self).get_parser(prog_name)

        parser.add_argument(
            'health_monitor',
            metavar='<health_monitor>',
            help=_('Name or UUID of the health monitor.')
        )

        return parser

    def take_action(self, parsed_args):

        args = {}

        client = self.app.client_manager.network

        obj = client.find_health_monitor(
            name_or_id=parsed_args.health_monitor,
            ignore_missing=False,
            **args)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)

        return (display_columns, data)


class CreateHealthMonitor(command.ShowOne):
    _description = _('Create a health monitor')

    def get_parser(self, prog_name):
        parser = super(CreateHealthMonitor, self).get_parser(prog_name)

        parser.add_argument(
            'pool',
            metavar='<pool>',
            help=_('Set the pool for the health monitor (name or ID).')
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_('Set the health monitor name.')
        )
        parser.add_argument(
            '--delay',
            metavar='<delay>',
            type=int,
            required=True,
            help=_('Set the time in seconds, between sending probes '
                   'to members.')
        )
        parser.add_argument(
            '--expected_codes',
            metavar='<codes>',
            help=_('The list of HTTP status codes expected in response '
                   'from the member to declare it healthy. Specify one '
                   'of the following values:\n'
                   '* A single value, such as 200\n'
                   '* A list, such as 200, 202\n'
                   '* A range, such as 200-204\n'
                   'The default is 200.')
        )
        parser.add_argument(
            '--http_method',
            metavar='{' + ','.join(HTTP_METHODS) + '}',
            choices=HTTP_METHODS,
            type=lambda s: s.upper(),  # case insensitive
            help=_('The HTTP method that the health monitor uses for requests.'
                   'One of [`GET`, `HEAD`, `POST`, `PUT`, `DELETE`,'
                   '`TRACE`, `OPTIONS`, `CONNECT`, `PATCH`]\n'
                   'Default is `GET`')
        )
        parser.add_argument(
            '--timeout',
            metavar='<timeout>',
            type=int,
            help=_('The maximum time, in seconds, that a monitor waits to '
                   'connect before it times out. This value must be less '
                   'than the delay value.')
        )
        parser.add_argument(
            '--max_retries',
            metavar='<max_retries>',
            type=int,
            required=True,
            choices=range(1, 10),
            help=_('The number of successful checks before changing the '
                   'operating status of the member to `ONLINE`. '
                   'A valid value is from 1 to 10.')
        )
        parser.add_argument(
            '--url_path',
            metavar='<url_path>',
            help=_('The HTTP URL path of the request sent by the monitor '
                   'to test the health of a backend member. Must be a string '
                   'that begins with a forward slash (/).'
                   'The default URL path is /.')
        )
        parser.add_argument(
            '--type',
            metavar='{' + ','.join(TYPE_VALUES) + '}',
            choices=TYPE_VALUES,
            type=lambda s: s.upper(),  # case insensitive
            required=True,
            help=_('The type of health monitor.\n'
                   'one of [`HTTP`, `HTTPS`, `PING`, `TCP`, `TLS-HELLO`]')
        )
        admin_group = parser.add_mutually_exclusive_group()
        admin_group.add_argument(
            '--enable',
            action='store_true',
            default=True,
            help=_('Enable health monitor (default).')
        )
        admin_group.add_argument(
            '--disable',
            action='store_true',
            default=None,
            help=_('Disable health monitor.')
        )

        return parser

    def take_action(self, parsed_args):

        args = {}
        if parsed_args.delay:
            args['delay'] = parsed_args.delay
        if parsed_args.expected_codes:
            args['expected_codes'] = parsed_args.expected_codes
        if parsed_args.max_retries:
            args['max_retries'] = parsed_args.max_retries
        if parsed_args.timeout:
            args['timeout'] = parsed_args.timeout
        if parsed_args.url_path:
            args['url_path'] = parsed_args.url_path
        if parsed_args.http_method:
            args['http_method'] = parsed_args.http_method
        if parsed_args.type:
            args['type'] = parsed_args.type
        if parsed_args.name:
            args['name'] = parsed_args.name
        if parsed_args.disable:
            args['is_admin_state_up'] = False

        client = self.app.client_manager.network

        pool = client.find_pool(name_or_id=parsed_args.pool,
                                ignore_missing=False)

        args['pool_id'] = pool.id

        obj = client.create_health_monitor(
            **args)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)

        return (display_columns, data)


class SetHealthMonitor(command.ShowOne):
    _description = _('Update a health monitor')

    def get_parser(self, prog_name):
        parser = super(SetHealthMonitor, self).get_parser(prog_name)

        parser.add_argument(
            'health_monitor',
            metavar='<health_monitor>',
            help=_('Health monitor to update (name or ID).')
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_('Human-readable name of the resource.')
        )
        parser.add_argument(
            '--delay',
            metavar='<delay>',
            type=int,
            help=_('The time, in seconds, between sending probes to members.')
        )
        parser.add_argument(
            '--expected_codes',
            metavar='<expected_codes>',
            help=_('The list of HTTP status codes expected in response '
                   'from the member to declare it healthy. Specify one '
                   'of the following values:\n'
                   '* A single value, such as 200\n'
                   '* A list, such as 200, 202\n'
                   '* A range, such as 200-204\n'
                   'The default is 200.')
        )
        parser.add_argument(
            '--http_method',
            metavar='{' + ','.join(HTTP_METHODS) + '}',
            choices=HTTP_METHODS,
            type=lambda s: s.upper(),  # case insensitive
            help=_('The HTTP method that the health monitor uses for requests.'
                   'One of [`GET`, `HEAD`, `POST`, `PUT`, `DELETE`,'
                   '`TRACE`, `OPTIONS`, `CONNECT`, `PATCH`]\n'
                   'Default is `GET`')
        )
        parser.add_argument(
            '--timeout',
            metavar='<timeout>',
            type=int,
            help=_('The maximum time, in seconds, that a monitor waits to '
                   'connect before it times out. This value must be less '
                   'than the delay value.')
        )
        parser.add_argument(
            '--max_retries',
            metavar='<max_retries>',
            type=int,
            required=True,
            choices=range(1, 10),
            help=_('The number of successful checks before changing the '
                   'operating status of the member to `ONLINE`. '
                   'A valid value is from 1 to 10.')
        )
        parser.add_argument(
            '--url_path',
            metavar='<url_path>',
            help=_('The HTTP URL path of the request sent by the monitor '
                   'to test the health of a backend member. Must be a string '
                   'that begins with a forward slash (/).'
                   'The default URL path is /.')
        )
        admin_group = parser.add_mutually_exclusive_group()
        admin_group.add_argument(
            '--enable',
            action='store_true',
            default=True,
            help=_('Enable health monitor (default).')
        )
        admin_group.add_argument(
            '--disable',
            action='store_true',
            default=None,
            help=_('Disable health monitor.')
        )

        return parser

    def take_action(self, parsed_args):

        args = {}
        if parsed_args.delay:
            args['delay'] = parsed_args.delay
        if parsed_args.expected_codes:
            args['expected_codes'] = parsed_args.expected_codes
        if parsed_args.max_retries:
            args['max_retries'] = parsed_args.max_retries
        if parsed_args.timeout:
            args['timeout'] = parsed_args.timeout
        if parsed_args.url_path:
            args['url_path'] = parsed_args.url_path
        if parsed_args.http_method:
            args['http_method'] = parsed_args.http_method
        if parsed_args.name:
            args['name'] = parsed_args.name
        if parsed_args.disable:
            args['is_admin_state_up'] = False

        client = self.app.client_manager.network

        hm = client.find_health_monitor(name_or_id=parsed_args.health_monitor,
                                        ignore_missing=False)

        obj = client.update_health_monitor(
            health_monitor=hm.id,
            **args)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)

        return (display_columns, data)


class DeleteHealthMonitor(command.Command):
    _description = _('Delete a health monitor')

    def get_parser(self, prog_name):
        parser = super(DeleteHealthMonitor, self).get_parser(prog_name)

        parser.add_argument(
            'health_monitor',
            metavar='<health_monitor>',
            nargs='+',
            help=_('The ID of the health monitor to delete')
        )
        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.network

        for hm in parsed_args.health_monitor:
            obj = client.find_health_monitor(name_or_id=hm,
                                             ignore_missing=False)
            client.delete_health_monitor(
                health_monitor=obj.id,
                ignore_missing=False)

        return
