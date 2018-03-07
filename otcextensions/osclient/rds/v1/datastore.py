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
"""Datastore v1 action implementations"""

import logging

# import six

# from osc_lib.cli import parseractions
from osc_lib.command import command
from osc_lib import utils

from otcextensions.i18n import _


LOG = logging.getLogger(__name__)


class ListTypes(command.Lister):
    _description = _("List Datastore types")

    def get_parser(self, prog_name):
        parser = super(ListTypes, self).get_parser(prog_name)

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds

        data = client.datastore_types()

        columns = (
            'name',
        )
        column_headers = (
            'Name',
        )

        return (
            column_headers,
            (utils.get_item_properties(
                s,
                columns,
            ) for s in data)
        )


class ListDatastoreVersions(command.Lister):
    _description = _("Display Datastore version details")

    def get_parser(self, prog_name):
        parser = super(ListDatastoreVersions, self).get_parser(prog_name)
        parser.add_argument(
            '--type',
            metavar="<type>",
            required=True,
            help=_("Datastore type (name)")
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds

        data = client.datastores(db_name=parsed_args.type)

        columns = (
            'id',
            'name',
            'datastore',
            'image',
            'packages'
        )
        column_headers = (
            'ID',
            'Name',
            'Datastore',
            'Image',
            'Packages'
        )

        return (
            column_headers,
            (utils.get_item_properties(
                s,
                columns,
            ) for s in data)
        )
