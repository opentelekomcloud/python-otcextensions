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
'''DMS Instance Maintenance Window action implementations'''
from osc_lib import utils
from osc_lib.command import command

from otcextensions.i18n import _


class ListMW(command.Lister):
    _description = _('List Maintenance Windows')
    columns = ('seq', 'begin', 'end', 'is_default')

    def get_parser(self, prog_name):
        parser = super(ListMW, self).get_parser(prog_name)

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dms

        data = client.maintenance_windows()

        table = (self.columns,
                 (utils.get_item_properties(
                     s, self.columns,
                 ) for s in data))
        return table
