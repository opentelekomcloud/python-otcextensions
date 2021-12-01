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
from osc_lib import exceptions
from osc_lib.command import command

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)

STATUS_CHOICES = [
    'PENDING_ACCEPTANCE',
    'REJECTED',
    'EXPIRED',
    'DELETED',
    'ACTIVE'
]


def _update_vpc_info(vpcinfo):
    if 'vpc_id' in vpcinfo:
        vpcinfo['router_id'] = vpcinfo.pop('vpc_id')
    if 'tenant_id' in vpcinfo:
        vpcinfo['project_id'] = vpcinfo.pop('tenant_id')
    return vpcinfo


def set_attributes_for_print(peerings):
    for peering in peerings:
        setattr(peering, 'local_router_id',
                peering.local_vpc_info['vpc_id'])
        setattr(peering, 'peer_router_id',
                peering.peer_vpc_info['vpc_id'])
        setattr(peering, 'peer_project_id',
                peering.peer_vpc_info['tenant_id'])
        yield peering


def translate_response(func):
    def new(self, *args, **kwargs):
        response = func(self, *args, **kwargs)
        setattr(response,
                'local_vpc_info',
                _update_vpc_info(response.local_vpc_info))
        setattr(response,
                'peer_vpc_info',
                _update_vpc_info(response.peer_vpc_info))
        columns = (
            'id',
            'name',
            'local_vpc_info',
            'peer_vpc_info',
            'description',
            'created_at',
            'updated_at',
            'status'
        )
        data = utils.get_item_properties(response, columns)
        return (columns, data)
    new.__name__ = func.__name__
    new.__doc__ = func.__doc__
    return new


class ListVpcPeerings(command.Lister):

    _description = _("List Vpc Peerings.")
    columns = (
        'Id',
        'Name',
        'Status',
        'Local Router Id',
        'Peer Router Id',
        'Peer Project Id')

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
            metavar='{' + ','.join(STATUS_CHOICES) + '}',
            type=lambda s: s.upper(),
            choices=STATUS_CHOICES,
            help=_("Specifies the status of the VPC peering connection."),
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
        if data:
            data = set_attributes_for_print(data)

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


class SetVpcPeering(command.ShowOne):
    _description = _("Accept VPC peering connection Request.")

    def get_parser(self, prog_name):
        parser = super(SetVpcPeering, self).get_parser(prog_name)
        parser.add_argument(
            'peering',
            metavar='<peering>',
            help=_("Specifies the Name or ID of the VPC peering connection."),
        )
        manage_request_group = parser.add_mutually_exclusive_group()
        manage_request_group.add_argument(
            '--accept',
            action='store_true',
            help=('Accept VPC peering connection request.')
        )
        manage_request_group.add_argument(
            '--reject',
            action='store_true',
            help=('Reject VPC peering connection request.')
        )
        return parser

    @translate_response
    def take_action(self, parsed_args):
        client = self.app.client_manager.vpc
        set_args = ('accept', 'reject')
        request_status = [request for request in set_args if
                          getattr(parsed_args, request)]
        peering = client.find_peering(parsed_args.peering)
        return client.set_peering(peering.id, request_status[0])


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
            '--local-router-id',
            metavar='<local_router_id>',
            required=True,
            help=_("Specifies information about the local router_id "
                   "involved in a VPC peering connection."),
        )
        parser.add_argument(
            '--peer-router-id',
            metavar='<peer_router_id>',
            required=True,
            help=_("Specifies information about the peer router_id "
                   "involved in a VPC peering connection."),
        )
        parser.add_argument(
            '--peer-project-id',
            metavar='<peer_project_id>',
            help=_("Specifies the ID of the project to which a "
                   "peer router belongs. It is required if the peer "
                   "router is from different project."),
        )
        return parser

    @translate_response
    def take_action(self, parsed_args):
        client = self.app.client_manager.vpc
        attrs = {
            'name': parsed_args.name,
            'request_vpc_info': {
                'vpc_id': parsed_args.local_router_id
            },
            'accept_vpc_info': {
                'vpc_id': parsed_args.peer_router_id
            }
        }
        val = getattr(parsed_args, 'peer_project_id')
        if val:
            attrs['accept_vpc_info']['tenant_id'] = val
            attrs['request_vpc_info']['tenant_id'] = client.get_project_id()

        val = getattr(parsed_args, 'description')
        if val:
            attrs['description'] = val

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
