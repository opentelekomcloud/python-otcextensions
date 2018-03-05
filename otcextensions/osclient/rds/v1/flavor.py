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

# import six

# from osc_lib.cli import parseractions
from osc_lib.command import command
from osc_lib import utils

from otcextensions.i18n import _


LOG = logging.getLogger(__name__)


class ListFlavor(command.Lister):
    _description = _("List flavors")

    def get_parser(self, prog_name):
        parser = super(ListFlavor, self).get_parser(prog_name)

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds

        data = client.flavors()

        columns = (
            'name',
            'ram',
            # 'id',
            'str_id',
            'flavor_detail'
        )
        column_headers = (
            'Name',
            'Ram',
            'ID',
            # 'Str_ID',
            'Flavor details'
        )

        return (
            column_headers,
            (utils.get_item_properties(
                s,
                columns,
            ) for s in data)
        )


class ShowFlavor(command.ShowOne):
    _description = _("Display DB Flavor details")

    def get_parser(self, prog_name):
        parser = super(ShowFlavor, self).get_parser(prog_name)
        parser.add_argument(
            'flavor',
            metavar="<flavor>",
            help=_("Flavor to display (name or ID)")
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds

        obj = client.get_flavor(parsed_args.flavor)

        LOG.debug('object is %s' % obj)
        columns = (
            'name',
            'ram',
            'str_id',
            # 'flavor',
            'flavor_detail',
            'price_detail'
        )
        data = utils.get_item_properties(obj, columns)

        return (columns, data)
