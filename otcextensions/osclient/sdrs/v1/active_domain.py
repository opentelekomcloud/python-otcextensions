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
'''SDRS Active-active domains CLI implementation'''
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _flatten_domain(i, obj):
    """Flatten the structure of active-active domains into a single dict
    """
    data = {
        'id': obj.domains[i].id,
        'name': obj.domains[i].name,
        'description': obj.domains[i].description,
        'sold_out': obj.domains[i].sold_out,
        'local_replication_cluster':
            obj.domains[i].local_replication_cluster.availability_zone,
        'remote_replication_cluster':
            obj.domains[i].remote_replication_cluster.availability_zone
    }

    return data


class ListDomain(command.Lister):
    _description = _('List Active-active domains')
    columns = (
        'ID',
        'name',
        'description',
        'sold_out',
        'local_replication_cluster',
        'remote_replication_cluster'
    )

    def get_parser(self, prog_name):
        parser = super(ListDomain, self).get_parser(prog_name)

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.sdrs

        data = client.get_domains()

        table = (self.columns,
                 (utils.get_dict_properties(
                     _flatten_domain(i, s), self.columns,
                 ) for i, s in enumerate(data)))
        return table
