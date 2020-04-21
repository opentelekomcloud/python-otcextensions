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
'''DMS Topic v1 action implementations'''
from osc_lib import utils
from osc_lib.command import command

from otcextensions.common import sdk_utils
from otcextensions.i18n import _


def _get_columns(item):
    column_map = {}
    hidden = ['location']
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map,
                                                           hidden)


class ListDMSInstanceTopic(command.Lister):
    _description = _('List DMS Instance topics')
    columns = ('ID', 'replication', 'partition', 'retention_time',
               'is_sync_flush', 'is_sync_replication')

    def get_parser(self, prog_name):
        parser = super(ListDMSInstanceTopic, self).get_parser(prog_name)

        parser.add_argument(
            'instance',
            metavar='<instance>',
            help=_('DMS Instance name or ID')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dms

        instance_obj = client.find_instance(parsed_args.instance,
                                            ignore_missing=False)
        data = client.topics(instance=instance_obj)

        table = (self.columns,
                 (utils.get_item_properties(
                     s, self.columns,
                 ) for s in data))
        return table


class DeleteDMSInstanceTopic(command.Command):
    _description = _('Delete DMS Instance Topic')

    def get_parser(self, prog_name):
        parser = super(DeleteDMSInstanceTopic, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help=_('ID or name of the Instance')
        )
        parser.add_argument(
            'topic',
            metavar='<topic>',
            nargs='+',
            help=_('Topic ID')
        )
        return parser

    def take_action(self, parsed_args):

        if parsed_args.instance:
            client = self.app.client_manager.dms
            instance = client.find_instance(
                parsed_args.instance,
                ignore_missing=False)
            client.delete_topic(instance=instance, topics=parsed_args.topic)


class CreateDMSInstanceTopic(command.ShowOne):
    _description = _('Create DMS Instance Topic')

    def get_parser(self, prog_name):
        parser = super(CreateDMSInstanceTopic, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help=_('Instance ID or Name.')
        )
        parser.add_argument(
            'id',
            metavar='<id>',
            help=_('Name/ID of the topic.')
        )
        parser.add_argument(
            '--partition',
            metavar='<part>',
            type=int,
            choices=range(1, 21),
            help=_(
                'The number of topic partitions, which is used to set the '
                'number of concurrently consumed messages. '
                'Value range: 1–20. Default value: 3.')
        )
        parser.add_argument(
            '--replication',
            metavar='<repl>',
            type=int,
            choices=range(1, 4),
            help=_(
                'The number of replicas, which is configured to ensure data '
                'reliability. Value range: 1–3. Default value: 3.')
        )
        parser.add_argument(
            '--retention-time',
            metavar='<hours>',
            type=int,
            choices=range(1, 169),
            default=72,
            help=_(
                'The retention period of a message. Its default value is '
                '72. Value range: 1–168. Default value: 72. Unit: hour.')
        )
        parser.add_argument(
            '--enable-sync-flush',
            action='store_true',
            help=_(
                'Whether to enable synchronous flushing. '
                'Default value: false. Synchronous flushing compromises '
                'performance.')
        )
        parser.add_argument(
            '--enable-sync-replication',
            action='store_true',
            help=_(
                'Whether to enable synchronous replication. After this '
                'function is enabled, the acks parameter on the producer '
                'client must be set to –1. Otherwise, this parameter does '
                'not take effect.')
        )
        return parser

    def take_action(self, parsed_args):

        attrs = {}

        attrs['id'] = parsed_args.id
        for attr in ['partition', 'replication', 'retention_time']:
            val = getattr(parsed_args, attr)
            if val is not None:
                attrs[attr] = val
        if parsed_args.enable_sync_flush:
            attrs['is_sync_flush'] = True
        if parsed_args.enable_sync_replication:
            attrs['is_sync_replication'] = True

        client = self.app.client_manager.dms

        instance = client.find_instance(parsed_args.instance,
                                        ignore_missing=False)

        obj = client.create_topic(instance=instance, **attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)
