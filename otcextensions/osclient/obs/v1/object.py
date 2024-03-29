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
'''OBS Object v1 action implementations'''
import logging
import os

from otcextensions.i18n import _

from osc_lib import exceptions
from osc_lib import utils
from osc_lib.cli import parseractions
from osc_lib.command import command

from otcextensions.common import sdk_utils

LOG = logging.getLogger(__name__)

_file_hash_cache = dict()


def _get_columns(item):
    column_map = {
        'Content Type': 'content_type',
        'Last Modified': 'last_modified_at',
        'Hash': 'etag',
        'Bytes': 'content_length',
        'Accept Ranges': 'accept_ranges',
    }
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


class CreateObject(command.ShowOne):
    _description = _('Upload object to container')

    def get_parser(self, prog_name):
        parser = super(CreateObject, self).get_parser(prog_name)
        parser.add_argument(
            'container',
            metavar='<container>',
            help=_('Container for new object'),
        )
        parser.add_argument(
            'objects',
            metavar='<filename>',
            nargs='+',
            help=_('Local filename(s) to upload'),
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_('Upload a file and rename it. '
                   'Can only be used when uploading a single object')
        )
        parser.add_argument(
            '--name-prefix',
            metavar='<prefix>',
            help=_('Object name prefix. '
                   'Useful when uploading multiple objects'),
            default=''
        )
        return parser

    def take_action(self, parsed_args):
        if parsed_args.name:
            if len(parsed_args.objects) > 1:
                msg = _('Attempting to upload multiple objects and '
                        'using --name is not permitted')
                raise exceptions.CommandError(msg)
        results = []
        for obj in parsed_args.objects:
            if len(obj) > 1024:
                LOG.warning(
                    _('Object name is %s characters long, default limit'
                      ' is 1024'), len(obj))
            prefix = parsed_args.name_prefix + os.path.basename(obj)
            data = self.app.client_manager.obs.create_object(
                container=parsed_args.container,
                name=parsed_args.name or prefix,
                data=open(obj, 'r').read()
            )
            results.append(data)

        display_columns, columns = _get_columns(data)
        data = utils.get_item_properties(data, columns)
        return (display_columns, data)


class DeleteObject(command.Command):
    _description = _('Delete object from container')

    def get_parser(self, prog_name):
        parser = super(DeleteObject, self).get_parser(prog_name)
        parser.add_argument(
            'container',
            metavar='<container>',
            help=_('Delete object(s) from <container>'),
        )
        parser.add_argument(
            'objects',
            metavar='<object>',
            nargs='+',
            help=_('Object(s) to delete'),
        )
        return parser

    def take_action(self, parsed_args):

        for obj in parsed_args.objects:
            self.app.client_manager.obs.delete_object(
                container=parsed_args.container,
                obj=obj,
            )


class ListObject(command.Lister):
    _description = _('List objects')

    def get_parser(self, prog_name):
        parser = super(ListObject, self).get_parser(prog_name)
        parser.add_argument(
            'container',
            metavar='<container>',
            help=_('Container to list'),
        )
        parser.add_argument(
            '--prefix',
            metavar='<prefix>',
            help=_('Filter list using <prefix>'),
        )
        parser.add_argument(
            '--delimiter',
            metavar='<delimiter>',
            help=_('Roll up items with <delimiter>'),
        )
        parser.add_argument(
            '--marker',
            metavar='<marker>',
            help=_('Anchor for paging'),
        )
        parser.add_argument(
            '--end-marker',
            metavar='<end-marker>',
            help=_('End anchor for paging'),
        )
        parser.add_argument(
            '--limit',
            metavar='<num-objects>',
            type=int,
            help=_('Limit the number of objects returned'),
        )
        parser.add_argument(
            '--long',
            action='store_true',
            default=False,
            help=_('List additional fields in output'),
        )
        parser.add_argument(
            '--all',
            action='store_true',
            default=False,
            help=_('List all objects in container (default is 10000)'),
        )
        return parser

    def take_action(self, parsed_args):

        if parsed_args.long:
            columns = (
                'name',
                'content length',
                'etag',
                # 'Content Type',
                'last modified',
            )
        else:
            columns = ('name',)

        kwargs = {}
        if parsed_args.prefix:
            kwargs['prefix'] = parsed_args.prefix
        if parsed_args.delimiter:
            kwargs['delimiter'] = parsed_args.delimiter
        if parsed_args.marker:
            kwargs['marker'] = parsed_args.marker
        if parsed_args.end_marker:
            kwargs['end_marker'] = parsed_args.end_marker
        if parsed_args.limit:
            kwargs['limit'] = parsed_args.limit
        if parsed_args.all:
            kwargs['full_listing'] = True

        data = self.app.client_manager.obs.objects(
            container=parsed_args.container,
            **kwargs
        )

        return (columns,
                (utils.get_item_properties(
                    s, columns,
                    formatters={},
                ) for s in data))


class SaveObject(command.Command):
    _description = _('Save object locally')

    def get_parser(self, prog_name):
        parser = super(SaveObject, self).get_parser(prog_name)
        parser.add_argument(
            '--file',
            metavar='<filename>',
            default='-',
            help=_('Destination filename (defaults to object name); using "-"'
                   ' as the filename will print the file to stdout'),
        )
        parser.add_argument(
            'container',
            metavar='<container>',
            help=_('Download <object> from <container>'),
        )
        parser.add_argument(
            'object',
            metavar='<object>',
            help=_('Object to save'),
        )
        return parser

    def take_action(self, parsed_args):

        self.app.client_manager.obs.download_object(
            container=parsed_args.container,
            obj=parsed_args.object,
            file=parsed_args.file
        )


class SetObject(command.Command):
    _description = _('Set object properties')

    def get_parser(self, prog_name):
        parser = super(SetObject, self).get_parser(prog_name)
        parser.add_argument(
            'container',
            metavar='<container>',
            help=_('Modify <object> from <container>'),
        )
        parser.add_argument(
            'object',
            metavar='<object>',
            help=_('Object to modify'),
        )
        parser.add_argument(
            '--property',
            metavar='<key=value>',
            required=True,
            action=parseractions.KeyValueAction,
            help=_('Set a property on this object '
                   '(repeat option to set multiple properties)')
        )
        return parser

    def take_action(self, parsed_args):
        self.app.client_manager.obs.object_set(
            parsed_args.container,
            parsed_args.object,
            properties=parsed_args.property,
        )


class ShowObject(command.ShowOne):
    _description = _('Display object details')

    def get_parser(self, prog_name):
        parser = super(ShowObject, self).get_parser(prog_name)
        parser.add_argument(
            'container',
            metavar='<container>',
            help=_('Display <object> from <container>'),
        )
        parser.add_argument(
            'object',
            metavar='<object>',
            help=_('Object to display'),
        )
        return parser

    def take_action(self, parsed_args):

        data = self.app.client_manager.obs.get_object(
            container=parsed_args.container,
            obj=parsed_args.object,
        )

        display_columns, columns = _get_columns(data)
        data = utils.get_item_properties(data, columns)

        return (display_columns, data)


class UnsetObject(command.Command):
    _description = _('Unset object properties')

    def get_parser(self, prog_name):
        parser = super(UnsetObject, self).get_parser(prog_name)
        parser.add_argument(
            'container',
            metavar='<container>',
            help=_('Modify <object> from <container>'),
        )
        parser.add_argument(
            'object',
            metavar='<object>',
            help=_('Object to modify'),
        )
        parser.add_argument(
            '--property',
            metavar='<key>',
            required=True,
            action='append',
            default=[],
            help=_('Property to remove from object '
                   '(repeat option to remove multiple properties)'),
        )
        return parser

    def take_action(self, parsed_args):
        self.app.client_manager.obs.object_unset(
            parsed_args.container,
            parsed_args.object,
            properties=parsed_args.property,
        )
