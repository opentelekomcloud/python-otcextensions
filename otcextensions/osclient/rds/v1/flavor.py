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
"""Flavor v1 action implementations"""
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def set_attributes_for_print_detail(instance):
    info = {}  # instance.copy()
    info['id'] = instance.id
    info['ram'] = instance.ram
    info['name'] = instance.name
    # info['str_id'] = instance['str_id']
    if getattr(instance, 'flavor_detail', None):
        for det in instance.flavor_detail:
            if det['name'] == 'cpu':
                info['vcpus'] = det['value']
    return info


class ListDatabaseFlavors(command.Lister):

    _description = _("List database flavors")
    columns = ['ID', 'Name', 'ram', 'spec_code']

    def get_parser(self, prog_name):
        parser = super(ListDatabaseFlavors, self).get_parser(prog_name)

        parser.add_argument(
            'dbId',
            metavar='<dbId>',
            help=_('ID of the datastore version.'),
        )

        parser.add_argument(
            'region',
            metavar='<region>',
            default='eu-de',
            nargs='?',
            help=_('Region. `eu-de` is left empty'),
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds

        data = client.flavors(dbId=parsed_args.dbId, region=parsed_args.region)

        return (
            self.columns,
            (utils.get_item_properties(
                s,
                self.columns,
            ) for s in data)
        )


class ShowDatabaseFlavor(command.ShowOne):
    _description = _("Shows details of a database flavor")
    columns = ('ID', 'Name', 'ram', 'spec_code')

    def get_parser(self, prog_name):
        parser = super(ShowDatabaseFlavor, self).get_parser(prog_name)
        parser.add_argument(
            'flavor',
            metavar='<flavor>',
            help=_('ID or name of the flavor'),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds

        obj = client.get_flavor(parsed_args.flavor)

        return (
            self.columns,
            utils.get_item_properties(
                obj,
                self.columns,
            )
        )
