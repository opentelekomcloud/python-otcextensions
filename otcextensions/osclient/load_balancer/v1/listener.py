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
'''LoadBalancer Listener v1 action implementations'''
import logging

from osc_lib.command import command
from osc_lib import exceptions
from osc_lib import utils

from otcextensions.i18n import _

from otcextensions.common import sdk_utils

LOG = logging.getLogger(__name__)


_formatters = {
    'load_balancer_ids': sdk_utils.ListOfIdsColumn,
}

SUPPORTED_PROTOCOLS = ['TCP', 'HTTP', 'HTTPS']


class ListListener(command.Lister):
    _description = _('List LoadBalancer Listeners')
    columns = (
        'ID', 'Name', 'description',
        'is_admin_state_up', 'protocol', 'protocol_port',
        'load_balancer_ids', 'default_pool_id')

    def get_parser(self, prog_name):
        parser = super(ListListener, self).get_parser(prog_name)
        parser.add_argument(
            '--protocol',
            metavar='<protocol>',
            help=_('Load balancer listener protocol to query\n'
                   'One of [`TCP`, `HTTP`, `HTTPS`]')
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
            if parsed_args.protocol.upper() in SUPPORTED_PROTOCOLS:
                args['protocol'] = parsed_args.protocol
            else:
                msg = (_('Protocol %s is not one of the supported %s')
                       % (parsed_args.protocol, SUPPORTED_PROTOCOLS))
                raise exceptions.CommandError(msg)

        if parsed_args.protocol_port:
            args['protocol_port'] = parsed_args.protocol_port

        client = self.app.client_manager.network

        data = client.listeners(**args)

        return (
            self.columns,
            (utils.get_item_properties(
                s, self.columns, formatters=_formatters
            ) for s in data))


class ShowListener(command.ShowOne):
    _description = _('Show LoadBalancer Listener details')
    columns = (
        'ID', 'Name', 'description',
        'is_admin_state_up', 'protocol', 'protocol_port',
        'load_balancer_ids', 'default_pool_id',
        'connection_limit')

    def get_parser(self, prog_name):
        parser = super(ShowListener, self).get_parser(prog_name)

        parser.add_argument(
            'listener',
            metavar='<listener>',
            help=_("Load balancer listener ID to show")
        )

        return parser

    def take_action(self, parsed_args):

        args = {}

        if parsed_args.listener is not None:
            args['name_or_id'] = parsed_args.listener

        client = self.app.client_manager.network

        obj = client.find_listener(
            name_or_id=parsed_args.listener,
            ignore_missing=False)

        data = utils.get_item_properties(
            obj, self.columns, formatters=_formatters)

        return (self.columns, data)


class CreateListener(command.ShowOne):
    _description = _('Create LoadBalancer Listener')
    columns = (
        'ID', 'Name', 'description',
        'is_admin_state_up', 'protocol', 'protocol_port',
        'load_balancer_ids', 'default_pool_id',
        'connection_limit')

    def get_parser(self, prog_name):
        parser = super(CreateListener, self).get_parser(prog_name)

        parser.add_argument(
            'protocol',
            metavar='<protocol>',
            help=_('The protocol for the resource. '
                   'One of [`TCP`, `HTTP`, `HTTPS`]')
        )
        parser.add_argument(
            'protocol_port',
            type=int,
            metavar='<protocol_port>',
            help=_('The protocol port number for the resource.')
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
            '--connection_limit',
            metavar='<connection_limit>',
            type=int,
            help=_("The maximum number of connections permitted for this "
                   "listener. Default value is -1 which represents infinite "
                   "connections.")
        )
        parser.add_argument(
            '--default_pool_id',
            metavar='<default_pool_id>',
            help=_("The ID of the pool used by the listener if no L7 policies "
                   "match.")
        )
        parser.add_argument(
            '--default_tls_container_ref',
            metavar='<default_tls_container_ref>',
            help=_("The URI of the key manager service secret containing a "
                   "PKCS12 format certificate/key bundle for TERMINATED_TLS "
                   "listeners. DEPRECATED: A secret container of type "
                   "\"certificate\" containing the certificate and key "
                   "for TERMINATED_TLS listeners.")
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_("A human-readable description for the resource.")
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_("A human-readable name for the resource.")
        )

        return parser

    def take_action(self, parsed_args):

        args = {}

        if parsed_args.protocol:
            if parsed_args.protocol.upper() in SUPPORTED_PROTOCOLS:
                args['protocol'] = parsed_args.protocol
            else:
                msg = (_('Protocol %s is not one of the supported %s')
                       % (parsed_args.protocol, SUPPORTED_PROTOCOLS))
                raise exceptions.CommandError(msg)
        if parsed_args.protocol_port:
            args['protocol_port'] = parsed_args.protocol_port
        if parsed_args.admin_state_up:
            args['admin_state_up'] = parsed_args.admin_state_up
        if parsed_args.connection_limit:
            args['connection_limit'] = parsed_args.connection_limit
        if parsed_args.default_pool_id:
            args['default_pool_id'] = parsed_args.default_pool_id
        if parsed_args.default_tls_container_ref:
            args['default_tls_container_ref'] = \
                parsed_args.default_tls_container_ref
        if parsed_args.description:
            args['description'] = parsed_args.description
        if parsed_args.name:
            args['name'] = parsed_args.name

        client = self.app.client_manager.network

        obj = client.create_listener(**args)

        data = utils.get_item_properties(
            obj, self.columns, formatters=_formatters)

        return (self.columns, data)


class UpdateListener(command.ShowOne):
    _description = _('Update LoadBalancer Listener')
    columns = (
        'ID', 'Name', 'description',
        'is_admin_state_up', 'protocol', 'protocol_port',
        'load_balancer_ids', 'default_pool_id',
        'connection_limit')

    def get_parser(self, prog_name):
        parser = super(UpdateListener, self).get_parser(prog_name)

        parser.add_argument(
            'listener',
            metavar='<listener>',
            help=_('The ID of the listener to query.')
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
            '--connection_limit',
            metavar='<connection_limit>',
            type=int,
            help=_("The maximum number of connections permitted for this "
                   "listener. Default value is -1 which represents infinite "
                   "connections.")
        )
        parser.add_argument(
            '--default_pool_id',
            metavar='<default_pool_id>',
            help=_("The ID of the pool used by the listener if no L7 policies "
                   "match.")
        )
        parser.add_argument(
            '--default_tls_container_ref',
            metavar='<default_tls_container_ref>',
            help=_("The URI of the key manager service secret containing a "
                   "PKCS12 format certificate/key bundle for TERMINATED_TLS "
                   "listeners. DEPRECATED: A secret container of type "
                   "\"certificate\" containing the certificate and key "
                   "for TERMINATED_TLS listeners.")
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_("A human-readable description for the resource.")
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_("A human-readable name for the resource.")
        )

        return parser

    def take_action(self, parsed_args):

        args = {}

        if parsed_args.admin_state_up:
            args['admin_state_up'] = parsed_args.admin_state_up
        if parsed_args.connection_limit:
            args['connection_limit'] = parsed_args.connection_limit
        if parsed_args.default_pool_id:
            args['default_pool_id'] = parsed_args.default_pool_id
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

        data = utils.get_item_properties(
            obj, self.columns, formatters=_formatters)

        return (self.columns, data)


class DeleteListener(command.Command):
    _description = _('Delete LoadBalancer Listener')

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
            client.delete_listener(
                listener=lsnr,
                ignore_missing=False)

        return
