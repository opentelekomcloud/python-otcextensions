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
from osc_lib.cli import parseractions
from osc_lib.command import command

from otcextensions.common import cli_utils
from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)

SERVER_TYPE_CHOICES = ['vm', 'vip', 'lb']
SERVICE_TYPE_CHOICES = ['gateway', 'interface']


_formatters = {
    'ports': cli_utils.YamlFormat,
    'tags': cli_utils.YamlFormat,
}


def _get_columns(item):
    column_map = {}
    hidden = [
        'location',
    ]
    return sdk_utils.get_osc_show_columns_for_sdk_resource(
        item, column_map, hidden
    )


def translate_response(func):
    def new(self, *args, **kwargs):
        obj = func(self, *args, **kwargs)
        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)
        return (display_columns, data)

    new.__name__ = func.__name__
    new.__doc__ = func.__doc__
    return new


class ListServices(command.Lister):

    _description = _('List VPC Endpoint Services.')
    columns = (
        'Id',
        'Service Name',
        'Service Type',
        'Server Type',
        'Connection Count',
        'Status',
    )

    def get_parser(self, prog_name):
        parser = super(ListServices, self).get_parser(prog_name)

        parser.add_argument(
            '--id',
            metavar='<id>',
            help=_('ID of the VPC Endpoint Service.'),
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_('Name of the VPC Endpoint Service.'),
        )
        parser.add_argument(
            '--status',
            metavar='<status>',
            help=_('Status of the VPC endpoint service.'),
        )
        parser.add_argument(
            '--sort-key',
            metavar='{created_at, updated_at}',
            type=lambda s: s.lower(),
            choices=['created_at', 'updated_at'],
            help=_('Sorting field of the VPC endpoint service list.'),
        )
        parser.add_argument(
            '--sort-dir',
            metavar='{asc, desc}',
            type=lambda s: s.lower(),
            choices=['asc', 'desc'],
            help=_('Sorting order of the VPC endpoint service list.'),
        )
        parser.add_argument(
            '--limit',
            metavar='<limit>',
            type=int,
            help=_('Limit number of VPC endpoint services displayed.'),
        )
        parser.add_argument(
            '--offset',
            metavar='<offset>',
            type=int,
            help=_('Service records after this Offset will be queried.'),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.vpcep
        args_list = [
            'id',
            'name',
            'limit',
            'offset',
            'sort_key',
            'sort_dir',
            'status',
        ]
        attrs = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        data = client.services(**attrs)

        return (
            self.columns,
            (utils.get_item_properties(s, self.columns) for s in data),
        )


class ShowService(command.ShowOne):
    _description = _('Show VPC Endpoint Service Details.')

    def get_parser(self, prog_name):
        parser = super(ShowService, self).get_parser(prog_name)
        parser.add_argument(
            'service',
            metavar='<service>',
            help=_('Name or ID of the VPC Endpoint Service.'),
        )
        return parser

    @translate_response
    def take_action(self, parsed_args):
        client = self.app.client_manager.vpcep
        return client.find_service(parsed_args.service)


class CreateService(command.ShowOne):
    _description = _('Create new VPC Endpoint Service.')

    def get_parser(self, prog_name):
        parser = super(CreateService, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help=_('Specifies name of the Endpoint Service.'),
        )
        parser.add_argument(
            '--port-id',
            metavar='<port_id>',
            required=True,
            help=_(
                'Specify the ID for identifying the backend '
                'resource of the VPC endpoint service.'
            ),
        )
        parser.add_argument(
            '--pool-id',
            metavar='<pool_id>',
            help=_(
                'Specify the ID of the cluster associated with '
                'the target VPCEP resource.'
            ),
        )
        parser.add_argument(
            '--router-id',
            metavar='<router_id>',
            dest='vpc_id',
            required=True,
            help=_(
                'ID of the router (VPC) to which the backend resource '
                'of the VPC endpoint service belongs.'
            ),
        )
        parser.add_argument(
            '--server-type',
            metavar='{LB, VM, VIP, BMS}',
            type=lambda s: s.upper(),
            choices=['LB', 'VM', 'VIP', 'BMS'],
            required=True,
            help=_('Specifies the resource type.'),
        )
        parser.add_argument(
            '--service-type',
            metavar='{gateway, interface}',
            type=lambda s: s.lower(),
            choices=['gateway', 'interface'],
            help=_('Specifies the type of the VPC endpoint service.'),
        )
        parser.add_argument(
            '--ports',
            metavar='client_port=<client-port>,'
            'server_port=<server-port>,'
            'protocol=<protocol>',
            action=parseractions.MultiKeyValueAction,
            required=True,
            required_keys=['client_port', 'server_port', 'protocol'],
            help=_(
                'Example: \n'
                '--ports client_port=8081,server_port=22,protocol=TCP\n'
                'Repeat option to provide multiple ports.'
            ),
        )
        parser.add_argument(
            '--tcp-proxy',
            metavar='{close, toa_open, proxy_open, open, proxy_vni}',
            type=lambda s: s.lower(),
            choices=['close', 'toa_open', 'proxy_open', 'open', 'proxy_vni'],
            help=_(
                'Whether the client IP address and port number or marker_id '
                'information is transmitted to the server.'
            ),
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
            '--disable-approval',
            action='store_true',
            help=_('Specifies whether connection approval is required.'),
        )
        return parser

    @translate_response
    def take_action(self, parsed_args):
        client = self.app.client_manager.vpcep

        attrs = {'service_name': parsed_args.name}
        args_list = [
            'port_id',
            'pool_id',
            'vpc_id',
            'service_type',
            'server_type',
            'tags',
            'tcp_proxy',
        ]
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val
        ports = []
        for port in parsed_args.ports:
            ports.append(
                {
                    'client_port': int(port['client_port']),
                    'server_port': int(port['server_port']),
                    'protocol': port['protocol'],
                }
            )
        attrs['ports'] = ports

        if parsed_args.disable_approval:
            attrs['approval_enabled'] = False
        return client.create_service(**attrs)


class UpdateService(command.ShowOne):
    _description = _('Update a Endpoint Service.')

    def get_parser(self, prog_name):
        parser = super(UpdateService, self).get_parser(prog_name)
        parser.add_argument(
            'service',
            metavar='<service>',
            help=_('Name or ID of the Vpc endpoint service.'),
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            dest='service_name',
            help=_('Name of the VPC endpoint service.'),
        )
        parser.add_argument(
            '--ports',
            metavar='client_port=<client-port>,'
            'server_port=<server-port>,'
            'protocol=<protocol>',
            action=parseractions.MultiKeyValueAction,
            required_keys=['client_port', 'server_port', 'protocol'],
            help=_(
                'Example: \n'
                '--ports client_port=8081,server_port=22,protocol=TCP\n'
                'Repeat option to provide multiple ports.'
            ),
        )
        parser.add_argument(
            '--port-id',
            metavar='<port_id>',
            help=_(
                'Specify the ID for identifying the backend resource of '
                'the VPC endpoint service.'
            ),
        )
        parser.add_argument(
            '--tcp-proxy',
            metavar='{close, toa_open, proxy_open, open, proxy_vni}',
            type=lambda s: s.lower(),
            choices=['close', 'toa_open', 'proxy_open', 'open', 'proxy_vni'],
            help=_(
                'Whether the client IP address and port number or marker_id '
                'information is transmitted to the server.'
            ),
        )
        approval_group = parser.add_mutually_exclusive_group()
        approval_group.add_argument(
            '--enable-approval',
            action='store_true',
            help=_('Connection approval is required.'),
        )
        approval_group.add_argument(
            '--disable-approval',
            action='store_true',
            help=_('Connection approval is not required.'),
        )
        return parser

    @translate_response
    def take_action(self, parsed_args):
        client = self.app.client_manager.vpcep
        args_list = [
            'service_name',
            'port_id',
            'tcp_proxy',
        ]
        attrs = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val
        ports = []
        for port in parsed_args.ports:
            ports.append(
                {
                    'client_port': int(port['client_port']),
                    'server_port': int(port['server_port']),
                    'protocol': port['protocol'],
                }
            )
        attrs['ports'] = ports
        if parsed_args.enable_approval:
            attrs['approval_enabled'] = True
        if parsed_args.disable_approval:
            attrs['approval_enabled'] = False
        service = client.find_service(parsed_args.service)
        return client.update_service(service, **attrs)


class DeleteService(command.Command):

    _description = _('Deletes VPC Endpoint Service.')

    def get_parser(self, prog_name):
        parser = super(DeleteService, self).get_parser(prog_name)
        parser.add_argument(
            'service',
            metavar='<service>',
            nargs='+',
            help=_('Vpc Endpoint Services(s) to delete (Name or ID)'),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.vpcep
        result = 0
        for service in parsed_args.service:
            try:
                obj = client.find_service(service)
                client.delete_service(obj.id)
            except Exception as e:
                result += 1
                LOG.error(
                    _(
                        'Failed to delete Vpc Endpoint Service with '
                        'name or ID "%(service)s": %(e)s'
                    ),
                    {'service': service, 'e': e},
                )
        if result > 0:
            total = len(parsed_args.service)
            msg = _(
                '%(result)s of %(total)s Vpc Endpoint Services(s) failed '
                'to delete.'
            ) % {'result': result, 'total': total}
            raise exceptions.CommandError(msg)
