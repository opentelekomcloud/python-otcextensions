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

from osc_lib import exceptions
from osc_lib import utils
from osc_lib.cli import format_columns
from osc_lib.cli import parseractions
from osc_lib.command import command

from otcextensions.common import cli_utils
from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


_formatters = {
    'active_status': format_columns.ListColumn,
    'tags': cli_utils.YamlFormat,
    'whitelist': format_columns.ListColumn,
    'route_tables': format_columns.ListColumn,
}


def _get_columns(item):
    column_map = {}
    hidden = [
        'location',
    ]
    return sdk_utils.get_osc_show_columns_for_sdk_resource(
        item, column_map, hidden
    )


class ListEndpoints(command.Lister):

    _description = _('List VPC Endpoints.')
    columns = ('Id', 'Endpoint Service Name', 'Status', 'Enable status')

    def get_parser(self, prog_name):
        parser = super(ListEndpoints, self).get_parser(prog_name)

        parser.add_argument(
            '--id',
            metavar='<id>',
            help=_('ID of the VPC endpoint.'),
        )
        parser.add_argument(
            '--service-name',
            metavar='<service_name>',
            dest='endpoint_service_name',
            help=_('Name of the VPC endpoint service.'),
        )
        parser.add_argument(
            '--sort-key',
            metavar='{created_at, updated_at}',
            type=lambda s: s.lower(),
            choices=['created_at', 'updated_at'],
            help=_('Sorting field of the VPC endpoint list.'),
        )
        parser.add_argument(
            '--sort-dir',
            metavar='{asc, desc}',
            type=lambda s: s.lower(),
            choices=['asc', 'desc'],
            help=_('Sorting order of the VPC endpoint list.'),
        )
        parser.add_argument(
            '--limit',
            metavar='<limit>',
            type=int,
            help=_('Limit number of VPC endpoints.'),
        )
        parser.add_argument(
            '--offset',
            metavar='<offset>',
            type=int,
            help=_('Endpoints after this offset will be queried.'),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.vpcep
        args_list = [
            'id',
            'endpoint_service_name',
            'limit',
            'offset',
            'sort_key',
            'sort_dir',
        ]
        params = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                params[arg] = val

        data = client.endpoints(**params)

        return (
            self.columns,
            (utils.get_item_properties(s, self.columns) for s in data),
        )


class CreateEndpoint(command.ShowOne):
    _description = _(
        'Create a VPC endpoint for accessing a VPC endpoint service.'
    )

    def get_parser(self, prog_name):
        parser = super(CreateEndpoint, self).get_parser(prog_name)
        parser.add_argument(
            '--service-id',
            metavar='<service_id>',
            dest='endpoint_service_id',
            help=_('ID of the Vpc endpoint service.'),
        )
        parser.add_argument(
            '--router-id',
            metavar='<router_id>',
            dest='vpc_id',
            required=True,
            help=_(
                'ID of the vpc/router where the VPC endpoint is to be created.'
            ),
        )
        parser.add_argument(
            '--network-id',
            metavar='<network_id>',
            dest='subnet_id',
            required=True,
            help=_('ID of the network created in the vpc/router.'),
        )
        parser.add_argument(
            '--port-ip',
            metavar='<port_ip>',
            help=_(
                'IP address for accessing the associated VPC endpoint service.'
            ),
        )
        parser.add_argument(
            '--route-tables',
            metavar='<route_tables>',
            dest='routetables',
            nargs='+',
            help=_('Lists the IDs of route tables.'),
        )
        parser.add_argument(
            '--whitelist',
            metavar='<whitelist>',
            nargs='+',
            help=_('Whitelist for controlling access to the VPC endpoint.'),
        )
        parser.add_argument(
            '--specification-name',
            metavar='<specification_name>',
            help=_('Name of the VPC endpoint specifications.'),
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_('Description of the VPC endpoint.'),
        )
        parser.add_argument(
            '--tags',
            metavar='key=<tag-key>,value=<tag-value>',
            action=parseractions.MultiKeyValueAction,
            dest='tags',
            required_keys=['key', 'value'],
            help=_(
                'Example: \n'
                '--tags key=test-key,value=test-value\n'
                'Repeat option to provide multiple tags.'
            ),
        )
        parser.add_argument(
            '--enable-dns',
            action='store_true',
            help=('Whether to create a private domain name. default (false)'),
        )
        parser.add_argument(
            '--enable-whitelist',
            action='store_true',
            help=('Whether access control is enabled.'),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.vpcep

        args_list = [
            'endpoint_service_id',
            'subnet_id',
            'vpc_id',
            'port_ip',
            'tags',
            'whitelist',
            'routetables',
            'enable_dns',
            'enable_whitelist',
            'specification_name',
            'description',
        ]
        attrs = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        obj = client.create_endpoint(**attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class ShowEndpoint(command.ShowOne):
    _description = _('Show VPC endpoint details.')

    def get_parser(self, prog_name):
        parser = super(ShowEndpoint, self).get_parser(prog_name)
        parser.add_argument(
            'endpoint',
            metavar='<endpoint>',
            help=_('ID of the VPC endpoint.'),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.vpcep
        obj = client.get_endpoint(parsed_args.endpoint)
        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)

        return (display_columns, data)


class DeleteEndpoint(command.Command):

    _description = _('Delete VPC endpoint(s).')

    def get_parser(self, prog_name):
        parser = super(DeleteEndpoint, self).get_parser(prog_name)
        parser.add_argument(
            'endpoint',
            metavar='<endpoint>',
            nargs='+',
            help=_('ID of vpc endpoint(s) to delete.'),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.vpcep
        result = 0
        for endpoint in parsed_args.endpoint:
            try:
                client.delete_endpoint(endpoint)
            except Exception as e:
                result += 1
                LOG.error(
                    _(
                        'Failed to delete VPC endpoint with '
                        'ID "%(endpoint)s": %(e)s'
                    ),
                    {'endpoint': endpoint, 'e': e},
                )
        if result > 0:
            total = len(parsed_args.endpoint)
            msg = _(
                '%(result)s of %(total)s VPC endpoint(s) failed to delete.'
            ) % {'result': result, 'total': total}
            raise exceptions.CommandError(msg)
