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

from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)

_formatters = {}


def _get_columns(item):
    column_map = {}
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


class ListJobbinary(command.Lister):
    _description = _('List Sahara jobbinary')
    columns = (
        'id', 'name', 'url', 'description',
        'is_public', 'is_protected'
    )

    def get_parser(self, prog_name):
        parser = super(ListJobbinary, self).get_parser(prog_name)
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

        if parsed_args.limit:
            query['limit'] = parsed_args.limit
        if parsed_args.marker:
            query['marker'] = parsed_args.marker

        data = client.jobbinaries(**query)

        table = (self.columns,
                 (utils.get_item_properties(
                     s, self.columns, formatters=_formatters
                 ) for s in data))
        return table


class DeleteJobbinary(command.Command):
    _description = _('Delete Jobbinaries')

    def get_parser(self, prog_name):
        parser = super(DeleteJobbinary, self).get_parser(prog_name)

        parser.add_argument(
            'id',
            metavar='<id>',
            nargs='+',
            help=_('UUID or name of the jb.')
        )

        return parser

    def take_action(self, parsed_args):
        if parsed_args.id:
            client = self.app.client_manager.mrs
            for id in parsed_args.id:
                client.delete_jobbinary(id, ignore_missing=False)


class CreateJobbinary(command.ShowOne):
    _description = _('Create jobbinary')

    columns = ('id', 'name', 'url', 'description',
               'is_public', 'is_protected')

    def get_parser(self, prog_name):
        parser = super(CreateJobbinary, self).get_parser(prog_name)

        parser.add_argument(
            '--name',
            metavar='<name>',
            required=True,
            help=_('Binary object name')
        )
        parser.add_argument(
            '--is_public',
            action='store_const',
            default='false',
            const='false',
            dest='is_public'
        )
        parser.add_argument(
            '--is_protected',
            action='store_const',
            const='false',
            dest='is_protected'
        )
        parser.add_argument(
            '--url',
            metavar='<url>',
            required=True,
            help=_('Binary object URL')
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_('Binary object description')
        )

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.mrs

        attrs = {}

        if parsed_args.name:
            attrs['name'] = parsed_args.name
        if parsed_args.url:
            attrs['url'] = parsed_args.url
        if parsed_args.description:
            attrs['description'] = parsed_args.description
        if parsed_args.is_public:
            attrs['is_public'] = parsed_args.is_public
        if parsed_args.is_protected:
            attrs['is_protected'] = parsed_args.is_protected
        obj = client.create_jobbinary(
            **attrs
        )

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return display_columns, data


class UpdateJobbinary(command.ShowOne):
    _description = _('Create jobbinary')

    columns = ('id', 'name', 'url', 'description',
               'is_public', 'is_protected')

    def get_parser(self, prog_name):
        parser = super(UpdateJobbinary, self).get_parser(prog_name)

        parser.add_argument(
            'jobbinary',
            metavar='<jobbinary>',
            help=_('Binary object name or ID')
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_('Binary object name')
        )
        parser.add_argument(
            '--is_public',
            action='store_const',
            default='false',
            const='false',
            dest='is_public'
        )
        parser.add_argument(
            '--is_protected',
            action='store_const',
            const='false',
            dest='is_protected'
        )
        parser.add_argument(
            '--url',
            metavar='<url>',
            help=_('Binary object URL')
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_('Binary object description')
        )

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.mrs

        attrs = {}

        if parsed_args.name:
            attrs['name'] = parsed_args.name
        if parsed_args.url:
            attrs['url'] = parsed_args.url
        if parsed_args.description:
            attrs['description'] = parsed_args.description
        if parsed_args.is_public:
            attrs['is_public'] = parsed_args.is_public
        if parsed_args.is_protected:
            attrs['is_protected'] = parsed_args.is_protected

        jobbinary = client.find_jobbinary(
            parsed_args.jobbinary,
            ignore_missing=False
        )

        if attrs:
            obj = client.update_jobbinary(
                jobbinary=jobbinary,
                **attrs
            )
        else:
            obj = jobbinary

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return display_columns, data


class ShowJobbinary(command.ShowOne):
    _description = _('Show the Jobbinary details')

    def get_parser(self, prog_name):
        parser = super(ShowJobbinary, self).get_parser(prog_name)

        parser.add_argument(
            'jobbinary',
            metavar='<jobbinary>',
            help=_('Name or ID of the jobbinary.')
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.mrs

        obj = client.find_jobbinary(
            parsed_args.jobbinary,
            ignore_missing=False
        )

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return display_columns, data
