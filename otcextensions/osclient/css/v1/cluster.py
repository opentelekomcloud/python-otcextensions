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
#
'''CSS ELK cluster v1 action implementations'''
import logging

from osc_lib import utils
from osc_lib.command import command
from osc_lib import exceptions
from otcextensions.common import sdk_utils
from collections import defaultdict

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _get_columns(item):
    column_map = {
    }
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


def set_attributes_for_print(obj):
    for data in obj:
        setattr(data, 'version', data.datastore.version)
        setattr(data, 'type', data.datastore.type)
        yield data


def translate_response(func):
    def new(self, *args, **kwargs):
        obj = func(self, *args, **kwargs)
        setattr(obj, 'version', obj.datastore.version)
        setattr(obj, 'type', obj.datastore.type)
        node_count = defaultdict(int)
        for node in obj.nodes:
            node_count[node['type']] += 1
        setattr(obj, 'node_count', dict(node_count))

        columns = (
            'id',
            'name',
            'type',
            'version',
            'endpoint',
            'disk_encryption',
            'cmk_id',
            'error',
            'instance',
            'instance_count',
            'node_count',
            'is_disk_encrypted',
            'is_https_enabled',
            'progress',
            'router_id',
            'subnet_id',
            'security_group_id',
            'status',
            'created_at',
            'updated_at'
        )
        data = utils.get_item_properties(obj, columns)
        return (columns, data)
    new.__name__ = func.__name__
    new.__doc__ = func.__doc__
    return new


class ListClusters(command.Lister):
    _description = _('List CSS Cluster')
    columns = (
        'ID',
        'Name',
        'Type',
        'Version',
        'Status',
        'Created At'
    )

    def get_parser(self, prog_name):
        parser = super(ListClusters, self).get_parser(prog_name)

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.css
        data = client.clusters()

        data = set_attributes_for_print(data)
        return (self.columns, (utils.get_item_properties(s, self.columns)
                               for s in data))


class CreateCluster(command.ShowOne):
    _description = _("Create a new CSS cluster instance.")

    def get_parser(self, prog_name):
        parser = super(CreateCluster, self).get_parser(prog_name)
        parser.add_argument(
            '--name',
            metavar='<name>',
            required=True,
            help=_("Cluster Name.")
        )
        parser.add_argument(
            '--elasticsearch-version',
            metavar='<elasticsearch_version>',
            help=_('Engine version. The value can be 6.2.3, 7.1.1 or 7.6.2.')
        )
        parser.add_argument(
            '--flavor',
            metavar='<flavor>',
            dest='flavor',
            help=_("flavor_ref spec_code")
        )

        parser.add_argument(
            '--instanceNum',
            metavar='<instanceNum>',
            type=int,
            required=True,
            help=_('Number of clusters. The value range is 1 to 32.')
        )

        parser.add_argument(
            '--volume-type',
            metavar='<volume_type>',
            default='COMMON',
            help=_('The Volume Type of the Node.')
        )

        parser.add_argument(
            '--volume-size',
            metavar='<volume_size>',
            type=int,
            help=_('The Volume Size of the Node.\n'
                   'Deafult value is set respective to flavor')
        )
        parser.add_argument(
            '--https-enable',
            metavar='<https_enable>',
            help=_('The https is enabled or not.')
        )
        parser.add_argument(
            '--system-cmk-id',
            metavar='<system_cmk_id>',
            help=_('The system encryption is used for cluster encryption.')
        )

        parser.add_argument(
            '--adminPwd',
            dest='adminPwd',
            help=_('Password of the cluster user admin in security mode.')
        )

        parser.add_argument(
            '--router-id',
            metavar='<router_id>',
            required=True,
            help=_('Router ID.')
        )
        parser.add_argument(
            '--network-id',
            metavar='<network_id>',
            required=True,
            help=_('Network ID.')
        )
        parser.add_argument(
            '--security-group-id',
            metavar='<security_group_id>',
            required=True,
            help=_('Security group ID.')
        )

        return parser

    @translate_response
    def take_action(self, parsed_args):

        client = self.app.client_manager.css

        attrs = {
            'name': parsed_args.name,
            'instanceNum': parsed_args.instanceNum,
            'instance': {
                'flavorRef': parsed_args.flavor,
                'volume': {
                    'volume_type': parsed_args.volume_type,
                    'size': parsed_args.volume_size
                },
                'nics': {
                    'vpcId': parsed_args.router_id,
                    'netId': parsed_args.network_id,
                    'securityGroupId': parsed_args.security_group_id
                }
            }
        }
        if parsed_args.https_enable:
            attrs['httpsEnable'] = parsed_args.https_enable
        if parsed_args.system_cmk_id:
            attrs['diskEncryption'] = {
                'systemEncrypted': 1,
                'systemCmkid': parsed_args.system_cmk_id
            }
        if parsed_args.adminPwd:
            attrs['authorityEnable'] = True
            attrs['adminPwd'] = parsed_args.adminPwd
        if parsed_args.elasticsearch_version:
            attrs['datastore'] = {
                'version': parsed_args.elasticsearch_version,
                'type': 'elasticsearch'
            }
        cluster = client.create_cluster(**attrs)
        return client.get_cluster(cluster.id)


class ShowCluster(command.ShowOne):
    _description = _('Show details of a CSS cluster')

    def get_parser(self, prog_name):
        parser = super(ShowCluster, self).get_parser(prog_name)
        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            help=_('Cluster name or ID.')
        )
        return parser

    @translate_response
    def take_action(self, parsed_args):
        client = self.app.client_manager.css

        return client.get_cluster(parsed_args.cluster)


class RestartCluster(command.ShowOne):
    _description = _('Restart a CSS cluster')

    def get_parser(self, prog_name):
        parser = super(RestartCluster, self).get_parser(prog_name)
        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            help=_("ID of the CSS cluster to be restart."),
        )
        return parser

    @translate_response
    def take_action(self, parsed_args):
        client = self.app.client_manager.css

        client.restart_cluster(parsed_args.cluster,)
        return client.get_cluster(parsed_args.cluster)


class ExtendCluster(command.ShowOne):
    _description = _('Scaling Out a Cluster with only Common Nodes.')

    def get_parser(self, prog_name):
        parser = super(ExtendCluster, self).get_parser(prog_name)
        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            help=_("ID of the CSS cluster to be extended."),
        )
        parser.add_argument(
            'modifySize',
            metavar='<modifySize>',
            type=int,
            help=_("Number of instances to be scaled out."),
        )
        return parser

    @translate_response
    def take_action(self, parsed_args):
        client = self.app.client_manager.css

        client.extend_cluster(
            parsed_args.cluster,
            parsed_args.modifySize
        )
        return client.get_cluster(parsed_args.cluster)


class DeleteCluster(command.Command):
    _description = _('Delete CSS Cluster(s)')

    def get_parser(self, prog_name):
        parser = super(DeleteCluster, self).get_parser(prog_name)
        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            nargs='+',
            help=_("ID(s) of the CSS cluster(s) to be deleted."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.css
        result = 0
        for clusterId in parsed_args.cluster:
            try:
                client.delete_cluster(clusterId, ignore_missing=False)
            except Exception as e:
                result += 1
                LOG.error(_("Failed to delete cluster(s) with "
                          "ID '%(clusterId)s': %(e)s"),
                          {'clusterId': clusterId, 'e': e})
        if result > 0:
            total = len(parsed_args.cluster)
            msg = (_("%(result)s of %(total)s Cluster(s) failed "
                   "to delete.") % {'result': result, 'total': total})
            raise exceptions.CommandError(msg)
