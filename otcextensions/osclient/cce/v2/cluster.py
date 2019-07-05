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
'''CCE Cluster v2 action implementations'''
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


CONTAINER_NET_MODE_CHOICES = ['overlay_l2', 'underslay_ipvlan', 'vpc-router']
CLUSTER_TYPES = ['BareMetal', 'VirtualMachine']


def _flatten_cluster(obj):
    data = {
        'id': obj.id,
        'name': obj.name,
        'status': obj.status.status,
        'type': obj.spec.type,
        'flavor': obj.spec.flavor,
        'endpoint': obj.status.endpoints.get('external_otc'),
        'vpc': obj.spec.host_network.vpc,
        'subnet': obj.spec.host_network.subnet,
        'version': obj.spec.version
    }

    return data


class ListCCECluster(command.Lister):
    _description = _('List CCE Clusters')
    columns = ('ID', 'name', 'status', 'flavor', 'version', 'endpoint')

    def get_parser(self, prog_name):
        parser = super(ListCCECluster, self).get_parser(prog_name)

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.cce

        data = client.clusters()

        table = (self.columns,
                 (utils.get_dict_properties(
                     _flatten_cluster(s), self.columns,
                 ) for s in data))
        return table


class ShowCCECluster(command.ShowOne):
    _description = _('Show single Cluster details')
    columns = ('ID', 'name', 'type', 'status', 'version', 'endpoint',
               'flavor', 'vpc', 'subnet')

    def get_parser(self, prog_name):
        parser = super(ShowCCECluster, self).get_parser(prog_name)
        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            help=_('ID of the cluster')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.cce

        obj = client.find_cluster(parsed_args.cluster)

        # display_columns, columns = _get_columns(obj)
        data = utils.get_dict_properties(_flatten_cluster(obj), self.columns)

        return (self.columns, data)


class DeleteCCECluster(command.Command):
    _description = _('Delete CCE Cluster')

    def get_parser(self, prog_name):
        parser = super(DeleteCCECluster, self).get_parser(prog_name)
        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            help=_('ID of the cluster')
        )
        return parser

    def take_action(self, parsed_args):

        if parsed_args.cluster:
            client = self.app.client_manager.cce
            client.delete_cluster(parsed_args.cluster)


class CreateCCECluster(command.Command):
    _description = _('Create CCE Cluster')
    columns = ('ID', 'name', 'version', 'endpoint')

    def get_parser(self, prog_name):
        parser = super(CreateCCECluster, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help=_('Name of the cluster.')
        )
        parser.add_argument(
            'vpc',
            metavar='<vpc>',
            help=_('The VPC ID of the container cluster.')
        )
        parser.add_argument(
            'subnet',
            metavar='<subnet>',
            help=_('The Subnet ID of the container cluster.')
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_('Text description of the cluster.')
        )
        parser.add_argument(
            '--version',
            metavar='<version>',
            help=_('Cluster version.')
        )
        parser.add_argument(
            '--flavor',
            metavar='<flavor>',
            required=True,
            help=_('Cluster flavor.')
        )
        parser.add_argument(
            '--type',
            metavar='{' + ','.join(CLUSTER_TYPES) + '}',
            choices=CLUSTER_TYPES,
            default='VirtualMachine',
            help=_('Cluster type.')
        )
        parser.add_argument(
            '--highway_subnet',
            metavar='<subnet_id>',
            help=_('ID of the high-speed network that is used to create '
                   'a bare metal node.')
        )
        parser.add_argument(
            '--container_net_mode',
            metavar='{' + ','.join(CONTAINER_NET_MODE_CHOICES) + '}',
            type=lambda s: s.lower(),
            choices=CONTAINER_NET_MODE_CHOICES,
            required=True,
            help=_('Container network mode.')
        )
        parser.add_argument(
            '--container_net_cidr',
            metavar='<CIDR>',
            help=_('Network segment of the container network.')
        )
        return parser

    def take_action(self, parsed_args):

        attrs = {}

        attrs['name'] = parsed_args.name
        spec = {}
        spec['type'] = parsed_args.type
        spec['flavor'] = parsed_args.flavor
        if parsed_args.version:
            spec['version'] = parsed_args.version
        if parsed_args.description:
            spec['description'] = parsed_args.description
        host_net = {
            'vpc': parsed_args.vpc,
            'subnet': parsed_args.subnet
        }
        if spec['type'] == 'BareMetal':
            host_net['highwaySubnet'] = parsed_args.highway_subnet
        spec['hostNetwork'] = host_net
        container_net = {
            'mode': parsed_args.container_net_mode
        }
        if parsed_args.container_net_cidr:
            container_net['cidr'] = parsed_args.container_net_cidr
        spec['containerNetwork'] = container_net

        attrs['spec'] = spec

        client = self.app.client_manager.cce

        obj = client.create_cluster(**attrs)

        data = utils.get_dict_properties(_flatten_cluster(obj), self.columns)

        return (self.columns, data)
