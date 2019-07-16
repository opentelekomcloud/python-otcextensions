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
'''Anti DDoS Floating IP statistics v1 action implementations'''
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.common import format

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


class ListFloatingIPEvents(command.Lister):
    _description = _('List Anti DDoS FloatingIP events')
    columns = (
        'start_time', 'end_time', 'status', 'trigger_bps',
        'trigger_pps', 'trigger_http_pps'
    )

    def get_parser(self, prog_name):
        parser = super(ListFloatingIPEvents, self).get_parser(prog_name)

        parser.add_argument(
            'floating_ip',
            metavar='<UUID>',
            help=_('UUID of the floating IP.')
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.anti_ddos

        data = client.floating_ip_events(
            floating_ip_id=parsed_args.floating_ip)

        table = (self.columns,
                 (utils.get_item_properties(
                     s, self.columns
                 ) for s in data))
        return table


class ListFloatingIPStatDay(command.Lister):
    _description = _('List Anti DDoS FloatingIP day statistics')
    columns = (
        'period_start', 'bps_in', 'bps_attack', 'total_bps',
        'pps_in', 'pps_attack', 'total_pps'
    )

    def get_parser(self, prog_name):
        parser = super(ListFloatingIPStatDay, self).get_parser(prog_name)

        parser.add_argument(
            'floating_ip',
            metavar='<UUID>',
            help=_('UUID of the floating IP.')
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.anti_ddos

        data = client.floating_ip_stat_day(
            floating_ip_id=parsed_args.floating_ip)

        table = (self.columns,
                 (utils.get_item_properties(s, self.columns)
                  for s in data))
        return table


class ListFloatingIPStatWeek(command.Lister):
    _description = _('List Anti DDoS FloatingIP week statistics')
    columns = (
        'period_start_date', 'ddos_intercept_times', 'ddos_blackhole_times',
        'max_attack_bps', 'max_attack_conns'
    )

    def get_parser(self, prog_name):
        parser = super(ListFloatingIPStatWeek, self).get_parser(prog_name)

        parser.add_argument(
            '--start_time',
            metavar='<yyyy-MM-ddTHH:mm:ss>',
            help=_('Start time of the period to be queried.')
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.anti_ddos

        query = {}

        if parsed_args.start_time:
            query['period_start_date'] = format.TimeTMsStr().serialize(
                parsed_args.start_time)

        data = client.floating_ip_stat_week(**query)

        table = (self.columns,
                 (utils.get_item_properties(s, self.columns)
                  for s in data.weekdata))
        return table
