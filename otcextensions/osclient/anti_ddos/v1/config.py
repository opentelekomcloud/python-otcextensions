#   Licensed under the Apache License, Version 2.0 (the 'License'); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an 'AS IS' BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#
'''Anti DDoS Config v1 action implementations'''
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.i18n import _
from otcextensions.common import sdk_utils

LOG = logging.getLogger(__name__)


_formatters = {
    'traffic_limited_list': sdk_utils.ListOfDictColumn,
    'http_limited_list': sdk_utils.ListOfDictColumn,
    'connection_limited_list': sdk_utils.ListOfDictColumn,
}


class ListConfig(command.Lister):
    _description = _('List Anti DDoS Defence policies')
    columns = (
        'traffic_limited_list', 'http_limited_list', 'connection_limited_list'
    )

    def get_parser(self, prog_name):
        parser = super(ListConfig, self).get_parser(prog_name)

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.anti_ddos

        data = client.configs()

        table = (self.columns,
                 (utils.get_item_properties(
                     s, self.columns, formatters=_formatters
                 ) for s in data))
        return table
