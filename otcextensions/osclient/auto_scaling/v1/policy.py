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
'''AS Configurations v1 action implementations'''
import argparse
import logging

from osc_lib.command import command
from osc_lib import utils

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def set_attributes_for_print_detail(obj):
    info = {}
    info['name'] = obj.name
    info['id'] = obj.id
    info['create_time'] = obj.create_time
    info['type'] = obj.type
    info['status'] = obj.status
    info['scaling_group_id'] = obj.scaling_group_id
    info['alarm_id'] = obj.alarm_id
    info['cool_down_time'] = obj.cool_down_time
    info['scheduled_policy'] = obj.scheduled_policy
    info['scaling_policy_action'] = obj.scaling_policy_action

    return info


class ListAutoScalingPolicy(command.Lister):
    _description = _('List AutoScaling Policies')
    columns = ('ID', 'Name')

    def get_parser(self, prog_name):
        parser = super(ListAutoScalingPolicy, self).get_parser(prog_name)
        parser.add_argument(
            '--limit',
            # dest='limit',
            metavar='<limit>',
            type=int,
            default=None,
            help=_('Limit the number of results displayed')
        )
        parser.add_argument(
            '--marker',
            # dest='marker',
            metavar='<ID>',
            help=_('Begin displaying the results for IDs greater than the '
                   'specified marker. When used with --limit, set this to '
                   'the last ID displayed in the previous run')
        )
        parser.add_argument(
            '--group',
            metavar='<group>',
            required=True,
            help=_('ScalingGroup ID or Name')
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.auto_scaling

        args = {}
        if parsed_args.limit:
            args['limit'] = parsed_args.limit
        if parsed_args.marker:
            args['marker'] = parsed_args.marker

        group = client.find_group(parsed_args.group, ignore_missing=False)

        data = client.policies(group=group.id, **args)

        return (
            self.columns,
            (utils.get_item_properties(
                s,
                self.columns,
            ) for s in data)
        )


class ShowAutoScalingPolicy(command.ShowOne):
    _description = _('Shows details of a AutoScalinig policy')
    columns = ['ID', 'Name', 'scaling_group_id', 'status',
               'type', 'alarm_id', 'scheduled_policy',
               'scaling_policy_action', 'cool_down_time']

    def get_parser(self, prog_name):
        parser = super(ShowAutoScalingPolicy, self).get_parser(prog_name)
        parser.add_argument(
            'policy',
            metavar='<policy>',
            help=_('ID of the configuration policy')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.auto_scaling

        obj = client.get_policy(parsed_args.policy)

        # display_columns, columns = _get_columns(obj)
        # data = utils.get_item_properties(
        #     obj, columns, formatters={'instance_config': _format_instance})

        fmt = set_attributes_for_print_detail(obj)
        # display_columns, columns = _get_columns(obj)
        data = utils.get_dict_properties(
            fmt, self.columns, formatters={})

        return (self.columns, data)


class CreateAutoScalingPolicy(command.ShowOne):
    _description = _('Creates AutoScalinig Policy')
    columns = ['ID', 'Name', 'scaling_group_id', 'status',
               'type', 'alarm_id', 'scheduled_policy',
               'scaling_policy_action', 'cool_down_time'
               ]
#     columns = ['ID', 'Name', 'instance_id', 'instance_name',
#                'flavor_id', 'image_id', 'disk',
#                'key_name', 'public_ip', 'user_data', 'metadata'
#                ]
#
    POLICY_TYPES = ['ALARM', 'SCHEDULED', 'RECURRENCE']

    def get_parser(self, prog_name):
        parser = super(CreateAutoScalingPolicy, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help=_('AS Policy name')
        )
        parser.add_argument(
            '--group',
            metavar='<group>',
            required=True,
            help=_('AS Group ID or Name for the AS Policy')
        )
        parser.add_argument(
            '--type',
            metavar='<type>',
            required=True,
            # choices=['ALARM', 'SCHEDULED', 'RECURRENCE'],
            help=_('AS Policy type [`ALARM`, `SCHEDULED`, `RECURRENCE`]')
        )
        parser.add_argument(
            '--cool_down_time',
            metavar='<cool_down_time>',
            type=int,
            help=_('Specifies the cooling time in seconds for the policy')
        )
        parser.add_argument(
            '--alarm_id',
            metavar='<alarm_id>',
            help=_('Specifies the alarm_id for the policy')
        )
        parser.add_argument(
            '--action_operation',
            metavar='<action_operation>',
            help=_('Specifies the policy operation '
                   'Can be [`ADD`, `REMOVE`, `SET`]')
        )
        parser.add_argument(
            '--action_instance_number',
            metavar='<action_instance_number>',
            type=int,
            help=_('Specifies number of instances to be operated')
        )
        parser.add_argument(
            '--launch_time',
            metavar='<launch_time>',
            help=_('Specifies the time when the scaling action is triggered. '
                   'The time format must comply with UTC.\n'
                   '* when type=`SCHEDULED`, then `YYYY-MM-DDThh:mmZ`\n'
                   '* when type=`RECURRENCE`, then `hh:mm`\n')
        )
        parser.add_argument(
            '--recurrence_type',
            metavar='<recurrence_type>',
            help=_(
                'Specifies the periodic triggering type\n'
                'This parameter is mandatory when type=`RECURRENCE`\n'
                'Can be [`Daily`, `Weekly`, `Monthly`]'
            )
        )
        parser.add_argument(
            '--recurrence_value',
            metavar='<recurrence_value>',
            help=_(
                'Specifies the frequency, at which actions are triggered\n'
                'When recurrente_type=`Daily` it is Null\n'
                'When recurrente_type=`Weekly` it\'s a week day number '
                '[1..7], where 1 is for Sunday\n'
                'When recurrente_type=`Monthly` it\'s a day number [1..31]\n'
            )
        )
        parser.add_argument(
            '--start_time',
            metavar='<start_time>',
            help=_('Specifies the start time in of the action in the '
                   '`YYYY-MM-DDThh:mmZ` format')
        )
        parser.add_argument(
            '--end_time',
            metavar='<end_time>',
            help=_('Specifies the end time in of the action in the '
                   '`YYYY-MM-DDThh:mmZ` format\n'
                   'Mandatory when type=`RECURRENCE`')
        )
        return parser

    def take_action(self, parsed_args):

        policy_attrs = {}
        policy_attrs['name'] = parsed_args.name
        policy_attrs['scaling_group_id'] = parsed_args.group
        policy_type = parsed_args.type.upper()
        if policy_type not in self.POLICY_TYPES:
            msg = (_('Unsupported policy type. Should be one of %s')
                   % self.POLICY_TYPES)
            raise argparse.ArgumentTypeError(msg)
        else:
            policy_attrs['type'] = policy_type
        if parsed_args.alarm_id:
            policy_attrs['alarm_id'] = parsed_args.alarm_id
        if parsed_args.cool_down_time:
            policy_attrs['cool_down_time'] = parsed_args.cool_down_time
        policy_action = {}
        if parsed_args.action_operation:
            policy_action['operation'] = parsed_args.action_operation
        if parsed_args.action_instance_number:
            policy_action['instance_number'] = \
                parsed_args.action_instance_number
        if policy_action.keys():
            policy_attrs['scaling_policy_action'] = policy_action
        scheduled_policy = {}
        if parsed_args.launch_time:
            scheduled_policy['launch_time'] = parsed_args.launch_time
        if parsed_args.recurrence_type:
            # TODO(agoncharov) validate input
            scheduled_policy['recurrence_type'] = parsed_args.recurrence_type
        if parsed_args.recurrence_value:
            scheduled_policy['recurrence_value'] = parsed_args.recurrence_value
        if parsed_args.launch_time:
            scheduled_policy['start_time'] = parsed_args.start_time
        if parsed_args.launch_time:
            scheduled_policy['end_time'] = parsed_args.end_time
        if scheduled_policy.keys():
            policy_attrs['scheduled_policy'] = scheduled_policy

        client = self.app.client_manager.auto_scaling

        policy = client.create_policy(**policy_attrs)

        fmt = set_attributes_for_print_detail(policy)
        # display_columns, columns = _get_columns(obj)
        data = utils.get_dict_properties(
            fmt, self.columns, formatters={})

        return (self.columns, data)


class DeleteAutoScalingPolicy(command.Command):
    _description = _('Deletes AutoScalinig policy')

    def get_parser(self, prog_name):
        parser = super(DeleteAutoScalingPolicy, self).get_parser(prog_name)
        parser.add_argument(
            'policy',
            nargs='+',
            metavar='<policy>',
            help=_('AS Policy ID')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.auto_scaling

        # TODO(agoncharov) - proper error handling (reporting)

        for pol in parsed_args.policy:
            client.delete_policy(pol)


class UpdateAutoScalingPolicy(command.ShowOne):
    _description = _('Updates AutoScalinig Policy')
    columns = ['ID', 'Name', 'scaling_group_id', 'status',
               'type', 'alarm_id', 'scheduled_policy',
               'scaling_policy_action', 'cool_down_time'
               ]
#     columns = ['ID', 'Name', 'instance_id', 'instance_name',
#                'flavor_id', 'image_id', 'disk',
#                'key_name', 'public_ip', 'user_data', 'metadata'
#                ]
#
    POLICY_TYPES = ['ALARM', 'SCHEDULED', 'RECURRENCE']

    def get_parser(self, prog_name):
        parser = super(UpdateAutoScalingPolicy, self).get_parser(prog_name)
        parser.add_argument(
            'policy',
            metavar='<policy>',
            help=_('AS Policy name or ID')
        )
        parser.add_argument(
            '--group',
            metavar='<group>',
            required=True,
            help=_('AS Group ID or Name for the AS Policy')
        )
        parser.add_argument(
            '--type',
            metavar='<type>',
            required=True,
            # choices=['ALARM', 'SCHEDULED', 'RECURRENCE'],
            help=_('AS Policy type [`ALARM`, `SCHEDULED`, `RECURRENCE`]')
        )
        parser.add_argument(
            '--cool_down_time',
            metavar='<cool_down_time>',
            type=int,
            help=_('Specifies the cooling time in seconds for the policy')
        )
        parser.add_argument(
            '--alarm_id',
            metavar='<alarm_id>',
            help=_('Specifies the alarm_id for the policy')
        )
        parser.add_argument(
            '--action_operation',
            metavar='<action_operation>',
            help=_('Specifies the policy operation '
                   'Can be [`ADD`, `REMOVE`, `SET`]')
        )
        parser.add_argument(
            '--action_instance_number',
            metavar='<action_instance_number>',
            type=int,
            help=_('Specifies number of instances to be operated')
        )
        parser.add_argument(
            '--launch_time',
            metavar='<launch_time>',
            help=_('Specifies the time when the scaling action is triggered. '
                   'The time format must comply with UTC.\n'
                   '* when type=`SCHEDULED`, then `YYYY-MM-DDThh:mmZ`\n'
                   '* when type=`RECURRENCE`, then `hh:mm`\n')
        )
        parser.add_argument(
            '--recurrence_type',
            metavar='<recurrence_type>',
            help=_(
                'Specifies the periodic triggering type\n'
                'This parameter is mandatory when type=`RECURRENCE`\n'
                'Can be [`Daily`, `Weekly`, `Monthly`]'
            )
        )
        parser.add_argument(
            '--recurrence_value',
            metavar='<recurrence_value>',
            help=_(
                'Specifies the frequency, at which actions are triggered\n'
                'When recurrente_type=`Daily` it is Null\n'
                'When recurrente_type=`Weekly` it is a week day number '
                '[1..7], where 1 is for Sunday’n'
                'When recurrente_type=`Monthly` it is a day number [1..31]\n'
            )
        )
        parser.add_argument(
            '--start_time',
            metavar='<start_time>',
            help=_('Specifies the start time in of the action in the '
                   '`YYYY-MM-DDThh:mmZ` format')
        )
        parser.add_argument(
            '--end_time',
            metavar='<end_time>',
            help=_('Specifies the end time in of the action in the '
                   '`YYYY-MM-DDThh:mmZ` format\n'
                   'Mandatory when type=`RECURRENCE`')
        )
        return parser

    def take_action(self, parsed_args):

        policy_attrs = {}
        # policy_attrs['name'] = parsed_args.name
        policy_attrs['scaling_group_id'] = parsed_args.group
        policy_type = parsed_args.type.upper()
        if policy_type not in self.POLICY_TYPES:
            msg = (_('Unsupported policy type. Should be one of %s')
                   % self.POLICY_TYPES)
            raise argparse.ArgumentTypeError(msg)
        else:
            policy_attrs['type'] = policy_type
        if parsed_args.alarm_id:
            policy_attrs['alarm_id'] = parsed_args.alarm_id
        if parsed_args.cool_down_time:
            policy_attrs['cool_down_time'] = parsed_args.cool_down_time
        policy_action = {}
        if parsed_args.action_operation:
            policy_action['operation'] = parsed_args.action_operation
        if parsed_args.action_instance_number:
            policy_action['instance_number'] = \
                parsed_args.action_instance_number
        if policy_action.keys():
            policy_attrs['scaling_policy_action'] = policy_action
        scheduled_policy = {}
        if parsed_args.launch_time:
            scheduled_policy['launch_time'] = parsed_args.launch_time
        if parsed_args.recurrence_type:
            # TODO(agoncharov) validate input
            scheduled_policy['recurrence_type'] = parsed_args.recurrence_type
        if parsed_args.recurrence_value:
            scheduled_policy['recurrence_value'] = parsed_args.recurrence_value
        if parsed_args.launch_time:
            scheduled_policy['start_time'] = parsed_args.start_time
        if parsed_args.launch_time:
            scheduled_policy['end_time'] = parsed_args.end_time
        if scheduled_policy.keys():
            policy_attrs['scheduled_policy'] = scheduled_policy

        client = self.app.client_manager.auto_scaling

        policy = client.update_policy(
            policy=parsed_args.policy, **policy_attrs)

        fmt = set_attributes_for_print_detail(policy)
        # display_columns, columns = _get_columns(obj)
        data = utils.get_dict_properties(
            fmt, self.columns, formatters={})

        return (self.columns, data)


class ExecuteAutoScalingPolicy(command.Command):
    _description = _('Executes AutoScalinig policy')

    def get_parser(self, prog_name):
        parser = super(ExecuteAutoScalingPolicy, self).get_parser(prog_name)
        parser.add_argument(
            'policy',
            metavar='<policy>',
            help=_('AS Policy ID or name')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.auto_scaling

        if parsed_args.policy:
            client.execute_policy(parsed_args.policy)


class EnableAutoScalingPolicy(command.Command):
    _description = _('Enables (resume) AutoScalinig policy')

    def get_parser(self, prog_name):
        parser = super(EnableAutoScalingPolicy, self).get_parser(prog_name)
        parser.add_argument(
            'policy',
            metavar='<policy>',
            help=_('AS Policy ID or name')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.auto_scaling

        if parsed_args.policy:
            client.resume_policy(parsed_args.policy)


class DisableAutoScalingPolicy(command.Command):
    _description = _('Disables (pause) AutoScalinig policy')

    def get_parser(self, prog_name):
        parser = super(DisableAutoScalingPolicy, self).get_parser(prog_name)
        parser.add_argument(
            'policy',
            metavar='<policy>',
            help=_('AS Policy ID or name')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.auto_scaling

        if parsed_args.policy:
            client.pause_policy(parsed_args.policy)
