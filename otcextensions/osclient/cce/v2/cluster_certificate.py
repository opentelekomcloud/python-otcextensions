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
'''CCE Cluster Certificates v2 action implementations'''
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _flatten_cluster_certificate(obj):
    """Flatten the structure of the cluster node into a single dict
    """
    data = {
        'name': obj.context.get('name', None),
        'cluster': obj.context.get('cluster', None),
        'user': obj.context.get('user', None),
        'ca': obj.ca,
        'client_certificate': obj.client_certificate,
        'client_key': obj.client_key,
    }

    return data


class ShowCCEClusterCertificates(command.ShowOne):
    _description = _('Show Cluster certificates details')
    columns = (
        'name',
        'cluster',
        'user',
        'ca',
        'client_certificate',
        'client_key')

    def get_parser(self, prog_name):
        parser = super(ShowCCEClusterCertificates, self).get_parser(prog_name)
        parser.add_argument(
            'cluster',
            metavar='<cluster>',
            help=_('ID of the cluster.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.cce

        cluster = client.find_cluster(parsed_args.cluster,
                                      ignore_missing=False)

        obj = client.get_cluster_certificates(
            cluster=cluster.id
        )

        flat_data = _flatten_cluster_certificate(obj)
        columns = tuple(flat_data)

        data = utils.get_dict_properties(
            flat_data,
            columns)

        return columns, data
