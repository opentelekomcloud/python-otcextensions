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
from osc_lib import exceptions
from osc_lib.cli import parseractions
from osc_lib.command import command
from distutils.util import strtobool

from otcextensions.i18n import _
from otcextensions.common import sdk_utils

LOG = logging.getLogger(__name__)

SERVER_TYPE_CHOICES = ['vm', 'vip', 'lb']
SERVICE_TYPE_CHOICES = ['gateway', 'interface']


def _get_columns(item):
    column_map = {
    }
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


class ListEndpointServices(command.Lister):

    _description = _("List VPC Endpoint Services.")
    columns = ('Id', 'Service Name', 'Service Type', 'Server Type', 'Connection Count', 'Status')

    def get_parser(self, prog_name):
        parser = super(ListEndpointServices, self).get_parser(prog_name)

        parser.add_argument(
            '--id',
            metavar='<id>',
            help=_("Specifies the ID of the VPC Endpoint Service."),
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_("Specifies the name of the VPC Endpoint Service."),
        )
        parser.add_argument(
            '--status',
            metavar='<status>',
            help=_("Specifies the status of the VPC endpoint service."),
        )
        parser.add_argument(
            '--sort-key',
            metavar='<sort_key>',
            help=_("Specifies the sorting field of the VPC endpoint "
                   "service list."),
        )
        parser.add_argument(
            '--sort-dir',
            metavar='<sort_dir>',
            help=_("Specifies the sorting method of the VPC endpoint "
                   "service list."),
        )
        parser.add_argument(
            '--limit',
            metavar='<limit>',
            type=int,
            help=_("Specifies the maximum number of VPC endpoint services "
                   "displayed on each page."),
        )
        parser.add_argument(
            '--offset',
            metavar='<offset>',
            type=int,
            help=_("Specifies the offset.."),
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
            'status'
        ]
        attrs = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        data = client.endpoint_services(**attrs)

        return (self.columns, (utils.get_item_properties(s, self.columns)
                               for s in data))


class ShowEndpointService(command.ShowOne):
    _description = _("Show VPC Endpoint Service Details.")

    def get_parser(self, prog_name):
        parser = super(ShowEndpointService, self).get_parser(prog_name)
        parser.add_argument(
            'endpointservice',
            metavar='<endpointservice>',
            help=_("Specifies the Name or ID of the VPC Endpoint Service."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.vpcep
        obj = client.get_endpoint_service(parsed_args.endpointservice)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class CreateEndpointService(command.ShowOne):
    _description = _("Create new VPC Endpoint Service.")

    def get_parser(self, prog_name):
        parser = super(CreateEndpointService, self).get_parser(prog_name)
        parser.add_argument(
            '--service-name',
            metavar='<service_name>',
            help=_("Specifies name of the Endpoint Service."),
        )
        parser.add_argument(
            '--port-id',
            metavar='<port_id>',
            required=True,
            help=_("Specifies the ID for identifying the backend "
                   "resource of the VPC endpoint service."),
        )
        parser.add_argument(
            '--pool-id',
            metavar='<pool_id>',
            help=_("Specifies the ID of the cluster associated with "
                   "the target VPCEP resource."),
        )
        parser.add_argument(
            '--vip-port-id',
            metavar='<vip_port_id>',
            help=_("Specifies the ID of the virtual NIC to which "
                   "the virtual IP address is bound."),
        )
        parser.add_argument(
            '--router-id',
            metavar='<router_id>',
            required=True,
            help=_("Specifies the ID of the VPC to which the backend "
                   "resource of the VPC endpoint service belongs."),
        )
        parser.add_argument(
            '--approval-enabled',
            metavar='<approval_enabled>',
            type=lambda x: bool(strtobool(str(x))),
            const=True,
            default=True,
            nargs='?',
            help=_("Specifies whether connection approval is required."),
        )
        parser.add_argument(
            '--server-type',
            metavar='{' + ','.join(SERVER_TYPE_CHOICES) + '}',
            type=lambda s: s.lower(),
            choices=SERVER_TYPE_CHOICES,
            required=True,
            help=_("Specifies the resource type."),
        )
        parser.add_argument(
            '--service-type',
            metavar='{' + ','.join(SERVICE_TYPE_CHOICES) + '}',
            type=lambda s: s.lower(),
            choices=SERVICE_TYPE_CHOICES,
            help=_("Specifies the type of the VPC endpoint service."),
        )
        parser.add_argument(
            '--ports',
            metavar='client_port=<client-port>,'
                    'server_port=<server-port>,'
                    'protocol=<protocol>',
            action=parseractions.MultiKeyValueAction,
            dest='ports',
            required=True,
            required_keys=['client_port', 'server_port', 'protocol'],
            help=_("Example: \n"
                   "--ports client_port=8081,server_port=22,protocol=TCP\n"
                   "Repeat option to provide multiple ports."),
        )
        parser.add_argument(
            '--tags',
            metavar='key=<tag-key>,value=<tag-value>',
            action=parseractions.MultiKeyValueAction,
            dest='tags',
            required_keys=['key', 'value'],
            help=_('Example: \n'
                   '--tags key=test-key,value=test-value\n'
                   'Repeat option to provide multiple tags.'),
        )
        parser.add_argument(
            '--tcp-proxy',
            metavar='<tcp_proxy>',
            help=_("Specifies whether the client IP address and port number "
                   "or marker_id information is transmitted to the server."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.vpcep

        args_list = [
            'service_name',
            'port_id',
            'pool_id',
            'vip_port_id',
            'router_id',
            'service_type',
            'server_type',
            'tags',
            'tcp_proxy']
        attrs = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val
        ports = []
        for port in parsed_args.ports:
            ports.append({'client_port': int(port['client_port']),
                          'server_port': int(port['server_port']),
                          'protocol': port['protocol']})
        attrs['ports'] = ports

        if not parsed_args.approval_enabled:
            attrs['approval_enabled'] = False

        obj = client.create_endpoint_service(**attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class UpdateEndpointService(command.ShowOne):
    _description = _("Update a NAT Gateway.")

    def get_parser(self, prog_name):
        parser = super(UpdateEndpointService, self).get_parser(prog_name)
        parser.add_argument(
            'endpointservice',
            metavar='<endpointservice>',
            help=_("Specifies the Name or ID of the Vpc endpoint service."),
        )
        parser.add_argument(
            '--approval-enabled',
            metavar='<approval_enabled>',
            type=bool,
            help=_("Specifies whether connection approval is required."),
        )
        parser.add_argument(
            '--service-name',
            metavar='<service_name>',
            help=_("Specifies the name of the VPC endpoint service."),
        )
        parser.add_argument(
            '--ports',
            metavar='client_port=<client-port>,'
                    'server_port=<server-port>,'
                    'protocol=<protocol>',
            action=parseractions.MultiKeyValueAction,
            dest='tags',
            required_keys=['client_port', 'server_port', 'protocol'],
            help=_("Example: \n"
                   "--ports client_port=8081,server_port=22,protocol=TCP\n"
                   "Repeat option to provide multiple ports."),
        )
        parser.add_argument(
            '--port-id',
            metavar='<port_id>',
            help=_("Specifies the ID for identifying the backend resource of "
                   "the VPC endpoint service."),
        )
        parser.add_argument(
            '--vip-port-id',
            metavar='<vip_port_id>',
            help=_("Specifies the ID of the virtual NIC to which "
                   "the virtual IP address is bound.."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.vpcep
        args_list = [
            'service_name',
            'ports',
            'port_id',
            'vip_port_id',
            'approval_enabled'
        ]
        attrs = {}
        for arg in args_list:
            if getattr(parsed_args, arg):
                attrs[arg] = getattr(parsed_args, arg)
        endpoint_service = client.get_endpoint_service(
            parsed_args.endpointservice)

        obj = client.update_endpoint_service(endpoint_service.id, **attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class DeleteEndpointService(command.Command):

    _description = _("Deletes VPC Endpoint Service.")

    def get_parser(self, prog_name):
        parser = super(DeleteEndpointService, self).get_parser(prog_name)
        parser.add_argument(
            'endpointservice',
            metavar='<endpointservice>',
            nargs='+',
            help=_("Vpc Endpoint Services(s) to delete (Name or ID)"),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.vpcep
        result = 0
        for endpointservice in parsed_args.endpointservice:
            try:
                obj = client.get_endpoint_service(endpointservice)
                client.delete_endpoint_service(obj.id)
            except Exception as e:
                result += 1
                LOG.error(_("Failed to delete Vpc Endpoint Service with "
                            "name or ID '%(endpointservice)s': %(e)s"),
                          {'endpointservice': endpointservice, 'e': e})
        if result > 0:
            total = len(parsed_args.endpointservice)
            msg = (_("%(result)s of %(total)s Vpc Endpoint Services(s) failed "
                     "to delete.") % {'result': result, 'total': total})
            raise exceptions.CommandError(msg)


class ListWhitelist(command.Lister):

    _description = _("List whitelist records of a VPC endpoint service.")
    columns = ('Connection Id', 'Permission', 'Created At')

    def get_parser(self, prog_name):
        parser = super(ListWhitelist, self).get_parser(prog_name)

        parser.add_argument(
            'endpoint_service',
            metavar='<endpoint_service>',
            help=_("Specifies the ID or name of the VPC Endpoint Service."),
        )
        parser.add_argument(
            '--sort-key',
            metavar='<sort_key>',
            help=_("Specifies the sorting field of the VPC endpoint list."),
        )
        parser.add_argument(
            '--sort-dir',
            metavar='<sort_dir>',
            help=_("Specifies the sorting method of the VPC endpoint list."),
        )
        parser.add_argument(
            '--limit',
            metavar='<limit>',
            type=int,
            help=_("Specifies the maximum number of endpoint connections "
                   "displayed on each page."),
        )
        parser.add_argument(
            '--offset',
            metavar='<offset>',
            type=int,
            help=_("Specifies the offset.."),
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
        data = client.endpoint_service_whitelists(
            parsed_args.endpoint_service, **attrs)

        return (self.columns, (utils.get_item_properties(s, self.columns)
                               for s in data))


class ManageWhitelist(command.Lister):
    _description = _("Manage whitelist records of a VPC endpoint service.")

    columns = ('Endpoint Id', 'Permission', 'Created At')

    def get_parser(self, prog_name):
        parser = super(ManageWhitelist, self).get_parser(prog_name)

        parser.add_argument(
            'endpointservice',
            metavar='<endpoint_service>',
            help=_("Specifies the ID or name of the VPC Endpoint Service."),
        )
        parser.add_argument(
            'domain',
            metavar='<domain>',
            nargs='+',
            help=_("Domain ID(s) to add to whitelist record of the "
                   "Vpc endpoint service."),
        )
        manage_request_group = parser.add_mutually_exclusive_group()
        manage_request_group.add_argument(
            '--add',
            action='store_true',
            help=("Add a domian to the whitelist record of the "
                  "Vpc endpoint service.")
        )
        manage_request_group.add_argument(
            '--remove',
            action='store_true',
            help=("Remove a domian from the whitelist record of the "
                  "Vpc endpoint service.")
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.vpcep
        domains = []
        for domain in parsed_args.domain:
            domains.append('iam:domain::' + domain)
        set_args = ('add', 'remove')
        request_status = [request for request in set_args if
                          getattr(parsed_args, request)]
        args = {
            'permissions': domains,
            'action': request_status[0]
        }

        data = client.manage_endpoint_service_whitelist(
            parsed_args.endpoint_service, **args)

        return (self.columns, (utils.get_item_properties(s, self.columns)
                               for s in data))


class ListConnections(command.Lister):

    _description = _("List VPC Endpoint Service Connections.")
    columns = ('Id', 'Domain Id', 'Status')

    def get_parser(self, prog_name):
        parser = super(ListConnections, self).get_parser(prog_name)

        parser.add_argument(
            'endpoint_service',
            metavar='<endpoint_service>',
            help=_("Specifies the ID or name of the VPC Endpoint Service."),
        )
        parser.add_argument(
            '--id',
            metavar='<id>',
            help=_("Specifies the ID of the VPC Endpoint."),
        )
        parser.add_argument(
            '--sort-key',
            metavar='<sort_key>',
            help=_("Specifies the sorting field of the VPC endpoint list."),
        )
        parser.add_argument(
            '--sort-dir',
            metavar='<sort_dir>',
            help=_("Specifies the sorting method of the VPC endpoint list."),
        )
        parser.add_argument(
            '--limit',
            metavar='<limit>',
            type=int,
            help=_("Specifies the maximum number of endpoint connections "
                   "displayed on each page."),
        )
        parser.add_argument(
            '--offset',
            metavar='<offset>',
            type=int,
            help=_("Specifies the offset.."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.vpcep
        args_list = [
            'id',
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

        data = client.endpoint_service_connections(
            parsed_args.endpoint_service, **attrs)

        return (self.columns, (utils.get_item_properties(s, self.columns)
                               for s in data))


class ManageConnections(command.Lister):
    _description = _("Manage VPC Endpoint Service Connections.")

    columns = ('Id', 'Domain Id', 'Status')

    def get_parser(self, prog_name):
        parser = super(ManageConnections, self).get_parser(prog_name)

        parser.add_argument(
            'endpointservice',
            metavar='<endpoint_service>',
            help=_("Specifies the ID or name of the VPC Endpoint Service."),
        )
        parser.add_argument(
            'endpoint',
            metavar='<endpoint>',
            nargs='+',
            help=_("VPC Endpoint(s) ID to Accept Or Reject "
                   "Connection to Service."),
        )
        manage_request_group = parser.add_mutually_exclusive_group()
        manage_request_group.add_argument(
            '--receive',
            action='store_true',
            help=('Accept VPC Endpoint Connection to Endpoint Service.')
        )
        manage_request_group.add_argument(
            '--reject',
            action='store_true',
            help=('Reject VPC Endpoint Connection to Endpoint Service.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.vpcep
        endpoints = []
        for endpoint in parsed_args.endpoint:
            endpoints.append(endpoint)
        set_args = ('receive', 'reject')
        request_status = [request for request in set_args if
                          getattr(parsed_args, request)]
        args = {
            'endpoints': endpoints,
            'action': request_status[0]
        }

        data = client.manage_endpoint_service_connections(
            parsed_args.endpoint_service, **args)

        return (self.columns, (utils.get_item_properties(s, self.columns)
                               for s in data))
