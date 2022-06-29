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
            'id',
            metavar='<id>',
            nargs='+',
            help=_('UUID or name of the cluster.')
        )

        return parser

    def take_action(self, parsed_args):
        if parsed_args.cluster_id:
            client = self.app.client_manager.mrs
            for id in parsed_args.cluster_id:
                client.delete_cluster(id=id, ignore_missing=False)


class CreateCluster(command.ShowOne):
    _description = _('Create/allocate cluster')

    columns = ('id')

    def get_parser(self, prog_name):
        parser = super(CreateCluster, self).get_parser(prog_name)

        parser.add_argument(
            '--name',
            metavar='<name>',
            required=True,
            help=_('DNS Name for the host.')
        )
        parser.add_argument('--auto_placement',
                            action='store_const',
                            default='on',
                            const='on',
                            dest='auto_placement')
        parser.add_argument('--no-auto_placement',
                            action='store_const',
                            const='off',
                            dest='auto_placement')
        parser.add_argument(
            '--availability_zone',
            metavar='<az>',
            required=True,
            help=_('The AZ the host belongs to.')
        )
        parser.add_argument(
            '--host_type',
            metavar='<type>',
            help=_('DeH type.')
        )
        parser.add_argument(
            '--quantity',
            metavar='[0..]',
            type=int,
            default=1,
            help=_('Number of DeHs to allocate.')
        )

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.deh

        attrs = {}

        if parsed_args.name:
            attrs['name'] = parsed_args.name
        if parsed_args.auto_placement:
            attrs['auto_placement'] = parsed_args.auto_placement
        if parsed_args.availability_zone:
            attrs['availability_zone'] = parsed_args.availability_zone
        if parsed_args.host_type:
            attrs['host_type'] = parsed_args.host_type
        if parsed_args.quantity:
            attrs['quantity'] = parsed_args.quantity

        obj = client.create_host(
            **attrs
        )

        table = (self.columns,
                 (utils.get_item_properties(
                     s, self.columns, formatters=_formatters
                 ) for s in obj.dedicated_host_ids))
        return table


class SetHost(command.ShowOne):
    _description = _('Update a Host')

    def get_parser(self, prog_name):
        parser = super(SetHost, self).get_parser(prog_name)

        parser.add_argument(
            'host',
            metavar='<host>',
            help=_('UUID or name of the host.')
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_('DNS Name for the host.')
        )
        parser.add_argument('--auto_placement',
                            action='store_const',
                            default='on',
                            const='on',
                            dest='auto_placement')
        parser.add_argument('--no-auto_placement',
                            action='store_const',
                            const='off',
                            dest='auto_placement')

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.mrs

        attrs = {}

        if parsed_args.name:
            attrs['name'] = parsed_args.name
        if parsed_args.auto_placement:
            attrs['auto_placement'] = parsed_args.auto_placement

        host = client.find_host(parsed_args.host, ignore_missing=False)

        if host:
            obj = client.update_host(
                host=host,
                **attrs
            )

            display_columns, columns = _get_columns(obj)
            data = utils.get_item_properties(obj, columns)

            return (display_columns, data)


class ListServer(command.Lister):
    _description = _('List Servers on a DeH')
    columns = (
        'addresses', 'id', 'name', 'metadata', 'status', 'user_id'
    )

    def get_parser(self, prog_name):
        parser = super(ListServer, self).get_parser(prog_name)

        parser.add_argument(
            'host',
            metavar='<host>',
            help=_('UUID of the DeH host.')
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.deh

        host = client.find_host(parsed_args.host, ignore_missing=False)

        if host:
            data = client.servers(host=host)

            table = (self.columns,
                     (utils.get_item_properties(
                         s, self.columns, formatters=_formatters
                     ) for s in data))
            return table


class ListHostType(command.Lister):
    _description = _('List DeH host types')
    columns = (
        'host_type', 'host_type_name'
    )

    def get_parser(self, prog_name):
        parser = super(ListHostType, self).get_parser(prog_name)

        parser.add_argument(
            'az',
            metavar='<az>',
            help=_('Availability zone.')
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.deh

        data = client.host_types(parsed_args.az)

        table = (self.columns,
                 (utils.get_item_properties(
                     s, self.columns, formatters=_formatters
                 ) for s in data))
        return table
