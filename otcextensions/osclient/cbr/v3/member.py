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
'''CBR Share member CLI implementation'''
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _flatten_member(obj):
    """Flatten the structure of the member into a single dict
    """
    data = {
        'id': obj.id,
        'status': obj.status,
        'created_at': obj.created_at,
        'updated_at': obj.updated_at,
        'backup_id': obj.backup_id,
        'image_id': obj.image_id,
        'dest_project_id': obj.dest_project_id,
        'vault_id': obj.vault_id
    }

    return data


def _add_members_to_obj(obj, data, columns):
    """Add members to obj.members
    """
    i = 0
    for member in obj.members:
        name = 'member_' + str(i + 1)
        data += ('\n'.join((f'{a}={v}' for a, v in member[i])),)
        columns = columns + (name, )
        i += 1
    return data, columns


class ListMembers(command.Lister):

    _description = _('List CBR Share Members')
    columns = ('id', 'status', 'created_at', 'updated_at', 'backup_id',
               'image_id', 'dest_project_id', 'vault_id')

    def get_parser(self, prog_name):
        parser = super(ListMembers, self).get_parser(prog_name)
        parser.add_argument(
            'backup',
            metavar='<backup>',
            help=_('Backup name or id.')
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
            '--limit',
            metavar='<limit>',
            type=int,
            help=_('Number of records displayed per page.'
                   ' The value must be a positive integer.')
        )
        parser.add_argument(
            '--marker',
            metavar='<marker>',
            help=_('ID of the last record displayed on the previous page.'
                   ' Only UUID is supported.')
        )
        parser.add_argument(
            '--offset',
            metavar='<offset>',
            type=int,
            help=_('Offset value, which is a positive integer.')
        )
        parser.add_argument(
            '--sort',
            metavar='<sort>',
            choices=['acs', 'desc', 'sort'],
            help=_('A group of properties separated by commas (,)'
                   ' and sorting directions.')
        )
        parser.add_argument(
            '--status',
            metavar='<status>',
            help=_('Status of a shared backup.')
        )
        parser.add_argument(
            '--vault-id',
            metavar='<vault_id>',
            help=_('ID of the vault where the shared backup is stored. '
                   'Only UUID is supported.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.cbr

        query = {}

        if parsed_args.dest_project_id:
            query['dest_project_id'] = parsed_args.dest_project_id
        if parsed_args.image_id:
            query['image_id'] = parsed_args.image_id
        if parsed_args.limit:
            query['limit'] = parsed_args.limit
        if parsed_args.marker:
            query['marker'] = parsed_args.marker
        if parsed_args.offset:
            query['offset'] = parsed_args.offset
        if parsed_args.sort:
            query['sort'] = parsed_args.sort
        if parsed_args.status:
            query['status'] = parsed_args.status
        if parsed_args.vault_id:
            query['vault_id'] = parsed_args.vault_id

        backup = client.find_backup(
            name_or_id=parsed_args.backup, ignore_missing=False)

        members_data = client.members(backup=backup.id, **query)

        table = (self.columns,
                 (utils.get_dict_properties(
                     _flatten_member(s), self.columns,
                 ) for s in members_data))
        return table


class ShowMember(command.ShowOne):
    _description = _('Show single CBR Share Member.')
    columns = ('id', 'status', 'created_at', 'updated_at', 'backup_id',
               'image_id', 'dest_project_id', 'vault_id')

    def get_parser(self, prog_name):
        parser = super(ShowMember, self).get_parser(prog_name)
        parser.add_argument(
            'backup',
            metavar='<backup>',
            help=_('Backup name or id.')
        )
        parser.add_argument(
            'member',
            metavar='<member_id>',
            help=_('Member ID, which is the project ID of the tenant'
                   ' who receives the shared backup.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.cbr

        backup = client.find_backup(
            name_or_id=parsed_args.backup,
            ignore_missing=False
        )
        obj = client.get_member(
            member=parsed_args.member,
            backup=backup.id
        )

        data = utils.get_dict_properties(
            _flatten_member(obj), self.columns)

        return (self.columns, data)


class AddMembers(command.Lister):
    _description = _('Add Share Member.')
    columns = ('id', 'status', 'created_at', 'updated_at', 'backup_id',
               'image_id', 'dest_project_id', 'vault_id')

    def get_parser(self, prog_name):
        parser = super(AddMembers, self).get_parser(prog_name)
        parser.add_argument(
            'backup',
            metavar='<backup>',
            help=_('Backup name or id.')
        )
        parser.add_argument(
            '--members',
            action='append',
            required=True,
            help=_('Project IDs of the backup share members to be added.')
        )
        return parser

    def take_action(self, parsed_args):

        attrs = {}
        client = self.app.client_manager.cbr
        backup = client.find_backup(
            name_or_id=parsed_args.backup,
            ignore_missing=False
        )

        attrs['members'] = parsed_args.members

        client = self.app.client_manager.cbr
        members_data = client.add_members(backup=backup.id,
                                          members=attrs['members'])

        data = (utils.get_dict_properties(_flatten_member(s),
                                          self.columns,) for s in members_data)
        return (self.columns, data)


class UpdateMember(command.ShowOne):
    _description = _('Update the Share Member Status.')
    columns = ('id', 'status', 'created_at', 'updated_at', 'backup_id',
               'image_id', 'dest_project_id', 'vault_id')

    def get_parser(self, prog_name):
        parser = super(UpdateMember, self).get_parser(prog_name)
        parser.add_argument(
            'backup',
            metavar='<backup>',
            help=_('Backup name or id.')
        )
        parser.add_argument(
            'member',
            metavar='<member_id>',
            help=_('Member ID, which is the same ID as in project ID.')
        )
        parser.add_argument(
            '--status',
            metavar='status',
            required=True,
            choices=['accepted', 'pending', 'rejected'],
            help=_('Status of a shared backup.')
        )
        parser.add_argument(
            '--vault-id',
            metavar='vault_id',
            help=_('Specifies the vault in which the shared backup is'
                   ' to be stored. Only UUID is supported. When updating'
                   ' the status of a backup share member status,'
                   ' if the backup is accepted, vault_id must be specified.'
                   ' If the backup is rejected, vault_id is not required.')
        )
        return parser

    def take_action(self, parsed_args):

        attrs = {}
        client = self.app.client_manager.cbr

        attrs['status'] = parsed_args.status

        if parsed_args.vault_id:
            attrs['vault'] = parsed_args.vault_id

        if attrs:
            obj = client.update_member(backup=parsed_args.backup,
                                       member=parsed_args.member, **attrs)

            data = utils.get_dict_properties(
                _flatten_member(obj), self.columns)

            return (self.columns, data)


class DeleteMember(command.Command):
    _description = _('Delete Share Member')

    def get_parser(self, prog_name):
        parser = super(DeleteMember, self).get_parser(prog_name)
        parser.add_argument(
            'backup',
            help=_('Backup name or id.')
        )
        parser.add_argument(
            'member',
            help=_('Member id.')
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.cbr

        backup = client.find_backup(
            name_or_id=parsed_args.backup,
            ignore_missing=False
        )

        self.app.client_manager.cbr.delete_member(
            backup=backup.id, member=parsed_args.member,
            ignore_missing=False)
