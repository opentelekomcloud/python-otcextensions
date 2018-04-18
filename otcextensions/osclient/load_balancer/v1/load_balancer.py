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
'''LoadBalancer v1 action implementations'''
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


_formatters = {
    'pool_ids': sdk_utils.ListOfIdsColumn,
    'listener_ids': sdk_utils.ListOfIdsColumn,
}


class ListLoadBalancer(command.Lister):
    _description = _('List LoadBalancers')
    columns = (
        'ID', 'Name', 'description',
        'provisioning_status', 'operating_status', 'is_admin_state_up',
        'vip_address', 'vip_subnet_id')

    def get_parser(self, prog_name):
        parser = super(ListLoadBalancer, self).get_parser(prog_name)

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.network

        data = client.load_balancers()

        return (
            self.columns,
            (utils.get_item_properties(
                s, self.columns, formatters=_formatters
            ) for s in data))


class ShowLoadBalancer(command.ShowOne):
    _description = _('Show LoadBalancer details')
    columns = (
        'ID', 'Name', 'description',
        'provisioning_status', 'operating_status', 'is_admin_state_up',
        'provider', 'pool_ids', 'listener_ids',
        'vip_address', 'vip_subnet_id', 'vip_port_id')

    def get_parser(self, prog_name):
        parser = super(ShowLoadBalancer, self).get_parser(prog_name)

        parser.add_argument(
            'load_balancer',
            metavar='<load_balancer>',
            help=_("The Name or ID of the Load balancer to show")
        )

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.network

        obj = client.find_load_balancer(
            name_or_id=parsed_args.load_balancer,
            ignore_missing=False
        )

        data = utils.get_item_properties(
            obj, self.columns, formatters=_formatters)

        return (self.columns, data)


class CreateLoadBalancer(command.ShowOne):
    _description = _('Create LoadBalancer.')
    columns = (
        'ID', 'Name', 'description',
        'provisioning_status', 'operating_status', 'is_admin_state_up',
        'provider', 'pool_ids', 'listener_ids',
        'vip_address', 'vip_subnet_id', 'vip_port_id')

    def get_parser(self, prog_name):
        parser = super(CreateLoadBalancer, self).get_parser(prog_name)

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
            '--vip_address',
            metavar='<vip_address>',
            help=_("The IP address of the Virtual IP (VIP).")
        )
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            '--vip_network_id',
            metavar='<vip_network_id>',
            help=_("The ID of the network for the Virtual IP (VIP). "
                   "One of vip_network_id, vip_port_id, or vip_subnet_id "
                   "must be specified.")
        )
        group.add_argument(
            '--vip_port_id',
            metavar='<vip_port_id>',
            help=_("The ID of the network for the Virtual IP (VIP). "
                   "One of vip_network_id, vip_port_id, or vip_subnet_id "
                   "must be specified.")
        )
        group.add_argument(
            '--vip_subnet_id',
            metavar='<vip_subnet_id>',
            help=_("The ID of the network for the Virtual IP (VIP). "
                   "One of vip_network_id, vip_port_id, or vip_subnet_id "
                   "must be specified.")
        )
        parser.add_argument(
            '--vip_qos_policy_id',
            metavar='<vip_qos_policy_id>',
            help=_("The ID of the QoS Policy which will apply to "
                   "the Virtual IP (VIP).")
        )
        # TODO(agoncharov) a full blown listeners structure is supported by API
        # parser.add_argument(
        #     '--listeners',
        #     metavar='<listeners>',
        #     help=_("The associated listener IDs, if any.")
        # )

        return parser

    def take_action(self, parsed_args):

        args = {}

        if parsed_args.admin_state_up:
            args['admin_state_up'] = parsed_args.admin_state_up
        if parsed_args.name:
            args['name'] = parsed_args.name
        if parsed_args.description:
            args['description'] = parsed_args.description
        if parsed_args.vip_address:
            args['vip_address'] = parsed_args.vip_address
        if parsed_args.vip_network_id:
            args['vip_network_id'] = parsed_args.vip_network_id
        if parsed_args.vip_port_id:
            args['vip_port_id'] = parsed_args.vip_port_id
        if parsed_args.vip_subnet_id:
            args['vip_subnet_id'] = parsed_args.vip_subnet_id
        if parsed_args.vip_qos_policy_id:
            args['vip_qos_policy_id'] = parsed_args.vip_qos_policy_id

        client = self.app.client_manager.network

        obj = client.create_load_balancer(**args)

        data = utils.get_item_properties(
            obj, self.columns, formatters=_formatters)

        return (self.columns, data)


class UpdateLoadBalancer(command.ShowOne):
    _description = _('Update LoadBalancer details')
    columns = (
        'ID', 'Name', 'description',
        'provisioning_status', 'operating_status', 'is_admin_state_up',
        'provider', 'pool_ids', 'listener_ids',
        'vip_address', 'vip_subnet_id', 'vip_port_id')

    def get_parser(self, prog_name):
        parser = super(UpdateLoadBalancer, self).get_parser(prog_name)

        parser.add_argument(
            'load_balancer',
            metavar='<load_balancer>',
            help=_("The ID for the load balancer.")
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
            '--vip_qos_policy_id',
            metavar='<vip_qos_policy_id>',
            help=_("The ID of the QoS Policy which will apply to "
                   "the Virtual IP (VIP).")
        )

        return parser

    def take_action(self, parsed_args):

        args = {}

        if parsed_args.admin_state_up:
            args['admin_state_up'] = parsed_args.admin_state_up
        if parsed_args.name:
            args['name'] = parsed_args.name
        if parsed_args.description:
            args['description'] = parsed_args.description
        if parsed_args.vip_qos_policy_id:
            args['vip_qos_policy_id'] = parsed_args.vip_qos_policy_id

        client = self.app.client_manager.network

        obj = client.update_load_balancer(
            load_balancer=parsed_args.load_balancer,
            **args)

        data = utils.get_item_properties(
            obj, self.columns, formatters=_formatters)

        return (self.columns, data)


class DeleteLoadBalancer(command.Command):
    _description = _('Delete LoadBalancer')

    def get_parser(self, prog_name):
        parser = super(DeleteLoadBalancer, self).get_parser(prog_name)

        parser.add_argument(
            'load_balancer',
            metavar='<load_balancer>',
            nargs='+',
            help=_("The ID for the load balancer.")
        )

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.network

        for lb in parsed_args.load_balancer:
            client.delete_load_balancer(
                load_balancer=lb,
                ignore_missing=False
            )

        return
