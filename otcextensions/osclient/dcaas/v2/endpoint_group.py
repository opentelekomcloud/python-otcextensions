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
#
"""Direct Connection Endpoint Group v2 action implementation"""
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.i18n import _
from otcextensions.common import sdk_utils

LOG = logging.getLogger(__name__)


def _get_columns(item):
    column_map = {
    }
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


class ListEndpointGroups(command.Lister):
    _description = _("List of Direct Connect Endpoint Groups.")
    columns = (
        'id',
        'tenant id',
        'name',
        'description',
        'endpoints',
        'type'
    )

    def get_parser(self, prog_name):
        parser = super(ListEndpointGroups, self).get_parser(prog_name)
        parser.add_argument(
            '--id',
            metavar='<id>',
            help=_("Specifies the ID of the Direct Connect Endpoint Group.")
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_("Specifies the name of the Direct Connect Endpoint Group.")
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_("Provides supplementary information about the Direct "
                   "Connect Endpoint Group.")
        )
        parser.add_argument(
            '--tenant_id',
            metavar='<tenant_id>',
            help=_("Specifies the project ID.")
        )
        parser.add_argument(
            '--endpoints',
            metavar='<endpoints>',
            type=list,
            help=_("Specifies the list of the endpoints in a Direct Connect "
                   "Endpoint Group.")
        )
        parser.add_argument(
            '--type',
            metavar='<type>',
            help=_("Specifies the type of the Direct Connect endpoints."
                   "The value can only be cidr.")
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dcaas

        args_list = [
            'id',
            'name',
            'description',
            'endpoints',
            'tenant_id',
            'type'
        ]

        attrs = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        data = client.endpoint_groups(**attrs)

        table = (self.columns, (utils.get_dict_properties(s, self.columns)
                                for s in data))
        return table


class ShowEndpointGroup(command.ShowOne):
    _description = _("Show Direct Connection Endpoint Group.")

    def get_parser(self, prog_name):
        parser = super(ShowEndpointGroup, self).get_parser(prog_name)
        parser.add_argument(
            'endpoint_group',
            metavar='<endpoint_group>',
            help=_("Specifies the endpoint group ID or name.")
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dcaas
        obj = client.find_endpoint_group(parsed_args.endpoint_group)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class CreateEndpointGroup(command.ShowOne):
    _description = _("Create new Direct Connection Endpoint Group.")

    def get_parser(self, prog_name):
        parser = super(CreateEndpointGroup, self).get_parser(prog_name)
        parser.add_argument(
            'tenant_id',
            metavar='<tenant_id>',
            help=_("Specifies the project ID.")
        )
        parser.add_argument(
            'endpoints',
            metavar='<endpoints>',
            type=list,
            help=_("Specifies the list of the endpoints in a Direct Connect "
                   "Endpoint Group.")
        )
        parser.add_argument(
            'type',
            metavar='<type>',
            help=_("Specifies the type of the Direct Connect endpoints."
                   "The value can only be cidr.")
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_("Specifies the name of the Direct Connect "
                   "Endpoint Group.")
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_("Provides supplementary information about the "
                   "Direct Connect Endpoint Group.")
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dcaas

        args_list = [
            'tenant_id',
            'endpoints',
            'type',
            'name',
            'description'
        ]
        attrs = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        obj = client.create_endpoint_group(**attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class UpdateEndpointGroup(command.ShowOne):
    _description = _("Update a Direct Connect Endpoint Group.")

    def get_parser(self, prog_name):
        parser = super(UpdateEndpointGroup, self).get_parser(prog_name)
        parser.add_argument(
            'endpoint_group',
            metavar='<endpoint_group>',
            help=_("Specifies the Endpoint Group ID or name.")
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_("Specifies the name of the Direct Connect "
                   "Endpoint Group.")
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_("Provides supplementary information about the Direct "
                   "Connect Endpoint Group.")
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dcaas

        args_list = [
            'name',
            'description'
        ]
        attrs = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        if parsed_args.endpoint_group:
            endpoint_group = client.find_endpoint_group(
                parsed_args.endpoint_group
            )
            obj = client.update_endpoint_group(
                endpoint_group.id, **attrs
            )

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class DeleteEndpointGroup(command.Command):
    _description = _("Delete the Direct Connect Endpoint Group.")

    def get_parser(self, prog_name):
        parser = super(DeleteEndpointGroup, self).get_parser(prog_name)
        parser.add_argument(
            'endpoint_group',
            metavar='<endpoint_group>',
            help=_("Direct Connect Endpoint Group to delete.")
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dcaas
        if parsed_args.endpoint_group:
            endpoint_group = client.find_endpoint_group(
                parsed_args.endpoint_group)
            client.delete_endpoint_group(endpoint_group.id)
