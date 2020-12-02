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

from otcextensions.i18n import _
from otcextensions.common import sdk_utils

LOG = logging.getLogger(__name__)


def _get_columns(item):
    column_map = {
    }
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


class ListEndpoints(command.Lister):

    _description = _("List VPC Endpoints.")
    columns = ('Id', 'Name', 'Spec', 'Router Id', 'Status')

    def get_parser(self, prog_name):
        parser = super(ListEndpoints, self).get_parser(prog_name)

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

        data = client.endpoints(**attrs)

        return (self.columns, (utils.get_item_properties(s, self.columns)
                               for s in data))


class ShowEndpoint(command.ShowOne):
    _description = _("Show VPC Endpoint Details.")

    def get_parser(self, prog_name):
        parser = super(ShowEndpoint, self).get_parser(prog_name)
        parser.add_argument(
            'endpoint',
            metavar='<endpoint>',
            help=_("Specifies the ID of the VPC Endpoint."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.vpcep
        obj = client.get_endpoint(parsed_args.endpoint)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class CreateEndpoint(command.ShowOne):
    _description = _(
        "Create a VPC endpoint for accessing a VPC endpoint service.")

    def get_parser(self, prog_name):
        parser = super(CreateEndpoint, self).get_parser(prog_name)
        parser.add_argument(
            'endpointservice',
            metavar='<endpoint_service_id>',
            help=_("Specifies the Id of Vpc endpoint service."),
        )
        parser.add_argument(
            '--router-id',
            metavar='<vpc_id>',
            required=True,
            help=_("Specifies the ID of the VPC where the VPC endpoint "
                   "is to be created."),
        )
        parser.add_argument(
            '--network-id',
            metavar='<subnet_id>',
            required=True,
            help=_("Specify the ID of the subnet created in the VPC."),
        )
        parser.add_argument(
            '--port-ip',
            metavar='<port_ip>',
            help=_("Specifies the IP address for accessing the associated "
                   "VPC endpoint service."),
        )

        # Tags for VPC Endpoint
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
            'routetables',
            metavar='<routetables>',
            nargs='+',
            help=_('Lists the IDs of route tables.'),
        )

        parser.add_argument(
            '--whitelist',
            metavar='<whitelist>',
            nargs='+',
            help=_("Specifies the whitelist for controlling access "
                   "to the VPC endpoint."),
        )
        manage_request_group = parser.add_mutually_exclusive_group()
        manage_request_group.add_argument(
            '--enable-dns',
            action='store_true',
            help=("Specifies whether connection approval is required.")
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
            'whitelist']
        attrs = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val
        attrs['routeTables'] = []
        for routetable in parsed_args.routetables:
            attrs['routeTables'].append({routetable})

        obj = client.create_endpoint(**attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class DeleteEndpoint(command.Command):

    _description = _("Deletes VPC Endpoint.")

    def get_parser(self, prog_name):
        parser = super(DeleteEndpoint, self).get_parser(prog_name)
        parser.add_argument(
            'endpoint',
            metavar='<endpoint>',
            nargs='+',
            help=_("Vpc Endpoint(s) ID to delete."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.vpcep
        result = 0
        for endpoint in parsed_args.endpoint:
            try:
                obj = client.find_endpoint(
                    endpoint, ignore_missing=False)
                client.delete_endpoint(obj.id)
            except Exception as e:
                result += 1
                LOG.error(_("Failed to delete Vpc Endpoint with "
                            "name or ID '%(endpoint)s': %(e)s"),
                          {'endpoint': endpoint, 'e': e})
        if result > 0:
            total = len(parsed_args.gateway)
            msg = (_("%(result)s of %(total)s Vpc Endpoint(s) failed "
                     "to delete.") % {'result': result, 'total': total})
            raise exceptions.CommandError(msg)
