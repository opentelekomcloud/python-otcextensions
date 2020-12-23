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


class ShowCCENodePool(command.ShowOne):
    _description = _('Show single Cluster node details')
    columns = ('ID', 'name', 'flavor', 'os', 'autoscaling',)

    def get_parser(self, prog_name):
        parser = super(ShowCCENodePool, self).get_parser(prog_name)
        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            help=_('ID of the cluster.')
        )
        parser.add_argument(
            'nodepool',
            metavar='<nodepool>',
            help=_('ID of the CCE node pool.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.cce

        cluster = client.find_cluster(parsed_args.cluster,
                                      ignore_missing=False)

        obj = client.find_node_pool(
            cluster=cluster.id,
            node_pool=parsed_args.nodepool
        )

        data = utils.get_dict_properties(
            _flatten_node_pool(obj), self.columns)

        return (self.columns, data)


class CreateCCENodePool(command.ShowOne):
    _description = _('Create CCE Node Pool')
    columns = ('ID', 'name')

    def get_parser(self, prog_name):
        parser = super(CreateCCENodePool, self).get_parser(prog_name)
        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            help=_('ID or name of the CCE cluster.')
        )
        parser.add_argument(
            'name',
            metavar='<name>',
            help=_('Name of the CCE Node Pool.')
        )
        parser.add_argument(
            '--autoscaling-enabled',
            metavar='<autoscaling_enabled>',
            default=False,
            type=bool,
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
            optional_keys=['encrypted', 'cmk_id'],
            help=_('Example: '
                   '--data-volume volumetype=SATA,size=100,encrypted=True,'
                   'cmk_id=12345qwertz \n'
                   'Repeat option for multiple data volumes.\n'
                   'Default: --data-volume volumetype=SATA,size=100')
        )
        parser.add_argument(
            '--ecs-group',
            metavar='<ecs_group>',
            help=_('ECS group id of the ECS group to which nodes belong '
                   'after creation.')
        )
        parser.add_argument(
            '--flavor',
            metavar='<flavor>',
            required=True,
            help=_('CCE cluster node flavor.')
        )
        parser.add_argument(
            '--initial-node-count',
            metavar='<initial_node_count>',
            default=0,
            type=int,
            help=_('Node count after Node pool creation.')
        )
        parser.add_argument(
            '--k8s-tag',
            metavar='<key_name>=<value=name>',
            action=parseractions.KeyValueAction,
            dest='k8s_tags',
            help=_('Kubernetes tags in form of key, value pairs. Repeat '
                   'option for multiple tags.\n'
                   'Example: '
                   '--k8s-tag keyname1=valuename1 '
                   '--k8s-tag keyname2=valuename2')
        )
        parser.add_argument(
            '--lvm-config',
            metavar='<lvm_config>',
            help=_('Config Map of the Docker data disk.')
        )
        parser.add_argument(
            '--min-node-count',
            metavar='<min_node_count>',
            type=int,
            help=_('If auto-scaling is enabled, the value describes the '
                   'minimum number of nodes of the cluster.')
        )
        parser.add_argument(
            '--max-node-count',
            metavar='<max_node_count>',
            type=int,
            help=_('If auto-scaling is enabled, the value describes the '
                   'maximum number of nodes of the cluster. The value '
                   'must be equal or greater as the min_node_count.')
        )
        parser.add_argument(
            '--max-pods',
            metavar='<max_pods>',
            type=int,
            help=_('Maximum number of pods on the node.')
        )
        parser.add_argument(
            '--node-image-id',
            metavar='<node_image_id>',
            help=_('Mandatory if custom image is used on a bare '
                   'metall node.')
        )
        parser.add_argument(
            '--node-pool-type',
            metavar='<node_pool_type>',
            help=_('Node pool type, currently only vm is supported.')
        )
        parser.add_argument(
            '--operating-system',
            metavar='<os>',
            required=True,
            help=_('CCE cluster node operating system.')
        )
        parser.add_argument(
            '--preinstall-script',
            metavar='<preinstall_script>',
            help=_('Script required before installation. '
                   'Input must be Base64 encoded.')
        )
        parser.add_argument(
            '--postinstall-script',
            metavar='<postinstall_script>',
            help=_('Script required after installation. '
                   'Input must be Base64 encoded.')
        )
        parser.add_argument(
            '--priority',
            metavar='<priority>',
            type=int,
            help=_('If auto-scaling is enabled, the value describes the '
                   'priority of the scale up functionality between '
                   'several Node Pools. A higher priority number '
                   'indicates a higher priority starting from 1.')
        )
        parser.add_argument(
            '--public-key',
            metavar='<public_key>',
            help=_('Additional public key to be added to for login.')
        )
        parser.add_argument(
            '--network-id',
            metavar='<network_id>',
            required=True,
            help=_('ID of the network to which the cluster node '
                   'will belong to.')
        )
        parser.add_argument(
            '--root-volume-size',
            metavar='<root_volume_size>',
            type=int,
            default=40,
            help=_('Root volume size in GB.')
        )
        parser.add_argument(
            '--root-volume-type',
            metavar='<root_volume_type>',
            choices=['SAS', 'SATA', 'SSD'],
            default='SATA',
            help=_('Root volume type.\nOptions: SAS, SATA, SSD.')
        )
        parser.add_argument(
            '--scale-down-cooldown-time',
            metavar='<time in minutes>',
            type=int,
            help=_('Interval in minutes during which nodes added '
                   'after a scale-up will not be deleted.')
        )
        parser.add_argument(
            '--ssh-key',
            metavar='<ssh-key>',
            required=True,
            help=_('Name of the SSH public key.')
        )
        parser.add_argument(
            '--tag',
            metavar='key=<keyname1>,value=<value1>',
            action=parseractions.MultiKeyValueAction,
            dest='tags',
            required_keys=['key', 'value'],
            help=_('Example: '
                   '--tag key=mykey1,value=myvalue1\n'
                   'Repeat option for multiple tags.')
        )
        parser.add_argument(
            '--taint',
            metavar='key=<keyname1>,value=<value1>,\n'
                    'effect=<NoSchedule|PreferNoSchedule|NoExecute',
            action=parseractions.MultiKeyValueAction,
            dest='taints',
            required_keys=['key', 'value', 'effect'],
            help=_('Example: '
                   '--taint key=mykey1,value=myvalue1,effect=NoSchedule\n'
                   'Repeat option for multiple taints.')
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
        if parsed_args.ecs_group:
            attrs['ecs_group'] = parsed_args.ecs_group
        if parsed_args.initial_node_count:
            attrs['initial_node_count'] = parsed_args.initial_node_count
        if parsed_args.k8s_tags:
            attrs['k8s_tags'] = parsed_args.k8s_tags
        if parsed_args.lvm_config:
            attrs['lvm_config'] = parsed_args.lvm_config
        if parsed_args.max_node_count:
            attrs['max_node_count'] = parsed_args.max_node_count
        if parsed_args.max_pods:
            attrs['max_pods'] = parsed_args.max_pods
        if parsed_args.min_node_count:
            attrs['min_node_count'] = parsed_args.min_node_count
        if parsed_args.node_image_id:
            attrs['node_image_id'] = parsed_args.node_image_id
        if parsed_args.node_pool_type:
            attrs['node_pool_type'] = parsed_args.node_pool_type
        if parsed_args.preinstall_script:
            attrs['preinstall_script'] = parsed_args.preinstall_script
        if parsed_args.postinstall_script:
            attrs['postinstall_script'] = parsed_args.postinstall_script
        if parsed_args.priority:
            attrs['priority'] = parsed_args.priority
        if parsed_args.public_key:
            attrs['public_key'] = parsed_args.public_key
        if parsed_args.root_volume_size:
            attrs['root_volume_size'] = parsed_args.root_volume_size
        if parsed_args.root_volume_type:
            attrs['root_volume_type'] = parsed_args.root_volume_type
        if parsed_args.scale_down_cooldown_time:
            sdct = parsed_args.scale_down_cooldown_time
            attrs['scale_down_cooldown_time'] = sdct
        if parsed_args.tags:
            attrs['tags'] = parsed_args.tags
        if parsed_args.taints:
            attrs['taints'] = parsed_args.taints

        obj = self.app.client_manager.sdk_connection.create_cce_node_pool(
            **attrs)

        data = utils.get_dict_properties(
            _flatten_node_pool(obj),
            self.columns)

        return (self.columns, data)


class DeleteCCENodePool(command.Command):
    _description = _('Delete CCE Node Pool')

    def get_parser(self, prog_name):
        parser = super(DeleteCCENodePool, self).get_parser(prog_name)
        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            help=_('ID of the cluster.')
        )
        parser.add_argument(
            'nodepool',
            metavar='<nodepool>',
            nargs='+',
            help=_('Name or ID of CCE Node pool. Repeat names with spaces '
                   'in between to delete multiple node pools.\n'
                   'Example: '
                   'openstack cce node pool delete testcluster pool1 pool2')
        )
        return parser

    def take_action(self, parsed_args):

        if parsed_args.cluster and parsed_args.nodepool:
            client = self.app.client_manager.cce
            cluster = client.find_cluster(parsed_args.cluster,
                                          ignore_missing=False)
            for pool in parsed_args.nodepool:
                obj = client.find_node_pool(
                    cluster=cluster.id,
                    node_pool=pool)
                client.delete_node_pool(
                    cluster=cluster.id,
                    node_pool=obj.id,
                    ignore_missing=False)
