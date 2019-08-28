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
'''CCE Cluster Nodes v1 action implementations'''
import argparse
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _flatten_cluster_node(obj):
    """Flatten the structure of the cluster node into a single dict
    """
    data = {
        'id': obj.id,
        'name': obj.name,
        'cluster_uuid': obj.spec.cluster_uuid,
        'private_ip': obj.spec.private_ip,
        'public_ip': obj.spec.public_ip,
        'status': obj.status,
        'memory': obj.spec.memory,
        'cpu': obj.spec.cpu,
        'flavor': obj.spec.flavor,
        'availability_zone': obj.spec.availability_zone,
        'ssh_key': obj.spec.ssh_key,
        'replica_count': obj.replica_count,
        'volumes': ';'.join(
            (x.disk_type + ':' + str(x.disk_size))
            for x in obj.spec.volume
        ) if obj.spec.volume else '',
        'conditions': ';'.join(
            (cond['type'] + '=' + cond['status'])
            for cond in obj.spec.status.conditions
        ) if obj.spec.status.conditions else ''
    }
    if obj.spec.status.capacity:
        cap_max = {
            'cpu_max': obj.spec.status.capacity.cpu,
            'mem_max': obj.spec.status.capacity.memory,
            'pods_max': obj.spec.status.capacity.pods,
        }
        data.update(cap_max)
    if obj.spec.status.allocatable:
        cap_alloc = {
            'cpu_allocatable': obj.spec.status.allocatable.cpu,
            'mem_allocatable': obj.spec.status.allocatable.memory,
            'pods_allocatable': obj.spec.status.allocatable.pods,
        }
        data.update(cap_alloc)

    return data


class ListCCEClusterNode(command.Lister):
    _description = _('List CCE Cluster Nodes')
    columns = ('ID', 'name', 'private_ip', 'public_ip',
               'availability_zone', 'status')

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

        data = client.cluster_nodes(parsed_args.cluster)

        table = (self.columns,
                 (utils.get_dict_properties(
                     _flatten_cluster_node(s), self.columns,
                 ) for s in data))
        return table


class ShowCCEClusterNode(command.ShowOne):
    _description = _('Show single Cluster node details')
    columns = ('ID', 'name', 'cluster_uuid',
               'flavor', 'cpu', 'memory', 'volumes',
               'cpu_max', 'mem_max', 'pods_max',
               'cpu_allocatable', 'mem_allocatable', 'pods_allocatable',
               'conditions',
               'private_ip', 'public_ip', 'availability_zone', 'ssh_key',
               'status', 'replica_count')

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

        obj = client.find_cluster_node(
            cluster=parsed_args.cluster,
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
            client.delete_cluster_nodes(
                cluster=parsed_args.cluster,
                node_names=parsed_args.node)


class CreateCCEClusterNode(command.Command):
    _description = _('Create CCE Cluster Node')

    columns = ('ID', 'name', 'cluster_uuid',
               'flavor', 'cpu', 'memory', 'volumes',
               'cpu_max', 'mem_max', 'pods_max',
               'cpu_allocatable', 'mem_allocatable', 'pods_allocatable',
               'conditions',
               'private_ip', 'public_ip', 'availability_zone', 'ssh_key',
               'status', 'replica_count')

    def get_parser(self, prog_name):
        parser = super(CreateCCEClusterNode, self).get_parser(prog_name)

        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            help=_('Name or ID of the cluster.')
        )
        parser.add_argument(
            '--flavor',
            metavar='<flavor>',
            required=True,
            help=_('The flavor for the server.')
        )
        parser.add_argument(
            '--label',
            metavar='<label>',
            help=_('The label attached to the node.')
        )
        parser.add_argument(
            '--volume',
            metavar='<volume>',
            action='append',
            required=True,
            help=_(
                'Disk information to attach to the instance.\n'
                'format = `DISK_TYPE`,`VOLUME_TYPE`,`SIZE`\n'
                '`DISK_TYPE` can be in [SYS, DATA] and identifies '
                'whether disk should be a system or data disk\n'
                '`VOLUME_TYPE` can be in: \n'
                '* `SATA` = Common I/O \n'
                '* `SAS` = High I/O \n'
                '* `SSD` = Ultra-High I/O \n'
                '`SIZE` is size in Gb (40 hardcoded for root, [100..32768])\n'
                '(Repeat multiple times for multiple disks).')
        )
        parser.add_argument(
            '--ssh_key',
            metavar='<ssh_key>',
            required=True,
            help=_('SSH Key used to create the node.')
        )
        parser.add_argument(
            '--assign_floating_ip',
            required=True,
            action='store_true',
            help=_('Whether to assign floating IP to the server or not.')
        )
        parser.add_argument(
            '--availability_zone',
            metavar='<availability_zone>',
            help=_('Availability zone to place server in.')
        )
        parser.add_argument(
            '--tag',
            metavar='<tag>',
            action='append',
            help=_('Tag to assign to the server in KEY=VALUE format. '
                   'Repeat for multiple values.')
        )
        parser.add_argument(
            '--replica_count',
            metavar='[1..15]',
            type=int,
            choices=range(1, 15),
            default=1,
            help=_('Number of node instances to create '
                   '(max 15 in the cluster).')
        )
        return parser

    def take_action(self, parsed_args):

        attrs = {}

        spec = {}
        spec['flavor'] = parsed_args.flavor
        spec['ssh_key'] = parsed_args.ssh_key
        spec['availability_zone'] = parsed_args.availability_zone
        if parsed_args.label:
            spec['label'] = parsed_args.label
        if parsed_args.assign_floating_ip:
            spec['assign_floating_ip'] = parsed_args.assign_floating_ip
        attrs['replica_count'] = parsed_args.replica_count
        spec['volume'] = []
        for disk in parsed_args.volume:
            disk_parts = disk.split(',')
            disk_data = {}
            if 3 == len(disk_parts):
                dt = disk_parts[0].upper()
                # Disk type: SYS->root; DATA->data
                if dt in ('SYS', 'DATA'):
                    disk_data['disk_type'] = 'data' if dt == 'DATA' else 'root'
                else:
                    msg = _('Disk Type is not in (SYS, DATA)')
                    raise argparse.ArgumentTypeError(msg)
                vt = disk_parts[1].upper()
                if vt in ('SATA', 'SAS', 'SSD'):
                    disk_data['volume_type'] = vt
                else:
                    msg = _('Volume Type is not in (SATA, SAS, SSD)')
                    raise argparse.ArgumentTypeError(msg)
                if dt == 'DATA':
                    # Size only relevant for data disk
                    if disk_parts[2].isdigit:
                        disk_data['disk_size'] = disk_parts[2]
                    else:
                        msg = _('Volume SIZE is not a digit')
                        raise argparse.ArgumentTypeError(msg)
                spec['volume'].append(disk_data)
            else:
                msg = _('Cannot parse disk information')
                raise argparse.ArgumentTypeError(msg)
        if parsed_args.tag:
            tags = []
            for tag in parsed_args.tag:
                (k, v) = tag.split('=')
                tags.append(k + '.' + v)
            spec['tags'] = tags

        attrs['spec'] = spec

        client = self.app.client_manager.cce

        obj = client.add_node(cluster=parsed_args.cluster, **attrs)

        data = utils.get_dict_properties(
            _flatten_cluster_node(obj),
            self.columns)

        return (self.columns, data)
