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

_formatters = {

}


def _get_columns(item):
    column_map = {
        'is_admin_state_up': 'admin_state_up',
    }
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


class ListPoolMember(command.Lister):
    _description = _('List members in a pool')
    columns = (
        'id', 'name', 'project_id', 'provisioning_status', 'address',
        'protocol_port', 'operating_status', 'weight')

    def get_parser(self, prog_name):
        parser = super(ListPoolMember, self).get_parser(prog_name)

        parser.add_argument(
            'pool',
            metavar='<pool>',
            help=_('Pool name or ID to list the members of.')
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_('Load balancer pool member name to query')
        )
        parser.add_argument(
            '--address',
            metavar='<address>',
            help=_('Load balancer pool member address to query')
        )
        parser.add_argument(
            '--protocol_port',
            metavar='<protocol_port>',
            type=int,
            help=_('Load balancer pool member port number to query')
        )
        parser.add_argument(
            '--weight',
            metavar='<weight>',
            type=int,
            help=_('Load balancer pool member weight to query')
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
    _description = _('Shows details of a single Member')

    def get_parser(self, prog_name):
        parser = super(ShowPoolMember, self).get_parser(prog_name)

        parser.add_argument(
            'pool',
            metavar='<pool>',
            help=_('Pool name or ID to show the members of.')
        )
        parser.add_argument(
            'member',
            metavar='<member>',
            help=_('Name or ID of the member to show.')
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

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)

        return (display_columns, data)


class CreatePoolMember(command.ShowOne):
    _description = _('Creating a member in a pool')

    def get_parser(self, prog_name):
        parser = super(CreatePoolMember, self).get_parser(prog_name)

        parser.add_argument(
            'pool',
            metavar='<pool>',
            help=_('ID or name of the pool to create the member for.')
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_('Name of the member.')
        )
        parser.add_argument(
            '--weight',
            metavar='<weight>',
            type=int,
            choices=range(0, 256),
            help='The weight of a member determines the portion of requests '
                 'or connections it services compared to the other members of '
                 'the pool.'
        )
        parser.add_argument(
            '--address',
            metavar='<ip_address>',
            help=_('The IP address of the backend member to receive traffic '
                   'from the load balancer.')
        )
        parser.add_argument(
            '--protocol_port',
            metavar='<protocol_port>',
            type=int,
            choices=range(1, 65535),
            help=_('The port on which the backend member listens for traffic.')
        )
        parser.add_argument(
            '--subnet_id',
            metavar='<subnet_id>',
            help=_('The subnet ID the member service is accessible from.')
        )
        admin_group = parser.add_mutually_exclusive_group()
        admin_group.add_argument(
            '--enable',
            action='store_true',
            default=True,
            help=_('Enable member (default).')
        )
        admin_group.add_argument(
            '--disable',
            action='store_true',
            default=None,
            help=_('Disable member.')
        )
        return parser

    def take_action(self, parsed_args):

        args = {}
        args['address'] = parsed_args.address
        if parsed_args.name:
            args['name'] = parsed_args.name
        if parsed_args.protocol_port:
            args['protocol_port'] = parsed_args.protocol_port
        if parsed_args.subnet_id:
            args['subnet_id'] = parsed_args.subnet_id
        if parsed_args.weight:
            args['weight'] = parsed_args.weight
        if parsed_args.disable:
            args['is_admin_state_up'] = False

        client = self.app.client_manager.network

        obj = client.create_pool_member(
            pool=parsed_args.pool, **args)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)

        return (display_columns, data)


class SetPoolMember(command.ShowOne):
    _description = _('Update a member')
    columns = ('ID', 'Name', 'address', 'is_admin_state_up',
               'protocol_port', 'operating_status',
               'subnet_id', 'weight', 'pool_id')

    def get_parser(self, prog_name):
        parser = super(SetPoolMember, self).get_parser(prog_name)

        parser.add_argument(
            'pool',
            metavar='<pool>',
            help=_('Pool name or ID to show the members of.')
        )
        parser.add_argument(
            'member',
            metavar='<member>',
            help=_('Name or ID of the member to show.')
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_('Name or ID of the member to update.')
        )
        parser.add_argument(
            '--weight',
            metavar='<weight>',
            type=int,
            choices=range(0, 256),
            help=_('The weight of a member determines the portion of requests '
                   'or connections it services compared to the other members '
                   'of the pool. For example, a member with a weight of 10 '
                   'receives five times as many requests as a member with a '
                   'weight of 2. A value of 0 means the member does not '
                   'receive new connections but continues to service existing '
                   'connections. A valid value is from 0 to 256. '
                   'Default is 1.')
        )
        admin_group = parser.add_mutually_exclusive_group()
        admin_group.add_argument(
            '--enable',
            action='store_true',
            default=True,
            help=_('Enable member (default).')
        )
        admin_group.add_argument(
            '--disable',
            action='store_true',
            default=None,
            help=_('Disable member.')
        )
        return parser

    def take_action(self, parsed_args):

        args = {}
        if parsed_args.disable:
            args['is_admin_state_up'] = False
        if parsed_args.name:
            args['name'] = parsed_args.name
        if parsed_args.weight:
            args['weight'] = parsed_args.weight

        client = self.app.client_manager.network

        obj = client.update_pool_member(
            pool_member=parsed_args.member,
            pool=parsed_args.pool,
            **args)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)

        return (display_columns, data)


class DeletePoolMember(command.Command):
    _description = _('Delete a member from a pool')

    def get_parser(self, prog_name):
        parser = super(DeletePoolMember, self).get_parser(prog_name)

        parser.add_argument(
            'pool',
            metavar='<pool>',
            help=_('Pool name or ID to delete the member from.')
        )
        parser.add_argument(
            'member',
            metavar='<member>',
            nargs='+',
            help=_('Name or ID of the member to be deleted.')
        )

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.network

        for member in parsed_args.member:
            obj = client.find_pool_member(name_or_id=member,
                                          pool=parsed_args.pool,
                                          ignore_missing=False)
            client.delete_pool_member(
                pool_member=obj.id,
                pool=parsed_args.pool,
                ignore_missing=False
            )

        return
