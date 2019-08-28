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
'''DCS Backup v1 action implementations'''
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.common import sdk_utils

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _get_columns(item):
    column_map = {
    }
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


class ListBackup(command.Lister):
    _description = _('List backups of a single DCS instance')
    columns = ('id', 'name', 'progress', 'status', 'error_code')

    def get_parser(self, prog_name):
        parser = super(ListBackup, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help=_('Name or ID of the instance')
        )
        parser.add_argument(
            '--limit',
            metavar='<limit>',
            type=int,
            help=_('Limit number of records to return.')
        )
        parser.add_argument(
            '--start',
            metavar='<start>',
            type=int,
            help=_('Start number for querying.')
        )
        parser.add_argument(
            '--from_time',
            metavar='<yyyyMMddHHmmss>',
            help=_('Start time of the period to be queried.')
        )
        parser.add_argument(
            '--to_time',
            metavar='<yyyyMMddHHmmss>',
            help=_('End time of the period to be queried.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dcs

        query = {}
        if parsed_args.limit:
            query['limit'] = parsed_args.limit
        if parsed_args.start:
            query['start'] = parsed_args.start
        if parsed_args.from_time:
            query['begin_time'] = parsed_args.from_time
        if parsed_args.to_time:
            query['end_time'] = parsed_args.to_time

        inst = client.find_instance(name_or_id=parsed_args.instance,
                                    ignore_missing=False)
        data = client.backups(
            instance={'id': inst.id},
            **query
        )

        table = (self.columns,
                 (utils.get_item_properties(
                     s, self.columns,
                 ) for s in data))
        return table


class DeleteBackup(command.Command):
    _description = _('Delete DCS instance backup')

    def get_parser(self, prog_name):
        parser = super(DeleteBackup, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help=_('ID of the instance.')
        )
        parser.add_argument(
            'backup',
            metavar='<backup>',
            nargs='+',
            help=_('ID of the instance backup to delete.')
        )
        return parser

    def take_action(self, parsed_args):

        if parsed_args.instance:
            client = self.app.client_manager.dcs
            inst = client.find_instance(name_or_id=parsed_args.instance,
                                        ignore_missing=False)
            for backup in parsed_args.backup:
                client.delete_instance_backup(
                    backup=backup,
                    instance_id=inst.id
                )


class CreateBackup(command.ShowOne):
    _description = _('Create a backup of a DCS instance')

    def get_parser(self, prog_name):
        parser = super(CreateBackup, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help=_('Name or ID of the DCS instance to take backup from.')
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_('Description of the backup.')
        )
        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.dcs

        attrs = {}

        if parsed_args.description:
            attrs['description'] = parsed_args.description

        inst = client.find_instance(name_or_id=parsed_args.instance,
                                    ignore_missing=False)

        obj = client.backup_instance(
            instance={'id': inst.id},
            **attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)
