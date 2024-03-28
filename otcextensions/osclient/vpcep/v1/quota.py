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
"""VPC Endpoint Service v1 action implementations"""
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _get_columns(item):
    column_map = {}
    hidden = [
        'location',
    ]
    return sdk_utils.get_osc_show_columns_for_sdk_resource(
        item, column_map, hidden
    )


class ListQuota(command.Lister):

    _description = _('List VPC endpoint resource quotas.')
    columns = (
        'Type',
        'Quota',
        'Used',
    )

    def get_parser(self, prog_name):
        parser = super(ListQuota, self).get_parser(prog_name)
        parser.add_argument(
            '--type',
            metavar='{endpoint, endpoint_service}',
            type=lambda s: s.lower(),
            choices=['endpoint', 'endpoint_service'],
            help=_('Specify the resource type.'),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.vpcep
        data = client.resource_quota(getattr(parsed_args, 'type'))

        return (
            self.columns,
            (utils.get_item_properties(s, self.columns) for s in data),
        )
