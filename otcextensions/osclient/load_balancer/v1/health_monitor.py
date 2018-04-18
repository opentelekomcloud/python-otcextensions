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
'''LoadBalancer Health Monitor v1 action implementations'''
import logging

from osc_lib import exceptions
from osc_lib import utils
from osc_lib.command import command

from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


_formatters = {
    'pool_ids': sdk_utils.ListOfIdsColumn,
}


HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE',
                'TRACE', 'OPTIONS', 'CONNECT', 'PATCH']
TYPE_VALUES = ['HTTP', 'HTTPS', 'PING', 'TCP', 'TLS-HELLO']


class ListHealthMonitor(command.Lister):
    _description = _('List LoadBalancer HealthMonitors')
    columns = ('ID', 'Name', 'type', 'is_admin_state_up',
               'url_path', 'expected_codes',
               'delay', 'max_retries', 'timeout', 'pool_ids')

    def get_parser(self, prog_name):
        parser = super(ListHealthMonitor, self).get_parser(prog_name)

        parser.add_argument(
            '--delay',
            metavar='<delay>',
            type=int,
            help=_("Health monitor delay to query")
        )
        parser.add_argument(
            '--expected_codes',
            metavar='<expected_codes>',
            help=_("Health monitor delay to query")
        )
        parser.add_argument(
            '--http_method',
            metavar='<http_method>',
            help=_("Health monitor HTTP Method to query\n"
                   "One of [`GET`, `HEAD`, `POST`, `PUT`, `DELETE`,"
                   "`TRACE`, `OPTIONS`, `CONNECT`, `PATCH`]")
        )
        parser.add_argument(
            '--max_retries',
            metavar='<max_retries>',
            type=int,
            choices=range(1, 10),
            help=_("The number of successful checks before changing the "
                   "operating status of the member to ONLINE. "
                   "A valid value is from 1 to 10.")
        )
        parser.add_argument(
            '--timeout',
            metavar='<timeout>',
            type=int,
            help=_("Health monitor timeout to query")
        )
        parser.add_argument(
            '--url_path',
            metavar='<url_path>',
            help=_("Health monitor url_path to query")
        )
        parser.add_argument(
            '--type',
            metavar='<type>',
            help=_("Health monitor type to use as a filter\n"
                   "one of [`HTTP`, `HTTPS`, `PING`, `TCP`, `TLS-HELLO`]")
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
            if parsed_args.http_method.upper() in HTTP_METHODS:
                args['http_method'] = parsed_args.http_method
            else:
                msg = (_('http_method %(method)s is not one of the '
                         'supported %(values)s')
                       % {'method': parsed_args.http_method,
                          'values': HTTP_METHODS})
                raise exceptions.CommandError(msg)
        if parsed_args.type:
            if parsed_args.type.upper() in TYPE_VALUES:
                args['type'] = parsed_args.type
            else:
                msg = (_('type %(type)s is not one of the '
                         'supported %(values)s')
                       % {'type': parsed_args.type, 'values': TYPE_VALUES})
                raise exceptions.CommandError(msg)

        client = self.app.client_manager.network

        data = client.health_monitors(**args)

        return (
            self.columns,
            (utils.get_item_properties(
                s, self.columns, formatters=_formatters
            ) for s in data))


class ShowHealthMonitor(command.ShowOne):
    _description = _('Show LoadBalancer HealthMonitor details')
    columns = ('ID', 'Name', 'type', 'is_admin_state_up',
               'http_method', 'url_path', 'expected_codes',
               'delay', 'max_retries', 'timeout', 'pool_ids')

    def get_parser(self, prog_name):
        parser = super(ShowHealthMonitor, self).get_parser(prog_name)

        parser.add_argument(
            'health_monitor',
            metavar='<health_monitor>',
            help=_("Health monitor ID or name")
        )

        return parser

    def take_action(self, parsed_args):

        args = {}

        client = self.app.client_manager.network

        obj = client.find_health_monitor(
            name_or_id=parsed_args.health_monitor,
            ignore_missing=False,
            **args)

        data = utils.get_item_properties(
            obj, self.columns, formatters=_formatters)

        return (self.columns, data)


class CreateHealthMonitor(command.ShowOne):
    _description = _('Create LoadBalancer HealthMonitor')
    columns = ('ID', 'Name', 'type', 'is_admin_state_up',
               'http_method', 'url_path', 'expected_codes',
               'delay', 'max_retries', 'timeout', 'pool_ids')

    def get_parser(self, prog_name):
        parser = super(CreateHealthMonitor, self).get_parser(prog_name)

        parser.add_argument(
            '--admin_state_up',
            dest='admin_state_up',
            type=sdk_utils.str2bool,
            nargs='?',
            help=_("The administrative state of the resource, which is up "
                   "(true) or down (false). Default is true.")
        )
        parser.add_argument(
            '--delay',
            metavar='<delay>',
            type=int,
            required=True,
            help=_("The time, in seconds, between sending probes to members.")
        )
        parser.add_argument(
            '--expected_codes',
            metavar='<expected_codes>',
            help=_("The list of HTTP status codes expected in response "
                   "from the member to declare it healthy. Specify one "
                   "of the following values:\n"
                   "* A single value, such as 200\n"
                   "* A list, such as 200, 202\n"
                   "* A range, such as 200-204\n"
                   "The default is 200.")
        )
        parser.add_argument(
            '--http_method',
            metavar='<http_method>',
            help=_("The HTTP method that the health monitor uses for requests."
                   "One of [`GET`, `HEAD`, `POST`, `PUT`, `DELETE`,"
                   "`TRACE`, `OPTIONS`, `CONNECT`, `PATCH`]\n"
                   "Default is `GET`")
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_("Human-readable name of the resource.")
        )
        parser.add_argument(
            '--max_retries',
            metavar='<max_retries>',
            type=int,
            required=True,
            choices=range(1, 10),
            help=_("The number of successful checks before changing the "
                   "operating status of the member to `ONLINE`. "
                   "A valid value is from 1 to 10.")
        )
        parser.add_argument(
            '--pool_id',
            metavar='<pool_id>',
            help=_("The ID of the pool.")
        )
        parser.add_argument(
            '--timeout',
            metavar='<timeout>',
            type=int,
            help=_("The maximum time, in seconds, that a monitor waits to "
                   "connect before it times out. This value must be less "
                   "than the delay value.")
        )
        parser.add_argument(
            '--type',
            metavar='<type>',
            required=True,
            help=_("The type of health monitor.\n"
                   "one of [`HTTP`, `HTTPS`, `PING`, `TCP`, `TLS-HELLO`]")
        )
        parser.add_argument(
            '--url_path',
            metavar='<url_path>',
            help=_("The HTTP URL path of the request sent by the monitor "
                   "to test the health of a backend member. Must be a string "
                   "that begins with a forward slash (/)."
                   "The default URL path is /.")
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
            if parsed_args.http_method.upper() in HTTP_METHODS:
                args['http_method'] = parsed_args.http_method
            else:
                msg = (_('http_method %(method)s is not one of the '
                         'supported %(values)s')
                       % {'method': parsed_args.http_method,
                          'values': HTTP_METHODS})
                raise exceptions.CommandError(msg)
        if parsed_args.type:
            if parsed_args.type.upper() in TYPE_VALUES:
                args['type'] = parsed_args.type
            else:
                msg = (_('type %(type)s is not one of the '
                         'supported %(values)s')
                       % {'type': parsed_args.type, 'values': TYPE_VALUES})
                raise exceptions.CommandError(msg)
        if parsed_args.pool_id:
            args['pool_id'] = parsed_args.pool_id
        if parsed_args.name:
            args['name'] = parsed_args.name
        if parsed_args.admin_state_up:
            args['admin_state_up'] = parsed_args.admin_state_up

        client = self.app.client_manager.network

        obj = client.create_health_monitor(
            **args)

        data = utils.get_item_properties(
            obj, self.columns, formatters=_formatters)

        return (self.columns, data)


class UpdateHealthMonitor(command.ShowOne):
    _description = _('Update LoadBalancer HealthMonitor details')
    columns = ('ID', 'Name', 'type', 'is_admin_state_up',
               'http_method', 'url_path', 'expected_codes',
               'delay', 'max_retries', 'timeout', 'pool_ids')

    def get_parser(self, prog_name):
        parser = super(UpdateHealthMonitor, self).get_parser(prog_name)

        parser.add_argument(
            'health_monitor',
            metavar='<health_monitor>',
            help=_("The ID of the health monitor to update")
        )
        parser.add_argument(
            '--admin_state_up',
            dest='admin_state_up',
            type=sdk_utils.str2bool,
            nargs='?',
            help=_("The administrative state of the resource, which is up "
                   "(true) or down (false). Default is true.")
        )
        parser.add_argument(
            '--delay',
            metavar='<delay>',
            type=int,
            help=_("The time, in seconds, between sending probes to members.")
        )
        parser.add_argument(
            '--expected_codes',
            metavar='<expected_codes>',
            help=_("The list of HTTP status codes expected in response "
                   "from the member to declare it healthy. Specify one "
                   "of the following values:\n"
                   "* A single value, such as 200\n"
                   "* A list, such as 200, 202\n"
                   "* A range, such as 200-204\n"
                   "The default is 200.")
        )
        parser.add_argument(
            '--http_method',
            metavar='<http_method>',
            help=_("The HTTP method that the health monitor uses for requests."
                   "One of [`GET`, `HEAD`, `POST`, `PUT`, `DELETE`,"
                   "`TRACE`, `OPTIONS`, `CONNECT`, `PATCH`]\n"
                   "Default is `GET`")
        )
        parser.add_argument(
            '--max_retries',
            metavar='<max_retries>',
            type=int,
            choices=range(1, 10),
            help=_("The number of successful checks before changing the "
                   "operating status of the member to `ONLINE`. "
                   "A valid value is from 1 to 10.")
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_("Human-readable name of the resource.")
        )
        parser.add_argument(
            '--timeout',
            metavar='<timeout>',
            type=int,
            help=_("The maximum time, in seconds, that a monitor waits to "
                   "connect before it times out. This value must be less "
                   "than the delay value.")
        )
        parser.add_argument(
            '--url_path',
            metavar='<url_path>',
            help=_("The HTTP URL path of the request sent by the monitor "
                   "to test the health of a backend member. Must be a string "
                   "that begins with a forward slash (/)."
                   "The default URL path is /.")
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
            if parsed_args.http_method.upper() in HTTP_METHODS:
                args['http_method'] = parsed_args.http_method
            else:
                msg = (_('http_method %(method)s is not one of the '
                         'supported %(values)s')
                       % {'method': parsed_args.http_method,
                          'values': HTTP_METHODS})
                raise exceptions.CommandError(msg)
        if parsed_args.name:
            args['name'] = parsed_args.name
        if parsed_args.admin_state_up:
            args['admin_state_up'] = parsed_args.admin_state_up

        client = self.app.client_manager.network

        obj = client.update_health_monitor(
            health_monitor=parsed_args.health_monitor,
            **args)

        data = utils.get_item_properties(
            obj, self.columns, formatters=_formatters)

        return (self.columns, data)


class DeleteHealthMonitor(command.Command):
    _description = _('Delete LoadBalancer HealthMonitor')

    def get_parser(self, prog_name):
        parser = super(DeleteHealthMonitor, self).get_parser(prog_name)

        parser.add_argument(
            'health_monitor',
            metavar='<health_monitor>',
            nargs='+',
            help=_("The ID of the health monitor to delete")
        )
        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.network

        for obj in parsed_args.health_monitor:
            client.delete_health_monitor(
                health_monitor=obj,
                ignore_missing=False)

        return
