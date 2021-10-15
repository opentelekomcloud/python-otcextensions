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
from osc_lib import exceptions
from osc_lib.cli import parseractions
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
        'description': obj.description,
        'object_type': obj.billing.object_type,
        'protect_type': obj.billing.protect_type,
        'provider_id': obj.provider_id,
        'status': obj.billing.status,
        'allocated': obj.billing.allocated,
        'size': obj.billing.size,
        'consistent_level': obj.billing.consistent_level
    }

    return data


def _format_resource_list(resources):
    """Formats the resource list

        :param list resources: List of resources where the
            key indicates if the resource is a volume or a server. The value
            shall contain the ID of the resource.

        :returns: a proper formated resource list for the API request
    """
    final_resources = []
    for resource in resources:
        resource_type = ''
        resource_id = ''
        if resource['server']:
            resource_type = 'OS::Nova::Server'
            resource_id = resource['server']
        elif resource['volume']:
            resource_type = 'OS::Nova::Volume'
            resource_id = resource['volume']
        else:
            raise Exception('Wrong input for --resource attribute. '
                            'The format is:\n'
                            '--resources server=id,volume=id\n'
                            'and can contain multiple values.')
        final_resources.append({
            'id': resource_id,
            'type': resource_type
        })
    return final_resources


def _add_resources_to_vault_obj(obj, data, columns):
    """Add associated servers to column and data tuples
    """
    i = 0
    for s in obj.resources:
        if obj.resources[i].name:
            name = 'resource_' + str(i + 1) + '_name'
            data += (obj.resources[i].name,)
            columns = columns + (name,)
        if obj.resources[i].id:
            id = 'resource_' + str(i + 1) + '_id'
            data += (obj.resources[i].id,)
            columns = columns + (id,)
        if obj.resources[i].type:
            type = 'resource_' + str(i + 1) + '_type'
            data += (obj.resources[i].type,)
            columns = columns + (type,)
        if obj.resources[i].protect_status:
            status = 'resource_' + str(i + 1) + '_status'
            data += (obj.resources[i].protect_status,)
            columns = columns + (status,)
        if obj.resources[i].size:
            size = 'resource_' + str(i + 1) + '_size'
            data += (obj.resources[i].size,)
            columns = columns + (size,)
        i += 1
    return data, columns


class ListVaults(command.Lister):
    _description = _('List CBR Vaults')
    columns = ('ID', 'name', 'protect_type', 'allocated', 'size', 'status')

    def get_parser(self, prog_name):
        parser = super(ListVaults, self).get_parser(prog_name)
        parser.add_argument(
            '--cloud-type',
            metavar='<cloud_type>',
            choices=['public', 'hybrid'],
            help=_('Vault type:\n'
                   'Choices: public, hybrid')
        )
        parser.add_argument(
            '--object-type',
            metavar='<object_type>',
            help=_('Resource type.')
        )
        parser.add_argument(
            '--policy-id',
            metavar='<policy_id>',
            help=_('ID of the policy.')
        )
        parser.add_argument(
            '--protect-type',
            metavar='<protect_type>',
            choices=['replication', 'backup'],
            help=_('Protection type.\n'
                   'Choices: backup, replication')
        )
        parser.add_argument(
            '--vault-id',
            metavar='<vault_id>',
            help=_('ID of the vault.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.cbr

        query = {}
        if parsed_args.cloud_type:
            query['cloud_type'] = parsed_args.cloud_type
        if parsed_args.object_type:
            query['object_type'] = parsed_args.object_type
        if parsed_args.policy_id:
            query['policy_id'] = parsed_args.policy_id
        if parsed_args.protect_type:
            query['protect_type'] = parsed_args.protect_type
        if parsed_args.vault_id:
            query['vault_id'] = parsed_args.vault_id

        data = client.vaults(**query)
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
        'description',
        'auto_bind',
        'auto_expand',
        'object_type',
        'protect_type',
        'provider_id',
        'status',
        'allocated',
        'size',
        'consistent_level',
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

        return (self.columns, data)


class CreateVault(command.ShowOne):
    _description = _('Create CBR Vault')
    columns = (
        'ID',
        'name',
        'description',
        'auto_bind',
        'auto_expand',
        'object_type',
        'protect_type',
        'provider_id',
        'status',
        'allocated',
        'size',
        'consistent_level',
    )

    def get_parser(self, prog_name):
        parser = super(CreateVault, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help=_('Name of the CBR Vault.')
        )
        '''
        parser.add_argument(
            '--auto-bind',
            action=store_true,
            help=_('Parameter enables automatic association of resources.')
        )
        parser.add_argument(
            '--bind-rules',
            metavar='<tag_key1=tag_value1,tag_key2=tag_value2>',
            action=parseractions.MultiKeyValueAction
            help=_('Bind multiple resources to CBR vault by using one or '
                   'more tags in the format:\n'
                   '--bind-rules tag_key1=tag_value1,tag_key2=tag_value2')
        )
        '''
        parser.add_argument(
            '--auto-expand',
            action='store_true',
            help=_('Parameter enables automatic expand of the vault '
                   'capacity.')
        )
        parser.add_argument(
            '--cloud-type',
            metavar='<cloud_type>',
            choices=['public', 'hybrid'],
            default='public',
            help=_('Cloud type.\n'
                   'Default: public\n'
                   'Choices: public, hybrid')
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_('Description of the CBR Vault.')
        )
        parser.add_argument(
            '--policy',
            metavar='<policy>',
            help=_('Name or ID of the Backup Policy for automatic backups.')
        )
        parser.add_argument(
            '--protect-type',
            metavar='<protect_type>',
            choices=['backup', 'replication'],
            default='backup',
            help=_('Operation type.\n'
                   'Default: backup\n'
                   'Choices: backup, replication')
        )
        parser.add_argument(
            '--resources',
            metavar='<server=id,volume=id>',
            action=parseractions.MultiKeyValueAction,
            help=_('One or more servers or volumes to be attached to the '
                   'vault in the format:\n'
                   '--resources server=id,volume=id,etc.')
        )
        parser.add_argument(
            '--size',
            metavar='<size>',
            type=int,
            default=100,
            help=_('Size of the Vault in GB.\n'
                   'Default: 100')
        )
        parser.add_argument(
            '--tags',
            metavar='<tag_key1=tag_value1,tag_key2=tag_value2>',
            action=parseractions.MultiKeyValueAction,
            help=_('One or more tags to be added in the format:\n'
                   '--tags key=value,key=value')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.cbr

        attrs = {
            'bind_rules': {},
            'billing': {
                'consistent_level': 'crash_consistent',
                'object_type': 'server'
            },
        }

        # mandatory params
        attrs['name'] = parsed_args.name
        attrs['protect_type'] = parsed_args.protect_type
        if parsed_args.resources:
            resources = _format_resource_list(parsed_args.resources)
            attrs['resources'] = resources
        else:
            attrs['resources'] = []
        attrs['billing']['size'] = parsed_args.size
        attrs['billing']['cloud_type'] = parsed_args.cloud_type

        # optional params
        if parsed_args.auto_expand:
            attrs['auto_expand'] = True
        if parsed_args.description:
            attrs['description'] = parsed_args.description
        if parsed_args.policy:
            policy = client.find_policy(parsed_args.policy)
            if policy.id:
                attrs['backup_policy_id'] = policy.id
            else:
                raise exceptions.BadRequest(
                    'The Policy '
                    + parsed_args.policy + 'was \n'
                    'not found.')
        if parsed_args.tags:
            for t in parsed_args.tags:
                for key in t.keys():
                    print('Hier ist mein Key: ' + key)

        obj = client.create_vault(**attrs)

        data = utils.get_dict_properties(
            _flatten_vault(obj), self.columns)

        return (self.columns, data)


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
