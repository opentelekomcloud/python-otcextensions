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

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def set_attributes_for_print(obj):
    for data in obj:
        setattr(data, 'method', data.backupMethod)
        setattr(data, 'keep_days', data.backupKeepDay)
        setattr(data, 'bucket_name', data.bucketName)
        yield data


def _get_columns(item):
    column_map = {
    }
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


SNAPSHOT_POLICY_CHOICES = ['true', 'false']


class ListSnapshots(command.Lister):

    _description = _('List CSS Backups')

    columns = (
        'Id',
        'Name',
        'Status',
        'Method',
        'Bucket Name',
        'Created',
        'Keep Days',
    )

    def get_parser(self, prog_name):
        parser = super(ListSnapshots, self).get_parser(prog_name)
        parser.add_argument(
            'cluster',
            metavar='cluster',
            help=_("Specifies the ID of the CSS Cluster."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.css
        data = client.snapshots(parsed_args.cluster)

        data = set_attributes_for_print(data)
        return (self.columns, (utils.get_item_properties(s, self.columns)
                               for s in data))


class CreateSnapshot(command.ShowOne):
    _description = _('Create a single CSS snapshot')

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
        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.css

        attrs = {}

        cluster = parsed_args.cluster
        attrs['name'] = parsed_args.name
        if parsed_args.description:
            attrs['description'] = parsed_args.description
        if parsed_args.indices:
            attrs['indices'] = parsed_args.indices

        obj = client.create_snapshot(cluster, **attrs)

        display_columns, columns = _get_columns(obj.backup)
        data = utils.get_item_properties(obj.backup, columns)

        return (display_columns, data)


class RestoreSnapshot(command.Command):
    _description = _('Restore the CSS cluster using the specified snapshot')

    def get_parser(self, prog_name):
        parser = super(RestoreSnapshot, self).get_parser(prog_name)
        parser.add_argument(
            'clusterId',
            metavar='<clusterId>',
            help=_('The cluster ID for which the snapshot belongs')
        )
        parser.add_argument(
            'snapshotId',
            metavar='<snapshotId>',
            help=_('The snapshot ID')
        )
        parser.add_argument(
            '--targetCluster',
            metavar='<targetCluster>',
            required=True,
            help=_('ID of the cluster, to which the snapshot '
                   'is to be restored.')
        )
        parser.add_argument(
            '--indices',
            metavar='<indices>',
            help=_('Name of the index to be restored. '
                   'Multiple index names are separated by commas (,).')
        )
        parser.add_argument(
            '--renamePattern',
            metavar='<renamePattern>',
            help=_('Rule for defining the indices to be restored. '
                   'The value contains a maximum of 1,024 characters.')
        )
        parser.add_argument(
            '--renameReplacement',
            metavar='<renameReplacement>',
            help=_('Rule for renaming an index. '
                   'The value contains 0 to 1,024 characters.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.css
        args_list = (
            'targetCluster',
            'indices',
            'renamePattern',
            'renameReplacement'
        )
        attrs = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        client.restore_from_snapshot(parsed_args.ClusterId,
                                     parsed_args.snapshotId,
                                     **attrs)


class SetSnapshotPolicy(command.Command):
    _description = _('Setting the Automatic Snapshot Creation Policy.')

    def get_parser(self, prog_name):
        parser = super(SetSnapshotPolicy, self).get_parser(prog_name)
        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            help=_('ID of the cluster to which the snapshot belongs.')
        )
        parser.add_argument(
            '--prefix',
            metavar='<prefix>',
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
            '--keepday',
            metavar='<keepday>',
            type=int,
            required=True,
            help=('Number of days that a snapshot can be retained.')
        )
        parser.add_argument(
            '--enable',
            metavar='<enable>',
            required=True,
            help=('Indicates that the automatic snapshot creation policy '
                  'is enabled or disabled. Value is true or false.')
        )
        parser.add_argument(
            '--delete-auto',
            metavar='<deleteAuto>',
            dest='deleteAuto',
            help=('Whether to delete all automatically created snapshots '
                  'when the automatic snapshot creation policy is disabled.'
                  'Value is true or false. Default vaule is false')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.css
        args_list = (
            'prefix',
            'period',
            'keepday',
            'enable',
            'deleteAuto',
        )
        attrs = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        client.set_snapshot_policy(
            parsed_args.cluster, **attrs)


class ShowSnapshotPolicy(command.ShowOne):
    _description = _('Show details of a CSS cluster backup policy.')

    columns = (
        'keepday',
        'period',
        'prefix',
        'bucket',
        'basePath',
        'agency',
        'enable',
        'indices',
        'snapshotCmkId',
    )

    def get_parser(self, prog_name):
        parser = super(ShowSnapshotPolicy, self).get_parser(prog_name)
        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            help=_('ID of the cluster to which the snapshot belongs.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.css

        obj = client.get_snapshot_policy(
            cluster=parsed_args.cluster,
        )
        setattr(obj, 'basepath', obj.basePath)
        setattr(obj, 'snapshotcmkid', obj.snapshotCmkId)
        data = utils.get_item_properties(obj, self.columns)
        return (self.columns, data)


class SetSnapshotConfiguration(command.Command):
    _description = _('Set Basic Configurations of a CSS Cluster Snapshot.')

    def get_parser(self, prog_name):
        parser = super(SetSnapshotConfiguration, self).get_parser(prog_name)
        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            help=_('ID of the cluster to which the snapshot belongs.')
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

        client.set_snapshot_configuration(
            parsed_args.cluster, auto_setting, **attrs
        )


class DeleteSnapshot(command.Command):
    _description = _('Delete CSS Cluster Snapshot(s).')

    def get_parser(self, prog_name):
        parser = super(DeleteSnapshot, self).get_parser(prog_name)
        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            help=_('ID of the cluster to which the snapshot belongs.')
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
        cluster = parsed_args.cluster
        result = 0
        for snapshotId in parsed_args.snapshot:
            try:
                client.delete_snapshot(cluster, snapshotId,
                                       ignore_missing=False)
            except Exception as e:
                result += 1
                LOG.error(_("Failed to delete snapshot with "
                          "ID '%(snapshotId)s': %(e)s"),
                          {'snapshotId': snapshotId, 'e': e})
        if result > 0:
            total = len(parsed_args.snapshotId)
            msg = (_("%(result)s of %(total)s Snapshot(s) failed "
                   "to delete.") % {'result': result, 'total': total})
            raise exceptions.CommandError(msg)


class DisableSnapshot(command.Command):
    _description = _('Disable the snapshot creation function.')

    def get_parser(self, prog_name):
        parser = super(DisableSnapshot, self).get_parser(prog_name)
        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            help=_('ID of the cluster to which the snapshot belongs.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.css
        client.disable_snapshot(parsed_args.cluster,
                                ignore_missing=False)
