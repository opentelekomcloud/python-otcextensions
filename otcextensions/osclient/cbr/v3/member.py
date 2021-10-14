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
import sys

from osc_lib import utils
from osc_lib.command import command
from openstack import exceptions

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


class AddMember(command.Lister):
    _description = _('Add one or more Project IDs for shared backups.')
    columns = ('ID', 'dest_project_id', 'status')

    def get_parser(self, prog_name):
        parser = super(AddMember, self).get_parser(prog_name)
        parser.add_argument(
            'backup',
            metavar='<backup_id>',
            help=_('The ID of the backup.')
        )
        parser.add_argument(
            '--members',
            metavar='<members>',
            nargs='+',
            required=True,
            help=_('One or more Project IDs to be added for a \n'
                   'backup sharing.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.cbr

        backup = client.find_backup(parsed_args.backup)

        try:
            data = client.add_members(
                backup=backup.id,
                members=parsed_args.members
            )
        except exceptions.BadRequestException as e:
            if (e.message == 'BackupService.6703') and (e.status_code == 400):
                sys.exit('Error: One or more share member already exist.')

        data = client.members(backup)

        table = (self.columns,
                 (utils.get_dict_properties(
                     s, self.columns,
                 ) for s in data))
        return table


class UpdateMember(command.ShowOne):
    _description = _('Update CBR Policy')
    columns = (
        'ID',
        'status',
        'image_id',
        'vault_id',
        'dest_project_id',
        'created_at'
    )

    def get_parser(self, prog_name):
        parser = super(UpdateMember, self).get_parser(prog_name)
        parser.add_argument(
            'backup',
            metavar='<backup_id>',
            help=_('The ID or name of the backup.')
        )
        parser.add_argument(
            '--member-id',
            metavar='<member_id>',
            required=True,
            help=_('Member ID. The member ID is the same as the project ID.')
        )
        parser.add_argument(
            '--status',
            metavar='<status>',
            required=True,
            choices=['accepted', 'pending', 'rejected'],
            help=_('Status of a shared backup.')
        )
        parser.add_argument(
            '--vault-id',
            metavar='<vault_id>',
            required=True,
            help=_('ID of the vault where the shared backup is stored.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.cbr
        attrs = {}

        attrs['backup'] = parsed_args.backup
        attrs['member'] = parsed_args.member_id
        attrs['status'] = parsed_args.status
        if parsed_args.vault_id:
            attrs['vault'] = parsed_args.vault_id

        if attrs:
            obj = client.update_member(**attrs)

        data = utils.get_dict_properties(
            obj, self.columns)

        return (self.columns, data)


class DeleteMember(command.Command):
    _description = _('Delete CBR Policy')

    def get_parser(self, prog_name):
        parser = super(DeleteMember, self).get_parser(prog_name)
        parser.add_argument(
            'backup',
            metavar='<backup_id>',
            help=_('The ID or name of the backup.')
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

        member = parsed_args.member_id
        backup = parsed_args.backup

        try:
            client.delete_member(
                member=member,
                backup=backup,
                ignore_missing=False
            )
        except exceptions.NotFoundException as e:
            if (e.message == 'BackupService.6705'):
                sys.exit('Error: Backup/Member not found.')
