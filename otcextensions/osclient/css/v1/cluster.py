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
"""CSS ELK cluster v1 action implementations"""

import logging

from osc_lib import exceptions
from osc_lib import utils
from osc_lib.cli import format_columns
from osc_lib.cli import parseractions
from osc_lib.command import command

from otcextensions.common import cli_utils
from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


DISK_TYPE_CHOICES = ['high', 'ultrahigh']
NODE_TYPE_CHOICES = ['ess', 'ess-cold', 'ess-client', 'ess-master']
VOLUME_TYPE_CHOICES = ['ULTRAHIGH', 'HIGH']
UPGRADE_TYPE_CHOICES = ['same', 'cross', 'cross-engine']


_formatters = {
    'nodes': cli_utils.YamlFormat,
    'elb_whitelist': cli_utils.YamlFormat,
    'datastore': cli_utils.YamlFormat,
    'tags': cli_utils.YamlFormat,
    'action_progress': format_columns.DictColumn,
    'actions': format_columns.ListColumn,
    'endpoints': cli_utils.YamlFormat,
}


def set_attributes_for_print(obj):
    for data in obj:
        if getattr(data, 'datastore'):
            setattr(data, 'type', data.datastore['type'])
            setattr(data, 'version', data.datastore['version'])
        yield data


def _get_columns(item):
    column_map = {}
    hidden = [
        'location',
    ]
    return sdk_utils.get_osc_show_columns_for_sdk_resource(
        item, column_map, hidden
    )


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
    _description = _('Create a new CSS cluster instance.')

    def get_parser(self, prog_name):
        parser = super(CreateCluster, self).get_parser(prog_name)
        parser.add_argument('name', metavar='<name>', help=_('Cluster Name.'))
        parser.add_argument(
            '--datastore-type',
            metavar='{elasticsearch, opensearch}',
            choices=['elasticsearch', 'opensearch'],
            type=lambda s: s.lower(),
            default='elasticsearch',
            help=_(
                'Cluster type. Values:\n'
                '- elasticsearch\n'
                '- opensearch\n'
                'The default value is elasticsearch.'
            ),
        )
        parser.add_argument(
            '--datastore-version',
            metavar='<datastore_version>',
            default='7.10.2',
            help=_(
                'CSS Cluster Engine Versions.\n'
                'If datastore_type is `elasticsearch` supported versions: '
                '(7.6.2, 7.9.3, 7.10.2)\n'
                'If datastore_type is `opensearch` supported versions: '
                '(1.3.6, 2.11.0)\n'
                '(default datastore_version: 7.10.2).'
            ),
        )
        parser.add_argument(
            '--availability-zone',
            metavar='<availability_zone>',
            help=_(
                'Separate multiple AZs with commas (,), for example, '
                'az1,az2. AZs must be unique. The number of nodes must be '
                'greater than or equal to the number of AZs.'
            ),
        )
        parser.add_argument(
            '--flavor',
            metavar='<flavor>',
            required=True,
            help=_('Cluster Instance flavor.'),
        )
        parser.add_argument(
            '--num-nodes',
            metavar='<num_nodes>',
            type=int,
            default=1,
            help=_(
                'Number of clusters nodes. The value range is 1 to 32. '
                '(default value: 1)'
            ),
        )
        disk_group = parser.add_argument_group('Volume Parameters')
        disk_group.add_argument(
            '--volume-size',
            metavar='<volume_size>',
            default=40,
            type=int,
            help=_(
                'Size of the instance disk volume in GB. '
                '(default value: 40)'
            ),
        )
        disk_group.add_argument(
            '--volume-type',
            metavar='{' + ','.join(DISK_TYPE_CHOICES) + '}',
            type=lambda s: s.upper(),
            default='HIGH',
            dest='volume_type',
            choices=[s.upper() for s in DISK_TYPE_CHOICES],
            help=_(
                'Volume type. Supported types: HIGH, ULTRAHIGH. '
                '(default value: HIGH)'
            ),
        )
        network_group = parser.add_argument_group('Network Parameters')
        network_group.add_argument(
            '--router-id',
            metavar='<router_id>',
            required=True,
            help=_('Router ID.'),
        )
        network_group.add_argument(
            '--network-id',
            metavar='<network_id>',
            required=True,
            help=_('Network ID.'),
        )
        network_group.add_argument(
            '--security-group-id',
            metavar='<security_group_id>',
            required=True,
            help=_('Security group ID.'),
        )
        parser.add_argument(
            '--https-enable',
            action='store_true',
            help=_('Whether communication is encrypted on the cluster.'),
        )
        parser.add_argument(
            '--cmk-id',
            metavar='<cmk_id>',
            help=_(
                'Encryption Key Id. '
                'The system encryption is used or cluster encryption.'
                'The Default Master Keys cannot be used to create grants.'
            ),
        )
        parser.add_argument(
            '--admin-pwd',
            metavar='<admin_pwd>',
            help=_('Password of the cluster user admin in security mode.'),
        )
        parser.add_argument(
            '--backup-policy',
            metavar='period=<period>,prefix=<prefix>,keepday=<keepday>',
            required_keys=['period', 'prefix', 'keepday'],
            optional_keys=['bucket', 'agency', 'basepath'],
            dest='backup_policy',
            action=parseractions.MultiKeyValueAction,
            help=_(
                'Automatic backup creation policy. '
                'This function is enabled by default.\n'
                'The following keys are required:\n'
                'period=<period>: Time when a snapshot is created '
                'every day.\n'
                'prefix=<prefix>: Prefix of the name of the snapshot '
                'that is automatically created.\n'
                'keepday=<keepday>: Number of days for which automatically '
                'created snapshots are reserved. Value range: 1 to 90.\n'
                'Optional Keys:\n'
                'bucket=<bucket>: OBS bucket used for storing backup.\n'
                'basepath=<basepath>: Storage path of the snapshot in '
                'the OBS bucket.\n'
                'agency=<agency>: IAM agency used to access OBS.'
            ),
        )
        parser.add_argument(
            '--tag',
            action=parseractions.MultiKeyValueAction,
            metavar='key=<key>,value=<value>',
            required_keys=['key', 'value'],
            dest='tags',
            help=_(
                'key=<key>: Tag key. The value can contain 1 to 36 '
                'characters. Only digits, letters, hyphens (-) and '
                'underscores (_) are allowed.\n'
                'value=<value>: Tag value. The value can contain 0 to 43 '
                'characters. Only digits, letters, hyphens (-) and '
                'underscores (_) are allowed.'
            ),
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help=('Wait for Cluster.'),
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
                'type': parsed_args.datastore_type,
            },
            'instance': {
                'flavorRef': parsed_args.flavor,
                'volume': {
                    'volume_type': parsed_args.volume_type,
                    'size': parsed_args.volume_size,
                },
                'nics': {
                    'vpcId': parsed_args.router_id,
                    'netId': parsed_args.network_id,
                    'securityGroupId': parsed_args.security_group_id,
                },
            },
        }

        availability_zone = parsed_args.availability_zone
        if availability_zone:
            attrs['instance']['availability_zone'] = availability_zone

        if parsed_args.https_enable:
            attrs['httpsEnable'] = True
            attrs['authorityEnable'] = True
            admin_password = parsed_args.admin_pwd
            if admin_password:
                attrs['adminPwd'] = admin_password
            else:
                raise exceptions.CommandError(
                    'Following arguments is required: --admin-pwd '
                    '(admin_pwd is mandatary in https_enable mode.)'
                )
        elif parsed_args.admin_pwd and not parsed_args.https_enable:
            attrs['authorityEnable'] = True
            attrs['adminPwd'] = parsed_args.admin_pwd

        if parsed_args.cmk_id:
            attrs['diskEncryption'] = {
                'systemEncrypted': 1,
                'systemCmkid': parsed_args.cmk_id,
            }
        backup_policy = parsed_args.backup_policy
        if backup_policy:
            if len(backup_policy) > 1:
                msg = '--backup-policy option cannot be repeated'
                raise exceptions.CommandError(msg)
            else:
                backup_policy = backup_policy[0]
                backup_policy['keepday'] = int(backup_policy['keepday'])
                if backup_policy.get('basepath'):
                    backup_policy['basePath'] = backup_policy['basepath']
                    del backup_policy['basepath']
                attrs['backupStrategy'] = backup_policy
        if parsed_args.tags:
            attrs['tags'] = parsed_args.tags

        cluster = client.create_cluster(**attrs)
        if parsed_args.wait:
            client.wait_for_cluster(
                cluster.id, parsed_args.timeout, print_status=True
            )
        return client.get_cluster(cluster.id)


class ListClusters(command.Lister):
    _description = _('List CSS Clusters.')
    columns = (
        'ID',
        'Name',
        'Type',
        'Version',
        'Status',
        'Created At',
    )

    def get_parser(self, prog_name):
        parser = super(ListClusters, self).get_parser(prog_name)

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.css
        data = client.clusters()

        return (
            self.columns,
            (
                utils.get_item_properties(
                    s, self.columns, formatters=_formatters
                )
                for s in set_attributes_for_print(data)
            ),
        )


class ListClusterNodes(command.Lister):
    _description = _('List CSS Cluster Nodes.')
    columns = (
        'ID',
        'Name',
        'IP',
        'Type',
        'Volume',
        'Availability Zone',
        'Status',
    )

    def get_parser(self, prog_name):
        parser = super(ListClusterNodes, self).get_parser(prog_name)
        parser.add_argument(
            'cluster', metavar='<cluster>', help=_('Cluster name or ID.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.css

        cluster = client.find_cluster(
            parsed_args.cluster, ignore_missing=False
        )

        _formatters = {'Volume': cli_utils.YamlFormat}
        return (
            self.columns,
            (
                utils.get_item_properties(
                    node, self.columns, formatters=_formatters
                )
                for node in cluster.nodes
            ),
        )


class ShowCluster(command.ShowOne):
    _description = _('Show details of a CSS cluster')

    def get_parser(self, prog_name):
        parser = super(ShowCluster, self).get_parser(prog_name)
        parser.add_argument(
            'cluster', metavar='<cluster>', help=_('Cluster name or ID.')
        )
        return parser

    @translate_response
    def take_action(self, parsed_args):
        client = self.app.client_manager.css

        cluster = client.find_cluster(
            parsed_args.cluster, ignore_missing=False
        )

        if not getattr(cluster, 'nodes'):
            cluster = client.get_cluster(cluster)

        return cluster


class RestartCluster(command.Command):
    _description = _('Restart a CSS cluster')

    def get_parser(self, prog_name):
        parser = super(RestartCluster, self).get_parser(prog_name)
        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            help=_('ID or Name of the CSS cluster to be restart.'),
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help=('Wait for Cluster to Restart.'),
        )
        parser.add_argument(
            '--timeout',
            metavar='<timeout>',
            type=int,
            default=300,
            help=_('Timeout for the wait in seconds (default 300 seconds).'),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.css
        cluster = client.find_cluster(
            parsed_args.cluster, ignore_missing=False
        )
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
            help=_('ID or Name of the CSS cluster to be extended.'),
        )
        parser.add_argument(
            '--extend',
            metavar='type=<type>,nodesize=<nodesize>,disksize=<disksize>',
            required_keys=['type', 'nodesize', 'disksize'],
            required=True,
            action=parseractions.MultiKeyValueAction,
            help=_(
                'Extend Cluster Nodes.'
                'Type: ess, ess-cold, ess-master, and ess-client.\n'
                'For type: ess-master and ess-client disksize cannot '
                'be extended.\n'
                'Examples:\n'
                '--extend type=ess,disksize=60,nodesize=2 '
                ' --extend type=ess-master,disksize=0,nodesize=2'
            ),
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help=('Wait for Cluster Scaling Task to complete.'),
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
        cluster = client.find_cluster(
            parsed_args.cluster, ignore_missing=False
        )
        attrs = {'grow': parsed_args.extend}
        client.extend_cluster_nodes(cluster, **attrs)
        if parsed_args.wait:
            client.wait_for_cluster(cluster.id, parsed_args.timeout)


class ExtendCluster(command.Command):
    _description = _("Scaling Out a Cluster's with only Common Nodes.")

    def get_parser(self, prog_name):
        parser = super(ExtendCluster, self).get_parser(prog_name)
        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            help=_('ID or Name of the CSS cluster to be extended.'),
        )
        parser.add_argument(
            '--add-nodes',
            metavar='<add_nodes>',
            type=int,
            required=True,
            help=_('Number of css nodes to be scaled out.'),
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help=('Wait for Cluster Scaling Task to complete.'),
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
        cluster = client.find_cluster(
            parsed_args.cluster, ignore_missing=False
        )
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
            help=_('ID or Name of the CSS cluster(s) to be deleted.'),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.css
        result = 0
        for name_or_id in parsed_args.cluster:
            try:
                cluster = client.find_cluster(name_or_id, ignore_missing=False)
                client.delete_cluster(cluster, ignore_missing=False)
            except Exception as e:
                result += 1
                LOG.error(
                    _(
                        'Failed to delete cluster(s) with '
                        "ID or Name '%(cluster)s': %(e)s"
                    ),
                    {'cluster': name_or_id, 'e': e},
                )
        if result > 0:
            total = len(parsed_args.cluster)
            msg = _(
                '%(result)s of %(total)s Cluster(s) failed ' 'to delete.'
            ) % {'result': result, 'total': total}
            raise exceptions.CommandError(msg)


class UpdateClusterName(command.ShowOne):
    _description = _('Change the name of a cluster.')

    def get_parser(self, prog_name):
        parser = super(UpdateClusterName, self).get_parser(prog_name)
        parser.add_argument(
            'cluster', metavar='<cluster>', help=_('Cluster name or ID.')
        )
        parser.add_argument(
            '--new-name',
            required=True,
            metavar='<new_name>',
            help=_('New cluster name.'),
        )
        return parser

    @translate_response
    def take_action(self, parsed_args):
        client = self.app.client_manager.css

        cluster = client.find_cluster(
            parsed_args.cluster, ignore_missing=False
        )

        client.update_cluster_name(cluster, parsed_args.new_name)

        return client.get_cluster(cluster)


class UpdateClusterPassword(command.Command):
    _description = _('Change the password of a cluster.')

    def get_parser(self, prog_name):
        parser = super(UpdateClusterPassword, self).get_parser(prog_name)
        parser.add_argument(
            'cluster', metavar='<cluster>', help=_('Cluster name or ID.')
        )
        parser.add_argument(
            '--new-password',
            required=True,
            metavar='<new_password>',
            help=_('New password.'),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.css

        cluster = client.find_cluster(
            parsed_args.cluster, ignore_missing=False
        )

        client.update_cluster_password(cluster, parsed_args.new_password)


class UpdateClusterSecurityGroup(command.Command):
    _description = _('Change the security group after a cluster is created')

    def get_parser(self, prog_name):
        parser = super(UpdateClusterSecurityGroup, self).get_parser(prog_name)
        parser.add_argument(
            'cluster', metavar='<cluster>', help=_('Cluster name or ID.')
        )
        parser.add_argument(
            '--security-group',
            required=True,
            metavar='<security_group>',
            help=_('New security group id or name.'),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.css
        network_client = self.app.client_manager.network

        cluster = client.find_cluster(
            parsed_args.cluster, ignore_missing=False
        )
        security_group = network_client.find_security_group(
            parsed_args.security_group, ignore_missing=False
        )

        client.update_cluster_security_group(cluster, security_group.id)


class UpdateClusterSecurityMode(command.Command):
    _description = _('Change the security mode of a cluster.')

    def get_parser(self, prog_name):
        parser = super(UpdateClusterSecurityMode, self).get_parser(prog_name)
        parser.add_argument(
            'cluster', metavar='<cluster>', help=_('Cluster name or ID.')
        )
        parser.add_argument(
            '--authority-enable',
            action='store_true',
            help=('Indicates whether to enable the security mode.'),
        )
        parser.add_argument(
            '--admin-pwd',
            metavar='<admin_pwd>',
            help=_('Cluster password in security mode.'),
        )
        parser.add_argument(
            '--https-enable',
            action='store_true',
            help=('Indicates whether to enable HTTPS.'),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.css
        attrs = {}

        if parsed_args.authority_enable:
            attrs['authority_enable'] = True

        if parsed_args.https_enable:
            attrs['https_enable'] = True

        if parsed_args.admin_pwd:
            attrs['admin_pwd'] = parsed_args.admin_pwd

        cluster = client.find_cluster(
            parsed_args.cluster, ignore_missing=False
        )

        client.update_cluster_security_mode(cluster, **attrs)


class UpdateClusterFlavor(command.Command):
    _description = _('Modify the specifications of a cluster.')

    def get_parser(self, prog_name):
        parser = super(UpdateClusterFlavor, self).get_parser(prog_name)
        parser.add_argument(
            'cluster', metavar='<cluster>', help=_('Cluster name or ID.')
        )
        parser.add_argument(
            '--node-type',
            metavar='{' + ','.join(NODE_TYPE_CHOICES) + '}',
            choices=NODE_TYPE_CHOICES,
            type=lambda s: s.lower(),
            help=('Type of the node to modify.'),
        )
        parser.add_argument(
            '--flavor',
            required=True,
            metavar='<flavor>',
            help=('ID of the new flavor.'),
        )
        parser.add_argument(
            '--check-replica',
            action='store_true',
            help=('Indicates whether to verify replicas.'),
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help=('Wait for Cluster.'),
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
        attrs = {}

        if parsed_args.node_type:
            attrs['node_type'] = parsed_args.node_type

        attrs['new_flavor'] = parsed_args.flavor

        if parsed_args.check_replica:
            attrs['check_replica'] = True

        cluster = client.find_cluster(
            parsed_args.cluster, ignore_missing=False
        )

        client.update_cluster_flavor(cluster, **attrs)

        if parsed_args.wait:
            client.wait_for_cluster(cluster.id, parsed_args.timeout)


class ScaleInCluster(command.Command):
    _description = _('Scale in a cluster by removing specified nodes.')

    def get_parser(self, prog_name):
        parser = super(ScaleInCluster, self).get_parser(prog_name)
        parser.add_argument(
            'cluster', metavar='<cluster>', help=_('Cluster name or ID.')
        )
        parser.add_argument(
            '--nodes',
            nargs='+',
            required=True,
            metavar='<nodes>',
            help=_('IDs of the nodes to remove.'),
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help=('Wait for Cluster.'),
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

        cluster = client.find_cluster(
            parsed_args.cluster, ignore_missing=False
        )

        client.scale_in_cluster(cluster, parsed_args.nodes)

        if parsed_args.wait:
            client.wait_for_cluster(cluster.id, parsed_args.timeout)


class ScaleInClusterByNodeType(command.Command):
    _description = _('Remove instances of specific types.')

    def get_parser(self, prog_name):
        parser = super(ScaleInClusterByNodeType, self).get_parser(prog_name)
        parser.add_argument(
            'cluster', metavar='<cluster>', help=_('Cluster name or ID.')
        )
        parser.add_argument(
            '--ess',
            metavar='<reduce_num>',
            type=int,
            help=_('Reduce the ess nodes.'),
        )
        parser.add_argument(
            '--ess-master',
            metavar='<reduce_num>',
            dest='ess-master',
            type=int,
            help=_('Reduce the ess-master nodes.'),
        )
        parser.add_argument(
            '--ess-client',
            metavar='<reduce_num>',
            dest='ess-client',
            type=int,
            help=_('Reduce the ess-client nodes.'),
        )
        parser.add_argument(
            '--ess-cold',
            metavar='<reduce_num>',
            dest='ess-cold',
            type=int,
            help=_('Reduce the ess-cold nodes.'),
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help=('Wait for Cluster.'),
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

        nodes = []

        for arg in ('ess', 'ess-master', 'ess-client', 'ess-cold'):
            value = getattr(parsed_args, arg)
            if value:
                nodes.append(
                    {
                        'type': arg,
                        'reducedNodeNum': value,
                    }
                )

        cluster = client.find_cluster(
            parsed_args.cluster, ignore_missing=False
        )

        client.scale_in_cluster_by_node_type(cluster, nodes)

        if parsed_args.wait:
            client.wait_for_cluster(cluster.id, parsed_args.timeout)


class UpdateClusterKernel(command.Command):
    _description = _('Upgrade cluster version.')

    def get_parser(self, prog_name):
        parser = super(UpdateClusterKernel, self).get_parser(prog_name)
        parser.add_argument(
            'cluster', metavar='<cluster>', help=_('Cluster name or ID.')
        )
        parser.add_argument(
            '--target-image-id',
            metavar='<target_image_id>',
            help=_('ID of the target image version.'),
        )
        parser.add_argument(
            '--upgrade-type',
            required=True,
            metavar='{' + ','.join(UPGRADE_TYPE_CHOICES) + '}',
            choices=UPGRADE_TYPE_CHOICES,
            type=lambda s: s.lower(),
            help=_('Upgrade type.'),
        )
        parser.add_argument(
            '--check-backup-indices',
            action='store_true',
            help=_('ID of the target image version.'),
        )
        parser.add_argument(
            '--agency',
            required=True,
            metavar='<agency>',
            help=_('Agency name.'),
        )
        parser.add_argument(
            '--check-cluster-load',
            action='store_true',
            help=_('Indicates whether to verify the load.'),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.css
        attrs = {}

        for arg in ('target_image_id', 'upgrade_type', 'agency'):
            value = getattr(parsed_args, arg)
            if value:
                attrs[arg] = value

        attrs['indices_backup_check'] = (
            True if parsed_args.check_backup_indices else False
        )

        if parsed_args.check_cluster_load:
            attrs['cluster_load_check'] = parsed_args.check_cluster_load

        cluster = client.find_cluster(
            parsed_args.cluster, ignore_missing=False
        )

        client.update_cluster_kernel(cluster, **attrs)


class ReplaceClusterNode(command.Command):
    _description = _('Replace a node in the cluster.')

    def get_parser(self, prog_name):
        parser = super(ReplaceClusterNode, self).get_parser(prog_name)
        parser.add_argument(
            'cluster', metavar='<cluster>', help=_('Cluster name or ID.')
        )
        parser.add_argument(
            '--node-id',
            required=True,
            metavar='<nodes_id>',
            help=_('IDs of the node to be replaced.'),
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help=('Wait for Cluster.'),
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

        cluster = client.find_cluster(
            parsed_args.cluster, ignore_missing=False
        )

        client.replace_cluster_node(cluster, parsed_args.node_id)

        if parsed_args.wait:
            client.wait_for_cluster(cluster.id, parsed_args.timeout)


class AddClusterNodes(command.Command):
    _description = _('Add master and client nodes to a cluster.')

    def get_parser(self, prog_name):
        parser = super(AddClusterNodes, self).get_parser(prog_name)
        parser.add_argument(
            'cluster', metavar='<cluster>', help=_('Cluster name or ID.')
        )
        parser.add_argument(
            '--node-type',
            required=True,
            metavar='<node_type>',
            help=_('Node type.'),
        )
        parser.add_argument(
            '--flavor', required=True, metavar='<flavor>', help=_('Flavor ID.')
        )
        parser.add_argument(
            '--node-size',
            required=True,
            type=int,
            metavar='<node_size>',
            help=_('Number of nodes.'),
        )
        parser.add_argument(
            '--volume-type',
            required=True,
            metavar='{' + ','.join(VOLUME_TYPE_CHOICES) + '}',
            choices=VOLUME_TYPE_CHOICES,
            type=lambda s: s.upper(),
            help=_('Node storage type.'),
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help=('Wait for Cluster.'),
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

        attrs = {
            'node_type': parsed_args.node_type,
            'flavor': parsed_args.flavor,
            'node_size': parsed_args.node_size,
            'volume_type': parsed_args.volume_type,
        }

        cluster = client.find_cluster(
            parsed_args.cluster, ignore_missing=False
        )

        client.add_cluster_nodes(cluster, **attrs)

        if parsed_args.wait:
            client.wait_for_cluster(cluster.id, parsed_args.timeout)


class RetryClusterUpgradeJob(command.Command):
    _description = _('Retry a task or terminate the impact of a task.')

    def get_parser(self, prog_name):
        parser = super(RetryClusterUpgradeJob, self).get_parser(prog_name)
        parser.add_argument(
            'cluster', metavar='<cluster>', help=_('Cluster name or ID.')
        )
        parser.add_argument(
            '--job-id',
            required=True,
            metavar='<job_id>',
            help=_('ID of the task to be retried.'),
        )
        parser.add_argument(
            '--retry-mode',
            metavar='<retry_mode>',
            default='abort',
            help=_(
                """If this parameter is not left blank,
                the impact of the task is terminated."""
            ),
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help=('Wait for Cluster.'),
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
        attrs = {}

        attrs['job_id'] = parsed_args.job_id

        attrs['retry_mode'] = parsed_args.retry_mode

        cluster = client.find_cluster(
            parsed_args.cluster, ignore_missing=False
        )

        client.retry_cluster_upgrade_job(cluster, **attrs)

        if parsed_args.wait:
            client.wait_for_cluster(cluster.id, parsed_args.timeout)


class ListClusterVersionUpgrades(command.Lister):
    _description = _('List available upgradable versions.')

    column_headers = [
        'Datastore Type',
        'Datastore Version',
        'Image Name',
        'Id',
        'Description',
        'Priority',
    ]

    columns = [
        'datastore_type',
        'datastore_version',
        'display_name',
        'id',
        'image_desc',
        'priority',
    ]

    def get_parser(self, prog_name):
        parser = super(ListClusterVersionUpgrades, self).get_parser(prog_name)
        parser.add_argument(
            'cluster', metavar='<cluster>', help=_('Cluster name or ID.')
        )
        parser.add_argument(
            '--upgrade-type',
            required=True,
            metavar='{same, cross}',
            choices=['same', 'cross'],
            type=lambda s: s.lower(),
            help=_('Version type.'),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.css

        cluster = client.find_cluster(
            parsed_args.cluster, ignore_missing=False
        )

        obj = client.get_cluster_version_upgrades(
            cluster, parsed_args.upgrade_type
        )

        image_info_list = obj.image_info_list

        _formatters = {}

        return (
            self.column_headers,
            (
                utils.get_item_properties(
                    s, self.columns, formatters=_formatters
                )
                for s in image_info_list
            ),
        )


class ShowClusterUpgradeStatus(command.Lister):
    _description = _('List CSS Cluster Nodes.')
    columns = (
        'ID',
        'Image Info',
        'Execute Times',
        'Start Time',
        'End Time',
        'Status',
    )

    def get_parser(self, prog_name):
        parser = super(ShowClusterUpgradeStatus, self).get_parser(prog_name)
        parser.add_argument(
            'cluster', metavar='<cluster>', help=_('Cluster name or ID.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.css

        cluster = client.find_cluster(
            parsed_args.cluster, ignore_missing=False
        )

        data = client.get_cluster_upgrade_status(cluster)

        _formatters = {'Image Info': cli_utils.YamlFormat}

        return (
            self.columns,
            (
                utils.get_item_properties(
                    s, self.columns, formatters=_formatters
                )
                for s in data
            ),
        )
