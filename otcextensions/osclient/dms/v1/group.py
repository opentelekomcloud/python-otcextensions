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
'''DMS Group v1 action implementations'''
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


class ListGroup(command.Lister):
    _description = _('List DMS Groups')
    columns = ('ID', 'name', 'produced_messages', 'consumed_messages',
               'available_messages')

    def get_parser(self, prog_name):
        parser = super(ListGroup, self).get_parser(prog_name)
        parser.add_argument(
            'queue',
            metavar='<queue>',
            help=_('ID of the queue')
        )
        parser.add_argument(
            '--include_deadletter',
            action='store_true',
            help=_('Indicates whether to list dead letter parameters '
                   'in the response message.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dms

        queue = client.find_queue(parsed_args.queue)

        data = client.groups(
            queue=queue.id,
            include_deadletter=parsed_args.include_deadletter)

        if parsed_args.include_deadletter:
            self.columns = self.columns + (
                'produced_deadletters',
                'available_deadletters'
            )

        table = (self.columns,
                 (utils.get_item_properties(
                     s, self.columns,
                 ) for s in data))
        return table


class DeleteGroup(command.Command):
    _description = _('Delete DMS Group')

    def get_parser(self, prog_name):
        parser = super(DeleteGroup, self).get_parser(prog_name)
        parser.add_argument(
            'queue',
            metavar='<queue>',
            help=_('ID of the queue')
        )
        parser.add_argument(
            'group',
            metavar='<group>',
            nargs='+',
            help=_('ID of the Group')
        )
        return parser

    def take_action(self, parsed_args):

        if parsed_args.group:
            client = self.app.client_manager.dms
            for group in parsed_args.group:
                client.delete_group(queue=parsed_args.queue, group=group)


class CreateGroup(command.ShowOne):
    _description = _('Create DMS Group')
    columns = ('ID', 'name')

    def get_parser(self, prog_name):
        parser = super(CreateGroup, self).get_parser(prog_name)
        parser.add_argument(
            'queue',
            metavar='<queue>',
            help=_('ID of the queue')
        )
        parser.add_argument(
            'name',
            metavar='<name>',
            help=_('Name of the cluster.')
        )
        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.dms

        obj = client.create_group(queue=parsed_args.queue,
                                  group=parsed_args.name)

        data = utils.get_item_properties(obj, self.columns)

        return (self.columns, data)
