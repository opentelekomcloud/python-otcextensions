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
'''AS Instance v1 action implementations'''
import logging

from osc_lib import exceptions
from osc_lib import utils
from osc_lib.command import command

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


class ListAutoScalingInstance(command.Lister):
    _description = _('List AutoScaling Instances')
    columns = ('ID', 'Name', 'scaling_group_name',
               'scaling_configuration_id', 'scaling_configuration_name',
               'lifecycle_state', 'health_status', 'create_time')

    def get_parser(self, prog_name):
        parser = super(ListAutoScalingInstance, self).get_parser(prog_name)
        parser.add_argument(
            '--group',
            metavar='<group>',
            required=True,
            help=_('AS Group ID or Name for the instances query')
        )
        parser.add_argument(
            '--life_cycle_state',
            metavar='<life_cycle_state>',
            help=_('Life cycle state of the instances to query\n'
                   'Could be in [`INSERVICE`, `PENDING`, `REMOVING`]')
        )
        parser.add_argument(
            '--health_status',
            metavar='<health_status>',
            help=_('Health status of the instances to query\n'
                   'Could be in [`INITIALIZING`, `NORMAL`, `ERROR`]')
        )
        parser.add_argument(
            '--limit',
            metavar='<limit>',
            type=int,
            help=_('Limit the number of results displayed')
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.auto_scaling

        args = {}
        if parsed_args.limit:
            args['limit'] = parsed_args.limit
        if parsed_args.life_cycle_state:
            args['life_cycle_state'] = parsed_args.life_cycle_state
        if parsed_args.health_status:
            args['health_status'] = parsed_args.health_status

        group = client.find_group(parsed_args.group, ignore_missing=False)

        data = client.instances(group=group.id, **args)

        return (
            self.columns,
            (utils.get_item_properties(
                s,
                self.columns,
            ) for s in data)
        )


class RemoveAutoScalingInstance(command.Command):
    _description = _('Removes AutoScalinig Instances')

    def get_parser(self, prog_name):
        parser = super(RemoveAutoScalingInstance, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help=_('AS Instance ID to be deleted')
        )
        parser.add_argument(
            '--delete_instance',
            action='store_true',
            default=False,
            help=_('Specifies, whether instance should be completely deleted')
        )
        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.auto_scaling
        client.remove_instance(
            instance=parsed_args.instance,
            delete_instance=parsed_args.delete_instance,
            ignore_missing=False
        )


class BatchActionAutoScalingInstance(command.Command):
    _description = _('Executes Action on AutoScalinig Instances')

    SUPPORTED_ACTIONS = ['ADD', 'REMOVE', 'PROTECT', 'UNPROTECT']

    def get_parser(self, prog_name):
        parser = super(BatchActionAutoScalingInstance, self).\
            get_parser(prog_name)
        parser.add_argument(
            '--group',
            metavar='<group>',
            required=True,
            help=_('AS Group ID or Name')
        )
        parser.add_argument(
            'action',
            metavar='<action>',
            help=_('Action to be performed\n'
                   'One of [`ADD`, `REMOVE`, `PROTECT`, `UNPROTECT`]')
        )
        parser.add_argument(
            'instance',
            metavar='<instance>',
            nargs='+',
            help=_('AS Instance ID to be deleted')
        )
        parser.add_argument(
            '--delete_instance',
            action='store_true',
            default=False,
            help=_('Specifies, whether instance should be completely deleted'
                   ' when action is ``REMOVE``')
        )
        return parser

    def take_action(self, parsed_args):

        action = parsed_args.action.upper()
        if action not in self.SUPPORTED_ACTIONS:
            msg = (_('Action %(action)s is not one of '
                     'the supported %(types)s') %
                   {'action': parsed_args.action,
                    'types': self.SUPPORTED_ACTIONS})
            raise exceptions.CommandError(msg)

        client = self.app.client_manager.auto_scaling
        client.batch_instance_action(
            group=parsed_args.group,
            instance=parsed_args.instance,
            action=action,
            delete_instance=parsed_args.delete_instance,
            ignore_missing=False
        )
