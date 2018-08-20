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
'''CTS Trace v1 action implementations'''
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.common import sdk_utils
from otcextensions.common import format

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)

TRACE_STATUSES = ['NORMAL', 'WARNING', 'INCIDENT']


def _get_columns(item):
    column_map = {
    }
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


class ListTrace(command.Lister):
    _description = _('List CTS traces')
    columns = (
        'id', 'name', 'user', 'service_type', 'type',
        'resource_type', 'resource_name', 'resource_id',
        'source_ip', 'level', 'time')

    def get_parser(self, prog_name):
        parser = super(ListTrace, self).get_parser(prog_name)
        parser.add_argument(
            '--tracker',
            metavar='<tracker>',
            default='system',
            help=_('Tracker name (currently only `system`)')
        )
        parser.add_argument(
            '--limit',
            metavar='<limit>',
            type=int,
            help=_('Limit number of records to return.')
        )
        parser.add_argument(
            '--next',
            metavar='<next>',
            type=int,
            help=_('ID of the previous trace to paginate output.')
        )
        parser.add_argument(
            '--service_type',
            metavar='<type>',
            help=_('Service type to query traces for.')
        )
        parser.add_argument(
            '--resource_type',
            metavar='<resource_type>',
            help=_('Resource type to query traces for.')
        )
        parser.add_argument(
            '--resource_id',
            metavar='<resource_id>',
            help=_('Resource ID to query traces for.')
        )
        parser.add_argument(
            '--resource_name',
            metavar='<resource_name>',
            help=_('Resource name to query traces for.')
        )
        parser.add_argument(
            '--trace_name',
            metavar='<name>',
            help=_('Trace name (operation) to query traces for.')
        )
        parser.add_argument(
            '--trace_id',
            metavar='<id>',
            help=_('Trace id to query traces for.')
        )
        parser.add_argument(
            '--level',
            metavar='{' + ','.join(TRACE_STATUSES) + '}',
            type=lambda s: s.upper(),
            choices=TRACE_STATUSES,
            help=_('Trace level to query traces for.')
        )
        parser.add_argument(
            '--user',
            metavar='<user>',
            help=_('User name to query traces for.')
        )
        parser.add_argument(
            '--start_time',
            metavar='<yyyy-MM-ddTHH:mm:ss>',
            help=_('Start time of the period to be queried.')
        )
        parser.add_argument(
            '--end_time',
            metavar='<yyyy-MM-ddTHH:mm:ss>',
            help=_('End time of the period to be queried.')
        )
        parser.add_argument(
            '--long',
            action='store_true',
            help=_('Return long format.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.cts

        query = {}
        if parsed_args.service_type:
            query['service_type'] = parsed_args.service_type
        if parsed_args.resource_type:
            query['res_type'] = parsed_args.resource_type
        if parsed_args.resource_id:
            query['res_id'] = parsed_args.resource_id
        if parsed_args.resource_name:
            query['res_name'] = parsed_args.resource_name
        if parsed_args.trace_name:
            query['trace_name'] = parsed_args.trace_name
        if parsed_args.trace_id:
            query['trace_id'] = parsed_args.trace_id
        if parsed_args.level:
            query['level'] = parsed_args.level
        if parsed_args.user:
            query['user'] = parsed_args.user

        if parsed_args.limit:
            query['limit'] = parsed_args.limit
        if parsed_args.next:
            query['next'] = parsed_args.next
        if parsed_args.start_time:
            query['from'] = format.TimeTMsStr().serialize(
                parsed_args.start_time)
        if parsed_args.end_time:
            query['to'] = format.TimeTMsStr().serialize(
                parsed_args.end_time)

        LOG.debug('query=%s' % query)

        data = client.traces(
            tracker=parsed_args.tracker,
            **query
        )

        columns = ()
        if not parsed_args.long:
            columns = self.columns
        else:
            columns = (
                'id', 'name', 'type', 'user', 'service_type',
                'resource_type', 'resource_name', 'resource_id',
                'source_ip', 'level', 'time', 'request', 'response'
            )

        table = (columns,
                 (utils.get_item_properties(
                     s, columns,
                 ) for s in data))
        return table
