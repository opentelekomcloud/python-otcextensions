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

from osc_lib import utils
from osc_lib.command import command

from otcextensions.i18n import _
from otcextensions.osclient.rds import sdk_utils


LOG = logging.getLogger(__name__)


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


class ShowDatastore(command.ShowOne):

    _description = _("Shows details of a datastore")
    columns = ['Name']

    def get_parser(self, prog_name):
        parser = super(ShowDatastore, self).get_parser(prog_name)
        parser.add_argument(
            'datastore',
            metavar='<datastore>',
            help=_('ID of the datastore'),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds

        data = client.datastore_types()

        datastore = None
        for ds in data:
            if ds.name == parsed_args.datastore:
                datastore = ds

        return (
            self.columns,
            utils.get_item_properties(datastore, self.columns)
        )


class ListDatastoreVersions(command.Lister):
    _description = _("Lists available versions for a datastore")
    columns = ['ID', 'Name']

    def get_parser(self, prog_name):
        parser = super(ListDatastoreVersions, self).get_parser(prog_name)
        parser.add_argument(
            'datastore',
            metavar='<datastore>',
            help=_('Name of the datastore'),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds

        data = client.datastore_versions(datastore=parsed_args.datastore)

        return (
            self.columns,
            (utils.get_item_properties(
                s,
                self.columns,
            ) for s in data)
        )


class ShowDatastoreVersion(command.ShowOne):
    _description = _("Shows details of a datastore version.")
    columns = ['Active', 'Datastore', 'ID', 'Image', 'Name', 'Packages', ]

    def get_parser(self, prog_name):
        parser = super(ShowDatastoreVersion, self).get_parser(prog_name)
        parser.add_argument(
            'datastore_version',
            metavar='<datastore_version>',
            help=_('ID or name of the datastore version.'),
        )
        parser.add_argument(
            '--datastore',
            metavar='<datastore>',
            default=None,
            required=True,
            help=_('ID or name of the datastore. Optional if the ID of'
                   'the datastore_version is provided.'),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds

        obj = client.get_datastore_version(
            datastore=parsed_args.datastore,
            datastore_version=parsed_args.datastore_version
        )

        # display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, self.columns)

        return (self.columns, data)
