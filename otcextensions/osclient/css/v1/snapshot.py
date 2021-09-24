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
'''CSS ELK cluster v1 action implementations'''
import logging

from osc_lib import utils
from osc_lib import exceptions
from osc_lib.command import command
from otcextensions.common import sdk_utils
from collections import defaultdict

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _get_columns(item):
    column_map = {
    }
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


def translate_response(func):
    def new(self, *args, **kwargs):
        obj = func(self, *args, **kwargs)
        delattr(obj, 'location')
        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)
        return (display_columns, data)
    new.__name__ = func.__name__
    new.__doc__ = func.__doc__
    return new


class ListSnapshots(command.Lister):

    _description = _('List CSS Backups')

    columns = (
        'ID',
        'Name',
        'Status',
        'Backup Method',
        'Bucket Name',
        'Created At',
        'Backup Keep Days',
    )

    def get_parser(self, prog_name):
        parser = super(ListSnapshots, self).get_parser(prog_name)
        parser.add_argument(
            'cluster',
            metavar='cluster',
            help=_("Specifies the ID or Name of the CSS Cluster."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.css
        cluster = client.find_cluster(parsed_args.cluster)
        data = client.snapshots(cluster)

        return (self.columns, (utils.get_item_properties(s, self.columns)
                               for s in data))


class CreateSnapshot(command.ShowOne):
    _description = _('Create a single CSS snapshot')
    columns = ('id', 'name')

    def get_parser(self, prog_name):
        parser = super(CreateSnapshot, self).get_parser(prog_name)

        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            help=_('Specify ID or Name of the CSS cluster from where '
                   'index data is to be backed up.')
        )

        parser.add_argument(
            'name',
            metavar='<name>',
            help=_('Snapshot name.')
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_('Description of a snapshot.')
        )
        parser.add_argument(
            '--indices',
            metavar='<indices>',
            help=_('Name of the index to be backed up. '
                   'Multiple index names are separated by commas.')
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

    def take_action(self, parsed_args):

        client = self.app.client_manager.css

        attrs = {}

        cluster = client.find_cluster(parsed_args.cluster)
        attrs['name'] = parsed_args.name
        if parsed_args.description:
            attrs['description'] = parsed_args.description
        if parsed_args.indices:
            attrs['indices'] = parsed_args.indices

        obj = client.create_snapshot(cluster, **attrs)
        if parsed_args.wait:
            client.wait_for_cluster(cluster.id, parsed_args.timeout)

        data = utils.get_item_properties(obj, self.columns)
        return (self.columns, data)


class RestoreSnapshot(command.Command):

    _description = _('Restore the CSS cluster using the specified snapshot')

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

    def get_parser(self, prog_name):
        parser = super(RestoreSnapshot, self).get_parser(prog_name)
        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            help=_('Cluster ID or Name to which the snapshot belongs.')
        )
        parser.add_argument(
            'snapshotId',
            metavar='<snapshotId>',
            help=_('The snapshot ID')
        )
        parser.add_argument(
            '--target-cluster',
            metavar='<target_cluster>',
            required=True,
            help=_('ID or Name of the cluster, to which the snapshot '
                   'is to be restored.')
        )
        parser.add_argument(
            '--indices',
            metavar='<indices>',
            help=_('Name of the index to be restored. '
                   'Multiple index names are separated by commas (,).')
        )
        parser.add_argument(
            '--rename-pattern',
            metavar='<rename_pattern>',
            help=_('Rule for defining the indices to be restored. '
                   'The value contains a maximum of 1,024 characters.')
        )
        parser.add_argument(
            '--rename-replacement',
            metavar='<rename_replacement>',
            help=_('Rule for renaming an index. '
                   'The value contains 0 to 1,024 characters.')
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

    def take_action(self, parsed_args):
        client = self.app.client_manager.css
        cluster = client.find_cluster(parsed_args.cluster)
        target_cluster = client.find_cluster(parsed_args.target_cluster)
        attrs = {
            'targetCluster': target_cluster.id
        }
        if parsed_args.rename_replacement:
            attrs['renameReplacement'] = parsed_args.rename_replacement
        if parsed_args.rename_pattern:
            attrs['renamePattern'] = parsed_args.rename_pattern
        if parsed_args.indices:
            attrs['indices'] = parsed_args.indices

        client.restore_snapshot(
            cluster, parsed_args.snapshotId, **attrs)

        if parsed_args.wait:
            client.wait_for_cluster(target_cluster.id, parsed_args.timeout)

        obj = client.get_cluster(target_cluster.id)
        setattr(obj, 'version', obj.datastore.version)
        setattr(obj, 'type', obj.datastore.type)
        node_count = defaultdict(int)
        for node in obj.nodes:
            node_count[node['type']] += 1
        setattr(obj, 'node_count', dict(node_count))

        data = utils.get_item_properties(obj, self.columns)
        return (self.columns, data)


class SetSnapshotPolicy(command.ShowOne):
    _description = _('Setting the Automatic Snapshot Creation Policy.')

    def get_parser(self, prog_name):
        parser = super(SetSnapshotPolicy, self).get_parser(prog_name)
        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            help=_('ID or Name of the cluster to which the snapshot belongs.')
        )
        parser.add_argument(
            '--name-prefix',
            metavar='<name_prefix>',
            required=True,
            help=('Prefix of the snapshot name that is automatically created.')
        )
        parser.add_argument(
            '--period',
            metavar='<period>',
            required=True,
            help=('Time when a snapshot is created every day.\n'
                  'Time format is followed by the time zone HH:mm z.\n'
                  'for example, 00:00 GMT+08:00 and 01:00 GMT+08:00.')
        )
        parser.add_argument(
            '--keep-days',
            metavar='<keep_days>',
            type=int,
            required=True,
            help=('Number of days that a snapshot can be retained.')
        )
        parser.add_argument(
            '--disable',
            action='store_true',
            help=('Disable the automatic snapshot creation policy.')
        )
        parser.add_argument(
            '--delete-auto',
            action='store_true',
            help=('Whether to delete all automatically created snapshots '
                  'when the automatic snapshot creation policy is disabled.'
                  'Value is true or false. Default vaule is false')
        )
        return parser

    @translate_response
    def take_action(self, parsed_args):
        client = self.app.client_manager.css
        attrs = {
            'prefix': parsed_args.name_prefix,
            'keepday': parsed_args.keep_days,
            'period': parsed_args.period,
            'enable': 'true'
        }
        if getattr(parsed_args, 'disable'):
            attrs['enable'] = 'false'
        if getattr(parsed_args, 'delete_auto'):
            attrs['deleteAuto'] = 'true'

        cluster = client.find_cluster(parsed_args.cluster)
        client.set_snapshot_policy(cluster, **attrs)
        return client.get_snapshot_policy(cluster)


class ShowSnapshotPolicy(command.ShowOne):
    _description = _('Show details of a CSS cluster backup policy.')

    def get_parser(self, prog_name):
        parser = super(ShowSnapshotPolicy, self).get_parser(prog_name)
        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            help=_('ID or Name of the cluster to which the snapshot belongs.')
        )
        return parser

    @translate_response
    def take_action(self, parsed_args):
        client = self.app.client_manager.css

        cluster = client.find_cluster(parsed_args.cluster)
        return client.get_snapshot_policy(cluster)


class SetSnapshotConfiguration(command.ShowOne):
    _description = _('Set Basic Configurations of a CSS Cluster Snapshot.')

    def get_parser(self, prog_name):
        parser = super(SetSnapshotConfiguration, self).get_parser(prog_name)
        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            help=_('ID or Name of the cluster to which the snapshot belongs.')
        )
        parser.add_argument(
            '--auto',
            action='store_true',
            help=('Set Snapshot Configuration Automatically.')
        )
        parser.add_argument(
            '--bucket',
            metavar='<bucket>',
            help=('OBS bucket used for index data backup.')
        )
        parser.add_argument(
            '--agency',
            metavar='<agency>',
            help=('IAM agency used to access OBS.')
        )
        parser.add_argument(
            '--cmk-id',
            metavar='<cmk_id>',
            help=('Key ID used for snapshot encryption.')
        )
        return parser

    @translate_response
    def take_action(self, parsed_args):
        client = self.app.client_manager.css
        auto_setting = getattr(parsed_args, 'auto')
        attrs = {}
        if not auto_setting:
            if not parsed_args.bucket or not parsed_args.agency:
                msg = ('Please provide --bucket and --agency '
                       'to set snapshot configuration')
                raise exceptions.CommandError(msg)
            attrs['bucket'] = parsed_args.bucket
            attrs['agency'] = parsed_args.agency

            if parsed_args.cmk_id:
                attrs['snapshotCmkId'] = parsed_args.cmk_id

        cluster = client.find_cluster(parsed_args.cluster)
        client.set_snapshot_configuration(
            cluster, auto_setting, **attrs
        )
        return client.get_snapshot_policy(cluster)


class DeleteSnapshot(command.Command):
    _description = _('Delete CSS Cluster Snapshot(s).')

    def get_parser(self, prog_name):
        parser = super(DeleteSnapshot, self).get_parser(prog_name)
        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            help=_('ID or Name of the cluster to which the snapshot belongs.')
        )
        parser.add_argument(
            'snapshot',
            metavar='<snapshot>',
            nargs='+',
            help=_("ID(s) of the snapshot(s) to be deleted."),
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.css
        cluster = client.find_cluster(parsed_args.cluster)
        result = 0
        for snapshotId in parsed_args.snapshot:
            try:
                client.delete_snapshot(cluster, snapshotId,
                                       ignore_missing=False)
            except Exception as e:
                result += 1
                LOG.error(_("Failed to delete Snapshot(s) with "
                          "ID or Name '%(snapshot)s': %(e)s"),
                          {'snapshot': snapshotId, 'e': e})
        if result > 0:
            total = len(parsed_args.snapshot)
            msg = (_("%(result)s of %(total)s Snapshot(s) failed "
                   "to delete.") % {'result': result, 'total': total})
            raise exceptions.CommandError(msg)


class DisableSnapshotFunction(command.Command):
    _description = _('Disable the snapshot creation function.')

    def get_parser(self, prog_name):
        parser = super(DisableSnapshotFunction, self).get_parser(prog_name)
        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            help=_('ID or Name of the cluster to which the snapshot belongs.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.css
        cluster = client.find_cluster(parsed_args.cluster)
        client.disable_snapshot(cluster)
