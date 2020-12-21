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
'''CCE Cluster Nodes v2 action implementations'''
import logging

from osc_lib import utils
from osc_lib.cli import parseractions
from osc_lib.command import command

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _flatten_node_pool(obj):
    """Flatten the structure of the node pool into a single dict
    """
    data = {
        'id': obj.id,
        'name': obj.name,
        'flavor': obj.spec.node_template_spec.flavor,
        'os': obj.spec.node_template_spec.os,
        'autoscaling': obj.spec.autoscaling.enable,
        'current_node': obj.status.current_node
    }

    return data


class ListCCENodePools(command.Lister):
    _description = _('List CCE Node Pools')
    columns = ('ID', 'name', 'flavor', 'os', 'autoscaling', 'current_node')

    def get_parser(self, prog_name):
        parser = super(ListCCENodePools, self).get_parser(prog_name)
        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            help=_('The ID or name of the cluster.')
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.cce

        cluster = client.find_cluster(parsed_args.cluster,
                                      ignore_missing=False)

        data = client.node_pools(cluster.id)

        table = (self.columns,
                 (utils.get_dict_properties(
                     _flatten_node_pool(s), self.columns,
                 ) for s in data))
        return table


class CreateCCENodePool(command.ShowOne):
    _description = _('Create CCE Node Pool')
    columns = ('ID', 'name')

    def get_parser(self, prog_name):
        parser = super(CreateCCENodePool, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help=_('Name of the CCE Node Pool.')
        )
        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            help=_('ID or name of the CCE cluster.')
        )
        parser.add_argument(
            '--autoscaling-enabled',
            metavar='<autoscaling_enabled>',
            default=False,
            help=_('Enables or disables Autoscaling for cluster nodes.')
        )
        parser.add_argument(
            '--az',
            metavar='<availability_zone>',
            default='random',
            help=_('Availability zone for cluster nodes.\n'
                   'Default: random')
        )
        parser.add_argument(
            '--data-volume',
            metavar='volumetype=<volumetype>,size=<disksize>,'
                    'encrypted=<True|False>,cmk_id=<cmk_id>',
            action=parseractions.MultiKeyValueAction,
            dest='data_volumes',
            required_keys=['volumetype', 'size'],
            help=_('Example: \n'
                   '--data-volume volumetype=SATA,size=100,encrypted=True,'
                   'cmk_id=12345qwertz \n'
                   'Multiple data volumes are not supported via Node Pools.\n'
                   'Default: --data-volume volumetype=SATA,size=100')
        )
        parser.add_argument(
            '--flavor',
            metavar='<flavor>',
            required=True,
            help=_('CCE cluster node flavor.')
        )
        parser.add_argument(
            '--operating-system',
            metavar='<os>',
            required=True,
            help=_('CCE cluster node operating system.')
        )
        parser.add_argument(
            '--network-id',
            metavar='<network_id>',
            required=True,
            help=_('ID of the network to which the cluster node '
                   'will belong to.')
        )
        parser.add_argument(
            '--ssh-key',
            metavar='<ssh-key>',
            required=True,
            help=_('Name of the SSH public key.')
        )
        return parser

    def take_action(self, parsed_args):

        attrs = {}
        # mandatory
        attrs['cluster'] = parsed_args.cluster
        attrs['flavor'] = parsed_args.flavor
        attrs['os'] = parsed_args.operating_system
        attrs['name'] = parsed_args.name
        attrs['network_id'] = parsed_args.network_id
        attrs['ssh_key'] = parsed_args.ssh_key

        # optional
        if parsed_args.az:
            attrs['availability_zone'] = parsed_args.az
        if parsed_args.autoscaling_enabled:
            attrs['autoscaling_enabled'] = parsed_args.autoscaling_enabled
        if parsed_args.data_volumes:
            attrs['data_volumes'] = parsed_args.data_volumes

        obj = self.app.client_manager.sdk_connection.create_cce_node_pool(
            **attrs)

        data = utils.get_dict_properties(
            _flatten_node_pool(obj),
            self.columns)

        return (self.columns, data)
