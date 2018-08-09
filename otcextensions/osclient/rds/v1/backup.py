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
"""Backup v1 action implementations"""
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def set_attributes_for_print_detail(obj):
    info = {}  # instance.copy()
    info['id'] = obj.id
    info['name'] = obj.name
    info['instance_id'] = obj.instance_id
    info['size'] = obj.size
    info['status'] = obj.status
    info['created'] = obj.created
    info['updated'] = obj.updated
    if obj.datastore:
        info['datastore_type'] = obj.datastore['type']
        info['datastore_version'] = obj.datastore['version']

    return info


class ListBackup(command.Lister):

    _description = _("List database backups/snapshots")
    columns = ('ID', 'Name', 'instance_id', 'datastore_type',
               'datastore_version',
               'size', 'status', 'created', 'updated')

    def get_parser(self, prog_name):
        parser = super(ListBackup, self).get_parser(prog_name)

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds

        data = client.backups()

        return (
            self.columns,
            (utils.get_dict_properties(
                set_attributes_for_print_detail(s),
                self.columns,
            ) for s in data)
        )


class CreateBackup(command.ShowOne):
    _description = _('Create Database backup')

    columns = ('ID', 'Name', 'instance_id', 'datastore_type',
               'datastore_version',
               'size', 'status', 'created', 'updated')

    def get_parser(self, prog_name):
        parser = super(CreateBackup, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help=_('ID of the instance to take backup from')
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            required=True,
            help=_('Name for the backup')
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_('Description for the backup')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds

        info = {}

        info['name'] = parsed_args.name
        if parsed_args.description:
            info['description'] = parsed_args.description

        data = client.create_backup(instance=parsed_args.instance,
                                    **info)

        return (
            self.columns,
            utils.get_dict_properties(
                set_attributes_for_print_detail(data),
                self.columns,
            )
        )


class DeleteBackup(command.Command):
    _description = _('Delete Backup')

    def get_parser(self, prog_name):
        parser = super(DeleteBackup, self).get_parser(prog_name)
        parser.add_argument(
            'backup',
            metavar='<backup>',
            nargs='+',
            help=_('ID of the backup')
        )
        return parser

    def take_action(self, parsed_args):

        if parsed_args.backup:
            client = self.app.client_manager.rds
            for bck in parsed_args.backup:
                client.delete_backup(
                    backup=bck,
                    ignore_missing=False)
