#   Licensed under the Apache License, Version 2.0 (the 'License'); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an 'AS IS' BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#
'''MRS clusters v1 action implementations'''
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.i18n import _
from otcextensions.common import sdk_utils

LOG = logging.getLogger(__name__)


_formatters = {
}


def _get_columns(item):
    column_map = {
    }
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


class ListJob(command.Lister):
    _description = _('List Sahara job')
    columns = (
        'id', 'name', 'type', 'description',
        'is_public', 'is_protected'
    )

    def get_parser(self, prog_name):
        parser = super(ListJob, self).get_parser(prog_name)
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

        data = client.job(**query)

        table = (self.columns,
                 (utils.get_item_properties(
                     s, self.columns, formatters=_formatters
                 ) for s in data))
        return table


class DeleteJob(command.Command):
    _description = _('Delete Job')

    def get_parser(self, prog_name):
        parser = super(DeleteJob, self).get_parser(prog_name)

        parser.add_argument(
            'id',
            metavar='<id>',
            nargs='+',
            help=_('UUID or name of the job.')
        )

        return parser

    def take_action(self, parsed_args):
        if parsed_args.id:
            client = self.app.client_manager.mrs
            for id in parsed_args.id:
                client.delete_job(id, ignore_missing=False)


class CreateJob(command.ShowOne):
    _description = _('Create job')

    columns = ('id', 'name', 'type', 'description',
               'is_public', 'is_protected')

    def get_parser(self, prog_name):
        parser = super(CreateJob, self).get_parser(prog_name)

        parser.add_argument(
            'name',
            metavar='<name>',
            help=_('Name for the job')
        )
        parser.add_argument('--is_public',
                            action='store_const',
                            default='false',
                            const='false',
                            dest='is_public')
        parser.add_argument('--is_protected',
                            action='store_const',
                            const='false',
                            dest='is_protected')
        parser.add_argument(
            '--type',
            metavar='<type>',
            required=True,
            help=_('type of the Job.')
        )

        parser.add_argument(
            '--libs',
            metavar='<libs>',
            help=_('libs of the Job.')
        )

        parser.add_argument(
            '--mains',
            metavar='<mains>',
            help=_('mains of the Job.')
        )

        parser.add_argument(
            '--interface',
            metavar='<interface>',
            help=_('interface of the Job.')
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_('Job description')
        )

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.mrs

        attrs = {}

        if parsed_args.name:
            attrs['name'] = parsed_args.name
        if parsed_args.type:
            attrs['type'] = parsed_args.type
        if parsed_args.description:
            attrs['description'] = parsed_args.description
        if parsed_args.is_public:
            attrs['is_public'] = parsed_args.is_public
        if parsed_args.is_protected:
            attrs['is_protected'] = parsed_args.is_protected
        if parsed_args.libs:
            attrs['libs'] = [parsed_args.libs]
        if parsed_args.mains:
            attrs['mains'] = [parsed_args.mains]
        if parsed_args.interface:
            attrs['interface'] = [parsed_args.interface]
        obj = client.create_job(
            **attrs
        )

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class UpdateJob(command.ShowOne):
    _description = _('Create job')

    columns = ('id', 'name', 'type', 'description',
               'is_public', 'is_protected')

    def get_parser(self, prog_name):
        parser = super(UpdateJob, self).get_parser(prog_name)

        parser.add_argument(
            'name',
            metavar='<name>',
            help=_('Name for the job')
        )
        parser.add_argument('--is_public',
                            action='store_const',
                            default='false',
                            const='false',
                            dest='is_public')
        parser.add_argument('--is_protected',
                            action='store_const',
                            const='false',
                            dest='is_protected')
        parser.add_argument(
            '--type',
            metavar='<type>',
            required=True,
            help=_('type of the Job')
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_('Job description')
        )

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.mrs

        attrs = {}

        if parsed_args.name:
            attrs['name'] = parsed_args.name
        if parsed_args.type:
            attrs['type'] = parsed_args.type
        if parsed_args.description:
            attrs['description'] = parsed_args.description
        if parsed_args.is_public:
            attrs['is_public'] = parsed_args.is_public
        if parsed_args.is_protected:
            attrs['is_protected'] = parsed_args.is_protected

        job = client.find_job(parsed_args.name,
                              ignore_missing=False)

        if job:
            obj = client.update_job(
                job=job,
                **attrs
            )

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class ShowJob(command.ShowOne):
    _description = _('Show the MRS Job details')

    def get_parser(self, prog_name):
        parser = super(ShowJob, self).get_parser(prog_name)

        parser.add_argument(
            'job',
            metavar='<job>',
            help=_('UUID of the job.')
        )

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.mrs

        obj = client.find_job(
            parsed_args.job,
        )

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)
