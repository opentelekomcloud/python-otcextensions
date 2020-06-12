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
"""VPC Peering v2 action implementations"""
import logging

from osc_lib import utils
from osc_lib.cli import parseractions
from osc_lib import exceptions
from osc_lib.command import command

from otcextensions.i18n import _
from otcextensions.common import sdk_utils

LOG = logging.getLogger(__name__)


def _get_columns(item):
    column_map = {
    }
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


def _format_vpc_info(vpc_info_list):
    # Map the route keys to match --route option.
    if len(vpc_info_list) > 1:
        raise RuntimeError('Repeating argument is not supported')
    vpc_info = vpc_info_list[0]
    if 'router_id' in vpc_info:
        vpc_info['vpc_id'] = vpc_info.pop('router_id')
    if 'project_id' in vpc_info:
        vpc_info['tenant_id'] = vpc_info.pop('project_id')
    return vpc_info


def translate_response(func):
    def new(self, *args, **kwargs):
        response = func(self, *args, **kwargs)
        response.request_vpc_info[
            'router_id'] = response.request_vpc_info.pop('vpc_id')
        response.request_vpc_info[
            'project_id'] = response.request_vpc_info.pop('tenant_id')
        response.accept_vpc_info[
            'router_id'] = response.accept_vpc_info.pop('vpc_id')
        response.accept_vpc_info[
            'project_id'] = response.accept_vpc_info.pop('tenant_id')
        display_columns, columns = _get_columns(response)
        data = utils.get_item_properties(response, columns)
        return (display_columns, data)
    new.__name__ = func.__name__
    new.__doc__ = func.__doc__
    return new


class ListVpcPeerings(command.Lister):

    _description = _("List Vpc Peerings.")
    columns = ('Id', 'Name', 'Request Vpc Info', 'Accept Vpc Info', 'Status')

    def get_parser(self, prog_name):
        parser = super(ListVpcPeerings, self).get_parser(prog_name)

        parser.add_argument(
            '--id',
            metavar='<id>',
            help=_("Specifies the ID of the VPC peering connection."),
        )
        parser.add_argument(
            '--limit',
            metavar='<limit>',
            type=int,
            help=_("Limit to fetch number of records."),
        )
        parser.add_argument(
            '--marker',
            metavar='<marker>',
            help=_("Specifies the start resource ID of pagination query."),
        )
        parser.add_argument(
            '--project-id',
            metavar='<project_id>',
            help=_("Specifies the project ID."),
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_("Specifies the Name of the VPC peering connection."),
        )
        parser.add_argument(
            '--router-id',
            metavar='<router_id>',
            help=_("Specifies the router/vpc ID of requester/accepter "
                   "of vpc peering."),
        )
        parser.add_argument(
            '--status',
            metavar='<status>',
            help=_("Specifies the status of the VPC peering connection.\n"
                   "Possible values are as follows:\n"
                   "PENDING_ACCEPTANCE\n"
                   "REJECTED\n"
                   "EXPIRED\n"
                   "DELETED\n"
                   "ACTIVE"),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.vpc
        args_list = [
            'id',
            'name',
            'limit',
            'marker',
            'project_id',
            'router_id',
            'status']
        attrs = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        data = client.peerings(**attrs)

        return (self.columns, (utils.get_item_properties(s, self.columns)
                               for s in data))


class ShowVpcPeering(command.ShowOne):
    _description = _("Show VPC peering connection details.")

    def get_parser(self, prog_name):
        parser = super(ShowVpcPeering, self).get_parser(prog_name)
        parser.add_argument(
            'peering',
            metavar='<peering>',
            help=_("Specifies the Name or ID of the VPC peering connection."),
        )
        return parser

    @translate_response
    def take_action(self, parsed_args):
        client = self.app.client_manager.vpc
        return client.find_peering(parsed_args.peering)


class AcceptVpcPeering(command.ShowOne):
    _description = _("Accept VPC peering connection Request.")

    def get_parser(self, prog_name):
        parser = super(AcceptVpcPeering, self).get_parser(prog_name)
        parser.add_argument(
            'peering',
            metavar='<peering>',
            help=_("Specifies the Name or ID of the VPC peering connection."),
        )
        return parser

    @translate_response
    def take_action(self, parsed_args):
        client = self.app.client_manager.vpc
        peering = client.find_peering(parsed_args.peering)
        return client.accept_peering(peering.id)


class RejectVpcPeering(command.ShowOne):
    _description = _("Reject VPC peering connection Request.")

    def get_parser(self, prog_name):
        parser = super(RejectVpcPeering, self).get_parser(prog_name)
        parser.add_argument(
            'peering',
            metavar='<peering>',
            help=_("Specifies the Name or ID of the VPC peering connection."),
        )
        return parser

    @translate_response
    def take_action(self, parsed_args):
        client = self.app.client_manager.vpc
        peering = client.find_peering(parsed_args.peering)
        return client.reject_peering(peering.id)


class CreateVpcPeering(command.ShowOne):
    _description = _("Create new Vpc Peering.")

    def get_parser(self, prog_name):
        parser = super(CreateVpcPeering, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help=_("Specifies the name of the VPC peering connection."),
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_("Specifies the description of the VPC peering connection."),
        )
        parser.add_argument(
            '--request-vpc-info',
            metavar='router_id=<router_id>,project_id=<project_id>',
            dest='request_vpc_info',
            action=parseractions.MultiKeyValueAction,
            required=True,
            required_keys=['router_id'],
            optional_keys=['project_id'],
            help=_("Specifies information about the local VPC.\n"
                   "router_id: Specifies the ID of a VPC involved "
                   "in a VPC peering connection.\n"
                   "project_id: Specifies the ID of Requester's Project."
                   "project_id is optional. It is required only when creating "
                   "vpc peering connection with a vpc from different project"),
        )
        parser.add_argument(
            '--accept-vpc-info',
            metavar='router_id=<router_id>,project_id=<project_id>',
            dest='accept_vpc_info',
            required=True,
            action=parseractions.MultiKeyValueAction,
            required_keys=['router_id'],
            optional_keys=['project_id'],
            help=_("Specifies information about the peer VPC.\n"
                   "router_id: Specifies the ID of a router involved "
                   "in a VPC peering connection.\n"
                   "project_id: Specifies the ID of Requester's Project."
                   "project_id is optional. It is required only when creating "
                   "vpc peering connection with a vpc from different project"),
        )
        return parser

    @translate_response
    def take_action(self, parsed_args):
        client = self.app.client_manager.vpc
        attrs = {}
        args_list = [
            'name',
            'request_vpc_info',
            'accept_vpc_info',
            'description'
        ]
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if arg in ['request_vpc_info', 'accept_vpc_info']:
                val = _format_vpc_info(val)
            if val:
                attrs[arg] = val

        return client.create_peering(**attrs)


class UpdateVpcPeering(command.ShowOne):
    _description = _("Update a VPC peering connection.")

    def get_parser(self, prog_name):
        parser = super(UpdateVpcPeering, self).get_parser(prog_name)
        parser.add_argument(
            'peering',
            metavar='<peering>',
            help=_("Specifies the Name or ID of the VPC peering connection."),
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_("Specifies the new name of the VPC peering connection."),
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_("Specifies the new descrition of the VPC peering "
                   "connection."),
        )
        return parser

    @translate_response
    def take_action(self, parsed_args):
        client = self.app.client_manager.vpc
        args_list = [
            'name', 'description'
        ]
        attrs = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val
        peering = client.find_peering(parsed_args.peering)

        return client.update_peering(peering.id, **attrs)


class DeleteVpcPeering(command.Command):

    _description = _("Deletes VPC Peering.")

    def get_parser(self, prog_name):
        parser = super(DeleteVpcPeering, self).get_parser(prog_name)
        parser.add_argument(
            'peering',
            metavar='<peering>',
            nargs='+',
            help=_("VPC Peering(s) to delete (Name or ID)"),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.vpc
        result = 0
        for peering in parsed_args.peering:
            try:
                obj = client.find_peering(peering)
                client.delete_peering(obj.id)
            except Exception as e:
                result += 1
                LOG.error(_("Failed to delete VPC peering connection with "
                          "name or ID '%(peering)s': %(e)s"),
                          {'peering': peering, 'e': e})
        if result > 0:
            total = len(parsed_args.peering)
            msg = (_("%(result)s of %(total)s VPC peering(s) failed "
                   "to delete.") % {'result': result, 'total': total})
            raise exceptions.CommandError(msg)
