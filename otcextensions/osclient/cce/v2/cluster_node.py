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


def _flatten_cluster_node(obj):
    """Flatten the structure of the cluster node into a single dict
    """
    data = {
        'id': obj.id,
        'name': obj.name,
        'private_ip': obj.status.private_ip,
        'public_ip': obj.status.floating_ip,
        'status': obj.status.status,
        'flavor': obj.spec.flavor,
        'ssh_key': obj.spec.login.get('sshKey', None),
        'availability_zone': obj.spec.availability_zone,
        'operating_system': obj.spec.os,
        'root_volume_type': obj.spec.root_volume.type,
        'root_volume_size': obj.spec.root_volume.size
    }

    i = 1
    for item in obj.spec.data_volumes:
        data['data_volume_type_' + str(i)] = item.get('type')
        data['data_volume_size_' + str(i)] = item.get('size')
        i += 1

    return data


class ListCCEClusterNode(command.Lister):
    _description = _('List CCE Cluster Nodes')
    columns = ('ID', 'name', 'private_ip', 'public_ip',
               'status')

    def get_parser(self, prog_name):
        parser = super(ListCCEClusterNode, self).get_parser(prog_name)
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

        data = client.cluster_nodes(cluster.id)

        table = (self.columns,
                 (utils.get_dict_properties(
                     _flatten_cluster_node(s), self.columns,
                 ) for s in data))
        return table


class ShowCCEClusterNode(command.ShowOne):
    _description = _('Show single Cluster node details')
    columns = (
        'ID',
        'name',
        'flavor',
        'private_ip',
        'public_ip',
        'availability_zone',
        'ssh_key',
        'status',
        'root_volume_type',
        'root_volume_size',)

    def get_parser(self, prog_name):
        parser = super(ShowCCEClusterNode, self).get_parser(prog_name)
        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            help=_('ID of the cluster.')
        )
        parser.add_argument(
            'node',
            metavar='<node>',
            help=_('ID of the cluster node.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.cce

        cluster = client.find_cluster(parsed_args.cluster,
                                      ignore_missing=False)

        obj = client.find_cluster_node(
            cluster=cluster.id,
            node=parsed_args.node
        )

        flat_data = _flatten_cluster_node(obj)
        columns = tuple(flat_data)

        data = utils.get_dict_properties(
            flat_data,
            columns)

        return (columns, data)


class DeleteCCEClusterNode(command.Command):
    _description = _('Delete CCE Cluster nodes')

    def get_parser(self, prog_name):
        parser = super(DeleteCCEClusterNode, self).get_parser(prog_name)
        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            help=_('ID of the cluster.')
        )
        parser.add_argument(
            'node',
            metavar='<node>',
            nargs='+',
            help=_('Name of the cluster node.')
        )
        return parser

    def take_action(self, parsed_args):

        if parsed_args.cluster and parsed_args.node:
            client = self.app.client_manager.cce
            cluster = client.find_cluster(parsed_args.cluster,
                                          ignore_missing=False)
            for node in parsed_args.node:
                obj = client.find_cluster_node(
                    cluster=cluster.id,
                    node=node)
                client.delete_cluster_node(
                    cluster=cluster.id,
                    node=obj.id,
                    ignore_missing=False)


class CreateCCEClusterNode(command.Command):
    _description = _('Create CCE Cluster Node')

    columns = (
        'ID',
        'name',
        'flavor',
        'private_ip',
        'public_ip',
        'availability_zone',
        'ssh_key',
        'status',
        'root_volume_type',
        'root_volume_size')

    def get_parser(self, prog_name):
        parser = super(CreateCCEClusterNode, self).get_parser(prog_name)

        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            help=_('ID or name of the CCE cluster.')
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_('Name of the CCE node.\nThe clustername and a random '
                   'number is used to create a node name by default.')
        )
        parser.add_argument(
            '--annotation',
            metavar='<key_name>=<value_name>',
            action=parseractions.KeyValueAction,
            dest='annotations',
            help=_('Annotations in form of key, value pairs.'
                   'Repeat option for multiple tags.\n'
                   'Example: '
                   '--annotation keyname1=valuename1 '
                   '--annotation keyname2=valuename2')
        )
        parser.add_argument(
            '--availability-zone',
            metavar='<availability_zone>',
            required=True,
            help=_('Availability zone to place server in.')
        )
        parser.add_argument(
            '--bandwidth',
            metavar='<bandwidth>',
            type=int,
            help=_('Bandwidth of the floating ip being created. fip-count'
                   'must be specified if bandwidth is used.')
        )
        parser.add_argument(
            '--count',
            metavar='<count>',
            default=1,
            type=int,
            help=_('Count of the cluster nodes to be created.\n'
                   'Default: 1.')
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
            '--dedicated-host',
            metavar='<dedicated_host>',
            help=_('Name or ID of the Dedicated Host to which nodes will.'
                   'be scheduled.')
        )
        parser.add_argument(
            '--ecs-group',
            metavar='<group_id>',
            help=_('ID of the ECS group where the CCE node can belong to.')
        )
        parser.add_argument(
            '--fault-domain',
            metavar='<fault_domain>',
            help=_('The node is created in the specified fault domain.')
        )
        parser.add_argument(
            '--flavor',
            metavar='<flavor>',
            required=True,
            help=_('The flavor for the node.')
        )
        parser.add_argument(
            '--floating-ip',
            metavar='<floating_ip>',
            action='append',
            help=_('Address or ID of the existing floating IP to be '
                   'attached to the new node.\n'
                   'Repeat option for multiple IPs to be attached to '
                   'multiple nodes.')
        )
        parser.add_argument(
            '--fip-count',
            metavar='<fip_count>',
            type=int,
            help=_('Count of floating IP addresses being attached to one '
                   'or more nodes.\nThe parameter must be used together with'
                   'bandwidth.')
        )
        parser.add_argument(
            '--k8s-tag',
            metavar='<key_name>=<value_name>',
            action=parseractions.KeyValueAction,
            dest='k8s_tags',
            help=_('Kubernetes tags in form of key, value pairs. Repeat '
                   'option for multiple tags.\n'
                   'Example:\n'
                   '--k8s-tag keyname1=valuename1 '
                   '--k8s-tag keyname2=valuename2')
        )
        parser.add_argument(
            '--label',
            metavar='<key_name>=<value_name>',
            action=parseractions.KeyValueAction,
            dest='labels',
            help=_('Option labels in form of key, value pairs. Repeat '
                   'option for multiple labels.\n'
                   'Example:\n'
                   '--label keyname1=valuename1 '
                   '--label keyname2=valuename2')
        )
        parser.add_argument(
            '--lvm-config',
            metavar='<lvm_config>',
            help=_('ConfigMap of the Docker data disk.')
        )
        parser.add_argument(
            '--max-pods',
            metavar='<max_pods>',
            type=int,
            help=_('Maximum number of pods on the node')
        )
        parser.add_argument(
            '--network',
            metavar='<network>',
            required=True,
            help=_('ID or name of the network where the node will be '
                   'created.')
        )
        parser.add_argument(
            '--node-image-id',
            metavar='<node_image_id>',
            help=_('ID of a custom image used in a bare metal scenario.')
        )
        parser.add_argument(
            '--os',
            metavar='<operating_system>',
            help=_('Operating system of the cluster node.')
        )
        parser.add_argument(
            '--postinstall-script',
            metavar='<postinstall_script>',
            help=_('Base64 encoded post installation script.')
        )
        parser.add_argument(
            '--preinstall-script',
            metavar='<preinstall_script>',
            help=_('Base64 encoded pre installation script.')
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
            help=_('Root volume type.\n'
                   'Options: SAS, SATA, SSD.')
        )
        parser.add_argument(
            '--ssh-key',
            metavar='<ssh_key>',
            required=True,
            help=_('SSH Key used to create the node.')
        )
        parser.add_argument(
            '--tag',
            metavar='key=<keyname1>,value=<value1>',
            action=parseractions.MultiKeyValueAction,
            dest='tags',
            required_keys=['key', 'value'],
            help=_('List of tags used to build UI labels. Repeat option for '
                   'multiple tags.\n'
                   'Example:\n'
                   '--tag key=mykey1,value=myvalue1')
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help=('Wait for the instance to become active')
        )
        parser.add_argument(
            '--wait-interval',
            metavar='<interval>',
            type=int,
            default=5,
            help=_('Check interval in seconds for successful creation check'
                   'when param wait is True.')
        )
        parser.add_argument(
            '--wait-timeout',
            metavar='<timeout>',
            type=int,
            default=3600,
            help=_('Maximum time in seconds to wait for successful creation'
                   'when param wait is True.')
        )
        return parser

    def take_action(self, parsed_args):

        attrs = {}

        # mandatory
        attrs['availability_zone'] = parsed_args.availability_zone
        attrs['cluster'] = parsed_args.cluster
        attrs['count'] = parsed_args.count
        attrs['flavor'] = parsed_args.flavor
        attrs['network'] = parsed_args.network
        attrs['ssh_key'] = parsed_args.ssh_key

        # optional
        if parsed_args.annotations:
            attrs['annotations'] = parsed_args.annotations
        if parsed_args.bandwidth:
            attrs['bandwidth'] = parsed_args.bandwidth
        if parsed_args.count:
            attrs['count'] = parsed_args.count
        if parsed_args.data_volumes:
            attrs['data_volumes'] = parsed_args.data_volumes
        if parsed_args.dedicated_host:
            attrs['dedicated_host'] = parsed_args.dedicated_host
        if parsed_args.ecs_group:
            attrs['ecs_group'] = parsed_args.ecs_group
        if parsed_args.fault_domain:
            attrs['fault_domain'] = parsed_args.fault_domain
        if parsed_args.floating_ip:
            attrs['floating_ips'] = parsed_args.floating_ip
        if parsed_args.fip_count:
            attrs['fip_count'] = parsed_args.fip_count
        if parsed_args.k8s_tags:
            attrs['k8s_tags'] = parsed_args.k8s_tags
        if parsed_args.labels:
            attrs['labels'] = parsed_args.labels
        if parsed_args.max_pods:
            attrs['max_pods'] = parsed_args.max_pods
        if parsed_args.name:
            attrs['name'] = parsed_args.name
        if parsed_args.network:
            attrs['network'] = parsed_args.network
        if parsed_args.node_image_id:
            attrs['node_image_id'] = parsed_args.node_image_id
        if parsed_args.os:
            attrs['os'] = parsed_args.os
        if parsed_args.postinstall_script:
            attrs['postinstall_script'] = parsed_args.postinstall_script
        if parsed_args.preinstall_script:
            attrs['preinstall_script'] = parsed_args.preinstall_script
        if parsed_args.root_volume_size:
            attrs['root_volume_size'] = parsed_args.root_volume_size
        if parsed_args.root_volume_type:
            attrs['root_volume_type'] = parsed_args.root_volume_type
        if parsed_args.tags:
            attrs['tags'] = parsed_args.tags
        if not parsed_args.wait:
            attrs['wait'] = False
        if parsed_args.wait_interval:
            attrs['wait_interval'] = parsed_args.wait_interval
        if parsed_args.wait_timeout:
            attrs['wait_timeout'] = parsed_args.wait_timeout

        obj = self.app.client_manager.sdk_connection.create_cce_cluster_node(
            **attrs)

        flat_data = _flatten_cluster_node(obj)
        columns = tuple(flat_data)

        data = utils.get_dict_properties(
            flat_data,
            columns)

        return (columns, data)
