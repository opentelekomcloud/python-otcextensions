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
        'status': obj.billing.status,
        'operation_type': obj.billing.protect_type,
        'object_type': obj.billing.object_type,
        'spec_code': obj.billing.spec_code,
        'size': obj.billing.size,
        'consistent_level': obj.billing.consistent_level,
        'charging_mode': obj.billing.charging_mode,
        'is_auto_pay': obj.billing.is_auto_pay,
        'is_auto_renew': obj.billing.is_auto_renew,
        'bind_rules': obj.bind_rules.tags,
        'resources': obj.resources,
        'tags': obj.tags,
    }

    return data


def _add_resources_to_vault_obj(obj, data, columns):
    """Add associated resources to column and data tuples
    """
    i = 0
    for s in obj.resources:
        if obj.resources[i].id:
            name = 'resource_id_' + str(i + 1)
            data += (obj.resources[i].id,)
            columns = columns + (name,)

            name = 'resource_type_' + str(i + 1)
            data += (obj.resources[i].type,)
            columns = columns + (name,)

            i += 1
    return data, columns


def _add_tags_to_vault_obj(obj, data, columns, name):
    if name == 'bind_rules':
        data += ('\n'.join((f'value={tag.value}, key={tag.key}'
                            for tag in obj.bind_rules.tags)),)
    else:
        data += ('\n'.join((f'value={tag.value}, key={tag.key}'
                            for tag in obj.tags)),)
    columns = columns + (name,)
    return data, columns


def _normalize_resources(resources):
    result = []
    for resource in resources:
        res = dict(map(lambda s: s.split('='), resource.split(' ')))
        result.append(res)
    return result


def _normalize_tags(tags):
    result = []
    for tag in tags:
        try:
            tag = tag.split('=')
            result.append({
                'key': tag[0],
                'value': tag[1]
            })
        except IndexError:
            result.append({'key': tag[0], 'value': ''})
    return result


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
        'status',
        'operation_type',
        'object_type',
        'spec_code',
        'size',
        'consistent_level',
        'charging_mode',
        'is_auto_pay',
        'is_auto_renew',
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

        obj = client.find_vault(
            name_or_id=parsed_args.vault,
            ignore_missing=False
        )

        data = utils.get_dict_properties(
            _flatten_vault(obj), self.columns)

        if obj.resources:
            data, self.columns = _add_resources_to_vault_obj(
                obj, data, self.columns)
        if obj.tags:
            data, self.columns = _add_tags_to_vault_obj(
                obj, data, self.columns, 'tags')
        if obj.bind_rules:
            data, self.columns = _add_tags_to_vault_obj(
                obj, data, self.columns, 'bind_rules')

        return self.columns, data


class CreateVault(command.ShowOne):
    _description = _('Create CBR Vault')
    columns = (
        'ID',
        'name',
        'backup_policy',
        'description',
        'enterprise_project_id',
        'auto_bind',
        'status',
        'operation_type',
        'object_type',
        'spec_code',
        'size',
        'consistent_level',
        'charging_mode',
        'is_auto_pay',
        'is_auto_renew',
    )

    def get_parser(self, prog_name):
        parser = super(CreateVault, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help=_('Name of the CBR Vault.')
        )
        parser.add_argument(
            '--backup_policy',
            metavar='<backup_policy>',
            help=_('Name or id of the CBR Policy.')
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_('User-defined CBR Vault description.')
        )
        parser.add_argument(
            '--enterprise_project_id',
            metavar='<enterprise_project_id>',
            help=_('Enterprise project ID.')
        )
        parser.add_argument(
            '--auto_bind',
            metavar='<auto_bind>',
            type=bool,
            help=_('Whether automatic association is supported.')
        )
        parser.add_argument(
            '--consistent_level',
            metavar='<consistent_level>',
            required=True,
            default='crash_consistent',
            choices=['crash_consistent', 'app_consistent'],
            help=_('Backup specifications, which can be \n'
                   'crash_consistent (crash consistent backup) or \n'
                   'app_consistent (application consistency backup) '
                   'Backup specifications.')
        )
        parser.add_argument(
            '--object_type',
            metavar='<object_type>',
            required=True,
            choices=['server', 'disk', 'turbo'],
            help=_('Object type.')
        )
        parser.add_argument(
            '--size',
            metavar='<size>',
            type=int,
            required=True,
            help=_('Capacity, in GB.\n'
                   'Ranges from 1 to 10485760.')
        )
        parser.add_argument(
            '--is_auto_renew',
            action='store_false',
            help=_('Whether to automatically renew the subscription '
                   'after expiration. By default, it is not renewed.')
        )
        parser.add_argument(
            '--is_auto_pay',
            action='store_false',
            help=_('Whether the fee is automatically deducted from the '
                   'customer account balance after an order is submitted. '
                   'The non-automatic payment mode is used by default.')
        )
        parser.add_argument(
            '--console_url',
            metavar='<console_url>',
            help=_('Redirection URL.')
        )
        parser.add_argument(
            '--resource',
            metavar='<resource>',
            action='append',
            help=_('Associated resources in "id=resource_id '
                   'type=resource_type name=resource_name" format.'
                   'Repeat for multiple values.')
        )
        parser.add_argument(
            '--tag',
            metavar='<tag>',
            action='append',
            help=_('Tag to assign to the server in KEY=VALUE format. '
                   'Repeat for multiple values.')
        )
        parser.add_argument(
            '--bind_rule',
            metavar='<bind_rule>',
            action='append',
            help=_('Filters automatically associated resources by tag '
                   'in KEY=VALUE format. '
                   'Repeat for multiple values.')
        )
        return parser

    def take_action(self, parsed_args):
        attrs = {
            'resources': [],
            'bind_rules': {
                'tags': []
            },
            'billing': {
                'cloud_type': 'public',
                'protect_type': 'backup',
                'charging_mode': 'post_paid'
            }
        }

        # mandatory
        attrs['name'] = parsed_args.name

        attrs['billing']['consistent_level'] = parsed_args.consistent_level
        attrs['billing']['object_type'] = parsed_args.object_type
        attrs['billing']['size'] = parsed_args.size

        if parsed_args.resource:
            attrs['resources'] = _normalize_resources(parsed_args.resource)

        # optional
        if parsed_args.is_auto_renew:
            attrs['billing']['is_auto_renew'] = parsed_args.is_auto_renew
        if parsed_args.is_auto_pay:
            attrs['billing']['is_auto_pay'] = parsed_args.is_auto_pay
        if parsed_args.console_url:
            attrs['billing']['console_url'] = parsed_args.console_url
        if parsed_args.backup_policy:
            attrs['backup_policy_id'] = parsed_args.backup_policy
        if parsed_args.description:
            attrs['description'] = parsed_args.description
        if parsed_args.enterprise_project_id:
            attrs['enterprise_project_id'] = parsed_args.enterprise_project_id
        if parsed_args.auto_bind:
            attrs['auto_bind'] = parsed_args.auto_bind
        if parsed_args.bind_rule:
            attrs['bind_rules']['tags'] = _normalize_tags(parsed_args.bind_rule)
        if parsed_args.tag:
            attrs['tags'] = _normalize_tags(parsed_args.tag)

        client = self.app.client_manager.cbr
        obj = client.create_vault(**attrs)

        data = utils.get_dict_properties(
            _flatten_vault(obj), self.columns)

        if obj.resources:
            data, self.columns = _add_resources_to_vault_obj(
                obj, data, self.columns)
        if obj.bind_rules.tags:
            data, self.columns = _add_tags_to_vault_obj(
                obj, data, self.columns, 'bind_rules')
        if obj.tags:
            data, self.columns = _add_tags_to_vault_obj(
                obj, data, self.columns, 'tags')

        return self.columns, data


class UpdateVault(command.ShowOne):
    _description = _('Update CBR Vault')
    columns = (
        'ID',
        'name',
        'backup_policy',
        'description',
        'enterprise_project_id',
        'auto_bind',
        'status',
        'operation_type',
        'object_type',
        'spec_code',
        'size',
        'consistent_level',
        'charging_mode',
        'is_auto_pay',
        'is_auto_renew',
    )

    def get_parser(self, prog_name):
        parser = super(UpdateVault, self).get_parser(prog_name)
        parser.add_argument(
            'vault',
            metavar='<vault>',
            help=_('ID or name of the CBR Vault.')
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_('Name of the CBR Vault.')
        )
        parser.add_argument(
            '--auto_bind',
            metavar='<auto_bind>',
            type=bool,
            help=_('Whether automatic association is supported.')
        )
        parser.add_argument(
            '--bind_rule',
            metavar='<bind_rule>',
            action='append',
            help=_('Filters automatically associated resources by tag '
                   'in KEY=VALUE format. '
                   'Repeat for multiple values.')
        )
        parser.add_argument(
            '--auto_expand',
            metavar='<auto_expand>',
            type=bool,
            help=_('Whether to enable auto capacity expansion for the vault.')
        )
        parser.add_argument(
            '--smn_notify',
            metavar='<smn_notify>',
            type=bool,
            help=_('Exception notification function.')
        )
        parser.add_argument(
            '--size',
            metavar='<size>',
            type=int,
            help=_('Capacity, in GB.\n'
                   'Ranges from 1 to 10485760.')
        )
        parser.add_argument(
            '--threshold',
            metavar='<threshold>',
            type=int,
            help=_('Vault capacity threshold. If the vault capacity usage '
                   'exceeds this threshold and smn_notify is true, '
                   'an exception notification is sent.\n'
                   'Ranges from 1 to 100.')
        )

        return parser

    def take_action(self, parsed_args):
        attrs = {
            'billing': {}
        }

        if parsed_args.name:
            attrs['name'] = parsed_args.name
        if parsed_args.auto_bind:
            attrs['auto_bind'] = parsed_args.auto_bind
        if parsed_args.bind_rule:
            attrs['bind_rules']['tags'] = _normalize_tags(parsed_args.bind_rule)
        if parsed_args.auto_expand:
            attrs['auto_expand'] = parsed_args.auto_expand
        if parsed_args.smn_notify:
            attrs['smn_notify'] = parsed_args.smn_notify
        if parsed_args.size:
            attrs['billing']['size'] = parsed_args.size
        if parsed_args.threshold:
            attrs['threshold'] = parsed_args.threshold

        client = self.app.client_manager.cbr
        vault = client.find_vault(
            name_or_id=parsed_args.vault,
            ignore_missing=False
        )

        if attrs:
            obj = client.update_vault(vault=vault.id, **attrs)
        else:
            obj = vault

        data = utils.get_dict_properties(
            _flatten_vault(obj), self.columns)

        if obj.resources:
            data, self.columns = _add_resources_to_vault_obj(
                obj, data, self.columns)
        if obj.bind_rules.tags:
            data, self.columns = _add_tags_to_vault_obj(
                obj, data, self.columns, 'bind_rules')
        if obj.tags:
            data, self.columns = _add_tags_to_vault_obj(
                obj, data, self.columns, 'tags')

        return self.columns, data


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
