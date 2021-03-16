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
'''CCE Cluster v2 action implementations'''
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


CONTAINER_NET_MODE_CHOICES = ['overlay_l2', 'underlay_ipvlan', 'vpc-router']
CLUSTER_TYPES = ['VirtualMachine']


def _flatten_cluster(obj):
    data = {
        'id': obj.id,
        'name': obj.name,
        'status': obj.status.status,
        'type': obj.spec.type,
        'flavor': obj.spec.flavor,
        'endpoint': obj.status.endpoints.get('external_otc'),
        'router_id': obj.spec.host_network.router_id,
        'network_id': obj.spec.host_network.network_id,
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
               'flavor', 'router_id', 'network_id')

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
            help=_('Name or ID of the cluster')
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help=_('Wait for the instance to become active')
        )
        parser.add_argument(
            '--wait-interval',
            type=int,
            help=_('Interval for checking status')
        )
        parser.add_argument(
            '--wait-timeout',
            type=int,
            help=_('Wait timeout')
        )
        return parser

    def take_action(self, parsed_args):

        attrs = {}
        for attr in [
            'cluster', 'wait', 'wait_timeout', 'wait_interval'
        ]:
            if getattr(parsed_args, attr):
                attrs[attr] = getattr(parsed_args, attr)

        if not parsed_args.wait:
            attrs['wait'] = False

        if parsed_args.cluster:
            self.app.client_manager.sdk_connection.delete_cce_cluster(
                **attrs
            )


class CreateCCECluster(command.ShowOne):
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
            'router',
            metavar='<router>',
            help=_('ID or name the Neutron Router.')
        )
        parser.add_argument(
            'network',
            metavar='<network>',
            help=_('ID or name of the Neutron network.')
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_('Text description of the cluster.')
        )
        parser.add_argument(
            '--multi-az',
            action='store_true',
            help=_('Support for multi-AZ cluster')
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
            '--container-network-mode',
            metavar='{' + ','.join(CONTAINER_NET_MODE_CHOICES) + '}',
            type=lambda s: s.lower(),
            choices=CONTAINER_NET_MODE_CHOICES,
            default='overlay_l2',
            help=_('Container network mode.')
        )
        parser.add_argument(
            '--container-network-cidr',
            metavar='<CIDR>',
            help=_('Network segment of the container network.')
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help=('Wait for the instance to become active')
        )
        parser.add_argument(
            '--wait-interval',
            type=int,
            help=_('Interval for checking status')
        )
        parser.add_argument(
            '--wait-timeout',
            type=int,
            help=_('Wait timeout')
        )
        return parser

    def take_action(self, parsed_args):

        attrs = {}
        for attr in [
            'name', 'type', 'flavor', 'router', 'network',
            'container_network_mode', 'annotations', 'authentication_proxy_ca',
            'authentication_mode', 'container_network_cidr',
            'cpu_manager_policy', 'dss_master_volumes', 'description',
            'external_ip', 'fix_pool_mask', 'labels', 'service_ip_range',
            'kube_proxy_mode', 'upgrade_from', 'version', 'wait',
            'wait_timeout', 'wait_interval'
        ]:
            if hasattr(parsed_args, attr) and getattr(parsed_args, attr):
                attrs[attr] = getattr(parsed_args, attr)

        if not parsed_args.wait:
            attrs['wait'] = False
        if parsed_args.multi_az:
            attrs['az'] = 'multi_az'

        obj = self.app.client_manager.sdk_connection.create_cce_cluster(
            **attrs)

        data = utils.get_dict_properties(_flatten_cluster(obj), self.columns)

        return (self.columns, data)
