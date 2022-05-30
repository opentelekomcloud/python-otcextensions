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
'''CES Alarm v1 action implementations'''
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _flatten_output(obj):
    data = {
        'type': obj.resources[0].type,
        'quota': obj.resources[0].quota,
        'used': obj.resources[0].used
    }
    return data


class ListQuotas(command.Lister):
    _description = _('List CES alarm quota')
    columns = (
        'type',
        'quota',
        'used'
    )

    def get_parser(self, prog_name):
        parser = super(ListQuotas, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.ces

        data = client.quotas()

        table = (self.columns,
                 (utils.get_dict_properties(
                     _flatten_output(s), self.columns
                 ) for s in data))
        return table
