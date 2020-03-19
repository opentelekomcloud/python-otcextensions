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
"""SNAT v2 action implementations"""
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


class ListSnatRules(command.Lister):

    _description = _("List SNAT Rules.")
    columns = (
        'Id',
        'Nat Gateway Id',
        'Network Id',
        'Cidr',
        'Floating Ip Address',
        'Status'
    )

    def get_parser(self, prog_name):
        parser = super(ListSnatRules, self).get_parser(prog_name)

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
            metavar='<project_id>',
            help=_('Specifies the project ID.'))
        parser.add_argument(
            '--nat-gateway-id',
            metavar='<nat_gateway_id>',
            help=_('Specifies the NAT gateway ID.'))
        parser.add_argument(
            '--network-id',
            metavar='<network_id>',
            help=_('Specifies the network ID used by theSNAT rule.'))
        parser.add_argument(
            '--cidr',
            metavar='<cidr>',
            help=_('Specifies a subset of the VPC subnetCIDR block or '
                   'a CIDR block of DirectConnect connection.'))
        parser.add_argument(
            '--source-type',
            metavar='<source_type>',
            help=_('Specifies Source Type.'))
        parser.add_argument(
            '--floating-ip-id',
            metavar='<floating_ip_id>',
            help=_('Specifies the EIP ID.'))
        parser.add_argument(
            '--floating-ip-address',
            metavar='<floating_ip_address>',
            help=_('Specifies the EIP.'))
        parser.add_argument(
            '--status',
            metavar='<status>',
            help=_('Specifies the status of the SNATrule.'))
        parser.add_argument(
            '--admin-state-up',
            metavar='<admin_state_up>',
            help=_('Specifies whether the SNAT rule isenabled or disabled.'))
        parser.add_argument(
            '--created-at',
            metavar='<created_at>',
            help=_('Specifies when the SNAT rule iscreated (UTC time). '
                   'Its valuerounds to 6 decimal places forseconds. '
                   'The format is yyyy-mm-ddhh:mm:ss.'))

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.nat
        args_list = [
            'id',
            'limit',
            'network_id',
            'project_id',
            'nat_gateway_id',
            'network_id',
            'cidr',
            'source_type',
            'floating_ip_id',
            'floating_ip_address',
            'status',
            'admin_state_up',
            'created_at']
        attrs = {}
        for arg in args_list:
            if getattr(parsed_args, arg):
                attrs[arg] = getattr(parsed_args, arg)

        data = client.snat_rules(**attrs)

        return (
            self.columns,
            (utils.get_item_properties(
                s,
                self.columns,
            ) for s in data)
        )


class ShowSnatRule(command.ShowOne):
    _description = _("Show Snat Rule details")

    def get_parser(self, prog_name):
        parser = super(ShowSnatRule, self).get_parser(prog_name)
        parser.add_argument(
            'snat',
            metavar='<snat_id>',
            help=_('Specifies the ID of the SNAT Rule'),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.nat
        obj = client.get_snat_rule(parsed_args.snat)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class CreateSnatRule(command.ShowOne):
    _description = _("Create new SNAT Rule")

    def get_parser(self, prog_name):
        parser = super(CreateSnatRule, self).get_parser(prog_name)
        parser.add_argument(
            '--nat-gateway-id',
            required=True,
            metavar='<nat_gateway_id>',
            help=_('Specifies the ID of the NAT gateway'))
        parser.add_argument(
            '--floating-ip-id',
            metavar='<floating_ip_id>',
            required=True,
            help=_('Specifies the EIP ID. Multiple EIPs '
                   'are separated using commas'))
        parser.add_argument(
            '--network-id',
            metavar='<network_id>',
            help=_('Specifies the network ID used by the SNAT rule. '
                   'This parameter and cidr arealternative.'))
        parser.add_argument(
            '--cidr',
            metavar='<cidr>',
            help=_('Specifies CIDR, which can be in the formatof a '
                   'network segment or a host IP address'))
        parser.add_argument(
            '--source-type',
            metavar='<source_type>',
            help=_(
                'Specifies the source type.\n0: Either network_id '
                'or cidr can be specified in a VPC.\n1: Only cidr '
                'can be specified over a Direct Connect connection.'
                '\nIf no value is entered, the default value 0 (VPC) '
                'is used.'))

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.nat

        args_list = [
            'nat_gateway_id',
            'floating_ip_id',
            'network_id',
            'cidr',
            'source_type'
        ]
        attrs = {}
        for arg in args_list:
            if getattr(parsed_args, arg):
                attrs[arg] = getattr(parsed_args, arg)

        obj = client.create_snat_rule(**attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class DeleteSnatRule(command.Command):

    _description = _("Deletes Snat Rule(s).")

    def get_parser(self, prog_name):
        parser = super(DeleteSnatRule, self).get_parser(prog_name)
        parser.add_argument(
            'snat',
            metavar='<snat_id>',
            help=_('Specifies the ID of the SNAT Rule'),
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.nat
        snat_rule = client.get_snat_rule(parsed_args.snat)
        client.delete_snat_rule(snat_rule.id)
