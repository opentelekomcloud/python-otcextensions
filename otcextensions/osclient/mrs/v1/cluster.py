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

'''MRS clusters v1 action implementations'''
import logging

from osc_lib import utils
from osc_lib.command import command
from datetime import datetime
from otcextensions.i18n import _
from otcextensions.common import sdk_utils

LOG = logging.getLogger(__name__)

CLUSTER_STATES = ['starting', 'running', 'terminated',
                  'failed', 'abnormal', 'terminating',
                  'frozen', 'scaling-out', 'scaling-in']
TIMESTAMP = '%Y-%m-%dT%H:%M:%S'

_formatters = {}


def _utc_to_timestamp(obj):
    obj = float(obj)
    return datetime.utcfromtimestamp(obj).strftime(TIMESTAMP)


def _flatten_cluster(obj):
    """Flatten the structure of the cluster into a single dict
    """
    data = {
        'id': obj.id,
        'name': obj.name,
        'status': obj.status,
        'region': obj.region,
        'cluster_type': obj.cluster_type,
        'availability_zone': obj.az_id,
        'version': obj.cluster_version,
        'tags': obj.tags,
        'created_at': _utc_to_timestamp(obj.created_at),
        'updated_at': _utc_to_timestamp(obj.updated_at),
        'billing_type': obj.billing_type,
        'vpc': obj.vpc,
        'master_node_flavor': obj.master_node_size,
        'core_node_flavor': obj.core_node_size,
        'external_ip': obj.external_ip,
        'internal_ip': obj.internal_ip,
        'master_num': obj.master_num,
        'core_num': obj.core_num,
        'master_node_size': obj.master_node_size,
        'core_node_size': obj.core_node_size,
        'component_list': obj.component_list,
        'deployment_id': obj.deployment_id,
        'instance_id': obj.instance_id,
        'vnc': obj.vnc,
        'project_id': obj.project_id,
        'volume_size': obj.volume_size,
        'volume_type': obj.volume_type,
        'subnet_id': obj.subnet_id,
        'subnet_name': obj.subnet_name,
        'security_group_id': obj.security_group_id,
        'non_master_security_group_id': obj.non_master_security_group_id,
        'safe_mode': obj.safe_mode,
        'key': obj.key,
        'master_ip': obj.master_ip,
        'preffered_private_ip': obj.preffered_private_ip,
        'charging_start_time': obj.charging_start_time,
        'task_node_groups': obj.task_node_groups,
        'node_groups': obj.node_groups,
        'bootstrap_scripts': obj.bootstrap_scripts,
        'scale': obj.scale
    }

    return data


def _get_columns(item):
    column_map = {}
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


def _normalize_tags(tags):
    result = ''
    for tag in tags:
        tag_parts = tag.split('=')
        if len(tag_parts) == 2 and tag_parts[1]:
            result += f'{tag_parts[0]}*{tag_parts[1]},'
        else:
            result += f'{tag_parts[0]},'
    return result[:-1]


def _add_tags_to_cluster_obj(obj, data, columns):
    res = ''
    tags = obj.tags[0].split(',')
    for tag in tags:
        tag_parts = tag.split('=')
        res += f'key={tag_parts[0]}, value={tag_parts[1]}\n'
    data += (res,)
    columns = columns + ('tags',)
    return data, columns


class ListCluster(command.Lister):
    _description = _('List MRS clusters')
    columns = (
        'id', 'name', 'status', 'region',
        'cluster_type', 'availability_zone', 'version'
    )

    def get_parser(self, prog_name):
        parser = super(ListCluster, self).get_parser(prog_name)
        parser.add_argument(
            '--project-id',
            metavar='<project_id>',
            help=_("Specifies the project ID."),
        )
        parser.add_argument(
            '--status',
            metavar='<status>',
            type=lambda s: s.lower(),
            choices=CLUSTER_STATES,
            help=_('Cluster status filter.')
        )
        parser.add_argument(
            '--tag',
            metavar='<tag>',
            action='append',
            help=_('Tag to assign to the server in KEY=VALUE format. '
                   'Repeat for multiple values.')
        )
        parser.add_argument(
            '--limit',
            metavar='<limit>',
            type=int,
            help=_('Limit number of records to return.')
        )
        parser.add_argument(
            '--marker',
            metavar='<marker>',
            help=_('Current page number.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.mrs

        query = {}

        if parsed_args.project_id:
            query['project_id'] = parsed_args.project_id
        if parsed_args.status:
            query['status'] = parsed_args.status
        if parsed_args.limit:
            query['limit'] = parsed_args.limit
        if parsed_args.marker:
            query['marker'] = parsed_args.marker
        if parsed_args.tag:
            query['tags'] = _normalize_tags(parsed_args.tag)

        data = client.clusters(**query)

        table = (self.columns,
                 (utils.get_dict_properties(
                     _flatten_cluster(s), self.columns,
                 ) for s in data))
        return table


class ShowCluster(command.ShowOne):
    _description = _('Show single Cluster details')
    columns = (
        'ID',
        'name',
        'status',
        'region',
        'cluster_type',
        'availability_zone',
        'version',
        'created_at',
        'updated_at',
        'billing_type',
        'vpc',
        'master_node_flavor',
        'core_node_flavor',
        'external_ip',
        'internal_ip',
        'master_num',
        'core_num',
        'master_node_size',
        'core_node_size',
        'deployment_id',
        'component_list',
        'deployment_id',
        'instance_id',
        'vnc',
        'project_id',
        'volume_size',
        'volume_type',
        'subnet_id',
        'subnet_name',
        'security_group_id',
        'non_master_security_group_id',
        'safe_mode',
        'key',
        'master_ip',
        'preffered_private_ip',
        'charging_start_time',
        'task_node_groups',
        'node_groups',
        'bootstrap_scripts',
        'scale'
    )

    def get_parser(self, prog_name):
        parser = super(ShowCluster, self).get_parser(prog_name)
        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            help=_('ID or name of the MRS cluster.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.mrs

        obj = client.find_cluster(
            name_or_id=parsed_args.cluster,
            ignore_missing=False
        )

        data = utils.get_dict_properties(
            _flatten_cluster(obj), self.columns)

        if obj.tags:
            data, self.columns = _add_tags_to_cluster_obj(
                obj, data, self.columns)
        return self.columns, data


class ListClusterHost(command.Lister):
    _description = _('Show the MRS Cluster Hosts')
    columns = (
        'id', 'name', 'status', 'flavor', 'type',
        'ip', 'mem', 'cpu', 'data_volume_size'
    )

    def get_parser(self, prog_name):
        parser = super(ListClusterHost, self).get_parser(prog_name)

        parser.add_argument(
            'cluster_id',
            metavar='<cluster_id>',
            help=_('id of the cluster.')
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.mrs

        query = {}

        if parsed_args.cluster_id:
            query['cluster_id'] = parsed_args.cluster_id

        data = client.hosts(**query)

        table = (self.columns,
                 (utils.get_item_properties(
                     s, self.columns, formatters=_formatters
                 ) for s in data))
        return table


class DeleteCluster(command.Command):
    _description = _('Delete Cluster')

    def get_parser(self, prog_name):
        parser = super(DeleteCluster, self).get_parser(prog_name)

        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            nargs='+',
            help=_('ID or Name of the cluster.')
        )

        return parser

    def take_action(self, parsed_args):
        if parsed_args.cluster:
            client = self.app.client_manager.mrs
            for cluster in parsed_args.cluster:
                client.delete_cluster(cluster=cluster, ignore_missing=False)


class UpdateCluster(command.ShowOne):
    _description = _('Update MRS Cluster')
    columns = (
        'ID',
        'name',
        'status',
        'region',
        'cluster_type',
        'availability_zone',
        'version',
        'created_at',
        'updated_at',
        'billing_type',
        'vpc',
        'master_node_flavor',
        'core_node_flavor',
        'external_ip',
        'internal_ip',
        'master_num',
        'core_num',
        'master_node_size',
        'core_node_size',
        'deployment_id',
        'component_list',
        'deployment_id',
        'instance_id',
        'vnc',
        'project_id',
        'volume_size',
        'volume_type',
        'subnet_id',
        'subnet_name',
        'security_group_id',
        'non_master_security_group_id',
        'safe_mode',
        'key',
        'master_ip',
        'preffered_private_ip',
        'charging_start_time',
        'task_node_groups',
        'node_groups',
        'bootstrap_scripts',
        'scale'
    )

    def get_parser(self, prog_name):
        parser = super(UpdateCluster, self).get_parser(prog_name)

        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            help=_('ID or Name of the cluster.')
        )
        parser.add_argument(
            'scale_type',
            metavar='<scale_type>',
            required=True,
            choices=['scale_in', 'scale_out'],
            help=_('Cluster scale-in or scale-out type.')
        )
        parser.add_argument(
            'node_id',
            metavar='<node_id>',
            required=True,
            help=_('ID of the newly added or removed node.')
        )
        parser.add_argument(
            'instances',
            metavar='<instances>',
            type=int,
            required=True,
            help=_('Number of nodes to be added or removed.')
        )
        parser.add_argument(
            'node_group',
            metavar='<node_group>',
            help=_('Node group to be scaled out or in.')
        )
        parser.add_argument(
            'skip_bootstrap',
            metavar='<skip_bootstrap>',
            type=bool,
            help=_('indicates whether the bootstrap action specified '
                   'during cluster creation is performed on nodes '
                   'added during scale-out.')
        )
        parser.add_argument(
            'scale_without_start',
            metavar='<scale_without_start>',
            type=bool,
            help=_('Whether to start components on the added '
                   'nodes after cluster scale-out.')
        )
        parser.add_argument(
            'server_id',
            metavar='<server_id>',
            action='append',
            help=_('Task node to be deleted during task node scale-in.'
                   'Repeat for multiple values.')
        )
        parser.add_argument(
            'node_size',
            metavar='<node_size>',
            help=_('Instance specifications of a Task node.'
                   'For example: c2.2xlarge.linux.mrs')
        )
        parser.add_argument(
            'data_volume_type',
            metavar='<data_volume_type>',
            choices=['SATA', 'SAS', 'SSD'],
            help=_('Data disk storage type of the Task node.')
        )
        parser.add_argument(
            'data_volume_count',
            metavar='<data_volume_count>',
            type=int,
            help=_('Number of data disks of a Task node.'
                   'Value range: 1 to 10.')
        )
        parser.add_argument(
            'data_volume_size',
            metavar='<data_volume_size>',
            type=int,
            help=_('Data disk storage space of a Task node.'
                   'Value range: 100 GB to 32,000 GB.')
        )
        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.mrs

        attrs = {
            'parameters': {
                'task_node_info': {}
            },
            'scale_type': parsed_args.scale_type,
            'node_id': parsed_args.node_id,
            'instances': parsed_args.instances
        }

        # mandatory
        if parsed_args.node_group:
            attrs['parameters']['node_group'] = parsed_args.node_group
        if parsed_args.skip_bootstrap:
            attrs['parameters']['skip_bootstrap_scripts'] = parsed_args.skip_bootstrap
        if parsed_args.scale_without_start:
            attrs['parameters']['scale_without_start'] = parsed_args.scale_without_start
        if parsed_args.server_id:
            attrs['parameters']['server_ids'] = parsed_args.server_id
        if parsed_args.node_size:
            attrs['parameters']['task_node_info']['node_size'] = parsed_args.node_size
            if parsed_args.data_volume_type:
                attrs['parameters']['task_node_info']['data_volume_type'] = parsed_args.data_volume_type
            if parsed_args.data_volume_count:
                attrs['parameters']['task_node_info']['data_volume_count'] = parsed_args.data_volume_count
            if parsed_args.data_volume_size:
                attrs['parameters']['task_node_info']['data_volume_size'] = parsed_args.data_volume_size

        cluster = client.find_cluster(
            name_or_id=parsed_args.cluster,
            ignore_missing=False
        )

        if attrs:
            obj = client.update_cluster(cluster=cluster.id, **attrs)
        else:
            obj = cluster

        data = utils.get_dict_properties(
            _flatten_cluster(obj), self.columns)

        return self.columns, data
