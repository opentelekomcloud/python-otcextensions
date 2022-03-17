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
'''CBR Restore point CLI implementation'''
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _flatten_checkpoint(obj):
    """Flatten the structure of the checkpoint into a single dict
    """
    vault_id, vault_name, backup_name = ('', '', '')
    if obj.vault:
        vault_id = obj.vault.id
        vault_name = obj.vault.name
    if obj.extra_info:
        backup_name = obj.extra_info.name
    data = {
        'created_at': obj.created_at,
        'id': obj.id,
        'project_id': obj.project_id,
        'status': obj.status,
        'name': obj.name,
        'vault_id': vault_id,
        'vault_name': vault_name,
        'backup_name': backup_name
    }

    return data


def _normalize_resources(resource_details):
    result = []
    for rd in resource_details:
        res = dict(map(lambda s: s.split('='), rd.split(' ')))
        result.append(res)
    return result


def _add_resources_to_obj(obj, data, columns):
    """Add resources to obj.vault
    """
    i = 0
    for s in obj.vault.resources:
        if obj.vault.resources[i].id:
            name = 'resource_' + str(i + 1)
            data += (obj.vault.resources[i].id,)
            columns = columns + (name,)
            i += 1
    return data, columns


def _add_skipped_resources_to_obj(obj, data, columns):
    """Add skipped resources to obj.vault
    """
    i = 0
    for s in obj.vault.skipped_resources:
        if obj.vault.resources[i].id:
            name = 'skipped_resource_' + str(i + 1)
            data += (obj.vault.skipped_resources[i].id,)
            columns = columns + (name,)
            i += 1
    return data, columns


class ShowCheckpoint(command.ShowOne):
    _description = _('Show single restore point details')
    columns = (
        'created_at',
        'id',
        'status',
        'name',
        'vault_id',
        'vault_name',
        'backup_name'
    )

    def get_parser(self, prog_name):
        parser = super(ShowCheckpoint, self).get_parser(prog_name)
        parser.add_argument(
            'checkpoint',
            metavar='<checkpoint>',
            help=_('ID of the CBR checkpoint.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.cbr

        obj = client.get_checkpoint(
            checkpoint=parsed_args.checkpoint
        )

        data = utils.get_dict_properties(
            _flatten_checkpoint(obj), self.columns)

        return (self.columns, data)


class CreateCheckpoint(command.ShowOne):
    _description = _('Create CBR Restore point')
    columns = (
        'created_at',
        'id',
        'status',
        'name',
        'vault_id',
        'vault_name',
        'backup_name'
    )

    def get_parser(self, prog_name):
        parser = super(CreateCheckpoint, self).get_parser(prog_name)

        parser.add_argument(
            '--vault-id',
            metavar='<vault_id>',
            required=True,
            help=_('Vault id.')
        )
        parser.add_argument(
            '--auto-trigger',
            dest='auto_trigger',
            action='store_true',
            help=_('Whether automatic triggering is enabled.')
        )
        parser.add_argument(
            '--description',
            default='backup',
            help=_('Backup description.')
        )
        parser.add_argument(
            '--no-incremental',
            dest='no_incremental',
            action='store_false',
            help=_('Scheduling rule.\n'
                   'Repeat Option for multiple rules.')
        )
        parser.add_argument(
            '--backup-name',
            metavar='backup_name',
            help=_('Backup name.')
        )
        parser.add_argument(
            '--resources',
            action='append',
            help=_('UUID list of resources to be backed up.')
        )

        parser.add_argument(
            '--resource-details',
            metavar='<resource_details>',
            action='append',
            help=_('Associated resource in "id=resource_id '
                   'type=resource_type name=resource_name" format.'
                   'Repeat for multiple values.')
        )

        return parser

    def take_action(self, parsed_args):

        attrs = {
            'parameters': {},
        }

        # mandatory
        attrs['vault_id'] = parsed_args.vault_id

        # optional

        if parsed_args.auto_trigger is not None:
            attrs['parameters'].update(auto_trigger=parsed_args.auto_trigger)
        if parsed_args.description:
            attrs['parameters'].update(
                description=parsed_args.description)
        if parsed_args.no_incremental is not None:
            attrs['parameters'].update(incremental=parsed_args.no_incremental)
        if parsed_args.backup_name:
            attrs['parameters'].update(
                name=parsed_args.backup_name)
        if parsed_args.resources:
            attrs['parameters'].update(
                resources=parsed_args.resources)
        if parsed_args.resource_details:
            attrs['parameters'].update(resource_details=_normalize_resources(
                parsed_args.resource_details))

        client = self.app.client_manager.cbr
        obj = client.create_checkpoint(**attrs)

        data = utils.get_dict_properties(
            _flatten_checkpoint(obj), self.columns)

        if obj.vault.resources:
            data, self.columns = _add_resources_to_obj(obj, data, self.columns)

        if obj.vault.skipped_resources:
            data, self.columns = _add_skipped_resources_to_obj(obj, data,
                                                               self.columns)

        return (self.columns, data)
