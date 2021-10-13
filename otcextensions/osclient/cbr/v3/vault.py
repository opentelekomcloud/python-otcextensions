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
from osc_lib.command import command

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _flatten_policy(obj):
    """Flatten the structure of the node pool into a single dict
    """
    od = obj.operation_definition
    data = {
        'id': obj.id,
        'name': obj.name,
        'enabled': obj.enabled,
        'operation_type': obj.operation_type,
        'retention_duration_days': od.retention_duration_days,
        'max_backups': od.max_backups,
        'year_backups': od.year_backups,
        'day_backups': od.day_backups,
        'week_backups': od.week_backups,
        'month_backups': od.month_backups,
        'timezone': od.timezone,
        'start_time': obj.trigger.properties.start_time,
    }

    return data


def _add_vaults_to_policy_obj(obj, data, columns):
    """Add associated vaults to column and data tuples
    """
    i = 0
    for s in obj.associated_vaults:
        if obj.associated_vaults[i].vault_id:
            name = 'associated_vault_' + str(i + 1)
            data += (obj.associated_vaults[i].vault_id,)
            columns = columns + (name,)
            i += 1
    return data, columns


def _add_scheduling_patterns(obj, data, columns):
    """Add scheduling patterns to column and data tuples
    """
    i = 0
    for s in obj.trigger.properties.pattern:
        name = 'schedule_pattern_' + str(i + 1)
        data += (obj.trigger.properties.pattern[i],)
        columns = columns + (name,)
        i += 1
    return data, columns


class ListVaults(command.Lister):
    _description = _('List CBR Vaults')
    columns = ('ID', 'name', 'operation_type', 'start_time', 'enabled')

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
            '--policy',
            metavar='<policy>',
            help=_('Name or ID of the policy.')
        )
        parser.add_argument(
            '--protect-type',
            metavar='<protect_type>',
            choices=['replication', 'backup'],
            help=_('Protection type.\n'
                   'Choices: backup, replication')
        )
        parser.add_argument(
            '--vault',
            metavar='<vault>',
            help=_('Name or ID of the vault.')
        )


        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.cbr

        query = {}
        if parsed_args.cloud_type:
            query['cloud_type'] = parsed_args.cloud_type
        if parsed_args.object_type:
            query['object_type'] = parsed_args.object_type
        if parsed_args.policy:
            try:
                policy_id = client.find_policy(parsed_args.policy)
            except:
                raise Exception('The policy was not found: '
                                + parsed_args.policy)            
            query['policy_id'] = policy_id
        if parsed_args.protect_type:
            query['protect_type'] = parsed_args.protect_type
        if parsed_args.vault:
            try:
                vault_id = client.find_vault(parsed_args.vault)
            except:
                raise Exception('The vault was not found: '
                                + parsed_args.vault)            
            query['vault_id'] = vault_id
        

        data = client.vaults(**query)

        table = (self.columns,
                 (utils.get_dict_properties(
                     s, self.columns,
                 ) for s in data))
        return table
