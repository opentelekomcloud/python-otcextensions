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
'''CBR Policy CLI implementation'''
import logging

from osc_lib import utils
from osc_lib import exceptions
from osc_lib.command import command

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _flatten_backup(obj):
    """Flatten the structure of the backup into a single dict
    """
    data = {
        'id': obj.id,
        'name': obj.name,
        'checkpoint_id': obj.checkpoint_id,
        'created_at': obj.created_at,
        'description': obj.description,
        'expired_at': obj.expired_at,
        'image_type': obj.image_type,
        'parent_id': obj.parent_id,
        'project_id': obj.project_id,
        'protected_at': obj.protected_at,
        'resource_az': obj.resource_az,
        'resource_id': obj.resource_id,
        'resource_name': obj.resource_name,
        'resource_size': obj.resource_size,
        'resource_type': obj.resource_type,
        'status': obj.status,
        'updated_at': obj.updated_at,
        'vault_id': obj.vault_id,
        'provider_id': obj.provider_id
    }

    return data


def _add_children_to_backup_obj(obj, data, columns):
    """Add children to column and data tuples
    """
    i = 0
    for s in obj.children:
        if obj.children[i]['id']:
            name = 'child_backup_' + str(i + 1)
            data += (obj.children[i]['id'],)
            columns = columns + (name,)
            i += 1
    return data, columns


class ListBackups(command.Lister):
    _description = _('List CBR Backups')
    columns = (
        'id',
        'name',
        'checkpoint_id',
        'created_at',
        'description',
        'expired_at',
        'image_type',
        'parent_id',
        'project_id',
        'protected_at',
        'resource_az',
        'resource_id',
        'resource_name',
        'resource_size',
        'resource_type',
        'status',
        'updated_at',
        'vault_id',
        'provider_id'
    )

    def get_parser(self, prog_name):
        parser = super(ListBackups, self).get_parser(prog_name)
        parser.add_argument(
            '--checkpoint-id',
            metavar='<checkpoint_id>',
            help=_('The ID of the restore point.')
        )
        parser.add_argument(
            '--dec',
            metavar='<dec>',
            type=bool,
            help=_('Dedicated cloud')
        )
        parser.add_argument(
            '--end-time',
            metavar='<end_time>',
            help=_('Time when the backup ends.')
        )
        parser.add_argument(
            '--image-type',
            metavar='<image_type>',
            choices=['backup', 'replication'],
            help=_('Backup type')
        )
        parser.add_argument(
            '--limit',
            metavar='<limit>',
            type=int,
            help=_('Number of records displayed per page.')
        )
        parser.add_argument(
            '--marker',
            metavar='<marker>',
            help=_('ID of the last record displayed on the previous page.')
        )
        parser.add_argument(
            '--member-status',
            metavar='<member_status>',
            choices=['pending', 'accept', 'reject'],
            help=_('The ID of the restore point.')
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_('Backup name.')
        )
        parser.add_argument(
            '--offset',
            type=int,
            metavar='<offset>',
            help=_('Offset value. The value must be a positive integer.')
        )
        parser.add_argument(
            '--own-type',
            metavar='<own_type>',
            choices=['all_granted', 'private', 'shared'],
            help=_('Owning type of a backup. private backups are queried'
                   ' by default.')
        )
        parser.add_argument(
            '--parent-id',
            metavar='<parent_id>',
            help=_('Parent backup ID.')
        )
        parser.add_argument(
            '--resource-az',
            metavar='<resource_az>',
            help=_('AZ-based filtering is supported.')
        )
        parser.add_argument(
            '--resource-id',
            metavar='<resource_id>',
            help=_('Resource ID.')
        )
        parser.add_argument(
            '--resource-name',
            metavar='<resource_name>',
            help=_('Resource name.')
        )
        parser.add_argument(
            '--resource-type',
            metavar='<resource_type>',
            choices=['OS::Cinder::Volume', 'OS::Nova::Server'],
            help=_('Resource type.')
        )
        parser.add_argument(
            '--sort',
            metavar='sort',
            help=_('A group of properties separated by commas (,)'
                   ' and sorting directions.')
        )
        parser.add_argument(
            '--start-time',
            metavar='<start_time>',
            help=_('Time when the backup starts.')
        )
        parser.add_argument(
            '--status',
            metavar='status',
            choices=['available', 'protecting', 'deleting', 'restoring',
                     'error', 'waiting_protect', 'waiting_delete',
                     'waiting_restore'],
            help=_('Status')
        )
        parser.add_argument(
            '--used-percent',
            metavar='<used_percent>',
            help=_('Backups are filtered based on the occupied vault capacity.')
        )
        parser.add_argument(
            '--vault-id',
            metavar='<vault_id>',
            help=_('Vault ID.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.cbr

        query = {}

        if parsed_args.checkpoint_id:
            query['checkpoint_id'] = parsed_args.checkpoint_id
        if parsed_args.dec:
            query['dec'] = parsed_args.dec
        if parsed_args.end_time:
            query['end_time'] = parsed_args.end_time
        if parsed_args.image_type:
            query['image_type'] = parsed_args.image_type
        if parsed_args.limit:
            query['limit'] = parsed_args.limit
        if parsed_args.marker:
            query['marker'] = parsed_args.marker
        if parsed_args.member_status:
            query['member_status'] = parsed_args.member_status
        if parsed_args.name:
            query['name'] = parsed_args.name
        if parsed_args.offset:
            query['offset'] = parsed_args.offset
        if parsed_args.own_type:
            query['own_type'] = parsed_args.own_type
        if parsed_args.parent_id:
            query['parent_id'] = parsed_args.parent_id
        if parsed_args.resource_az:
            query['resource_az'] = parsed_args.resource_az
        if parsed_args.resource_id:
            query['resource_id'] = parsed_args.resource_id
        if parsed_args.resource_name:
            query['resource_name'] = parsed_args.resource_name
        if parsed_args.resource_type:
            query['resource_type'] = parsed_args.resource_type
        if parsed_args.sort:
            query['sort'] = parsed_args.sort
        if parsed_args.start_time:
            query['start_time'] = parsed_args.start_time
        if parsed_args.status:
            query['status'] = parsed_args.status
        if parsed_args.used_percent:
            query['used_percent'] = parsed_args.used_percent
        if parsed_args.vault_id:
            query['vault_id'] = parsed_args.vault_id

        data = client.backups(**query)

        table = (self.columns,
                 (utils.get_dict_properties(
                     _flatten_backup(s), self.columns,
                 ) for s in data))
        return table


class ShowBackup(command.ShowOne):
    _description = _('Show single Backup details')
    columns = (
        'id',
        'name',
        'checkpoint_id',
        'created_at',
        'description',
        'expired_at',
        'image_type',
        'parent_id',
        'project_id',
        'protected_at',
        'resource_az',
        'resource_id',
        'resource_name',
        'resource_size',
        'resource_type',
        'status',
        'updated_at',
        'vault_id',
        'provider_id'
    )

    def get_parser(self, prog_name):
        parser = super(ShowBackup, self).get_parser(prog_name)
        parser.add_argument(
            'backup',
            metavar='<backup>',
            help=_('ID or name of the CBR backup.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.cbr

        obj = client.find_backup(
            name_or_id=parsed_args.backup,
            ignore_missing=False
        )

        data = utils.get_dict_properties(
            _flatten_backup(obj), self.columns)

        if obj.children:
            data, self.columns = _add_children_to_backup_obj(
                obj, data, self.columns)

        return (self.columns, data)


class DeleteBackup(command.Command):
    _description = _('Delete CBR Backup')

    def get_parser(self, prog_name):
        parser = super(DeleteBackup, self).get_parser(prog_name)
        parser.add_argument(
            'backup',
            metavar='<backup>',
            help=_('ID or name of the CBR Backup.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.cbr

        backup = client.find_backup(
            name_or_id=parsed_args.backup,
            ignore_missing=False
        )

        self.app.client_manager.cbr.delete_backup(
            backup=backup.id,
            ignore_missing=False)


class RestoreBackup(command.Command):
    _description = _('Restore CBR Backup data')

    columns = (
        'id',
        'name',
        'checkpoint_id',
        'created_at',
        'description',
        'expired_at',
        'image_type',
        'parent_id',
        'project_id',
        'protected_at',
        'resource_az',
        'resource_id',
        'resource_name',
        'resource_size',
        'resource_type',
        'status',
        'updated_at',
        'vault_id',
        'provider_id',
    )

    def get_parser(self, prog_name):
        parser = super(RestoreBackup, self).get_parser(prog_name)
        parser.add_argument(
            '--backup-id',
            metavar='<backup_id>',
            required=True,
            help=_('Disk backup ID.')
        )
        parser.add_argument(
            '--volume-id',
            metavar='<volume_id>',
            required=True,
            help=_('ID of the disk to which data is restored.')
        )
        parser.add_argument(
            '--power-on',
            metavar='<power_on>',
            type=bool,
            help=_('Whether the server is powered on after restoration. ')
        )
        parser.add_argument(
            '--server-id',
            metavar='<server_id>',
            help=_('ID of the target VM to be restored. This parameter is'
                   ' mandatory for VM restoration.')
        )
        parser.add_argument(
            '--target-disk-volume-id',
            metavar='<target_disk_volume_id>',
            help=_('ID of the target disk to be restored. This parameter is'
                   ' mandatory for disk restoration..')
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.cbr

        query = {}

        if parsed_args.backup_id:
            query['backup_id'] = parsed_args.backup_id

        if parsed_args.volume_id:
            query['volume_id'] = parsed_args.volume_id

        if parsed_args.power_on:
            query['power_on'] = parsed_args.power_on

        if parsed_args.server_id:
            query['server_id'] = parsed_args.server_id

        if parsed_args.volume_id:
            query['target_disk_volume_id'] = parsed_args.target_disk_volume_id

        obj = self.app.client_manager.cbr.restore_data(
            **query)

        data = utils.get_dict_properties(
            _flatten_backup(obj), self.columns)

        if obj.children:
            data, self.columns = _add_children_to_backup_obj(
                obj, data, self.columns)

        return (self.columns, data)

