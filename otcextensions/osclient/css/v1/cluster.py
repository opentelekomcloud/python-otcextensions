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
from osc_lib.cli import parseractions
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
            'actions',
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
            '--version',
            metavar='<version>',
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
        parser.add_argument(
            '--backup-policy',
            metavar='period=<period>,prefix=<prefix>,keepday=<keepday>',
            required_keys=['period', 'prefix', 'keepday'],
            dest='backup_policy',
            action=parseractions.MultiKeyValueAction,
            help=_('Automatic backup creation policy.'
                   'This function is enabled by default.'
                   'The following keys are required:\n'
                   'period=<period>: Time when a snapshot is created '
                   'every day.\n'
                   'prefix=<prefix>: Prefix of the name of the snapshot '
                   'that is automatically created.\n'
                   'keepday=<keepday>: Number of days for which automatically '
                   'created snapshots are reserved. Value range: 1 to 90.'),
        )
        parser.add_argument(
            '--tag',
            action=parseractions.MultiKeyValueAction,
            metavar='key=<key>,value=<value>',
            required_keys=['key', 'value'],
            dest='tags',
            help=_('key=<key>: Tag key. The value can contain 1 to 36 '
                   'characters. Only digits, letters, hyphens (-) and '
                   'underscores (_) are allowed.\n'
                   'value=<value>: Tag value. The value can contain 0 to 43 '
                   'characters. Only digits, letters, hyphens (-) and '
                   'underscores (_) are allowed.'),
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help=('Wait for Cluster to Restart.')
        )
        parser.add_argument(
            '--timeout',
            metavar='<timeout>',
            type=int,
            default=15,
            help=_("Timeout for the wait in minutes. (Default 15 mins)"),
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
        if parsed_args.version:
            attrs['datastore'] = {
                'version': parsed_args.version,
                'type': 'elasticsearch'
            }
        backup_policy = parsed_args.backup_policy
        if backup_policy:
            if len(backup_policy) > 1:
                msg = '--backup-policy option cannot be repeated'
                raise exceptions.CommandError(msg)
            else:
                backup_policy = backup_policy[0]
                backup_policy['keepday'] = int(backup_policy['keepday'])
                attrs['backupStrategy'] = backup_policy
        if parsed_args.tags:
            attrs['tags'] = parsed_args.tags

        cluster = client.create_cluster(**attrs)
        if parsed_args.wait:
            client.wait_for_cluster(cluster.id, parsed_args.timeout)
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

        return client.find_cluster(parsed_args.cluster)


class RestartCluster(command.ShowOne):
    _description = _('Restart a CSS cluster')

    def get_parser(self, prog_name):
        parser = super(RestartCluster, self).get_parser(prog_name)
        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            help=_("ID or Name of the CSS cluster to be restart."),
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help=('Wait for Cluster to Restart.')
        )
        parser.add_argument(
            '--timeout',
            metavar='<timeout>',
            type=int,
            default=10,
            help=_("Timeout for the wait in minutes. (Default 10 mins)"),
        )
        return parser

    @translate_response
    def take_action(self, parsed_args):
        client = self.app.client_manager.css
        cluster = client.find_cluster(parsed_args.cluster)
        client.restart_cluster(cluster)
        if parsed_args.wait:
            client.wait_for_cluster(cluster.id, parsed_args.timeout)
        return client.get_cluster(cluster.id)


class ExtendCluster(command.ShowOne):
    _description = _('Scaling Out a Cluster with only Common Nodes.')

    def get_parser(self, prog_name):
        parser = super(ExtendCluster, self).get_parser(prog_name)
        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            help=_("ID or Name of the CSS cluster to be extended."),
        )
        parser.add_argument(
            '--add-nodes',
            metavar='<add_nodes>',
            type=int,
            required=True,
            help=_("Number of css nodes to be scaled out."),
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help=('Wait for Cluster Scaling Task to complete.')
        )
        parser.add_argument(
            '--timeout',
            metavar='<timeout>',
            type=int,
            default=15,
            help=_("Timeout for the wait in minutes. (Default 15 mins)"),
        )
        return parser

    @translate_response
    def take_action(self, parsed_args):
        client = self.app.client_manager.css
        cluster = client.find_cluster(parsed_args.cluster)
        client.extend_cluster(cluster, parsed_args.add_nodes)
        if parsed_args.wait:
            client.wait_for_cluster(cluster.id, parsed_args.timeout)
        return client.get_cluster(cluster.id)


class DeleteCluster(command.Command):
    _description = _('Delete CSS Cluster(s)')

    def get_parser(self, prog_name):
        parser = super(DeleteCluster, self).get_parser(prog_name)
        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            nargs='+',
            help=_("ID or Name of the CSS cluster(s) to be deleted."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.css
        result = 0
        for name_or_id in parsed_args.cluster:
            try:
                cluster = client.find_cluster(name_or_id, ignore_missing=False)
                client.delete_cluster(cluster.id)
            except Exception as e:
                result += 1
                LOG.error(_("Failed to delete cluster(s) with "
                          "ID or Name '%(cluster)s': %(e)s"),
                          {'cluster': name_or_id, 'e': e})
        if result > 0:
            total = len(parsed_args.cluster)
            msg = (_("%(result)s of %(total)s Cluster(s) failed "
                   "to delete.") % {'result': result, 'total': total})
            raise exceptions.CommandError(msg)
