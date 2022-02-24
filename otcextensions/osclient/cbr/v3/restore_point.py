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


def _flatten_task(obj):
    """Flatten the structure of the restore point into a single dict
    """

    data = {
        'id': obj.id,
        'checkpoint_id': obj.checkpoint_id,
        'policy_id': obj.policy_id,
        'provider_id': obj.provider_id,
        'vault_id': obj.vault_id,
        'vault_name': obj.vault_name,
        'operation_type': obj.operation_type,
        'error_mesage': obj.error_info.message,
        'error_code': obj.error_info.code,
        'created_at': obj.created_at,
        'ended_at': obj.ended_at,
        'started_at': obj.started_at,
        'updated_at': obj.updated_at,
    }

    return data


class ListRestorePoints(command.Lister):
    _description = _('List CBR Restore Points')
    columns = ('id', 'checkpoint_id', 'provider_id',
               'operation_type', 'created_at', 'ended_at')

    def get_parser(self, prog_name):
        parser = super(ListTasks, self).get_parser(prog_name)

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.cbr

        data = client.tasks()

        table = (self.columns,
                 (utils.get_dict_properties(
                     _flatten_task(s), self.columns,
                 ) for s in data))
        return table