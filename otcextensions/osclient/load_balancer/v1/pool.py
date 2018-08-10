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
'''LoadBalancer Pool v1 action implementations'''
import json
import logging

from osc_lib import exceptions
from osc_lib import utils
from osc_lib.command import command

from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


_formatters = {
    'health_monitor_ids': sdk_utils.ListOfIdsColumnBR,
    'listener_ids': sdk_utils.ListOfIdsColumnBR,
    'load_balancer_ids': sdk_utils.ListOfIdsColumnBR,
    'member_ids': sdk_utils.ListOfIdsColumnBR,
}


LB_ALGORITHM_VALUES = ['LEAST_CONNECTIONS', 'ROUND_ROBIN', 'SOURCE_IP']
PROTOCOL_VALUES = ['HTTP', 'HTTPS', 'PROXY', 'TCP']


def _get_columns(item):
    column_map = {
        'is_admin_state_up': 'admin_state_up',
        'load_balancer_ids': 'loadbalancers',
        'listener_ids': 'listeners',
        'status': 'provisioning_status',
        'health_monitor_id': 'healthmonitor_id'
        # 'listeners': 'listener_ids',
        # 'pools': 'pool_ids',
    }
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


class ListPool(command.Lister):
    _description = _('List LoadBalancer pools')
    column_headers = (
        'id', 'name', 'project_id', 'provisioning_status', 'protocol',
        'lb_algorithm', 'admin_state_up')
    columns = (
        'id', 'name', 'project_id', 'provisioning_status', 'protocol',
        'lb_algorithm', 'is_admin_state_up')

    def get_parser(self, prog_name):
        parser = super(ListPool, self).get_parser(prog_name)

        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_('Load balancer pool description to query')
        )
        parser.add_argument(
            '--lb_algorithm',
            metavar='{' + ','.join(LB_ALGORITHM_VALUES) + '}',
            type=lambda s: s.upper(),
            choices=LB_ALGORITHM_VALUES,
            help=_('Load balancer pool algorithm to query'
                   'one of [`LEAST_CONNECTIONS`, `ROUND_ROBIN`, `SOURCE_IP`]')
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_('Load balancer pool name to query')
        )
        parser.add_argument(
            '--protocol',
            metavar='{' + ','.join(PROTOCOL_VALUES) + '}',
            type=lambda s: s.upper(),
            choices=PROTOCOL_VALUES,
            help=_('Load balancer pool protocol to query'
                   'one of [`HTTP`, `HTTPS`, `PROXY`, `TCP`]')
        )
        parser.add_argument(
            '--load_balancer',
            metavar='<load_balancer>',
            help=_('Filter by load balancer (name or ID).')
        )
        # parser.add_argument(
        #     '--listener',
        #     metavar='<listener>',
        #     help=_('Filter by listener (name or ID).')
        # )
        return parser

    def take_action(self, parsed_args):

        args = {}
        if parsed_args.description:
            args['description'] = parsed_args.description
        if parsed_args.lb_algorithm:
            args['lb_algorithm'] = parsed_args.lb_algorithm
        if parsed_args.name:
            args['name'] = parsed_args.name
        if parsed_args.load_balancer:
            args['load_balancer_id'] = parsed_args.load_balancer
        if parsed_args.protocol:
            args['protocol'] = parsed_args.protocol
        if parsed_args.lb_algorithm:
            args['lb_algorithm'] = parsed_args.lb_algorithm
        # if parsed_args.listener:
        #     args['listener_id'] = parsed_args.listener

        client = self.app.client_manager.network

        data = client.pools(**args)

        return (
            self.column_headers,
            (utils.get_item_properties(
                s, self.columns, formatters=_formatters
            ) for s in data))


class ShowPool(command.ShowOne):
    _description = _('Show LoadBalancer pool details')

    def get_parser(self, prog_name):
        parser = super(ShowPool, self).get_parser(prog_name)

        parser.add_argument(
            'pool',
            metavar='<pool>',
            help=_('Load balancer pool id to show.')
        )

        return parser

    def take_action(self, parsed_args):

        args = {}

        client = self.app.client_manager.network

        obj = client.find_pool(
            name_or_id=parsed_args.pool,
            ignore_missing=False,
            **args
        )

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)

        return (display_columns, data)


class CreatePool(command.ShowOne):
    _description = _('Create a pool')

    def get_parser(self, prog_name):
        parser = super(CreatePool, self).get_parser(prog_name)

        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_('Set pool name.')
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_('Set pool description.')
        )
        parser.add_argument(
            '--protocol',
            metavar='{' + ','.join(PROTOCOL_VALUES) + '}',
            type=lambda s: s.upper(),
            choices=PROTOCOL_VALUES,
            required=True,
            help=_('The protocol for the pool. '
                   'One of [`HTTP`, `HTTPS`, `PROXY`, `TCP`].')
        )
        parser.add_argument(
            '--lb_algorithm',
            metavar='{' + ','.join(LB_ALGORITHM_VALUES) + '}',
            type=lambda s: s.upper(),
            choices=LB_ALGORITHM_VALUES,
            required=True,
            help=_('The load balancing algorithm for the pool. '
                   'One of [`LEAST_CONNECTIONS`, `ROUND_ROBIN`, `SOURCE_IP`].')
        )
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            '--listener_id',
            metavar='<listener>',
            help=_('The ID of the listener for the pool. '
                   'Either listener_id or loadbalancer_id must be specified.')
        )
        group.add_argument(
            '--loadbalancer_id',
            metavar='<loadbalancer>',
            help=_('The ID of the loadbalancer for the pool. '
                   'Either listener_id or loadbalancer_id must be specified.')
        )
        parser.add_argument(
            '--session_persistence',
            metavar='<session_persistence>',
            help=_('A JSON object specifying the session persistence '
                   'for the pool or null for no session persistence. '
                   'See Pool Session Persistence. Default is null.')
        )
        admin_group = parser.add_mutually_exclusive_group()
        admin_group.add_argument(
            '--enable',
            action='store_true',
            default=True,
            help=_('Enable pool (default).')
        )
        admin_group.add_argument(
            '--disable',
            action='store_true',
            default=None,
            help=_('Disable pool.')
        )

        return parser

    def take_action(self, parsed_args):

        args = {}

        if parsed_args.protocol:
            args['protocol'] = parsed_args.protocol
        if parsed_args.lb_algorithm:
            args['lb_algorithm'] = parsed_args.lb_algorithm
        if parsed_args.listener_id is not None:
            args['listener_id'] = parsed_args.listener_id
        if parsed_args.loadbalancer_id is not None:
            args['loadbalancer_id'] = parsed_args.loadbalancer_id
        if parsed_args.disable is not None:
            args['is_admin_state_up'] = False
        if parsed_args.name is not None:
            args['name'] = parsed_args.name
        if parsed_args.description is not None:
            args['description'] = parsed_args.description
        if parsed_args.session_persistence is not None:
            args['session_persistence'] = json.loads(
                parsed_args.session_persistence)

        client = self.app.client_manager.network

        obj = client.create_pool(**args)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)

        return (display_columns, data)


class SetPool(command.ShowOne):
    _description = _('Update a pool')

    def get_parser(self, prog_name):
        parser = super(SetPool, self).get_parser(prog_name)

        parser.add_argument(
            'pool',
            metavar='<pool>',
            help=_('The ID of the pool to update.')
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_('Human-readable name of the resource.')
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_('A human-readable description for the resource.')
        )
        parser.add_argument(
            '--session_persistence',
            metavar='<session_persistence>',
            help=_('A JSON object specifying the session persistence '
                   'for the pool or null for no session persistence. '
                   'See Pool Session Persistence. Default is null.')
        )
        parser.add_argument(
            '--lb_algorithm',
            metavar='{' + ','.join(LB_ALGORITHM_VALUES) + '}',
            type=lambda s: s.upper(),
            choices=LB_ALGORITHM_VALUES,
            help=_('The load balancing algorithm for the pool. '
                   'One of [`LEAST_CONNECTIONS`, `ROUND_ROBIN`, `SOURCE_IP`].')
        )
        admin_group = parser.add_mutually_exclusive_group()
        admin_group.add_argument(
            '--enable',
            action='store_true',
            default=True,
            help=_('Enable pool (default).')
        )
        admin_group.add_argument(
            '--disable',
            action='store_true',
            default=None,
            help=_('Disable pool.')
        )
        return parser

    def take_action(self, parsed_args):

        args = {}

        if parsed_args.lb_algorithm:
            args['lb_algorithm'] = parsed_args.lb_algorithm
        if parsed_args.disable is not None:
            args['is_admin_state_up'] = False
        if parsed_args.name is not None:
            args['name'] = parsed_args.name
        if parsed_args.description is not None:
            args['description'] = parsed_args.description
        if parsed_args.session_persistence is not None:
            args['session_persistence'] = json.loads(
                parsed_args.session_persistence)

        client = self.app.client_manager.network

        obj = client.update_pool(
            pool=parsed_args.pool,
            **args)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)

        return (display_columns, data)


class DeletePool(command.Command):
    _description = _('Delete a pool')

    def get_parser(self, prog_name):
        parser = super(DeletePool, self).get_parser(prog_name)

        parser.add_argument(
            'pool',
            metavar='<pool>',
            nargs='+',
            help=_('The ID of the pool to delete.')
        )

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.network

        for pool in parsed_args.pool:
            obj = client.find_pool(name_or_id=pool, ignore_missing=False)
            client.delete_pool(pool=obj.id, ignore_missing=False)

        return
