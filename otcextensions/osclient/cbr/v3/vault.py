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
'''CBR Vault CLI implementation'''
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _flatten_vault(obj):
    """Flatten the structure of the vault into a single dict
    """
    data = {
        'id': obj.id,
        'name': obj.name,
        'auto_bind': obj.auto_bind,
        'auto_expand': obj.auto_expand,
        'backup_policy_id': obj.backup_policy_id,
        'created_at': obj.created_at,
        'description': obj.description,
        'project_id': obj.project_id,
        'provider_id': obj.provider_id,
        'user_id': obj.user_id,
        # 'billing': obj.billing,
        # 'bind_rules': obj.bind_rules,
        # 'resources': obj.resources,
        # 'tags': obj.tags,
    }

    return data


class ListVaults(command.Lister):
    _description = _('List CBR Vaults')
    columns = ('ID', 'name', 'backup_policy_id', 'description', 'created_at')

    def get_parser(self, prog_name):
        parser = super(ListVaults, self).get_parser(prog_name)

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.cbr

        data = client.vaults()

        table = (self.columns,
                 (utils.get_dict_properties(
                     _flatten_vault(s), self.columns,
                 ) for s in data))
        return table


class ShowVault(command.ShowOne):
    _description = _('Show single Vault details')
    columns = (
        'ID',
        'name',
        'auto_bind',
        'auto_expand',
        'backup_policy_id',
        'created_at',
        'description',
        'project_id',
        'provider_id',
        'user_id',
    )

    def get_parser(self, prog_name):
        parser = super(ShowVault, self).get_parser(prog_name)
        parser.add_argument(
            'vault',
            metavar='<vault>',
            help=_('ID or name of the CBR vault.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.cbr

        obj = client.find_policy(
            name_or_id=parsed_args.policy,
            ignore_missing=False
        )

        data = utils.get_dict_properties(
            _flatten_vault(obj), self.columns)

        return self.columns, data


class CreateVault(command.ShowOne):
    _description = _('Create CBR Vault')
    columns = (
    )


class UpdateVault(command.ShowOne):
    _description = _('Update CBR Vault')
    columns = (
    )


class DeleteVault(command.Command):
    _description = _('Delete CBR Vault')

    def get_parser(self, prog_name):
        parser = super(DeleteVault, self).get_parser(prog_name)
        parser.add_argument(
            'vault',
            metavar='<vault>',
            help=_('ID or name of the CBR Vault.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.cbr

        vault = client.find_vault(
            name_or_id=parsed_args.vault,
            ignore_missing=False
        )

        self.app.client_manager.cbr.delete_vault(
            vault=vault.id,
            ignore_missing=False)
