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

import logging
import json

from osc_lib.command import command
from osc_lib import exceptions
from osc_lib import utils

from otcextensions.i18n import _

from otcextensions.common import sdk_utils

LOG = logging.getLogger(__name__)


_formatters = {
    'listener_ids': sdk_utils.ListOfIdsColumn,
    'load_balancer_ids': sdk_utils.ListOfIdsColumn,
    'member_ids': sdk_utils.ListOfIdsColumn,
}


LB_ALGORITHM_VALUES = ['LEAST_CONNECTIONS', 'ROUND_ROBIN', 'SOURCE_IP']
PROTOCOL_VALUES = ['HTTP', 'HTTPS', 'PROXY', 'TCP']


class ListPool(command.Lister):
    _description = _('List LoadBalancer pools')
    columns = ('ID', 'Name', 'description', 'is_admin_state_up',
               'lb_algorithm', 'protocol', 'load_balancer_ids')

    def get_parser(self, prog_name):
        parser = super(ListPool, self).get_parser(prog_name)

        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_("Load balancer pool description to query")
        )
        parser.add_argument(
            '--lb_algorithm',
            metavar='<lb_algorithm>',
            help=_("Load balancer pool algorithm to query"
                   "one of [`LEAST_CONNECTIONS`, `ROUND_ROBIN`, `SOURCE_IP`]")
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_("Load balancer pool name to query")
        )
        parser.add_argument(
            '--protocol',
            metavar='<protocol>',
            help=_("Load balancer pool protocol to query"
                   "one of [`HTTP`, `HTTPS`, `PROXY`, `TCP`]")
        )
        parser.add_argument(
            '--load_balancer_id',
            metavar='<load_balancer_id>',
            help=_("The ID of the load balancer to query pools for")
        )
        return parser

    def take_action(self, parsed_args):

        args = {}
        if parsed_args.description:
            args['description'] = parsed_args.description
        if parsed_args.lb_algorithm:
            args['lb_algorithm'] = parsed_args.lb_algorithm
        if parsed_args.name:
            args['name'] = parsed_args.name
        if parsed_args.load_balancer_id:
            args['load_balancer_id'] = parsed_args.load_balancer_id
        if parsed_args.protocol:
            if parsed_args.protocol.upper() in PROTOCOL_VALUES:
                args['protocol'] = parsed_args.protocol
            else:
                msg = (_('Protocol %s is not one of the supported %s')
                       % (parsed_args.protocol, PROTOCOL_VALUES))
                raise exceptions.CommandError(msg)
        if parsed_args.lb_algorithm:
            if parsed_args.lb_algorithm.upper() in LB_ALGORITHM_VALUES:
                args['lb_algorithm'] = parsed_args.lb_algorithm
            else:
                msg = (_('lb_algorithm %s is not one of the supported %s')
                       % (parsed_args.lb_algorithm, LB_ALGORITHM_VALUES))
                raise exceptions.CommandError(msg)

        client = self.app.client_manager.network

        data = client.pools(**args)

        return (
            self.columns,
            (utils.get_item_properties(
                s, self.columns, formatters=_formatters
            ) for s in data))


class ShowPool(command.ShowOne):
    _description = _('Show LoadBalancer pool details')
    columns = ('ID', 'Name', 'description', 'is_admin_state_up',
               'lb_algorithm', 'protocol', 'session_persistence',
               'healthmonitor_id', 'load_balancer_ids',
               'listener_ids', 'member_ids')

    def get_parser(self, prog_name):
        parser = super(ShowPool, self).get_parser(prog_name)

        parser.add_argument(
            'pool',
            metavar='<pool>',
            help=_("Load balancer pool id to show")
        )

        return parser

    def take_action(self, parsed_args):

        args = {}

        if parsed_args.pool is not None:
            args['name_or_id'] = parsed_args.pool

        client = self.app.client_manager.network

        obj = client.find_pool(**args)

        data = utils.get_item_properties(
            obj, self.columns, formatters=_formatters)

        return (self.columns, data)


class CreatePool(command.ShowOne):
    _description = _('Create LoadBalancer Pool')
    columns = ('ID', 'Name', 'description', 'is_admin_state_up',
               'lb_algorithm', 'protocol', 'session_persistence',
               'healthmonitor_id', 'load_balancer_ids',
               'listener_ids', 'member_ids')

    def get_parser(self, prog_name):
        parser = super(CreatePool, self).get_parser(prog_name)

        parser.add_argument(
            'protocol',
            metavar='<protocol>',
            help=_("The protocol for the resource. "
                   "One of [`HTTP`, `HTTPS`, `PROXY`, `TCP`].")
        )
        parser.add_argument(
            'lb_algorithm',
            metavar='<lb_algorithm>',
            help=_("The load balancing algorithm for the pool. "
                   "One of [`LEAST_CONNECTIONS`, `ROUND_ROBIN`, `SOURCE_IP`].")
        )
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            '--listener_id',
            metavar='<listener_id>',
            help=_("The ID of the listener for the pool. "
                   "Either listener_id or loadbalancer_id must be specified.")
        )
        group.add_argument(
            '--loadbalancer_id',
            metavar='<loadbalancer_id>',
            help=_("The ID of the loadbalancer for the pool. "
                   "Either listener_id or loadbalancer_id must be specified.")
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
            '--description',
            metavar='<description>',
            help=_("A human-readable description for the resource.")
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_("Human-readable name of the resource.")
        )
        parser.add_argument(
            '--session_persistence',
            metavar='<session_persistence>',
            help=_("A JSON object specifying the session persistence "
                   "for the pool or null for no session persistence. "
                   "See Pool Session Persistence. Default is null.")
        )
        return parser

    def take_action(self, parsed_args):

        args = {}

        if parsed_args.protocol:
            if parsed_args.protocol.upper() in PROTOCOL_VALUES:
                args['protocol'] = parsed_args.protocol
            else:
                msg = (_('Protocol %s is not one of the supported %s')
                       % (parsed_args.protocol, PROTOCOL_VALUES))
                raise exceptions.CommandError(msg)
        if parsed_args.lb_algorithm:
            if parsed_args.lb_algorithm.upper() in LB_ALGORITHM_VALUES:
                args['lb_algorithm'] = parsed_args.lb_algorithm
            else:
                msg = (_('lb_algorithm %s is not one of the supported %s')
                       % (parsed_args.lb_algorithm, LB_ALGORITHM_VALUES))
                raise exceptions.CommandError(msg)

        if parsed_args.listener_id is not None:
            args['listener_id'] = parsed_args.listener_id
        if parsed_args.loadbalancer_id is not None:
            args['loadbalancer_id'] = parsed_args.loadbalancer_id
        if parsed_args.admin_state_up is not None:
            args['admin_state_up'] = parsed_args.admin_state_up
        if parsed_args.name is not None:
            args['name'] = parsed_args.name
        if parsed_args.description is not None:
            args['description'] = parsed_args.description
        if parsed_args.session_persistence is not None:
            args['session_persistence'] = json.loads(
                parsed_args.session_persistence)

        client = self.app.client_manager.network

        obj = client.create_pool(**args)

        data = utils.get_item_properties(
            obj, self.columns, formatters=_formatters)

        return (self.columns, data)


class UpdatePool(command.ShowOne):
    _description = _('Update LoadBalancer Pool details')
    columns = ('ID', 'Name', 'description', 'is_admin_state_up',
               'lb_algorithm', 'protocol', 'session_persistence',
               'healthmonitor_id', 'load_balancer_ids',
               'listener_ids', 'member_ids')

    def get_parser(self, prog_name):
        parser = super(UpdatePool, self).get_parser(prog_name)

        parser.add_argument(
            'pool',
            metavar='<pool>',
            help=_("The ID of the pool to delete.")
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
            '--description',
            metavar='<description>',
            help=_("A human-readable description for the resource.")
        )
        parser.add_argument(
            '--lb_algorithm',
            metavar='<lb_algorithm>',
            help=_("The load balancing algorithm for the pool. "
                   "One of [`LEAST_CONNECTIONS`, `ROUND_ROBIN`, `SOURCE_IP`].")
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_("Human-readable name of the resource.")
        )
        parser.add_argument(
            '--session_persistence',
            metavar='<session_persistence>',
            help=_("A JSON object specifying the session persistence "
                   "for the pool or null for no session persistence. "
                   "See Pool Session Persistence. Default is null.")
        )
        return parser

    def take_action(self, parsed_args):

        args = {}

        if parsed_args.lb_algorithm:
            if parsed_args.lb_algorithm.upper() in LB_ALGORITHM_VALUES:
                args['lb_algorithm'] = parsed_args.lb_algorithm
            else:
                msg = (_('lb_algorithm %s is not one of the supported %s')
                       % (parsed_args.lb_algorithm, LB_ALGORITHM_VALUES))
                raise exceptions.CommandError(msg)

        if parsed_args.admin_state_up is not None:
            args['admin_state_up'] = parsed_args.admin_state_up
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

        data = utils.get_item_properties(
            obj, self.columns, formatters=_formatters)

        return (self.columns, data)


class DeletePool(command.Command):
    _description = _('Delete LoadBalancer Pool')

    def get_parser(self, prog_name):
        parser = super(DeletePool, self).get_parser(prog_name)

        parser.add_argument(
            'pool',
            metavar='<pool>',
            nargs='+',
            help=_("The ID of the pool to delete.")
        )

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.network

        for pool in parsed_args.pool:
            client.delete_pool(pool=pool, ignore_missing=False)

        return
