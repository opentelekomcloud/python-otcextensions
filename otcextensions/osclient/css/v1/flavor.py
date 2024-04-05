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
from osc_lib.command import command

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)

CSS_ENGINE_VERSIONS = ('7.6.2', '7.9.3', '7.10.2')

CSS_NODE_TYPES = (
    'ess',
    'ess-master',
    'ess-client',
    'ess-cold',
)


class ListFlavors(command.Lister):
    _description = _('List Supported Flavors for a Cluster Version.')
    columns = (
        'Id',
        'Name',
        'Version',
        'Type',
        'Availability Zones',
        'Disk Range',
        'vCPUs',
        'RAM',
    )

    def get_parser(self, prog_name):
        parser = super(ListFlavors, self).get_parser(prog_name)

        parser.add_argument(
            '--datastore-version',
            metavar='<datastore_version>',
            type=lambda s: s.lower(),
            choices=CSS_ENGINE_VERSIONS,
            help=_(
                'CSS Cluster Engine Versions. Supported Versions: '
                '{' + ', '.join(CSS_ENGINE_VERSIONS) + '}'
            ),
        )
        parser.add_argument(
            '--node-type',
            metavar='<node_type>',
            type=lambda s: s.lower(),
            choices=CSS_NODE_TYPES,
            help=_(
                'Specify Cluster Node Type. Supported Types: '
                '{' + ', '.join(CSS_NODE_TYPES) + '}'
            ),
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.css
        data = client.flavors()

        node_type = parsed_args.node_type
        datastore_version = parsed_args.datastore_version

        return (
            self.columns,
            (
                utils.get_item_properties(s, self.columns)
                for s in data
                if (not node_type or s.type == node_type)
                and (not datastore_version or s.version == datastore_version)
            ),
        )
