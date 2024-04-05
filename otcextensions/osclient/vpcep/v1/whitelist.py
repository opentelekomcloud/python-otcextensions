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
"""VPC Endpoint Service v1 action implementations"""
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _get_columns(item):
    column_map = {}
    hidden = [
        'location',
    ]
    return sdk_utils.get_osc_show_columns_for_sdk_resource(
        item, column_map, hidden
    )


class ListWhitelist(command.Lister):

    _description = _('List whitelist records of a VPC endpoint service.')
    columns = ('Id', 'Permission', 'Created At')

    def get_parser(self, prog_name):
        parser = super(ListWhitelist, self).get_parser(prog_name)

        parser.add_argument(
            'service',
            metavar='<service>',
            help=_('ID or name of the VPC Endpoint Service.'),
        )
        parser.add_argument(
            '--sort-key',
            metavar='{created_at}',
            type=lambda s: s.lower(),
            choices=['created_at'],
            help=_('Sorting field of the whitelist records.'),
        )
        parser.add_argument(
            '--sort-dir',
            metavar='{asc, desc}',
            type=lambda s: s.lower(),
            choices=['asc', 'desc'],
            help=_('Sorting order of the whitelist record list.'),
        )
        parser.add_argument(
            '--limit',
            metavar='<limit>',
            type=int,
            help=_('Limit number of whitelist records to fetch.'),
        )
        parser.add_argument(
            '--offset',
            metavar='<offset>',
            type=int,
            help=_('Whitelist records after this Offset will be queried.'),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.vpcep
        args_list = [
            'limit',
            'offset',
            'sort_key',
            'sort_dir',
        ]
        attrs = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val
        endpoint_service = client.find_service(parsed_args.service)
        data = client.service_whitelist(endpoint_service, **attrs)

        return (
            self.columns,
            (utils.get_item_properties(s, self.columns) for s in data),
        )


class ManageWhitelist(command.Lister):
    _description = _('Manage whitelist records of a VPC endpoint service.')

    columns = ('Permission',)

    def get_parser(self, prog_name):
        parser = super(ManageWhitelist, self).get_parser(prog_name)

        parser.add_argument(
            'service',
            metavar='<service>',
            help=_('ID or name of the VPC Endpoint Service.'),
        )
        parser.add_argument(
            'domain',
            metavar='<domain>',
            nargs='+',
            help=_(
                'Domain ID(s) to add to whitelist record of the '
                'Vpc endpoint service.'
            ),
        )
        manage_request_group = parser.add_mutually_exclusive_group(
            required=True
        )
        manage_request_group.add_argument(
            '--add',
            action='store_true',
            help=(
                'Add a domian to the whitelist record of the '
                'Vpc endpoint service.'
            ),
        )
        manage_request_group.add_argument(
            '--remove',
            action='store_true',
            help=(
                'Remove a domian from the whitelist record of the '
                'Vpc endpoint service.'
            ),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.vpcep
        set_args = ('add', 'remove')
        request_status = [
            request for request in set_args if getattr(parsed_args, request)
        ]

        endpoint_service = client.find_service(parsed_args.service)
        data = client.manage_service_whitelist(
            endpoint_service,
            domains=parsed_args.domain,
            action=request_status[0],
        )
        return (
            self.columns,
            (utils.get_item_properties(s, self.columns) for s in data),
        )
