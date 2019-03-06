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
'''MRS clusters v1 action implementations'''
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.i18n import _
from otcextensions.common import sdk_utils

LOG = logging.getLogger(__name__)

CLUSTER_STATES = ['available', 'fault', 'released']


_formatters = {
}


def _get_columns(item):
    column_map = {
    }
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


class ListCluster(command.Lister):
    _description = _('List MRS clusters')
    columns = (
        'id', 'name', 'status', 'flavor',
        'cluster_type', 'availability_zone', 'version'
    )

    def get_parser(self, prog_name):
        parser = super(ListCluster, self).get_parser(prog_name)
        parser.add_argument(
            '--id',
            metavar='<id>',
            help=_('Cluster id.')
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_('Cluster name.')
        )
        parser.add_argument(
            '--cluster_type',
            metavar='<cluster_type>',
            help=_('Cluster type.')
        )
        parser.add_argument(
            '--version',
            metavar='<version>',
            help=_('Cluster version.')
        )
        parser.add_argument(
            '--flavor',
            metavar='<flavor>',
            help=_('Flavor ID.')
        )
        parser.add_argument(
            '--status',
            metavar='{' + ','.join(CLUSTER_STATES) + '}',
            type=lambda s: s.lower(),
            choices=CLUSTER_STATES,
            help=_('Cluster status filter.')
        )
        parser.add_argument(
            '--availability_zone',
            metavar='<availability_zone>',
            help=_('Availability zone.')
        )
        parser.add_argument(
            '--limit',
            metavar='<limit>',
            type=int,
            help=_('Number of entries to display.')
        )
        parser.add_argument(
            '--marker',
            metavar='<marker>',
            help=_('ID of the last record on the previous page.')
        )
        parser.add_argument(
            '--changes_since',
            metavar='<changes_since>',
            help=_('Filters the response by a date and time stamp when the '
                   'MRS last changed status. Format: '
                   'CCYY-MM-DDThh:mm:ss+hh:mm')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.mrs

        query = {}

        if parsed_args.id:
            query['id'] = parsed_args.id
        if parsed_args.name:
            query['name'] = parsed_args.name
        if parsed_args.flavor:
            query['flavor'] = parsed_args.flavor
        if parsed_args.status:
            query['status'] = parsed_args.status
        if parsed_args.cluster_type:
            query['cluster_type'] = parsed_args.cluster_type
        if parsed_args.version:
            query['version'] = parsed_args.version
        if parsed_args.availability_zone:
            query['availability_zone'] = parsed_args.availability_zone
        if parsed_args.limit:
            query['limit'] = parsed_args.limit
        if parsed_args.marker:
            query['marker'] = parsed_args.marker
        if parsed_args.changes_since:
            query['changes_since'] = parsed_args.changes_since

        data = client.clusters(**query)

        table = (self.columns,
                 (utils.get_item_properties(
                     s, self.columns, formatters=_formatters
                 ) for s in data))
        return table


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
