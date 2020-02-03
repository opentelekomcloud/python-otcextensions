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
"""DNAT v2 action implementations"""
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


class ListDnatRules(command.Lister):

    _description = _("List DNAT Rules.")
    columns = (
        'Id',
        'Nat Gateway Id',
        'Port Id',
        'Private IP',
        'Floating Ip Address',
        'Protocol',
        'Status'
    )

    def get_parser(self, prog_name):
        parser = super(ListDnatRules, self).get_parser(prog_name)

        parser.add_argument(
            '--id',
            metavar='<id>',
            help=_('Specifies the ID of the SNAT rule.'))
        parser.add_argument(
            '--limit',
            metavar='<limit>',
            type=int,
            help=_('Limit to fetch number of records.'))
        parser.add_argument(
            '--project-id',
            metavar='<tenant_id>',
            dest='tenant_id',
            help=_('Specifies the project ID.'))
        parser.add_argument(
            '--nat-gateway-id',
            metavar='<nat_gateway_id>',
            help=_('Specifies the NAT gateway ID.'))
        parser.add_argument(
            '--port-id',
            metavar='<port_id>',
            help=_('Specifies the port ID of an ECS or a BMS.'))
        parser.add_argument(
            '--private-ip',
            metavar='<private_ip>',
            help=_('Specifies the private IP address, for example, '
                   'the IP address of a Direct Connect connection.'))
        parser.add_argument(
            '--internal-service-port',
            metavar='<internal_service_port>',
            help=_('Specifies port used by ECSs or BMSs toprovide '
                   'services for external systems.'))
        parser.add_argument(
            '--floating-ip-id',
            metavar='<floating_ip_id>',
            help=_('Specifies the EIP ID.'))
        parser.add_argument(
            '--floating-ip-address',
            metavar='<floating_ip_address>',
            help=_('Specifies the EIP.'))
        parser.add_argument(
            '--external-service-port',
            metavar='<external_service_port>',
            help=_('Specifies the port for providing external services.'))
        parser.add_argument(
            '--protocol',
            metavar='<protocol>',
            help=_('Specifies the protocol type.'))
        parser.add_argument(
            '--status',
            metavar='<status>',
            help=_('Specifies the status of the DNAT rule.'))
        parser.add_argument(
            '--admin-state-up',
            metavar='<admin_state_up>',
            help=_('Specifies whether the DNAT rule is enabled or disabled.'))
        parser.add_argument(
            '--created-at',
            metavar='<created_at>',
            help=_('Specifies when the DNAT rule is created (UTC time). '
                   'Its valuerounds to 6 decimal places forseconds. '
                   'The format is yyyy-mm-ddhh:mm:ss.'))

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.nat
        args_list = [
            'id',
            'limit',
            'tenant_id',
            'nat_gateway_id',
            'port_id',
            'private_ip',
            'internal_service_port',
            'floating_ip_id',
            'floating_ip_address',
            'external_service_port',
            'protocol',
            'status',
            'admin_state_up',
            'created_at'
        ]
        attrs = {}
        for arg in args_list:
            if getattr(parsed_args, arg):
                attrs[arg] = getattr(parsed_args, arg)

        data = client.dnat_rules(**attrs)

        return (
            self.columns,
            (utils.get_item_properties(
                s,
                self.columns,
            ) for s in data)
        )


class ShowDnatRule(command.ShowOne):
    _description = _("Show Dnat Rule details")

    def get_parser(self, prog_name):
        parser = super(ShowDnatRule, self).get_parser(prog_name)
        parser.add_argument(
            'dnat_rule_id',
            metavar='<dnat_rule_id>',
            help=_('Specifies the ID of the SNAT Rule'),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.nat
        obj = client.get_dnat_rule(parsed_args.dnat_rule_id)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class CreateDnatRule(command.ShowOne):
    _description = _("Create new DNAT Rule")

    def get_parser(self, prog_name):
        parser = super(CreateDnatRule, self).get_parser(prog_name)
        parser.add_argument(
            'nat_gateway_id',
            metavar="<nat_gateway_id>",
            help=_("Specifies the ID of the NAT gateway"))
        parser.add_argument(
            '--port-id',
            metavar='<port_id>',
            help=_('Specifies the port ID of an ECS or a BMS.'))
        parser.add_argument(
            '--private-ip',
            metavar='<private_ip>',
            help=_('Specifies the private IP address, for example, '
                   'the IP address of a Direct Connect connection.'))
        parser.add_argument(
            '--internal-service-port',
            metavar='<internal_service_port>',
            help=_('Specifies port used by ECSs or BMSs toprovide '
                   'services for external systems.'))
        parser.add_argument(
            'floating_ip_id',
            metavar="<floating_ip_id>",
            help=_('Specifies the EIP ID. Multiple EIPs are '
                   'separated using commas'))
        parser.add_argument(
            '--external-service-port',
            metavar='<external_service_port>',
            help=_('Specifies the port for providing external services.'))
        parser.add_argument(
            '--protocol',
            metavar='<protocol>',
            help=_('Specifies the protocol type.'))

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.nat

        args_list = [
            'nat_gateway_id',
            'port_id',
            'private_ip',
            'internal_service_port',
            'floating_ip_id',
            'external_service_port',
            'protocol'
        ]
        attrs = {}
        for arg in args_list:
            if getattr(parsed_args, arg):
                attrs[arg] = getattr(parsed_args, arg)

        obj = client.create_dnat_rule(**attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class DeleteDnatRule(command.Command):

    _description = _("Deletes Dnat Rule(s).")

    def get_parser(self, prog_name):
        parser = super(DeleteDnatRule, self).get_parser(prog_name)
        parser.add_argument(
            'dnat_rule_id',
            metavar='<dnat_rule_id>',
            help=_('Specifies the ID of the DNAT Rule'),
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.nat
        dnat_rule = client.get_dnat_rule(parsed_args.dnat_rule_id)
        return client.delete_dnat_rule(dnat_rule.id)
