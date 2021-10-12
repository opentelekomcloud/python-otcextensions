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
'''CBR Share Backup implementation'''
import logging

from osc_lib import utils
from osc_lib import exceptions
from osc_lib.command import command

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)

class ListMembers(command.Lister):
    _description = _('List CBR Shares')
    columns = ('ID', 'dest_project_id', 'vault_id', 'image_id')

    def get_parser(self, prog_name):
        parser = super(ListMembers, self).get_parser(prog_name)
        parser.add_argument(
            'backup',
            metavar='<backup_id>',
            help=_('The ID or name of the backup.')
        )
        parser.add_argument(
            '--dest-project-id',
            metavar='<dest_project_id>',
            help=_('ID of the project with which the backup is shared.')
        )
        parser.add_argument(
            '--image-id',
            metavar='<image_id>',
            help=_('ID of the image created from the accepted backup.')
        )
        parser.add_argument(
            '--status',
            metavar='<status>',
            help=_('Status of a shared backup.')
        )
        parser.add_argument(
            '--vault-id',
            metavar='<vault_id>',
            help=_('ID of the vault where the shared backup is stored.')
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.cbr

        query = {}
        
        if parsed_args.dest_project_id:
            query['dest_project_id'] = parsed_args.dest_project_id
        if parsed_args.image_id:
            query['image_id'] = parsed_args.image_id
        if parsed_args.status:
            query['status'] = parsed_args.status
        if parsed_args.vault_id:
            query['vault_id'] = parsed_args.vault_id

        backup = client.find_backup(parsed_args.backup)
        query['backup'] = backup

        data = client.members(**query)

        table = (self.columns,
                 (utils.get_dict_properties(
                     s, self.columns,
                 ) for s in data))
        return table


class ShowMember(command.ShowOne):
    _description = _('Show single Member details')
    columns = (
        'ID',
        'status',
        'image_id',
        'vault_id',
        'dest_project_id',
        'created_at'
    )

    def get_parser(self, prog_name):
        parser = super(ShowMember, self).get_parser(prog_name)
        parser.add_argument(
            'backup',
            metavar='<backup_id>',
            help=_('The ID of the backup.')
        )
        parser.add_argument(
            '--member-id',
            metavar='<member_id>',
            required=True,
            help=_('Member ID. The member ID is the same as the project ID.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.cbr

        obj = client.get_member(
            member=parsed_args.member_id,
            backup=parsed_args.backup
        )

        data = utils.get_dict_properties(
            obj, self.columns)

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
        'max_backups',
        'day_backups',
        'week_backups',
        'month_backups',
        'year_backups',
        'timezone',
    )

    def get_parser(self, prog_name):
        parser = super(CreatePolicy, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help=_('Name of the CBR Policy.')
        )
        parser.add_argument(
            '--disable',
            action='store_false',
            help=_('Disables CBR Policy which is enabled by default.')
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
            '--pattern',
            metavar='<pattern>',
            required=True,
            action='append',
            dest='patterns',
            help=_('Scheduling rule.\n'
                   'Repeat Option for multiple rules.')
        )
        parser.add_argument(
            '--day-backups',
            metavar='<day_backups>',
            type=int,
            help=_('Specifies the number of retained daily backups.\n'
                   'Ranges from 0 to 100.\n'
                   'If this parameter is configured, timezone is '
                   'mandatory.')
        )
        parser.add_argument(
            '--week-backups',
            metavar='<week_backups>',
            type=int,
            help=_('Specifies the number of retained weekly backups.\n'
                   'Ranges from 0 to 100.\n'
                   'If this parameter is configured, timezone is '
                   'mandatory.')
        )
        parser.add_argument(
            '--month-backups',
            metavar='<month_backups>',
            type=int,
            help=_('Specifies the number of retained monthly backups.\n'
                   'Ranges from 0 to 100.\n'
                   'If this parameter is configured, timezone is '
                   'mandatory.')
        )
        parser.add_argument(
            '--year-backups',
            metavar='<year_backups>',
            type=int,
            help=_('Specifies the number of retained yearly backups.\n'
                   'Ranges from 0 to 100.\n'
                   'If this parameter is configured, timezone is '
                   'mandatory.')
        )
        parser.add_argument(
            '--timezone',
            metavar='<timezone>',
            help=_('Timezone where the user is located, e.g. UTC+08:00.')
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
            '--retention-duration-days',
            metavar='<retention_duration_days>',
            default=-1,
            type=int,
            help=_('Duration of retaining a backup, in days.\n'
                   '-1 indicates that the backups will not be '
                   'cleared based on the retention duration.\n'
                   'Ranges from 1 to 99999.')
        )
        return parser

    def take_action(self, parsed_args):

        attrs = {
            'operation_definition': {},
            'trigger': {
                'properties': {
                    'pattern': []
                }
            }
        }

        # mandatory
        attrs['name'] = parsed_args.name
        attrs['enabled'] = parsed_args.disable
        attrs['operation_type'] = parsed_args.operation_type
        attrs['trigger']['properties']['pattern'] = parsed_args.patterns

        # optional
        if parsed_args.day_backups:
            attrs['operation_definition'].update(
                day_backups=parsed_args.day_backups)
        if parsed_args.week_backups:
            attrs['operation_definition'].update(
                week_backups=parsed_args.week_backups)
        if parsed_args.month_backups:
            attrs['operation_definition'].update(
                month_backups=parsed_args.month_backups)
        if parsed_args.year_backups:
            attrs['operation_definition'].update(
                year_backups=parsed_args.year_backups)
        if parsed_args.max_backups:
            attrs['operation_definition'].update(
                max_backups=parsed_args.max_backups)
        if parsed_args.retention_duration_days:
            rdd = parsed_args.retention_duration_days
            attrs['operation_definition'].update(
                retention_duration_days=rdd)

        if (parsed_args.day_backups
            or parsed_args.week_backups
            or parsed_args.month_backups
                or parsed_args.year_backups) and not parsed_args.timezone:
            msg = ("Parameter timezone must be provided if "
                   "<day|week|month|year>_backups are being used.")
            raise exceptions.BadRequest(msg)

        if parsed_args.timezone:
            attrs['operation_definition'].update(
                timezone=parsed_args.timezone)

        client = self.app.client_manager.cbr
        obj = client.create_policy(**attrs)

        data = utils.get_dict_properties(
            _flatten_policy(obj), self.columns)

        if obj.trigger.properties.pattern:
            data, self.columns = _add_scheduling_patterns(
                obj, data, self.columns)

        return (self.columns, data)


class UpdatePolicy(command.ShowOne):
    _description = _('Update CBR Policy')
    columns = (
        'ID',
        'name',
        'operation_type',
        'start_time',
        'enabled',
        'retention_duration_days',
        'max_backups',
        'day_backups',
        'week_backups',
        'month_backups',
        'year_backups',
        'timezone',
    )

    def get_parser(self, prog_name):
        parser = super(UpdatePolicy, self).get_parser(prog_name)
        parser.add_argument(
            'policy',
            metavar='<policy>',
            help=_('ID or name of the CBR Policy.')
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_('Name of the CBR Policy.')
        )
        parser.add_argument(
            '--disable',
            action='store_true',
            help=_('Disables CBR Policy which is enabled by default.')
        )
        parser.add_argument(
            '--enable',
            action='store_true',
            help=_('Enables CBR Policy.')
        )
        parser.add_argument(
            '--pattern',
            metavar='<pattern>',
            action='append',
            dest='patterns',
            help=_('Scheduling rule.\n'
                   'Repeat Option for multiple rules.')
        )
        parser.add_argument(
            '--day-backups',
            metavar='<day_backups>',
            type=int,
            help=_('Specifies the number of retained daily backups.\n'
                   'Ranges from 0 to 100.\n'
                   'If this parameter is configured, timezone is '
                   'mandatory.')
        )
        parser.add_argument(
            '--week-backups',
            metavar='<week_backups>',
            type=int,
            help=_('Specifies the number of retained weekly backups.\n'
                   'Ranges from 0 to 100.\n'
                   'If this parameter is configured, timezone is '
                   'mandatory.')
        )
        parser.add_argument(
            '--month-backups',
            metavar='<month_backups>',
            type=int,
            help=_('Specifies the number of retained monthly backups.\n'
                   'Ranges from 0 to 100.\n'
                   'If this parameter is configured, timezone is '
                   'mandatory.')
        )
        parser.add_argument(
            '--year-backups',
            metavar='<year_backups>',
            type=int,
            help=_('Specifies the number of retained yearly backups.\n'
                   'Ranges from 0 to 100.\n'
                   'If this parameter is configured, timezone is '
                   'mandatory.')
        )
        parser.add_argument(
            '--timezone',
            metavar='<timezone>',
            help=_('Timezone where the user is located, e.g. UTC+08:00.')
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
            '--retention-duration-days',
            metavar='<retention_duration_days>',
            type=int,
            help=_('Duration of retaining a backup, in days.\n'
                   '-1 indicates that the backups will not be '
                   'cleared based on the retention duration.\n'
                   'Ranges from 1 to 99999.')
        )
        return parser

    def take_action(self, parsed_args):

        attrs = {}

        if parsed_args.name:
            attrs['name'] = parsed_args.name
        if parsed_args.enable:
            attrs['enabled'] = True
        if parsed_args.disable:
            attrs['enabled'] = False
        if parsed_args.patterns:
            trigger = {
                'trigger': {
                    'properties': {
                        'pattern': parsed_args.patterns
                    }
                }
            }
            attrs.update(trigger)

        if (parsed_args.day_backups
            or parsed_args.week_backups
            or parsed_args.month_backups
            or parsed_args.year_backups
            or parsed_args.max_backups
            or parsed_args.retention_duration_days
                or parsed_args.timezone):
            attrs['operation_definition'] = {}
            if parsed_args.day_backups:
                attrs['operation_definition'].update(
                    day_backups=parsed_args.day_backups)
            if parsed_args.week_backups:
                attrs['operation_definition'].update(
                    week_backups=parsed_args.week_backups)
            if parsed_args.month_backups:
                attrs['operation_definition'].update(
                    month_backups=parsed_args.month_backups)
            if parsed_args.year_backups:
                attrs['operation_definition'].update(
                    year_backups=parsed_args.year_backups)
            if parsed_args.max_backups:
                attrs['operation_definition'].update(
                    max_backups=parsed_args.max_backups)
            if parsed_args.retention_duration_days:
                rdd = parsed_args.retention_duration_days
                attrs['operation_definition'].update(
                    retention_duration_days=rdd)
            if parsed_args.timezone:
                attrs['operation_definition'].update(
                    timezone=parsed_args.timezone)

        client = self.app.client_manager.cbr
        policy = client.find_policy(
            name_or_id=parsed_args.policy,
            ignore_missing=False
        )

        if attrs:
            obj = client.update_policy(policy=policy.id, **attrs)
        else:
            obj = policy

        data = utils.get_dict_properties(
            _flatten_policy(obj), self.columns)

        if obj.associated_vaults:
            data, self.columns = _add_vaults_to_policy_obj(
                obj, data, self.columns)

        if obj.trigger.properties.pattern:
            data, self.columns = _add_scheduling_patterns(
                obj, data, self.columns)

        return (self.columns, data)


class DeletePolicy(command.Command):
    _description = _('Delete CBR Policy')

    def get_parser(self, prog_name):
        parser = super(DeletePolicy, self).get_parser(prog_name)
        parser.add_argument(
            'policy',
            metavar='<policy>',
            help=_('ID or name of the CBR Policy.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.cbr

        policy = client.find_policy(
            name_or_id=parsed_args.policy,
            ignore_missing=False
        )

        self.app.client_manager.cbr.delete_policy(
            policy=policy.id,
            ignore_missing=False)
