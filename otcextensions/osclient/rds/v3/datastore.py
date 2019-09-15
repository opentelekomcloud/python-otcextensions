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
"""Datastore v3 action implementations"""
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.i18n import _


LOG = logging.getLogger(__name__)

DB_TYPE_CHOICES = ['mysql', 'postgresql', 'sqlserver']


def _get_columns(item):
    column_map = {
    }
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


class ListDatastores(command.Lister):

    _description = _("List available datastores")
    columns = ['Name']

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds

        data = client.datastore_types()

        return (
            self.columns,
            (utils.get_item_properties(
                s,
                self.columns,
            ) for s in data)
        )


class ListDatastoreVersions(command.Lister):
    _description = _("Lists available versions for a datastore")
    columns = ['ID', 'Name']

    def get_parser(self, prog_name):
        parser = super(ListDatastoreVersions, self).get_parser(prog_name)

        parser.add_argument(
            'db_name',
            metavar='{' + ','.join(DB_TYPE_CHOICES) + '}',
            type=lambda s: s.lower(),
            choices=DB_TYPE_CHOICES,
            help=_('Name of the datastore Engine.'),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds

        data = client.datastore_versions(datastore_name=parsed_args.db_name)

        return (
            self.columns,
            (utils.get_item_properties(
                s,
                self.columns,
            ) for s in data)
        )
