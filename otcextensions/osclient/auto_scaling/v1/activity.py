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
'''AS Activity Log v1 action implementations'''
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


class ListAutoScalingActivityLogs(command.Lister):
    _description = _('List AutoScaling Activity Logs')
    columns = (
        'ID', 'status', 'description',
        'instance_value', 'desire_value',
        'start_time', 'end_time')

    def get_parser(self, prog_name):
        parser = super(ListAutoScalingActivityLogs, self).get_parser(prog_name)
        parser.add_argument(
            '--group',
            metavar='<group>',
            required=True,
            help=_('AS Group ID or name')
        )
        parser.add_argument(
            '--start_time',
            metavar='<start_time>',
            help=_('Specifies the start time for querying scaling '
                   'action logs. Format: `YYYY-MM-DDThh:mm:ssZ`')
        )
        parser.add_argument(
            '--end_time',
            metavar='<end_time>',
            help=_('Specifies the end time for querying scaling '
                   'action logs. Format: `YYYY-MM-DDThh:mm:ssZ`')
        )
        parser.add_argument(
            '--limit',
            metavar='<limit>',
            type=int,
            help=_('Specifies the batch size of the records for pagination')
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.auto_scaling

        args = {}
        if parsed_args.limit:
            args['limit'] = parsed_args.limit
        if parsed_args.start_time:
            args['start_time'] = parsed_args.start_time
        if parsed_args.end_time:
            args['end_time'] = parsed_args.end_time

        group = client.find_group(parsed_args.group, ignore_missing=False)

        data = client.activities(group=group.id, **args)

        return (
            self.columns,
            (utils.get_item_properties(
                s,
                self.columns,
            ) for s in data)
        )
