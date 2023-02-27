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

from osc_lib.cli import parseractions
from osc_lib import utils
from osc_lib.cli import format_columns
from osc_lib.command import command
from osc_lib import exceptions
from otcextensions.common import sdk_utils

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


CSS_ENGINE_VERSIONS = ('7.6.2', '7.9.3', '7.10.2')

DISK_TYPE_CHOICES = ['common', 'high', 'ultrahigh']


_formatters = {
    'nodes': format_columns.ListDictColumn,
    'elb_whitelist': format_columns.DictColumn,
    'datastore': format_columns.DictColumn,
    'tags': format_columns.ListDictColumn,
    'action_progress': format_columns.DictColumn,
    'actions': format_columns.ListColumn,
}


def set_attributes_for_print(obj):
    for data in obj:
        setattr(data, 'type', data.datastore['type'])
        setattr(data, 'version', data.datastore['version'])
        yield data


def _get_columns(item):
    column_map = {}
    hidden = [
        'location',
    ]
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map,
                                                           hidden)


def translate_response(func):
    def new(self, *args, **kwargs):
        obj = func(self, *args, **kwargs)
        setattr(obj, 'num_nodes', len(obj.nodes))
        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)
        return (display_columns, data)

    new.__name__ = func.__name__
    new.__doc__ = func.__doc__
    return new


class CreateCluster(command.ShowOne):
    _description = _("Create a new CSS cluster instance.")

    def get_parser(self, prog_name):
        parser = super(CreateCluster, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help=_('Cluster Name.')
        )
        parser.add_argument(
            '--datastore-type',
            metavar='<datastore_type>',
            default='elasticsearch',
            help=_('Cluster type. The default value is elasticsearch.'),
        )
        parser.add_argument(
            '--datastore-version',
            metavar='<datastore_version>',
            default='7.10.2',
            help=_('CSS Cluster Engine Versions. Supported ElasticSearch '
                   'Versions: {' + ', '.join(CSS_ENGINE_VERSIONS) + '} '
                   '(default: 7.10.2).'),
        )
        parser.add_argument(
            '--availability-zone',
            metavar='<availability_zone>',
            help=_('Separate multiple AZs with commas (,), for example, '
                   'az1,az2. AZs must be unique. The number of nodes must be '
                   'greater than or equal to the number of AZs.')
        )
        parser.add_argument(
            '--flavor',
            metavar='<flavor>',
            required=True,
            help=_('Cluster Instance flavor.')
        )
        parser.add_argument(
            '--num-nodes',
            metavar='<num_nodes>',
            type=int,
            default=1,
            help=_('Number of clusters nodes. The value range is 1 to 32. '
                   '(default value: 1)')
        )
        disk_group = parser.add_argument_group('Volume Parameters')
        disk_group.add_argument(
            '--volume-size',
            metavar='<volume_size>',
            default=40,
            type=int,
            help=_('Size of the instance disk volume in GB. '
                   '(default value: 40)')
        )
        disk_group.add_argument(
            '--volume-type',
            metavar='{' + ','.join(DISK_TYPE_CHOICES) + '}',
            type=lambda s: s.upper(),
            default='COMMON',
            dest='volume_type',
            choices=[s.upper() for s in DISK_TYPE_CHOICES],
            help=_('Volume type. Supported types: COMMON, HIGH, ULTRAHIGH. '
                   '(default value: COMMON)')
        )
        network_group = parser.add_argument_group('Network Parameters')
        network_group.add_argument(
            '--router-id',
            metavar='<router_id>',
            required=True,
            help=_('Router ID.')
        )
        network_group.add_argument(
            '--network-id',
            metavar='<network_id>',
            required=True,
            help=_('Network ID.')
        )
        network_group.add_argument(
            '--security-group-id',
            metavar='<security_group_id>',
            required=True,
            help=_('Security group ID.')
        )
        parser.add_argument(
            '--https-enable',
            action='store_true',
            help=_('Whether communication is encrypted on the cluster.')
        )
        parser.add_argument(
            '--cmk-id',
            metavar='<cmk_id>',
            help=_('Encryption Key Id. '
                   'The system encryption is used for cluster encryption.'
                   'The Default Master Keys cannot be used to create grants.')
        )
        parser.add_argument(
            '--admin-pwd',
            metavar='<admin_pwd>',
            help=_('Password of the cluster user admin in security mode.')
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
            default=1200,
            help=_('Timeout for the wait in seconds (default 1200 seconds).'),
        )
        return parser

    @translate_response
    def take_action(self, parsed_args):

        client = self.app.client_manager.css

        attrs = {
            'name': parsed_args.name,
            'instanceNum': parsed_args.num_nodes,
            'datastore': {
                'version': parsed_args.datastore_version,
                'type': parsed_args.datastore_type
            },
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

        availability_zone = parsed_args.availability_zone
        if availability_zone:
            attrs['instance']['availability_zone'] = availability_zone

        if parsed_args.https_enable:
            attrs['httpsEnable'] = 'true'
            attrs['authorityEnable'] = True
            admin_password = parsed_args.admin_pwd
            if admin_password:
                attrs['adminPwd'] = admin_password
            else:
                raise exceptions.CommandError(
                    'Following arguments is required: --admin-pwd '
                    '(admin_pwd is mandatary in https_enable mode.)'
                )

        if parsed_args.cmk_id:
            attrs['diskEncryption'] = {
                'systemEncrypted': 1,
                'systemCmkid': parsed_args.cmk_id
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


class ListClusters(command.Lister):
    _description = _('List CSS Clusters.')
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

        return (
            self.columns, (
                utils.get_item_properties(
                    s, self.columns, formatters=_formatters
                )
                for s in set_attributes_for_print(data)
            )
        )


class ListClusterNodes(command.Lister):
    _description = _('List CSS Cluster Nodes.')
    columns = (
        'ID',
        'Name',
        'Private IP',
        'Node Type',
        'Volume',
        'Availability Zone',
        'Status',

    )

    def get_parser(self, prog_name):
        parser = super(ListClusterNodes, self).get_parser(prog_name)
        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            help=_('Cluster name or ID.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.css

        cluster = client.find_cluster(parsed_args.cluster)

        _formatters = {
            'Volume': format_columns.DictColumn
        }
        return (
            self.columns, (
                utils.get_item_properties(
                    node, self.columns, formatters=_formatters
                )
                for node in cluster.nodes
            )
        )


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


class RestartCluster(command.Command):
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
            default=300,
            help=_("Timeout for the wait in seconds (default 300 seconds)."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.css
        cluster = client.find_cluster(parsed_args.cluster)
        client.restart_cluster(cluster)
        if parsed_args.wait:
            client.wait_for_cluster(cluster.id, parsed_args.timeout)


class ExtendClusterNodes(command.Command):
    _description = _('Scaling Out a Cluster with Special Nodes.')

    def get_parser(self, prog_name):
        parser = super(ExtendClusterNodes, self).get_parser(prog_name)
        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            help=_("ID or Name of the CSS cluster to be extended."),
        )
        parser.add_argument(
            '--extend',
            metavar='type=<type>,nodesize=<nodesize>,disksize=<disksize>',
            required_keys=['type', 'nodesize', 'disksize'],
            required=True,
            action=parseractions.MultiKeyValueAction,
            help=_('Extend Cluster Nodes.'
                   'Type: ess, ess-cold, ess-master, and ess-client.\n'
                   'For type: ess-master and ess-client disksize cannot '
                   'be extended.\n'
                   'Examples:\n'
                   '--extend type=ess,disksize=60,nodesize=2 '
                   ' --extend type=ess-master,disksize=0,nodesize=2')
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
            default=1200,
            help=_('Timeout for the wait in seconds (default 1200 seconds).'),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.css
        cluster = client.find_cluster(parsed_args.cluster)
        attrs = {'grow': parsed_args.extend}
        client.extend_cluster_nodes(cluster, **attrs)
        if parsed_args.wait:
            client.wait_for_cluster(cluster.id, parsed_args.timeout)


class ExtendCluster(command.Command):
    _description = _('Scaling Out a Cluster\'s with only Common Nodes.')

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
            default=1200,
            help=_("Timeout for the wait in seconds (default 1200 seconds)."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.css
        cluster = client.find_cluster(parsed_args.cluster)
        client.extend_cluster(cluster, parsed_args.add_nodes)
        if parsed_args.wait:
            client.wait_for_cluster(cluster.id, parsed_args.timeout)


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
