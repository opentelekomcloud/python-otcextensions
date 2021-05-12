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
'''CBR Policy CLI implementation'''
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _flatten_policy(obj):
    """Flatten the structure of the node pool into a single dict
    """
    od = obj.operation_definition
    data = {
        'id': obj.id,
        'name': obj.name,
        'enabled': obj.enabled,
        'operation_type': obj.operation_type,
        'retention_duration_days': od.retention_duration_days,
        'year_backups': od.year_backups,
        'day_backups': od.day_backups,
        'week_backups': od.week_backups,
        'month_backups': od.month_backups,
        'timezone': od.timezone,
        'start_time': obj.trigger.properties.start_time,
        'scheduler_id': obj.trigger.id,
        'scheduler_name': obj.trigger.name,
    }

    return data


def _add_vaults_to_policy_obj(obj, data, columns):
    """Add associated vaults to column and data tuples
    """
    i = 0
    for s in obj.associated_vaults:
        if obj.associated_vaults[i].vault_id:
            name = 'associated_vault_' + str(i + 1)
            data += (obj.associated_vaults[i].vault_id,)
            columns = columns + (name,)
            i += 1
    return data, columns


def _add_scheduling_patterns(obj, data, columns):
    """Add scheduling patterns to column and data tuples
    """
    i = 0
    for s in obj.trigger.properties.pattern:
        name = 'schedule_pattern_' + str(i + 1)
        data += (obj.trigger.properties.pattern[i],)
        columns = columns + (name,)
        i += 1
    return data, columns


class ListPolicies(command.Lister):
    _description = _('List CBR Policies')
    columns = ('ID', 'name', 'operation_type', 'start_time', 'enabled')

    def get_parser(self, prog_name):
        parser = super(ListPolicies, self).get_parser(prog_name)
        parser.add_argument(
            '--vault-id',
            metavar='<vault_id>',
            help=_('The ID of the vault.')
        )
        parser.add_argument(
            '--operation-type',
            metavar='<operation_type>',
            choices=['backup', 'replication'],
            help=_('Policy type')
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.cbr

        query = {}

        if parsed_args.vault_id:
            query['vault_id'] = parsed_args.vault_id
        if parsed_args.operation_type:
            query['operation_type'] = parsed_args.operation_type

        data = client.policies(**query)

        table = (self.columns,
                 (utils.get_dict_properties(
                     _flatten_policy(s), self.columns,
                 ) for s in data))
        return table


class ShowPolicy(command.ShowOne):
    _description = _('Show single Policy details')
    columns = (
        'ID',
        'name',
        'operation_type',
        'start_time',
        'enabled',
        'retention_duration_days',
        'day_backups',
        'week_backups',
        'month_backups',
        'year_backups',
        'timezone',
        'scheduler_id',
        'scheduler_name',
    )

    def get_parser(self, prog_name):
        parser = super(ShowPolicy, self).get_parser(prog_name)
        parser.add_argument(
            'policy',
            metavar='<policy>',
            help=_('ID or name of the CBR policy.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.cbr

        policy = client.find_policy(parsed_args.policy,
                                    ignore_missing=False)

        obj = client.find_policy(
            name_or_id=policy.id,
        )

        data = utils.get_dict_properties(
            _flatten_policy(obj), self.columns)

        if obj.associated_vaults:
            data, self.columns = _add_vaults_to_policy_obj(
                obj, data, self.columns)

        if obj.trigger.properties.pattern:
            data, self.columns = _add_scheduling_patterns(
                obj, data, self.columns)

        return (self.columns, data)

class CreatePolicy(command.ShowOne):
    _description = _('Create CBR Policy')
    columns = (
        'ID',
        'name',
        'operation_type',
        'start_time',
        'enabled',
        'retention_duration_days',
        'day_backups',
        'week_backups',
        'month_backups',
        'year_backups',
        'timezone',
        'scheduler_id',
        'scheduler_name',
    )

    def get_parser(self, prog_name):
        parser = super(CreatePolicy, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help=_('Name of the CBR Policy.')
        )
        parser.add_argument(
            '--enabled',
            metavar='<autoscaling_enabled>',
            default=True,
            type=bool,
            help=_('Enables or disables CBR Policy')
        )
        parser.add_argument(
            '--operation-type',
            metavar='<operation_type>',
            default='backup',
            choices=['backup', 'replication'],
            help=_('backup or replication\n'
                   'Default: backup')
        )
        parser.add_argument(
            '--day-backups',
            metavar='<day_backups>',
            type=int,
            help=_('Specifies the number of retained daily backups.\n'
                   'Ranges from 0 to 100.\n'
                   'If this parameter is configured, timezone is '
                   'mandatory.)
        )
        parser.add_argument(
            '--max-backups',
            metavar='<max_backups>',
            type=int,
            help=_('Maximum number of retained backups.\n'
                   'Can be -1, backups will not cleared or ranges\n'
                   'from 0 to 99999.')
        )
        parser.add_argument(
            '--month-backups',
            metavar='<month_backups>',
            type=int,
            help=_('Specifies the number of retained monthly backups.\n'
                   'Ranges from 0 to 100.\n'
                   'If this parameter is configured, timezone is '
                   'mandatory.)
        )
        parser.add_argument(
            '--retention-duration-days',
            metavar='<retention_duration_days>',
            default=-1,
            type=int,
            help=_('Duration of retaining a backup, in days.\n'
                   '-1 indicates that the backups will not be '
                   'cleared based on the retention duration.\n'
                   'Ranges from 1 to 99999.')
        )
        parser.add_argument(
            '--timezone',
            metavar='<timezone>',
            help=_('Timezone where the user is located, e.g. UTC+08:00.')
        )
        parser.add_argument(
            '--week-backups',
            metavar='<week_backups>',
            type=int,
            help=_('Specifies the number of retained weekly backups.\n'
                   'Ranges from 0 to 100.\n'
                   'If this parameter is configured, timezone is '
                   'mandatory.)
        )
        parser.add_argument(
            '--year-backups',
            metavar='<year_backups>',
            type=int,
            help=_('Specifies the number of retained yearly backups.\n'
                   'Ranges from 0 to 100.\n'
                   'If this parameter is configured, timezone is '
                   'mandatory.)
        )
        parser.add_argument(
            '--pattern',
            metavar='<pattern>',
            required=True,
            action='append',
            help=_('Scheduling rule.\n'
                   'Repeat Option for multiple rules.)
        )
        return parser

    def take_action(self, parsed_args):

        attrs = {}
        # mandatory
        attrs['cluster'] = parsed_args.cluster


        # optional
        if parsed_args.az:
            attrs['availability_zone'] = parsed_args.az


        obj = self.app.client_manager.sdk_connection.create_cce_node_pool(
            **attrs)

        data = utils.get_dict_properties(
            _flatten_node_pool(obj),
            self.columns)

        return (self.columns, data)
