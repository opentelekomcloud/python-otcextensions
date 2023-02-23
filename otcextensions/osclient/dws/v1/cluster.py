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
'''DWS cluster v1 action implementations'''
import logging

from osc_lib import utils
from osc_lib.cli import format_columns
from osc_lib.command import command
from osc_lib import exceptions
from otcextensions.common import sdk_utils

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


_formatters = {
    'floating_ip': format_columns.DictColumn,
    'endpoints': format_columns.ListDictColumn,
    'public_endpoints': format_columns.ListDictColumn,
    'maintenance_window': format_columns.DictColumn,
    'parameter_group': format_columns.DictColumn,
    'private_ip': format_columns.ListColumn,
    'action_progress': format_columns.DictColumn,
    'public_domain': format_columns.ListColumn,
    'private_domain': format_columns.ListColumn,
    'nodes': format_columns.ListDictColumn,
    'plugins': format_columns.ListDictColumn
}


def _get_columns(item):
    column_map = {}
    hidden = [
        'location',
        'plugins'
    ]
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map,
                                                           hidden)


def set_attributes_for_print(obj):
    for data in obj:
        yield data


def translate_response(func):
    def new(self, *args, **kwargs):
        obj = func(self, *args, **kwargs)
        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)
        return (display_columns, data)

    new.__name__ = func.__name__
    new.__doc__ = func.__doc__
    return new


class ListClusters(command.Lister):
    _description = _('List DWS Clusters.')
    columns = (
        'ID',
        'Name',
        'Num Nodes',
        'Flavor',
        'Status',
        'Version',
        'Created At'
    )

    def get_parser(self, prog_name):
        parser = super(ListClusters, self).get_parser(prog_name)

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dws
        data = client.clusters()

        return (self.columns, (utils.get_item_properties(s, self.columns)
                               for s in data))


class CreateCluster(command.ShowOne):
    _description = _('Create a new DWS cluster instance.')

    def get_parser(self, prog_name):
        parser = super(CreateCluster, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help=_('Cluster Name.')
        )
        parser.add_argument(
            '--flavor',
            metavar='<flavor>',
            dest='node_type',
            required=True,
            help=_('DWS Cluster Flavor (Node Type).')
        )
        parser.add_argument(
            '--availability-zone',
            metavar='<availability_zone>',
            required=True,
            help=_('Availability Zone.')
        )
        parser.add_argument(
            '--num-nodes',
            metavar='<num_nodes>',
            dest='number_of_node',
            type=int,
            default=3,
            help=_('Number of cluster Nodes. The value range is 3 to 256. '
                   'For a hybrid data warehouse (standalone), the value is 1.')
        )
        parser.add_argument(
            '--num-cn',
            metavar='<num_cn>',
            dest='number_of_cn',
            type=int,
            help=_('Number of deployed CNs. The value ranges from 2 to the '
                   'number of cluster nodes minus 1. The maximum value is 20 '
                   'and the default value is 3.')
        )

        network_group = parser.add_argument_group('Network Parameters')
        network_group.add_argument(
            '--router-id',
            metavar='<router_id>',
            dest='vpc_id',
            required=True,
            help=_('Router ID.')
        )
        network_group.add_argument(
            '--network-id',
            metavar='<network_id>',
            dest='subnet_id',
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
            '--username',
            metavar='<username>',
            dest='user_name',
            required=True,
            help=_('Administrator username for logging in to a '
                   'GaussDB(DWS) cluster. The username must:\n'
                   '- Consist of lowercase letters, digits, or underscores.\n'
                   '- Start with a lowercase letter or an underscore.\n'
                   '- Contain 1 to 63 characters.\n'
                   '- Cannot be a keyword of the GaussDB(DWS) database.')
        )
        parser.add_argument(
            '--password',
            metavar='<password>',
            dest='user_pwd',
            required=True,
            help=_('Administrator password for logging in to a '
                   'GaussDB(DWS) cluster.')
        )
        parser.add_argument(
            '--port',
            metavar='<port>',
            default=8000,
            type=int,
            help=_('Service port of a cluster. The value ranges from '
                   '8000 to 30000. The default value is 8000.')
        )
        parser.add_argument(
            '--floating-ip',
            metavar='<floating_ip>',
            help=_('Bind Floating Ip to a DWS Cluster.\n'
                   'Possible values can be:\n'
                   '- "auto" - To automatically assign Floating IP.\n'
                   '- ID or IP of existing floating ip.')
        )
        parser.add_argument(
            '--enterprise-project-id',
            metavar='<enterprise_project_id>',
            help=_('Enterprise project. The default '
                   'enterprise project ID is 0.')
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
            default=1800,
            help=_('Timeout for the wait in seconds (Default 1800 seconds).'),
        )
        return parser

    @translate_response
    def take_action(self, parsed_args):

        client = self.app.client_manager.dws

        attrs = {}
        for arg in ('name', 'vpc_id', 'subnet_id', 'security_group_id',
                    'number_of_node', 'user_name', 'user_pwd', 'node_type',
                    'port', 'availability_zone', 'enterprise_project_id',
                    'number_of_cn'):
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
            floating_ip = network_client.find_ip(floating_ip)

        cluster = client.create_cluster(**attrs)
        if parsed_args.wait:
            client.wait_for_cluster(cluster.id, wait=parsed_args.timeout)
        return client.get_cluster(cluster.id)


class ShowCluster(command.ShowOne):
    _description = _('Show details of a DWS cluster')

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
        client = self.app.client_manager.dws

        obj = client.find_cluster(parsed_args.cluster)
        if obj.private_ip is None:
            obj = client.get_cluster(obj.id)
        return obj


class RestartCluster(command.Command):
    _description = _('Restart a DWS cluster')

    def get_parser(self, prog_name):
        parser = super(RestartCluster, self).get_parser(prog_name)
        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            help=_('ID or Name of the DWS cluster to be restart.'),
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
            help=_('Timeout for the wait in seconds. (Default 300 seconds)'),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dws
        cluster = client.find_cluster(parsed_args.cluster)
        client.restart_cluster(cluster)
        if parsed_args.wait:
            client.wait_for_cluster(cluster.id, wait=parsed_args.timeout)


class ResetPassword(command.Command):
    _description = _('Reset the password of cluster administrator.')

    def get_parser(self, prog_name):
        parser = super(ResetPassword, self).get_parser(prog_name)
        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            help=_('ID or Name of the DWS cluster to be restart.'),
        )
        parser.add_argument(
            '--password',
            metavar='<password>',
            required=True,
            help=_('New password of the GaussDB(DWS) cluster administrator.\n'
                   'A password must conform to the following rules:\n'
                   '- Contains 8 to 32 characters.\n'
                   '- Cannot be the same as the username or the username '
                   'written in reverse order.\n'
                   '- Contains at least three types of the following:\n'
                   '- > Lowercase letters\n'
                   '- > Uppercase letters\n'
                   '- > Digits\n'
                   '- > Special characters\n'
                   '- Cannot be the same as previous passwords.\n'
                   '- Cannot be a weak password.'),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dws
        cluster = client.find_cluster(parsed_args.cluster)
        return client.reset_password(cluster, parsed_args.password)


class ExtendCluster(command.Command):
    _description = _('Scaling Out a Cluster with only Common Nodes.')

    def get_parser(self, prog_name):
        parser = super(ExtendCluster, self).get_parser(prog_name)
        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            help=_('ID or Name of the DWS cluster to be extended.'),
        )
        parser.add_argument(
            '--add-nodes',
            metavar='<add_nodes>',
            type=int,
            required=True,
            help=_('Number of dws nodes to be scaled out.'),
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
            default=1800,
            help=_('Timeout for the wait in seconds. (Default 1800 seconds)'),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dws
        cluster = client.find_cluster(parsed_args.cluster)
        client.extend_cluster(cluster, parsed_args.add_nodes)
        if parsed_args.wait:
            client.wait_for_cluster(cluster.id, wait=parsed_args.timeout)


class DeleteCluster(command.Command):
    _description = _('Delete DWS Cluster(s)')

    def get_parser(self, prog_name):
        parser = super(DeleteCluster, self).get_parser(prog_name)
        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            nargs='+',
            help=_("ID or Name of the DWS cluster(s) to be deleted."),
        )
        parser.add_argument(
            '--keep-last-manual-snapshot',
            metavar='<keep_last_manual_snapshot>',
            type=int,
            default=0,
            help=_('The number of latest manual snapshots that need '
                   'to be retained for a cluster.'),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dws
        result = 0
        for name_or_id in parsed_args.cluster:
            try:
                cluster = client.find_cluster(name_or_id, ignore_missing=False)
                client.delete_cluster(
                    cluster.id, parsed_args.keep_last_manual_snapshot)
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
