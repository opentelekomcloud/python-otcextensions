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
import json
import logging

from osc_lib import utils
from osc_lib.cli import parseractions
from osc_lib.command import command

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _flatten_vault(obj):
    """Flatten the structure of the vault into a single dict
    """
    bind_rules = []
    if obj.bind_rules and "tags" in obj.bind_rules:
        bind_rules = obj.bind_rules["tags"]
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
        'bind_rules': bind_rules,
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


def _add_tags_to_vault_obj(obj, data, columns):
    data += ('\n'.join((f'value={tag["value"]}, key={tag["key"]}'
                        for tag in obj.tags)),)
    columns = columns + ('tags',)
    return data, columns


def _add_bind_rules_to_vault_obj(obj, data, columns):
    """Add associated bind rules to column and data tuples
    """
    data += ('\n'.join((f'value={tag["value"]}, key={tag["key"]}'
                        for tag in obj.bind_rules['tags'])),)
    columns = columns + ('bind_rules',)
    return data, columns


def _add_associated_policy_to_vault_obj(data, columns):
    """Add associated resources to column and data tuples
    """
    return_data = ()
    for k, v in data['associate_policy'].items():
        return_data += (v,)
        columns = columns + (k,)
    return return_data, columns


def _add_associated_resources_to_vault_obj(data, columns):
    """Add associated resources to column and data tuples
    """
    return_data = ()
    i = 0
    for s in data['add_resource_ids']:
        name = 'resource_' + str(i + 1)
        return_data += (s,)
        columns = columns + (name,)
        i += 1
    return return_data, columns


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
        parser.add_argument(
            '--id',
            metavar='<id>',
            help=_('Vault ID.')
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_('Vault name')
        )
        parser.add_argument(
            '--cloud-type',
            metavar='<cloud_type>',
            help=_('Cloud type, which is public.')
        )
        parser.add_argument(
            '--limit',
            type=int,
            metavar='<limit>',
            help=_('Limit.')
        )
        parser.add_argument(
            '--object-type',
            metavar='<object_type>',
            help=_('Object type, which can be server or disk.')
        )
        parser.add_argument(
            '--offset',
            type=int,
            metavar='<offset>',
            help=_('Offset value. The value must be a positive integer.')
        )
        parser.add_argument(
            '--policy-id',
            metavar='<policy_id>',
            help=_('Policy ID.')
        )
        parser.add_argument(
            '--protect-type',
            metavar='<protect_type>',
            help=_('Protection type, which is backup.')
        )
        parser.add_argument(
            '--status',
            metavar='<status>',
            help=_('Status.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.cbr
        args = {}
        if parsed_args.id:
            args['id'] = parsed_args.id
        if parsed_args.name:
            args['name'] = parsed_args.name
        if parsed_args.cloud_type:
            args['cloud_type'] = parsed_args.cloud_type
        if parsed_args.limit:
            args['limit'] = parsed_args.limit
        if parsed_args.object_type:
            args['object_type'] = parsed_args.object_type
        if parsed_args.offset:
            args['offset'] = parsed_args.offset
        if parsed_args.policy_id:
            args['policy_id'] = parsed_args.policy_id
        if parsed_args.protect_type:
            args['protect_type'] = parsed_args.protect_type
        if parsed_args.status:
            args['status'] = parsed_args.status

        data = list(client.vaults(**args))

        columns = list(self.columns)
        seen_columns = set(columns)
        for s in data:
            if s.resources:
                _, new_cols = _add_resources_to_vault_obj(s, (), tuple())
                for col in new_cols:
                    if col not in seen_columns:
                        columns.append(col)
                        seen_columns.add(col)
            if s.tags and 'tags' not in seen_columns:
                columns.append('tags')
                seen_columns.add('tags')
        def row_generator():
            for s in data:
                row_columns = list(self.columns)
                row_data = utils.get_dict_properties(
                    _flatten_vault(s), row_columns
                )
                if s.resources:
                    row_data, row_columns = _add_resources_to_vault_obj(
                        s, row_data, tuple(row_columns)
                    )
                if s.tags:
                    row_data, row_columns = _add_tags_to_vault_obj(
                        s, row_data, tuple(row_columns)
                    )
                row_dict = {col: val for col, val in zip(row_columns, row_data)}
                yield tuple(row_dict.get(col, '') for col in columns)
        table = (columns, row_generator())
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
                obj, data, self.columns)
        if obj.bind_rules.get('tags'):
            if obj.bind_rules['tags']:
                data, self.columns = _add_bind_rules_to_vault_obj(
                    obj, data, self.columns)
        return self.columns, data


class CreateVault(command.ShowOne):
    _description = _('Create CBR Vault')
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
        parser = super(CreateVault, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help=_('Name of the CBR Vault.')
        )
        parser.add_argument(
            '--backup-policy',
            metavar='<backup_policy>',
            help=_('Name or id of the CBR Policy.')
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_('User-defined CBR Vault description.')
        )
        parser.add_argument(
            '--enterprise-project-id',
            metavar='<enterprise_project_id>',
            help=_('Enterprise project ID.')
        )
        parser.add_argument(
            '--auto-bind',
            metavar='<auto_bind>',
            type=bool,
            help=_('Whether automatic association is supported.')
        )
        parser.add_argument(
            '--bind-rule',
            metavar='<bind_rule>',
            action='append',
            help=_('Filters automatically associated resources by tag '
                   'in KEY=VALUE format. '
                   'Repeat for multiple values.')
        )
        parser.add_argument(
            '--consistent-level',
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
            '--object-type',
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
            '--is-auto-renew',
            action='store_false',
            help=_('Whether to automatically renew the subscription '
                   'after expiration. By default, it is not renewed.')
        )
        parser.add_argument(
            '--is-auto-pay',
            action='store_false',
            help=_('Whether the fee is automatically deducted from the '
                   'customer account balance after an order is submitted. '
                   'The non-automatic payment mode is used by default.')
        )
        parser.add_argument(
            '--console-url',
            metavar='<console_url>',
            help=_('Redirection URL.')
        )
        parser.add_argument(
            '--resource',
            metavar='name=<name>,value=<value>,type=<type>',
            action=parseractions.MultiKeyValueAction,
            dest='resource',
            required_keys=['id', 'type'],
            optional_keys=['name'],
            help=_('Associated resource in "id=resource_id,'
                   'type=resource_type,name=resource_name" format.'
                   'Repeat for multiple values.')
        )
        parser.add_argument(
            '--tag',
            metavar='<tag>',
            action='append',
            help=_('Tag to assign to the server in KEY=VALUE format. '
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
            attrs['resources'] = parsed_args.resource

        # optional
        if parsed_args.is_auto_renew:
            attrs['billing']['is_auto_renew'] = parsed_args.is_auto_renew
        if parsed_args.is_auto_pay:
            attrs['billing']['is_auto_pay'] = parsed_args.is_auto_pay
        if parsed_args.console_url:
            attrs['billing']['console_url'] = parsed_args.console_url
        if parsed_args.backup_policy:
            attrs['backup_policy_id'] = parsed_args.backup_policy
        if parsed_args.bind_rule:
            attrs['bind_rules'] = {'tags': []}
            attrs['bind_rules']['tags'] = _normalize_tags(
                parsed_args.bind_rule)
        if parsed_args.description:
            attrs['description'] = parsed_args.description
        if parsed_args.enterprise_project_id:
            attrs['enterprise_project_id'] = parsed_args.enterprise_project_id
        if parsed_args.auto_bind:
            attrs['auto_bind'] = parsed_args.auto_bind
        if parsed_args.tag:
            attrs['tags'] = _normalize_tags(parsed_args.tag)

        client = self.app.client_manager.cbr
        obj = client.create_vault(**attrs)

        data = utils.get_dict_properties(
            _flatten_vault(obj), self.columns)

        if obj.resources:
            data, self.columns = _add_resources_to_vault_obj(
                obj, data, self.columns)
        if obj.bind_rules.get('tags'):
            if obj.bind_rules['tags']:
                data, self.columns = _add_bind_rules_to_vault_obj(
                    obj, data, self.columns)
        if obj.tags:
            data, self.columns = _add_tags_to_vault_obj(
                obj, data, self.columns)

        return self.columns, data


class UpdateVault(command.ShowOne):
    _description = _('Update CBR Vault')
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
            '--auto-bind',
            metavar='<auto_bind>',
            type=bool,
            help=_('Whether automatic association is supported.')
        )
        parser.add_argument(
            '--bind-rule',
            metavar='<bind_rule>',
            action='append',
            help=_('Filters automatically associated resources by tag '
                   'in KEY=VALUE format. '
                   'Repeat for multiple values.')
        )
        parser.add_argument(
            '--auto-expand',
            metavar='<auto_expand>',
            type=bool,
            help=_('Whether to enable auto capacity expansion for the vault.')
        )
        parser.add_argument(
            '--smn-notify',
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
            'billing': {},
        }

        if parsed_args.name:
            attrs['name'] = parsed_args.name
        if parsed_args.auto_bind:
            attrs['auto_bind'] = parsed_args.auto_bind
        if parsed_args.bind_rule:
            attrs['bind_rules'] = {'tags': []}
            attrs['bind_rules']['tags'] = _normalize_tags(
                parsed_args.bind_rule
            )
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
        if obj.bind_rules.get('tags'):
            if obj.bind_rules['tags']:
                data, self.columns = _add_bind_rules_to_vault_obj(
                    obj, data, self.columns)
        if obj.tags:
            data, self.columns = _add_tags_to_vault_obj(
                obj, data, self.columns)

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


class AssociateVaultResource(command.ShowOne):
    _description = _('Associate resource to the CBR Vault')

    columns = ()

    def get_parser(self, prog_name):
        parser = super(AssociateVaultResource, self).get_parser(prog_name)
        parser.add_argument(
            'vault',
            metavar='<vault>',
            help=_('ID or name of the CBR Vault.')
        )
        parser.add_argument(
            '--resource',
            metavar='name=<name>,value=<value>,type=<type>',
            action=parseractions.MultiKeyValueAction,
            dest='resource',
            required_keys=['id', 'type'],
            optional_keys=['name'],
            help=_('Associated resource in "id=resource_id,'
                   'type=resource_type,name=resource_name" format.'
                   'Repeat for multiple values.')
        )
        return parser

    def take_action(self, parsed_args):

        resources = []

        client = self.app.client_manager.cbr
        vault = client.find_vault(
            name_or_id=parsed_args.vault,
            ignore_missing=False
        )

        resources = parsed_args.resource

        if resources:
            obj = client.associate_resources(
                vault=vault.id,
                resources=resources
            )

            data = json.loads(obj._content.decode('utf-8'))

            if data['add_resource_ids']:
                data, self.columns = _add_associated_resources_to_vault_obj(
                    data, self.columns)

            return self.columns, data


class DissociateVaultResource(command.Command):
    _description = _('Dissociate resource from the CBR Vault')

    def get_parser(self, prog_name):
        parser = super(DissociateVaultResource, self).get_parser(prog_name)
        parser.add_argument(
            'vault',
            metavar='<vault>',
            help=_('ID or name of the CBR Vault.')
        )
        parser.add_argument(
            '--resource',
            metavar='<resource>',
            action='append',
            help=_('Removed resource IDs.'
                   'Repeat for multiple values.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.cbr

        vault = client.find_vault(
            name_or_id=parsed_args.vault,
            ignore_missing=False
        )

        if parsed_args.resource:
            client.dissociate_resources(
                vault=vault.id,
                resources=parsed_args.resource
            )


class BindVaultPolicy(command.ShowOne):
    _description = _('Bind policy to the CBR Vault')

    columns = ()

    def get_parser(self, prog_name):
        parser = super(BindVaultPolicy, self).get_parser(prog_name)
        parser.add_argument(
            'vault',
            metavar='<vault>',
            help=_('ID or name of the CBR Vault.')
        )
        parser.add_argument(
            'policy',
            metavar='<policy>',
            help=_('ID or name of the CBR Vault.')
        )
        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.cbr
        vault = client.find_vault(
            name_or_id=parsed_args.vault,
            ignore_missing=False
        )

        if parsed_args.policy:
            obj = client.bind_policy(
                vault=vault.id,
                policy=parsed_args.policy
            )

            data = json.loads(obj._content.decode('utf-8'))
            if data['associate_policy']:
                data, self.columns = _add_associated_policy_to_vault_obj(
                    data, self.columns)

            return self.columns, data


class UnbindVaultPolicy(command.Command):
    _description = _('Unbind policy from the CBR Vault')

    def get_parser(self, prog_name):
        parser = super(UnbindVaultPolicy, self).get_parser(prog_name)
        parser.add_argument(
            'vault',
            metavar='<vault>',
            help=_('ID or name of the CBR Vault.')
        )
        parser.add_argument(
            'policy',
            metavar='<policy>',
            help=_('ID or name of the CBR Vault.')
        )
        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.cbr
        vault = client.find_vault(
            name_or_id=parsed_args.vault,
            ignore_missing=False
        )

        client.unbind_policy(
            vault=vault.id,
            policy=parsed_args.policy
        )
