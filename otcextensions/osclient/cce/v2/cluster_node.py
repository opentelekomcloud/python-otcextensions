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
'''CCE Cluster Nodes v2 action implementations'''
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
                client.delete_cluster_node(
                    cluster=cluster.id,
                    node=node,
                    ignore_missing=False)


class CreateCCEClusterNode(command.Command):
    _description = _('Create CCE Cluster Node')

    columns = ('ID', 'name', 'flavor',
               'private_ip', 'public_ip', 'availability_zone', 'ssh_key',
               'status')

    def get_parser(self, prog_name):
        parser = super(CreateCCEClusterNode, self).get_parser(prog_name)

        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            help=_('Name of the cluster.')
        )
        parser.add_argument(
            '--flavor',
            metavar='<flavor>',
            required=True,
            help=_('The flavor for the server.')
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
            '--root_volume',
            metavar='<root_volume>',
            required=True,
            help=_(
                'Root disk information to attach to the instance.\n'
                'format = `VOLUME_TYPE`,`SIZE`\n'
                '`VOLUME_TYPE` can be in: \n'
                '* `SATA` = Common I/O \n'
                '* `SAS` = High I/O \n'
                '* `SSD` = Ultra-High I/O \n'
                '`SIZE` is size in Gb.')
        )
        parser.add_argument(
            '--ssh_key',
            metavar='<ssh_key>',
            required=True,
            help=_('SSH Key used to create the node.')
        )
        parser.add_argument(
            '--availability_zone',
            metavar='<availability_zone>',
            help=_('Availability zone to place server in.')
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

    def parse_disk(self, disk):
        disk_parts = disk.split(',')
        disk_data = {}
        if 2 == len(disk_parts):
            vt = disk_parts[0].upper()
            if vt in ('SATA', 'SAS', 'SSD'):
                disk_data['volumetype'] = vt
            else:
                msg = _('Volume Type is not in (SATA, SAS, SSD)')
                raise argparse.ArgumentTypeError(msg)
            # Size only relevant for data disk
            if disk_parts[1].isdigit:
                disk_data['size'] = disk_parts[1]
            else:
                msg = _('Volume SIZE is not a digit')
                raise argparse.ArgumentTypeError(msg)
        else:
            msg = _('Cannot parse disk information')
            raise argparse.ArgumentTypeError(msg)
        return disk_data

    def take_action(self, parsed_args):

        attrs = {'metadata': {}}

        attrs['metadata']['name'] = parsed_args.cluster

        spec = {}
        spec['flavor'] = parsed_args.flavor
        spec['login'] = {'sshKey': parsed_args.ssh_key}
        spec['az'] = parsed_args.availability_zone
        spec['count'] = parsed_args.count
        spec['rootVolume'] = self.parse_disk(parsed_args.root_volume)
        spec['dataVolumes'] = [self.parse_disk(parsed_args.volume)]

        if parsed_args.annotation:
            annotations = {}
            for annotation in parsed_args.annotation:
                (k, v) = annotation.split('=')
                annotations[k] = v
            attrs['metadata']['annotations'] = annotations
        if parsed_args.label:
            labels = {}
            for label in parsed_args.label:
                (k, v) = label.split('=')
                labels[k] = v
            attrs['metadata']['labels'] = labels

        attrs['spec'] = spec

        client = self.app.client_manager.cce

        cluster = client.find_cluster(parsed_args.cluster,
                                      ignore_missing=False)

        obj = client.create_cluster_node(cluster=cluster.id, **attrs)

        data = utils.get_dict_properties(
            _flatten_cluster_node(obj),
            self.columns)

        return (self.columns, data)
