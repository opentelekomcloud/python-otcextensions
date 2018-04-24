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
'''LoadBalancer Pool Member v1 action implementations'''
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


class ListPoolMember(command.Lister):
    _description = _('List LoadBalancer pool members')
    columns = ('ID', 'Name', 'address', 'is_admin_state_up',
               'protocol_port', 'subnet_id', 'operating_status', 'weight')

    def get_parser(self, prog_name):
        parser = super(ListPoolMember, self).get_parser(prog_name)

        parser.add_argument(
            'pool',
            metavar='<pool>',
            help=_("The ID of the pool to query")
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_("Load balancer pool member name to query")
        )
        parser.add_argument(
            '--address',
            metavar='<address>',
            help=_("Load balancer pool member address to query")
        )
        parser.add_argument(
            '--protocol_port',
            metavar='<protocol_port>',
            type=int,
            help=_("Load balancer pool member port number to query")
        )
        parser.add_argument(
            '--weight',
            metavar='<weight>',
            type=int,
            help=_("Load balancer pool member weight to query")
        )

        return parser

    def take_action(self, parsed_args):

        args = {}
        if parsed_args.address:
            args['address'] = parsed_args.address
        if parsed_args.protocol_port:
            args['protocol_port'] = parsed_args.protocol_port
        if parsed_args.name:
            args['name'] = parsed_args.name
        if parsed_args.weight:
            args['weight'] = parsed_args.weight

        client = self.app.client_manager.network

        data = client.pool_members(pool=parsed_args.pool, **args)

        return (
            self.columns,
            (utils.get_item_properties(
                s, self.columns
            ) for s in data))


class ShowPoolMember(command.ShowOne):
    _description = _('Show LoadBalancer pool member details')
    columns = ('ID', 'Name', 'address', 'is_admin_state_up',
               'protocol_port', 'operating_status',
               'subnet_id', 'weight', 'pool_id')

    def get_parser(self, prog_name):
        parser = super(ShowPoolMember, self).get_parser(prog_name)

        parser.add_argument(
            'pool',
            metavar='<pool>',
            help=_("The ID of the pool to query")
        )
        parser.add_argument(
            'member',
            metavar='<member>',
            help=_("Load balancer pool member id or name to show")
        )

        return parser

    def take_action(self, parsed_args):

        args = {}

        client = self.app.client_manager.network

        obj = client.find_pool_member(
            name_or_id=parsed_args.member,
            pool=parsed_args.pool,
            ignore_missing=False,
            **args)

        data = utils.get_item_properties(
            obj, self.columns,)

        return (self.columns, data)


class CreatePoolMember(command.ShowOne):
    _description = _('Create LoadBalancer pool member')
    columns = ('ID', 'Name', 'address', 'is_admin_state_up',
               'protocol_port', 'operating_status',
               'subnet_id', 'weight', 'pool_id')

    def get_parser(self, prog_name):
        parser = super(CreatePoolMember, self).get_parser(prog_name)

        parser.add_argument(
            'pool',
            metavar='<pool>',
            help=_("The ID of the pool to query")
        )
        parser.add_argument(
            'address',
            metavar='<address>',
            help=_("The IP address of the backend member to receive traffic "
                   "from the load balancer.")
        )
        parser.add_argument(
            'protocol_port',
            metavar='<protocol_port>',
            type=int,
            help=_("The port on which the backend member listens for traffic.")
        )
        parser.add_argument(
            '--admin_state_up',
            dest='admin_state_up',
            type=sdk_utils.str2bool,
            nargs='?',
            help=_("The administrative state of the resource, which is up "
                   "(true) or down (false). Default is true.")
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_("Human-readable name of the resource.")
        )
        parser.add_argument(
            '--subnet_id',
            metavar='<subnet_id>',
            help=_("The subnet ID the member service is accessible from.")
        )
        parser.add_argument(
            '--weight',
            metavar='<weight>',
            type=int,
            help=_("The weight of a member determines the portion of requests "
                   "or connections it services compared to the other members "
                   "of the pool. For example, a member with a weight of 10 "
                   "receives five times as many requests as a member with a "
                   "weight of 2. A value of 0 means the member does not "
                   "receive new connections but continues to service existing "
                   "connections. A valid value is from 0 to 256. "
                   "Default is 1.")
        )
        return parser

    def take_action(self, parsed_args):

        args = {}
        args['address'] = parsed_args.address
        if parsed_args.admin_state_up:
            args['admin_state_up'] = parsed_args.admin_state_up
        if parsed_args.name:
            args['name'] = parsed_args.name
        if parsed_args.protocol_port:
            args['protocol_port'] = parsed_args.protocol_port
        if parsed_args.subnet_id:
            args['subnet_id'] = parsed_args.subnet_id
        if parsed_args.weight:
            args['weight'] = parsed_args.weight

        client = self.app.client_manager.network

        obj = client.create_pool_member(
            pool=parsed_args.pool, **args)

        data = utils.get_item_properties(
            obj, self.columns,)

        return (self.columns, data)


class UpdatePoolMember(command.ShowOne):
    _description = _('Update LoadBalancer pool member details')
    columns = ('ID', 'Name', 'address', 'is_admin_state_up',
               'protocol_port', 'operating_status',
               'subnet_id', 'weight', 'pool_id')

    def get_parser(self, prog_name):
        parser = super(UpdatePoolMember, self).get_parser(prog_name)

        parser.add_argument(
            'pool',
            metavar='<pool>',
            help=_("The ID of the pool to query.")
        )
        parser.add_argument(
            'member',
            metavar='<member>',
            help=_("The ID of the pool member.")
        )
        parser.add_argument(
            '--admin_state_up',
            dest='admin_state_up',
            type=sdk_utils.str2bool,
            nargs='?',
            help=_("The administrative state of the resource, which is up "
                   "(true) or down (false). Default is true.")
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_("Human-readable name of the resource.")
        )
        parser.add_argument(
            '--weight',
            metavar='<weight>',
            type=int,
            help=_("The weight of a member determines the portion of requests "
                   "or connections it services compared to the other members "
                   "of the pool. For example, a member with a weight of 10 "
                   "receives five times as many requests as a member with a "
                   "weight of 2. A value of 0 means the member does not "
                   "receive new connections but continues to service existing "
                   "connections. A valid value is from 0 to 256. "
                   "Default is 1.")
        )
        return parser

    def take_action(self, parsed_args):

        args = {}
        if parsed_args.admin_state_up:
            args['admin_state_up'] = parsed_args.admin_state_up
        if parsed_args.name:
            args['name'] = parsed_args.name
        if parsed_args.weight:
            args['weight'] = parsed_args.weight

        client = self.app.client_manager.network

        obj = client.update_pool_member(
            pool_member=parsed_args.member,
            pool=parsed_args.pool,
            **args)

        data = utils.get_item_properties(
            obj, self.columns,)

        return (self.columns, data)


class DeletePoolMember(command.Command):
    _description = _('Delete LoadBalancer pool member')

    def get_parser(self, prog_name):
        parser = super(DeletePoolMember, self).get_parser(prog_name)

        parser.add_argument(
            'pool',
            metavar='<pool>',
            help=_("The ID of the pool to query.")
        )
        parser.add_argument(
            'member',
            metavar='<member>',
            nargs='+',
            help=_("The ID of the pool member.")
        )

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.network

        for member in parsed_args.member:
            client.delete_pool_member(
                pool_member=member,
                pool=parsed_args.pool,
                ignore_missing=False
            )

        return
