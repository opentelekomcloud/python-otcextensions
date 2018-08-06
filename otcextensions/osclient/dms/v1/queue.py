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
'''DMS Queue v1 action implementations'''
import argparse
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


class ListDMSQueue(command.Lister):
    _description = _('List DMS Queues')
    columns = ('ID', 'name', 'queue_mode', 'description', 'redrive_policy',
               'max_consume_count', 'retention_hours')

    def get_parser(self, prog_name):
        parser = super(ListDMSQueue, self).get_parser(prog_name)

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dms

        data = client.queues()

        table = (self.columns,
                 (utils.get_item_properties(
                     s, self.columns,
                 ) for s in data))
        return table


class ShowDMSQueue(command.ShowOne):
    _description = _('Show single Queue details')
    columns = ('ID', 'name', 'queue_mode', 'description', 'redrive_policy',
               'max_consume_count', 'retention_hours')

    def get_parser(self, prog_name):
        parser = super(ShowDMSQueue, self).get_parser(prog_name)
        parser.add_argument(
            'queue',
            metavar='<queue>',
            help=_('ID of the queue')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dms

        obj = client.get_queue(parsed_args.queue)

        # display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, self.columns)

        return (self.columns, data)


class DeleteDMSQueue(command.Command):
    _description = _('Delete DMS Queue')

    def get_parser(self, prog_name):
        parser = super(DeleteDMSQueue, self).get_parser(prog_name)
        parser.add_argument(
            'queue',
            metavar='<queue>',
            help=_('ID of the queue')
        )
        return parser

    def take_action(self, parsed_args):

        if parsed_args.cluster:
            client = self.app.client_manager.dms
            client.delete_queue(parsed_args.queue)


class CreateDMSQueue(command.Command):
    _description = _('Create DMS Queue')
    columns = ('ID', 'name', 'queue_mode', 'description', 'redrive_policy',
               'max_consume_count', 'retention_hours')

    def get_parser(self, prog_name):
        parser = super(CreateDMSQueue, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            required=True,
            help=_('Name of the cluster.')
        )
        parser.add_argument(
            'queue_mode',
            metavar='<queue_mode>',
            help=_('Indicates the queue type.\n'
                   'Options:\n'
                   '* `NORMAL`: Standard queue. Best-effort ordering. '
                   'Messages might be retrieved in an order different from '
                   'which they were sent. Select standard queues when '
                   'throughput is important.\n'
                   '* `FIFO`: First-ln-First-out (FIFO) queue. FIFO delivery. '
                   'Messages are retrieved in the order they were sent. '
                   'Select FIFO queues when the order of messages is '
                   'important.\n'
                   '* `KAFKA_HA`: High-availability Kafka queue. All message '
                   'replicas are flushed to a disk synchronously. Select the '
                   'high availability mode when message reliability is '
                   'important.\n'
                   '* `KAFKA_HT`: High-throughput Kafka queue. All message '
                   'replicas are flushed to a disk asynchronously. Select the '
                   'high throughput mode when message delivery performance '
                   'is important.\n'
                   'Default value: `NORMAL`.')
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_('Indicates the basic information about a queue.\n'
                   'The queue description must be 0 to 160 characters in '
                   'length, and does not contain angle brackets (<) and (>).\n'
                   'NOTE: "\\" is defined as an escape character in the queue '
                   'description. If you need to enter a backward slash (\\) '
                   'or a double quotation mark (") in the queue description, '
                   'enter \\ or \\" ')
        )
        parser.add_argument(
            '--redrive_policy',
            metavar='<redrive_policy>',
            help=_('This parameter is mandatory only when queue_mode is '
                   'NORMAL or FIFO.\n'
                   'Indicates whether to enable dead letter messages. '
                   'Dead letter messages indicate messages that cannot be '
                   'normally consumed.\n'
                   'If a message fails to be consumed after the number of '
                   'consumption attempts of this message reaches the maximum '
                   'value, DMS stores this message into the dead letter queue.'
                   'This message will be retained in the deal letter queue '
                   'for 72 hours. During this period, consumers can consume '
                   'the dead letter message.\n'
                   'Dead letter messages can be consumed only by the consumer '
                   'group that generates these dead letter messages.\n'
                   'Dead letter messages of a FIFO queue are stored and '
                   'consumed based on the FIFO sequence.\n'
                   'Options:\n'
                   '* `enable`\n'
                   '* `disable`\n'
                   'Default value: disable.')
        )
        parser.add_argument(
            '--max_consume_count',
            metavar='<max_consume_count>',
            type=int,
            help=_('This parameter is mandatory only when redrive_policy '
                   'is set to enable.\n'
                   'This parameter indicates the maximum number of allowed '
                   'message consumption failures. When a message fails to be '
                   'consumed after the number of consumption attempts of '
                   'this message reaches this value, DMS stores this message '
                   'into the dead letter queue.\n'
                   'Value range: 1–100.')
        )
        parser.add_argument(
            '--retention_hours',
            metavar='<retention_hours>',
            type=int,
            help=_('This parameter is mandatory only when queue_mode is '
                   'set to KAFKA_HA or KAFKA_HT.\n'
                   'This parameter indicates the retention time of messages '
                   'in Kafka queues.\n'
                   'Value range: 1 to 72 hours.')
        )
        return parser

    def take_action(self, parsed_args):

        attrs = {}

        attrs['name'] = parsed_args.name
        if parsed_args.queue_mode:
            mode = parsed_args.queue_mode.upper()
            if mode in ('NORMAL', 'FIFO', 'KAFKA_HA', 'KAFKA_HT'):
                attrs['queue_mode'] = mode
            else:
                msg = _('Queue mode is not in (NORMAL, FIFO, KAFKA_HA, '
                        'KAFKA_HT)')
                raise argparse.ArgumentTypeError(msg)
        if parsed_args.description:
            attrs['description'] = parsed_args.description
        if parsed_args.redrive_policy:
            attrs['redrive_policy'] = parsed_args.redrive_policy
        if parsed_args.retention_hours:
            attrs['retention_hours'] = parsed_args.retention_hours
        if parsed_args.max_consume_count:
            attrs['max_consume_count'] = parsed_args.max_consume_count

        client = self.app.client_manager.dms

        obj = client.create_queue(**attrs)

        data = utils.get_item_properties(obj, self.columns)

        return (self.columns, data)
