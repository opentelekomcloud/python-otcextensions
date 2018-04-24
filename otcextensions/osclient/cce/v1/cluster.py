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
'''CCE Cluster v1 action implementations'''
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _flatten_cluster(obj):
    data = {
        'id': obj.id,
        'name': obj.name,
        # 'status': obj.status['status'],
        'cpu': obj.spec.cpu,
        'memory': obj.spec.memory,
        'endpoint': obj.spec.endpoint,
        'availability_zone': obj.spec.availability_zone,
        'vpc': obj.spec.vpc,
        # 'nodes': len(obj.spec.host_list.spec.host_list)
    }
    if obj.status:
        data['status'] = obj.status['status']
    try:
        data['nodes'] = len(obj.spec.host_list.spec.host_list)
    except AttributeError:
        pass

    return data


class ListCCECluster(command.Lister):
    _description = _('List CCE Clusters')
    columns = ('ID', 'name', 'cpu', 'memory', 'endpoint')

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
    columns = ('ID', 'name', 'status', 'cpu', 'memory', 'endpoint',
               'availability_zone',
               'vpc', 'nodes')

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

        obj = client.get_cluster(parsed_args.cluster)

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
            help=_('ID of the cluster')
        )
        return parser

    def take_action(self, parsed_args):

        if parsed_args.cluster:
            client = self.app.client_manager.cce
            client.delete_cluster(parsed_args.cluster)
