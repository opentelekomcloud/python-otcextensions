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
'''CES Alarm v1 action implementations'''
import logging

from osc_lib import utils
from osc_lib.command import command


from otcextensions.i18n import _
from otcextensions.common import sdk_utils

LOG = logging.getLogger(__name__)


def _get_columns(item):
    column_map = {
    }
    inv_columns = ['']
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map,
                                                           inv_columns)


class ListMetricData(command.Lister):
    _description = _('List CES event data')
    columns = (
        'timestamp',
        'type',
        'value'
    )

    def get_parser(self, prog_name):
        parser = super(ListMetricData, self).get_parser(prog_name)
        parser.add_argument(
            '--namespace',
            metavar='<namespace>',
            required=True,
            help=_('Specifies the namespace of the metric such as:\n'
                   'SYS.ECS, SYS.AS')
        )
        parser.add_argument(
            '--type',
            metavar='<type>',
            required=True,
            help=_('Specifies the event type such as:\n'
                   'instance_host_info')
        )
        parser.add_argument(
            '--dim',
            metavar='<key,value>',
            required=True,
            help=_('Specifies the monitoring dimension:\n'
                   'dim.0=instance_id,123-456-789')
        )
        parser.add_argument(
            '--time-from',
            metavar='<from>',
            required=True,
            help=_('UNIX timestamp in ms from which the data is '
                   'collected.')
        )
        parser.add_argument(
            '--time-to',
            metavar='<to>',
            required=True,
            help=_('UNIX timestamp in ms to which the data is '
                   'collected.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.ces

        query = {}
        query['namespace'] = parsed_args.namespace
        query['type'] = parsed_args.type
        query['dim.0'] = parsed_args.dim
        query['from'] = parsed_args.time_from
        query['to'] = parsed_args.time_to

        data = client.event_data(**query)

        table = (self.columns,
                 (utils.get_dict_properties(
                     s, self.columns
                 ) for s in data))
        return table
