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
'''DWS Flavors (Node Types) action implementation'''
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


class ListFlavors(command.Lister):
    _description = _('List Flavors (Node Types) of a DWS Cluster')
    columns = (
        'ID',
        'Name',
        'Availability Zones',
        'vCPU',
        'RAM',
        'Disk Size',
        'Disk Type',
    )

    def take_action(self, parsed_args):
        client = self.app.client_manager.dws
        data = client.flavors()
        return (self.columns, (utils.get_item_properties(s, self.columns)
                               for s in data))
