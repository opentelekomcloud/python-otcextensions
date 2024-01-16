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
"""ModelArts Querying Dedicated Resource Pools v1 action implementations"""

import logging

from osc_lib import utils
from osc_lib.command import command
from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _flatten_output(obj):
    data = {
        "total_count,": obj.total_count,
        "count": obj.count,
        "clusters": obj.clusters,
    }
    return data


def _get_columns(item):
    column_map = {}
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


class ListDedicatedResourcePools(command.Lister):
    _description = _("This API is used to query dedicated resource pools.")
    columns = ("total_count", "count", "clusters")

    table_columns = ("total_count", "count", "clusters")

    def get_parser(self, prog_name):
        parser = super(ListDedicatedResourcePools, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1

        query = {}
        data = client.dedic_res_pools(**query)

        table = (
            self.columns,
            (
                utils.get_dict_properties(_flatten_output(s), self.columns)
                for s in data
            ),
        )
        return table
