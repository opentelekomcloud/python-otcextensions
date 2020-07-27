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
"""VPC Route v2 action implementations"""
import logging

from osc_lib import utils
from osc_lib import exceptions
from osc_lib.command import command

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def set_attributes_for_print(routes):
    for route in routes:
        yield route


def translate_response(func):
    def new(self, *args, **kwargs):
        response = func(self, *args, **kwargs)
        columns = (
            'id',
            'type',
            'nexthop',
            'destination',
            'router_id',
            'project_id'
        )
        data = utils.get_item_properties(response, columns)
        return (columns, data)
    new.__name__ = func.__name__
    new.__doc__ = func.__doc__
    return new


class ListVpcRoutes(command.Lister):

    _description = _("List Vpc Routes.")
    columns = (
        'Id',
        'Type',
        'Router Id',
        'Project Id',
        'NextHop',
        'Destination'
    )

    def get_parser(self, prog_name):
        parser = super(ListVpcRoutes, self).get_parser(prog_name)

        parser.add_argument(
            '--id',
            metavar='<id>',
            help=_("Specifies the ID of the VPC route."),
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
            '--router-id',
            metavar='<router_id>',
            help=_("Specifies the router/vpc ID."),
        )
        parser.add_argument(
            '--destination',
            metavar='<destination>',
            help=_("Specifies that the route destination address (CIDR) "
                   "is used as the filtering condition."),
        )
        parser.add_argument(
            '--type',
            metavar='<type>',
            help=_("Specifies that the type is used as the filtering "
                   "condition. Currently, the value can only be peering."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.vpc
        args_list = [
            'id',
            'type',
            'limit',
            'marker',
            'project_id',
            'router_id',
            'destination']
        attrs = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        data = client.routes(**attrs)
        if data:
            data = set_attributes_for_print(data)

        return (self.columns, (utils.get_item_properties(s, self.columns)
                               for s in data))


class ShowVpcRoute(command.ShowOne):
    _description = _("Show VPC Route Details.")

    def get_parser(self, prog_name):
        parser = super(ShowVpcRoute, self).get_parser(prog_name)
        parser.add_argument(
            'route',
            metavar='<route>',
            help=_("Specifies the ID of the VPC route."),
        )
        return parser

    @translate_response
    def take_action(self, parsed_args):
        client = self.app.client_manager.vpc
        return client.get_route(parsed_args.route)


class AddVpcRoute(command.ShowOne):
    _description = _("Add Vpc Route.")

    def get_parser(self, prog_name):
        parser = super(AddVpcRoute, self).get_parser(prog_name)
        parser.add_argument(
            '--destination',
            metavar='<destination>',
            required=True,
            help=_("Specifies the destination address in the CIDR "
                   "notation format, for example, 192.168.200.0/24."),
        )
        parser.add_argument(
            '--nexthop',
            metavar='<nexthop>',
            required=True,
            help=_("Specifies the next hop. If the type is "
                   "peering, enter the VPC peering connection ID."),
        )
        parser.add_argument(
            '--type',
            metavar='<type>',
            default='peering',
            help=_("Specifies the route type. Currently, the value can "
                   "only be peering."),
        )
        parser.add_argument(
            '--router-id',
            metavar='<router_id>',
            required=True,
            help=_("Specifies the requesting router ID for creating a route."),
        )
        return parser

    @translate_response
    def take_action(self, parsed_args):
        client = self.app.client_manager.vpc
        args_list = [
            'type',
            'router_id',
            'destination',
            'nexthop']
        attrs = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        return client.add_route(**attrs)


class DeleteVpcRoute(command.Command):

    _description = _("Deletes VPC Route.")

    def get_parser(self, prog_name):
        parser = super(DeleteVpcRoute, self).get_parser(prog_name)
        parser.add_argument(
            'route',
            metavar='<route>',
            nargs='+',
            help=_("VPC Routes(s) ID to delete"),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.vpc
        result = 0
        for route in parsed_args.route:
            try:
                obj = client.get_route(route)
                client.delete_route(obj.id)
            except Exception as e:
                result += 1
                LOG.error(_("Failed to delete VPC route with "
                          "ID '%(route)s': %(e)s"),
                          {'route': route, 'e': e})
        if result > 0:
            total = len(parsed_args.route)
            msg = (_("%(result)s of %(total)s VPC route(s) failed "
                   "to delete.") % {'result': result, 'total': total})
            raise exceptions.CommandError(msg)
