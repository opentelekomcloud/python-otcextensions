# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
"""Backup v3 action implementations"""

from osc_lib import utils
from osc_lib.command import command

from otcextensions.common import sdk_utils
from otcextensions.i18n import _


BACKUP_TYPE_CHOICES = ['auto', 'manual', 'fragment', 'incremental']


_formatters = {
}


def _get_columns(item):
    column_map = {}
    hidden = ['location']
    return sdk_utils.get_osc_show_columns_for_sdk_resource(
        item, column_map, hidden)


class ListBackup(command.Lister):
    _description = _("List database backups")
    column_headers = (
        'ID', 'Name', 'Type', 'Instance Id', 'Size (KB)'
    )

    columns = (
        'id', 'name', 'type', 'instance_id', 'size'
    )

    def get_parser(self, prog_name):
        parser = super(ListBackup, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help=_('Specify instance ID or Name to get backup list'),
        )
        parser.add_argument(
            '--backup-id',
            metavar='<backup_id>',
            help=_('Specify the backup ID.'),
        )
        parser.add_argument(
            '--backup-type',
            metavar='{' + ','.join(BACKUP_TYPE_CHOICES) + '}',
            choices=BACKUP_TYPE_CHOICES,
            type=lambda s: s.lower(),
            help=_('Specify the backup type.'),
        )
        parser.add_argument(
            '--offset',
            metavar='<offset>',
            type=int,
            help=_('Specify the index position.'),
        )
        parser.add_argument(
            '--limit',
            metavar='<limit>',
            type=int,
            help=_('Specify the limit of resources to be queried.'),
        )
#         parser.add_argument(
#             '--begin-time',
#             metavar='<begin_time>',
#             help=_('Specify the start time for obtaining the backup list.'),
#         )
#         parser.add_argument(
#             '--end-time',
#             metavar='<end_time>',
#             help=_('Specify the end time for obtaining the backup list.'),
#         )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds
        attrs = {}
        args_list = [
            'backup_id', 'backup_type', 'offset', 'limit'
            # , 'begin_time', 'end_time'
        ]
        for arg in args_list:
            if getattr(parsed_args, arg):
                attrs[arg] = getattr(parsed_args, arg)
        if parsed_args.limit:
            attrs['paginated'] = False

        instance = client.find_instance(parsed_args.instance,
                                        ignore_missing=False)

        data = client.backups(instance=instance, **attrs)

        return (self.column_headers, (utils.get_item_properties(
            s,
            self.columns,
        ) for s in data))


class CreateBackup(command.ShowOne):
    _description = _('Create Database backup')

    def get_parser(self, prog_name):
        parser = super(CreateBackup, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help=_('Name for the backup'))
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help=_('ID or Name of the instance to create backup from'))
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_('Description for the backup'))
        parser.add_argument(
            '--databases',
            metavar='<databases>',
            help=_(
                'Specifies a CSV list of self-built SQL Server'
                'databases that are partially backed up'
                '(Only SQL Server support partial backups.)'))
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds

        attrs = {'name': parsed_args.name}
        if parsed_args.description:
            attrs['description'] = parsed_args.description

        instance = client.find_instance(parsed_args.instance,
                                        ignore_missing=False)

        if (parsed_args.databases
                and instance.datastore['type'].lower() == 'sqlserver'):
            attrs['databases'] = []
            databases = parsed_args.databases
            databases = databases.split(",")
            for db_name in databases:
                attrs['databases'].append({'name': db_name})
        else:
            # Do we want to raise error otherwise?
            pass

        obj = client.create_backup(instance=instance,
                                   **attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns,
                                         formatters=_formatters)

        return (display_columns, data)


class DeleteBackup(command.Command):
    _description = _('Delete Backup')

    def get_parser(self, prog_name):
        parser = super(DeleteBackup, self).get_parser(prog_name)
        parser.add_argument('backup',
                            metavar='<backup_id>',
                            nargs='+',
                            help=_('ID of the backup'))
        return parser

    def take_action(self, parsed_args):

        if parsed_args.backup:
            client = self.app.client_manager.rds
            for bck in parsed_args.backup:
                client.delete_backup(backup=bck, ignore_missing=False)


class ListBackupDownloadLinks(command.Lister):
    _description = _('List Backup Download Links')

    column_headers = ('Size (KB)', 'URL', 'Expires at')
    columns = ('size', 'download_link', 'expires_at')

    def get_parser(self, prog_name):
        parser = super(ListBackupDownloadLinks, self).get_parser(prog_name)
        parser.add_argument('backup_id',
                            metavar='<backup_id>',
                            help=_('ID of the backup'))
        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.rds
        data = client.backup_download_links(backup_id=parsed_args.backup_id)
        return (self.column_headers, (utils.get_item_properties(
            s,
            self.columns,
            formatters={}
        ) for s in data))
