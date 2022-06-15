# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

'''MRS clusters v1 action implementations'''
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.i18n import _
from otcextensions.common import sdk_utils

LOG = logging.getLogger(__name__)

_formatters = {}


def _get_columns(item):
    column_map = {}
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


class ListDatasource(command.Lister):
    _description = _('List Sahara datasoruces')
    columns = (
        'id', 'name', 'type', 'url', 'description',
        'is_public', 'is_protected'
    )

    def get_parser(self, prog_name):
        parser = super(ListDatasource, self).get_parser(prog_name)
        parser.add_argument(
            '--type',
            metavar='<type>',
            help=_('type of the datasource')
        )
        parser.add_argument(
            '--limit',
            metavar='<limit>',
            type=int,
            help=_('Number of entries to display.')
        )
        parser.add_argument(
            '--marker',
            metavar='<marker>',
            help=_('ID of the last record on the previous page.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.mrs

        query = {}

        if parsed_args.type:
            query['type'] = parsed_args.type
        if parsed_args.limit:
            query['limit'] = parsed_args.limit
        if parsed_args.marker:
            query['marker'] = parsed_args.marker

        data = client.datasources(**query)

        table = (self.columns,
                 (utils.get_item_properties(
                     s, self.columns, formatters=_formatters
                 ) for s in data))
        return table


class DeleteDatasource(command.Command):
    _description = _('Delete Data Source')

    def get_parser(self, prog_name):
        parser = super(DeleteDatasource, self).get_parser(prog_name)

        parser.add_argument(
            'id',
            metavar='<id>',
            nargs='+',
            help=_('Data source ID')
        )

        return parser

    def take_action(self, parsed_args):
        if parsed_args.id:
            client = self.app.client_manager.mrs
            for id in parsed_args.id:
                client.delete_datasource(id, ignore_missing=False)


class CreateDatasource(command.ShowOne):
    _description = _('Create datasource')

    columns = ('id', 'name', 'type', 'url', 'description',
               'is_public', 'is_protected')

    def get_parser(self, prog_name):
        parser = super(CreateDatasource, self).get_parser(prog_name)

        parser.add_argument(
            '--name',
            metavar='<name>',
            required=True,
            help=_('Name for the datasource')
        )
        parser.add_argument(
            '--is_public',
            action='store_const',
            default='false',
            const='false',
            dest='is_public',
            help=_('Whether the data source is public')
        )
        parser.add_argument(
            '--is_protected',
            action='store_const',
            default='false',
            const='false',
            dest='is_protected',
            help=_('Whether the data source is protected')
        )
        parser.add_argument(
            '--type',
            metavar='<type>',
            required=True,
            help=_('Data source type')
        )
        parser.add_argument(
            '--url',
            metavar='<url>',
            required=True,
            help=_('Data source URL')
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_('Data source description')
        )

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.mrs

        attrs = {}

        if parsed_args.name:
            attrs['name'] = parsed_args.name
        if parsed_args.type:
            attrs['type'] = parsed_args.type
        if parsed_args.url:
            attrs['url'] = parsed_args.url
        if parsed_args.description:
            attrs['description'] = parsed_args.description
        if parsed_args.is_public:
            attrs['is_public'] = parsed_args.is_public
        if parsed_args.is_protected:
            attrs['is_protected'] = parsed_args.is_protected
        obj = client.create_datasource(
            **attrs
        )

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return display_columns, data


class UpdateDatasource(command.ShowOne):
    _description = _('Update Data Source')

    columns = ('id', 'name', 'type', 'url', 'description',
               'is_public', 'is_protected')

    def get_parser(self, prog_name):
        parser = super(UpdateDatasource, self).get_parser(prog_name)

        parser.add_argument(
            'datasource',
            metavar='<datasource>',
            help=_('ID or name of the data source')
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_('Name for the data source')
        )
        parser.add_argument(
            '--is_public',
            action='store_const',
            default='false',
            const='false',
            dest='is_public',
            help=_('Whether the data source is public')
        )
        parser.add_argument(
            '--is_protected',
            action='store_const',
            const='false',
            dest='is_protected',
            help=_('Whether the data source is protected')
        )
        parser.add_argument(
            '--type',
            metavar='<type>',
            help=_('Data source type')
        )
        parser.add_argument(
            '--url',
            metavar='<url>',
            help=_('Data source URL')
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_('Data source description')
        )

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.mrs

        attrs = {}

        if parsed_args.name:
            attrs['name'] = parsed_args.name
        if parsed_args.type:
            attrs['type'] = parsed_args.type
        if parsed_args.url:
            attrs['url'] = parsed_args.url
        if parsed_args.description:
            attrs['description'] = parsed_args.description
        if parsed_args.is_public:
            attrs['is_public'] = parsed_args.is_public
        if parsed_args.is_protected:
            attrs['is_protected'] = parsed_args.is_protected

        datasource = client.find_datasource(
            parsed_args.datasource,
            ignore_missing=False
        )
        print(f'ATTRIBUTES: {attrs}')
        if attrs:
            obj = client.update_datasource(
                datasource=datasource,
                **attrs
            )
        else:
            obj = datasource
        print(f'OBJECT: {obj}')
        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return display_columns, data


class ShowDatasource(command.ShowOne):
    _description = _('Show the MRS Data source details')

    def get_parser(self, prog_name):
        parser = super(ShowDatasource, self).get_parser(prog_name)

        parser.add_argument(
            'datasource',
            metavar='<datasource>',
            help=_('ID or name of the of the data source')
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.mrs

        obj = client.find_datasource(
            parsed_args.datasource,
            ignore_missing=False
        )

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return display_columns, data
