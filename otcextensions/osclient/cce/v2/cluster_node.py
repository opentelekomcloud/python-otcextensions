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
import argparse
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
        'availability_zone': obj.spec.availability_zone
    }

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
    columns = ('ID', 'name', 'flavor',
               'private_ip', 'public_ip', 'availability_zone', 'ssh_key',
               'status')

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

        data = utils.get_dict_properties(
            _flatten_cluster_node(obj), self.columns)

        return (self.columns, data)


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
        'status')

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
            help=_('Name of the CCE Node Pool.')
        )
        parser.add_argument(
            '--annotation',
            metavar='<key_name>=<value=name>',
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
            help=_('Bandwidth of the floating ip being created. fip_count'
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
            metavar='<dedicated-host>',
            help=_('Name or ID of the Dedicated Host to which nodes will.'
                   'be scheduled.')
        )
        parser.add_argument(
            '--ecs-group',
            metavar='<group-id>',
            help=_('ID of the ECS group where the CCE node can belong to.')
        )
        parser.add_argument(
            '--fault-domain',
            metavar='<fault-domain>',
            help=_('The node is created in the specified fault domain.')
        )
        parser.add_argument(
            '--flavor',
            metavar='<flavor>',
            required=True,
            help=_('The flavor for the node.')
        )
        # MUST BE REWORKED
        parser.add_argument(
            '--floating-ip',
            metavar='<floating-ip>',
            action='append',
            help=_('Address or ID of the existing floating IP to be '
                   'attached to the new node.\n'
                   'Repeat option for multiple IPs to be attached to '
                   'multiple nodes. The node count and the floating IP count '
                   'must be identical.')
        )
        parser.add_argument(
            '--volume',
            metavar='<volume>',
            required=True,
            help=_(
                'Disk information to attach to the instance.\n'
                'format = `VOLUME_TYPE`,`SIZE`\n'
                '`VOLUME_TYPE` can be in: \n'
                '* `SATA` = Common I/O \n'
                '* `SAS` = High I/O \n'
                '* `SSD` = Ultra-High I/O \n'
                '`SIZE` is size in Gb.')
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
            '--annotation',
            metavar='<annotation>',
            action='append',
            help=_('Annotation to assign to the server in KEY=VALUE format. '
                   'Repeat for multiple values.')
        )
        parser.add_argument(
            '--label',
            metavar='<label>',
            action='append',
            help=_('Label to assign to the server in KEY=VALUE format. '
                   'Repeat for multiple values.')
        )
        parser.add_argument(
            '--count',
            metavar='[1..]',
            type=int,
            default=1,
            help=_('Number of node instances to create '
                   '(max 15 in the cluster).')
        )
        return parser

    def take_action(self, parsed_args):

        attrs = {}

        # mandatory


        obj = self.app.client_manager.sdk_connection.create_cce_node_pool(
            **attrs)

        data = utils.get_dict_properties(
            _flatten_cluster_node(obj),
            self.columns)

        return (self.columns, data)
