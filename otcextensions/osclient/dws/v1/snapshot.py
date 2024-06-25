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
"""DWS Snapshot action implementations"""

import logging

from osc_lib import exceptions
from osc_lib import utils
from osc_lib.command import command

from otcextensions.common import sdk_utils
from otcextensions.i18n import _
from otcextensions.osclient.dws.v1 import cluster as _cluster

LOG = logging.getLogger(__name__)


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
        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)

    new.__name__ = func.__name__
    new.__doc__ = func.__doc__
    return new


class ListSnapshots(command.Lister):
    _description = _('List DWS Backups.')

    columns = (
        'ID',
        'Name',
        'Type',
        'Cluster Id',
    )

    def get_parser(self, prog_name):
        parser = super(ListSnapshots, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dws
        data = client.snapshots()

        return (
            self.columns,
            (utils.get_item_properties(s, self.columns) for s in data),
        )


class CreateSnapshot(command.ShowOne):
    _description = _('Create snapshot for a specified cluster.')

    def get_parser(self, prog_name):
        parser = super(CreateSnapshot, self).get_parser(prog_name)

        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            help=_(
                'ID or name of the cluster for which you want to '
                'create a snapshot.'
            ),
        )
        parser.add_argument(
            'name',
            metavar='<name>',
            help=_(
                'Snapshot name, which must be unique and start with a '
                'letter. It consists of 4 to 64 characters, which are '
                'case-insensitive and contain letters, digits, '
                'hyphens (-), and underscores (_) only.'
            ),
        )

        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_(
                'Snapshot description. If no value is specified, '
                'the description is empty. Enter a maximum of 256 '
                'characters. The following special characters are '
                'not allowed: !<>\'=&"'
            ),
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help=('Wait for the Cluster snapshotting task to finish.'),
        )
        parser.add_argument(
            '--timeout',
            metavar='<timeout>',
            type=int,
            default=900,
            help=_('Timeout for the wait in seconds (Default 900 seconds).'),
        )
        return parser

    @translate_response
    def take_action(self, parsed_args):
        client = self.app.client_manager.dws
        cluster = client.find_cluster(
            parsed_args.cluster, ignore_missing=False
        )

        attrs = {'name': parsed_args.name, 'cluster_id': cluster.id}
        if parsed_args.description:
            attrs['description'] = parsed_args.description

        obj = client.create_snapshot(**attrs)
        if parsed_args.wait:
            client.wait_for_cluster(cluster.id, wait=parsed_args.timeout)

        return client.get_snapshot(obj.id)


class ShowSnapshot(command.ShowOne):
    _description = _('Show details of a DWS snapshot.')

    def get_parser(self, prog_name):
        parser = super(ShowSnapshot, self).get_parser(prog_name)
        parser.add_argument(
            'snapshot', metavar='<snapshot>', help=_('Snapshot name or ID.')
        )
        return parser

    @translate_response
    def take_action(self, parsed_args):
        client = self.app.client_manager.dws

        return client.find_snapshot(parsed_args.snapshot, ignore_missing=False)


class RestoreSnapshot(command.ShowOne):
    _description = _('Restore clusters using the snapshot.')

    def get_parser(self, prog_name):
        parser = super(RestoreSnapshot, self).get_parser(prog_name)
        parser.add_argument('name', metavar='<name>', help=_('Cluster Name.'))
        parser.add_argument(
            '--snapshot-id',
            metavar='<snapshot_id>',
            required=True,
            help=_('ID of the snapshot to be restored.'),
        )
        parser.add_argument(
            '--availability-zone',
            metavar='<availability_zone>',
            help=_(
                'AZ of a cluster. The default value is the same '
                'as that of the original cluster.'
            ),
        )
        network_group = parser.add_argument_group('Network Parameters')
        network_group.add_argument(
            '--router-id',
            metavar='<router_id>',
            dest='vpc_id',
            help=_(
                'Router ID, which is used for configuring cluster '
                'network. The default value is the same as that of '
                'the original cluster.'
            ),
        )
        network_group.add_argument(
            '--network-id',
            metavar='<network_id>',
            dest='subnet_id',
            help=_(
                'Network ID, which is used for configuring cluster '
                'network. The default value is the same as that of '
                'the original cluster.'
            ),
        )
        network_group.add_argument(
            '--security-group-id',
            metavar='<security_group_id>',
            help=_(
                'Security group ID, which is used for configuring '
                'cluster network. The default value is the same as '
                'that of the original cluster.'
            ),
        )
        parser.add_argument(
            '--port',
            metavar='<port>',
            type=int,
            help=_(
                'Service port of a cluster. The value ranges from '
                '8000 to 30000. The default value is 8000.'
            ),
        )
        parser.add_argument(
            '--floating-ip',
            metavar='<floating_ip>',
            help=_(
                'Public IP address. If the parameter is not specified, '
                'public connection is not used by default.\n'
                'Possible values can be:\n'
                '- "auto" - To automatically assign Floating IP.\n'
                '- "ID" or "IP" of existing floating ip.'
            ),
        )
        parser.add_argument(
            '--enterprise-project-id',
            metavar='<enterprise_project_id>',
            help=_(
                'Enterprise project. The default '
                'enterprise project ID is 0.'
            ),
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help=('Wait for the status of Restored cluster to be available.'),
        )
        parser.add_argument(
            '--timeout',
            metavar='<timeout>',
            type=int,
            default=1800,
            help=_('Timeout for the wait in seconds (Default 1800 seconds).'),
        )
        return parser

    @_cluster.translate_response
    def take_action(self, parsed_args):
        client = self.app.client_manager.dws

        attrs = {}
        for arg in (
            'name',
            'vpc_id',
            'subnet_id',
            'security_group_id',
            'port',
            'availability_zone',
            'enterprise_project_id',
        ):
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        floating_ip = parsed_args.floating_ip

        if floating_ip and floating_ip.lower() == 'auto':
            attrs['public_ip'] = {
                'public_bind_type': 'auto_assign',
                'eip_id': ''
            }
        elif floating_ip:
            network_client = self.app.client_manager.network
            floating_ip_resp = network_client.find_ip(
                floating_ip, ignore_missing=False
            )
            attrs['public_ip'] = {
                'public_bind_type': 'bind_existing',
                'eip_id': floating_ip_resp.id,
            }

        obj = client.restore_snapshot(parsed_args.snapshot_id, **attrs)

        if parsed_args.wait:
            client.wait_for_cluster(obj.id, parsed_args.timeout)
        return client.get_cluster(obj.id)


class DeleteSnapshot(command.Command):
    _description = _('Delete specified manual snapshot(s).')

    def get_parser(self, prog_name):
        parser = super(DeleteSnapshot, self).get_parser(prog_name)
        parser.add_argument(
            'snapshot',
            metavar='<snapshot>',
            nargs='+',
            help=_('ID or Name of the Snapshot(s) to be deleted.'),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dws
        result = 0
        for name_or_id in parsed_args.snapshot:
            try:
                snapshot = client.find_snapshot(
                    name_or_id, ignore_missing=False
                )
                client.delete_snapshot(snapshot.id)
            except Exception as e:
                result += 1
                LOG.error(
                    _(
                        'Failed to delete snapshot(s) with '
                        "ID or Name '%(snapshot)s': %(e)s"
                    ),
                    {'snapshot': name_or_id, 'e': e},
                )
        if result > 0:
            total = len(parsed_args.snapshot)
            msg = _(
                '%(result)s of %(total)s Snapshot(s) failed ' 'to delete.'
            ) % {'result': result, 'total': total}
            raise exceptions.CommandError(msg)
