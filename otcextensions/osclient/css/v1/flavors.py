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
'''CSS ELK cluster v1 action implementations'''
import logging

from osc_lib import utils
from osc_lib.command import command
from otcextensions.common import sdk_utils

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _get_columns(item):
    column_map = {
    }
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


class ListFlavors(command.Lister):
    _description = _('Show details of a CSS cluster')
    columns = (
        'ID',
        'Name',
        'VCPUs',
        'RAM',
        'Disk Range',
    )

    def take_action(self, parsed_args):
        client = self.app.client_manager.css
        data = client.flavors()
        return (self.columns, (utils.get_item_properties(s, self.columns)
                               for s in data))
