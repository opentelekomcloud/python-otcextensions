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
"""ModelArts service v1 action implementations"""
import logging

from osc_lib import utils
from osc_lib.command import command
from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _flatten_output(obj):
    data = {
        "service_name": obj.service_name,
        "service_id": obj.service_id,
        "events": obj.events,
        "total_count": obj.total_count,
        "count": obj.count,
    }
    return data


def _get_columns(item):
    column_map = {}
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


class ListServiceEventLogs(command.Lister):
    _description = _("Get properties of a service")
    columns = ("service_name", "service_id", "events", "total_count", "count")

    table_columns = (
        "service_name",
        "service_id",
        "events",
        "total_count",
        "count",
    )

    def get_parser(self, prog_name):
        parser = super(ListServiceEventLogs, self).get_parser(prog_name)
        parser.add_argument(
            "--service_id",
            metavar="<service_id>",
            help=_("ID of the service."),
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1

        query = {}
        if parsed_args.service_id:
            query["service_id"] = parsed_args.service_id

        data = client.service_event_logs(**query)

        table = (
            self.columns,
            (
                utils.get_dict_properties(_flatten_output(s), self.columns)
                for s in data
            ),
        )
        return table
