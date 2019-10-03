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
"""Backup v3 action implementations"""
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def set_attributes_for_print_detail(obj):
    info = {}
    attr_list = [
        'id',
        'name',
        'type',
        'size',
        'status',
        'begin_time',
        'end_time',
        'instance_id']
    for attr in dir(obj):
        if attr == 'datastore' and getattr(obj, attr):
            info['datastore_type'] = obj.datastore['type']
            info['datastore_version'] = obj.datastore['version']
        elif attr == 'databases' and getattr(obj, attr):
            info['databases'] = []
            for database in obj.databases:
                info['databases'].append(database['name'])
        elif attr in attr_list and getattr(obj, attr):
            info[attr] = getattr(obj, attr)
    return info


class ListBackup(command.Lister):

    _description = _("List database backups/snapshots")
    columns = (
        'ID',
        'Name',
        'Type',
        'Instance Id',
        'Datastore Type',
        'Datastore Version')

    def get_parser(self, prog_name):
        parser = super(ListBackup, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help=_('Specify instance ID or Name to get backup list'),
        )
        parser.add_argument(
            '--backup_id',
            metavar='<backup_id>',
            help=_('Specify the backup ID.'),
        )
        parser.add_argument(
            '--backup_type',
            metavar='<backup_type>',
            choices=['auto', 'manual', 'fragment', 'incremental'],
            help=_('Specify the backup type.'),
        )
        parser.add_argument(
            '--offset',
            metavar='<offset>',
            help=_('Specify the index position.'),
        )
        parser.add_argument(
            '--limit',
            metavar='<limit>',
            help=_('Specify the limit of resources to be queried.'),
        )
        parser.add_argument(
            '--begin_time',
            metavar='<begin_time>',
            help=_('Specify the start time for obtaining the backup list.'),
        )
        parser.add_argument(
            '--end_time',
            metavar='<end_time>',
            help=_('Specify the end time for obtaining the backup list.'),
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds
        attrs = {}
        args_list = [
            'backup_id',
            'backup_type',
            'offset',
            'limit',
            'begin_time',
            'end_time']
        for arg in args_list:
            if getattr(parsed_args, arg):
                attrs[arg] = getattr(parsed_args, arg)

        data = client.backups(parsed_args.instance, **attrs)

        return (
            self.columns,
            (utils.get_dict_properties(
                set_attributes_for_print_detail(s),
                self.columns,
            ) for s in data)
        )


class CreateBackup(command.ShowOne):
    _description = _('Create Database backup')

    columns = ('ID', 'Name', 'type', 'instance_id',
               'status', 'begin_time', 'databases')

    def get_parser(self, prog_name):
        parser = super(CreateBackup, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help=_('Name for the backup')
        )
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help=_('ID or Name of the instance to create backup from')
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_('Description for the backup')
        )
        parser.add_argument(
            '--databases',
            metavar='<databases>',
            help=_('Specifies a list of self-built SQL Server'
                    'databases that are partially backed up'
                    '(Only SQL Server support partial backups.)')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds

        attrs = {'name': parsed_args.name}
        if parsed_args.description:
            attrs['description'] = parsed_args.description
        if parsed_args.databases:
            attrs['databases'] = []
            databases = parsed_args.databases
            databases = databases.split(",")
            for db_name in databases:
                attrs['databases'].append({'name': db_name})

        data = client.create_backup(parsed_args.instance, **attrs)

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
