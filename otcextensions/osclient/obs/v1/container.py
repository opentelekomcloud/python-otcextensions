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
"""OBS Container v1 action implementations"""
import logging

from otcextensions.i18n import _

from osc_lib import utils
from osc_lib.cli import parseractions
from osc_lib.command import command

from otcextensions.common import sdk_utils


LOG = logging.getLogger(__name__)

STORAGE_CLASSES = ['STANDARD', 'STANDARD_IA', 'GLACIER']


def _get_columns(item):
    column_map = {
        # 'tenant_id': 'project_id',
        # 'is_ha': 'ha',
        # 'is_distributed': 'distributed',
        # 'is_admin_state_up': 'admin_state_up',
    }
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


class CreateContainer(command.ShowOne):
    _description = _("Create new container")

    def get_parser(self, prog_name):
        parser = super(CreateContainer, self).get_parser(prog_name)
        parser.add_argument(
            'container',
            metavar='<container-name>',
            help=_('New container name(s)'),
        )
        parser.add_argument(
            '--storage-class',
            metavar='{' + ','.join(STORAGE_CLASSES) + '}',
            type=lambda s: s.upper(),
            choices=STORAGE_CLASSES,
            help=_('Storage class'),
        )
        return parser

    def take_action(self, parsed_args):
        # raise NotImplementedError
        attrs = {
            'name': parsed_args.container
        }

        if parsed_args.storage_class:
            attrs['storage_class'] = parsed_args.storage_class

        data = self.app.client_manager.obs.create_container(**attrs)
        display_columns, columns = _get_columns(data)
        data = utils.get_item_properties(data, columns)
        #
        return (display_columns, data)


class DeleteContainer(command.Command):
    _description = _("Delete container")

    def get_parser(self, prog_name):
        parser = super(DeleteContainer, self).get_parser(prog_name)
        parser.add_argument(
            '--recursive', '-r',
            action='store_true',
            default=False,
            help=_('Recursively delete objects and container'),
        )
        parser.add_argument(
            'containers',
            metavar='<container>',
            nargs="+",
            help=_('Container(s) to delete'),
        )
        return parser

    def take_action(self, parsed_args):
        for container in parsed_args.containers:
            if parsed_args.recursive:
                # TODO(agoncharov) do a mass delete
                # through the boto3.delete_objects
                objs = self.app.client_manager.obs.objects(
                    container=container)
                for obj in objs:
                    self.app.client_manager.obs.delete_object(
                        container=container,
                        object=obj['name'],
                    )
            self.app.client_manager.obs.delete_container(
                container=container,
            )


class ListContainer(command.Lister):
    _description = _("List containers")

    def get_parser(self, prog_name):
        parser = super(ListContainer, self).get_parser(prog_name)
        # parser.add_argument(
        #     "--prefix",
        #     metavar="<prefix>",
        #     help=_("Filter list using <prefix>"),
        # )
        # parser.add_argument(
        #     "--marker",
        #     metavar="<marker>",
        #     help=_("Anchor for paging"),
        # )
        # parser.add_argument(
        #     "--end-marker",
        #     metavar="<end-marker>",
        #     help=_("End anchor for paging"),
        # )
        # parser.add_argument(
        #     "--limit",
        #     metavar="<num-containers>",
        #     type=int,
        #     help=_("Limit the number of containers returned"),
        # )
        # parser.add_argument(
        #     '--long',
        #     action='store_true',
        #     default=False,
        #     help=_('List additional fields in output'),
        # )
        # parser.add_argument(
        #     '--all',
        #     action='store_true',
        #     default=False,
        #     help=_('List all containers (default is 10000)'),
        # )
        return parser

    def take_action(self, parsed_args):

        # if parsed_args.long:
        #     columns = ('Name', 'Bytes', 'Count')
        # else:
        columns = ('name', 'creation_date')

        kwargs = {}
        # if parsed_args.prefix:
        #     kwargs['prefix'] = parsed_args.prefix
        # if parsed_args.marker:
        #     kwargs['marker'] = parsed_args.marker
        # if parsed_args.end_marker:
        #     kwargs['end_marker'] = parsed_args.end_marker
        # if parsed_args.limit:
        #     kwargs['limit'] = parsed_args.limit
        # if parsed_args.all:
        #     kwargs['full_listing'] = True

        data = self.app.client_manager.obs.containers(
            **kwargs
        )

        return (columns,
                (utils.get_item_properties(
                    s, columns,
                    formatters={},
                ) for s in data))


class SaveContainer(command.Command):
    _description = _("Save container contents locally")

    def get_parser(self, prog_name):
        parser = super(SaveContainer, self).get_parser(prog_name)
        parser.add_argument(
            'container',
            metavar='<container>',
            help=_('Container to save'),
        )
        return parser

    def take_action(self, parsed_args):
        raise NotImplementedError
        self.app.client_manager.obs.container_save(
            container=parsed_args.container,
        )


class SetContainer(command.Command):
    _description = _("Set container properties")

    def get_parser(self, prog_name):
        parser = super(SetContainer, self).get_parser(prog_name)
        parser.add_argument(
            'container',
            metavar='<container>',
            help=_('Container to modify'),
        )
        parser.add_argument(
            "--property",
            metavar="<key=value>",
            required=True,
            action=parseractions.KeyValueAction,
            help=_("Set a property on this container "
                   "(repeat option to set multiple properties)")
        )
        return parser

    def take_action(self, parsed_args):
        raise NotImplementedError

        self.app.client_manager.obs.container_set(
            parsed_args.container,
            properties=parsed_args.property,
        )


class ShowContainer(command.ShowOne):
    _description = _("Display container details")

    def get_parser(self, prog_name):
        parser = super(ShowContainer, self).get_parser(prog_name)
        parser.add_argument(
            'container',
            metavar='<container>',
            help=_('Container to display'),
        )
        return parser

    def take_action(self, parsed_args):

        data = self.app.client_manager.obs.get_container(
            container=parsed_args.container,
        )

        display_columns, columns = _get_columns(data)
        data = utils.get_item_properties(data, columns)
        #
        return (display_columns, data)


class UnsetContainer(command.Command):
    _description = _("Unset container properties")

    def get_parser(self, prog_name):
        parser = super(UnsetContainer, self).get_parser(prog_name)
        parser.add_argument(
            'container',
            metavar='<container>',
            help=_('Container to modify'),
        )
        parser.add_argument(
            '--property',
            metavar='<key>',
            required=True,
            action='append',
            default=[],
            help=_('Property to remove from container '
                   '(repeat option to remove multiple properties)'),
        )
        return parser

    def take_action(self, parsed_args):
        raise NotImplementedError
        self.app.client_manager.obs.container_unset(
            parsed_args.container,
            properties=parsed_args.property,
        )
