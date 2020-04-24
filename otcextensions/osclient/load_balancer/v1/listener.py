#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#
'''LoadBalancer Listener v1 action implementations'''
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


SUPPORTED_PROTOCOLS = ['TCP', 'HTTP', 'HTTPS', 'UDP']

_formatters = {
    'load_balancer_ids': sdk_utils.ListOfIdsColumnBR,
}


def _get_columns(item):
    column_map = {
        'is_admin_state_up': 'admin_state_up',
        'load_balancer_ids': 'loadbalancers',
        # 'listeners': 'listener_ids',
        # 'pools': 'pool_ids',
    }
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


class ListListener(command.Lister):
    _description = _('List listeners')
    column_headers = (
        'id', 'default_pool_id', 'name', 'project_id', 'protocol',
        'protocol_port', 'admin_state_up')
    columns = (
        'id', 'default_pool_id', 'name', 'project_id', 'protocol',
        'protocol_port', 'is_admin_state_up')

    def get_parser(self, prog_name):
        parser = super(ListListener, self).get_parser(prog_name)
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_('List listeners by listener name.')
        )
        parser.add_argument(
            '--load_balancer',
            metavar='<load_balancer>',
            help=_('Filter by load balancer (name or ID).')
        )
        parser.add_argument(
            '--protocol',
            metavar='{' + ','.join(SUPPORTED_PROTOCOLS) + '}',
            type=lambda s: s.upper(),
            choices=SUPPORTED_PROTOCOLS,
            help=_('Load balancer listener protocol to query\n'
                   'One of [`TCP`, `HTTP`, `HTTPS`, `UDP`]')
        )
        parser.add_argument(
            '--protocol_port',
            type=int,
            metavar='<protocol_port>',
            help=_('Load balancer listener protocol port to query')
        )
        return parser

    def take_action(self, parsed_args):

        args = {}

        if parsed_args.protocol:
            args['protocol'] = parsed_args.protocol
        if parsed_args.protocol_port:
            args['protocol_port'] = parsed_args.protocol_port
        if parsed_args.name:
            args['name'] = parsed_args.name
        # NOTE: loadbalancer_id is not supported in neutron
        if parsed_args.load_balancer:
            args['load_balancer_id'] = parsed_args.load_balancer

        client = self.app.client_manager.network

        data = client.listeners(**args)

        return (
            self.column_headers,
            (utils.get_item_properties(
                s, self.columns, formatters=_formatters
            ) for s in data))


class ShowListener(command.ShowOne):
    _description = _('Show the details of a single listener')

    def get_parser(self, prog_name):
        parser = super(ShowListener, self).get_parser(prog_name)

        parser.add_argument(
            'listener',
            metavar='<listener>',
            help=_('Name or UUID of the listener.')
        )

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.network

        obj = client.find_listener(
            name_or_id=parsed_args.listener,
            ignore_missing=False)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)

        return (display_columns, data)


class CreateListener(command.ShowOne):
    _description = _('Create LoadBalancer Listener')

    def get_parser(self, prog_name):
        parser = super(CreateListener, self).get_parser(prog_name)

        parser.add_argument(
            'load_balancer',
            metavar='<load_balancer>',
            help=_('Load balancer for the listener (name or ID).')
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_('Set the listener name.')
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_('Set the description of this listener.')
        )

        parser.add_argument(
            '--protocol',
            metavar='{' + ','.join(SUPPORTED_PROTOCOLS) + '}',
            type=lambda s: s.upper(),
            choices=SUPPORTED_PROTOCOLS,
            required=True,
            help=_('The protocol for the listener. '
                   'One of [`TCP`, `HTTP`, `HTTPS`, `UDP`]')
        )
        parser.add_argument(
            '--protocol_port',
            type=int,
            metavar='<port>',
            required=True,
            help=_('Set the protocol port number for the listener.')
        )
        parser.add_argument(
            '--connection_limit',
            metavar='<limit>',
            type=int,
            help=_('The maximum number of connections permitted for this '
                   'listener. Default value is -1 which represents infinite '
                   'connections.')
        )
        parser.add_argument(
            '--default_pool',
            metavar='<pool>',
            help=_('The ID of the pool used by the listener if no L7 policies '
                   'match.')
        )
        parser.add_argument(
            '--default_tls_container_ref',
            metavar='<default_tls_container_ref>',
            help=_('The URI of the key manager service secret containing a '
                   'PKCS12 format certificate/key bundle for TERMINATED_TLS '
                   'listeners. DEPRECATED: A secret container of type '
                   '\"certificate\" containing the certificate and key '
                   'for TERMINATED_TLS listeners.')
        )
        admin_group = parser.add_mutually_exclusive_group()
        admin_group.add_argument(
            '--enable',
            action='store_true',
            default=True,
            help=_('Enable listener (default).')
        )
        admin_group.add_argument(
            '--disable',
            action='store_true',
            default=None,
            help=_('Disable listener.')
        )
        return parser

    def take_action(self, parsed_args):

        args = {}

        if parsed_args.load_balancer:
            args['load_balancer_id'] = parsed_args.load_balancer
        if parsed_args.protocol:
            args['protocol'] = parsed_args.protocol
        if parsed_args.protocol_port:
            args['protocol_port'] = parsed_args.protocol_port
        if parsed_args.disable:
            args['is_admin_state_up'] = False
        if parsed_args.connection_limit:
            args['connection_limit'] = parsed_args.connection_limit
        if parsed_args.default_pool:
            args['default_pool_id'] = parsed_args.default_pool
        if parsed_args.default_tls_container_ref:
            args['default_tls_container_ref'] = \
                parsed_args.default_tls_container_ref
        if parsed_args.description:
            args['description'] = parsed_args.description
        if parsed_args.name:
            args['name'] = parsed_args.name

        client = self.app.client_manager.network

        obj = client.create_listener(**args)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)

        return (display_columns, data)


class SetListener(command.ShowOne):
    _description = _('Update a listener')

    def get_parser(self, prog_name):
        parser = super(SetListener, self).get_parser(prog_name)

        parser.add_argument(
            'listener',
            metavar='<listener>',
            help=_('Listener to modify (ID).')
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_('Set the listener name.')
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_('Set the description of this listener.')
        )
        parser.add_argument(
            '--connection_limit',
            metavar='<connection_limit>',
            type=int,
            help=_('The maximum number of connections permitted for this '
                   'listener. Default value is -1 which represents infinite '
                   'connections.')
        )
        parser.add_argument(
            '--default_pool',
            metavar='<pool>',
            help=_('The ID of the pool used by the listener if no L7 policies '
                   'match.')
        )
        parser.add_argument(
            '--default_tls_container_ref',
            metavar='<default_tls_container_ref>',
            help=_('The URI of the key manager service secret containing a '
                   'PKCS12 format certificate/key bundle for TERMINATED_TLS '
                   'listeners. DEPRECATED: A secret container of type '
                   '\"certificate\" containing the certificate and key '
                   'for TERMINATED_TLS listeners.')
        )
        admin_group = parser.add_mutually_exclusive_group()
        admin_group.add_argument(
            '--enable',
            action='store_true',
            default=True,
            help=_('Enable load balancer (default).')
        )
        admin_group.add_argument(
            '--disable',
            action='store_true',
            default=None,
            help=_('Disable load balancer.')
        )

        return parser

    def take_action(self, parsed_args):

        args = {}

        if parsed_args.disable:
            args['is_admin_state_up'] = False
        if parsed_args.connection_limit:
            args['connection_limit'] = parsed_args.connection_limit
        if parsed_args.default_pool:
            args['default_pool_id'] = parsed_args.default_pool
        if parsed_args.default_tls_container_ref:
            args['default_tls_container_ref'] = \
                parsed_args.default_tls_container_ref
        if parsed_args.description:
            args['description'] = parsed_args.description
        if parsed_args.name:
            args['name'] = parsed_args.name

        client = self.app.client_manager.network

        obj = client.update_listener(
            listener=parsed_args.listener,
            **args)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)

        return (display_columns, data)


class DeleteListener(command.Command):
    _description = _('Delete a listener')

    def get_parser(self, prog_name):
        parser = super(DeleteListener, self).get_parser(prog_name)

        parser.add_argument(
            'listener',
            metavar='<listener>',
            nargs='+',
            help=_('The ID of the listener to delete.')
        )

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.network

        for lsnr in parsed_args.listener:
            obj = client.find_listener(name_or_id=lsnr, ignore_missing=False)
            client.delete_listener(
                listener=obj.id,
                ignore_missing=False)

        return
