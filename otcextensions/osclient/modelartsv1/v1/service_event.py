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
"""ModelArts Service Update Logs v1 action implementations"""
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.common import cli_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


class ServiceEvents(command.Lister):
    _description = _("List update logs of a real-time service.")
    columns = (
        "Occur Time",
        "Event Type",
        "Event Info",
    )

    def get_parser(self, prog_name):
        parser = super(ServiceEvents, self).get_parser(prog_name)

        parser.add_argument(
            "service",
            metavar="<service>",
            help=_("Service ID or Name."),
        )
        parser.add_argument(
            "--event-type",
            metavar="<event_type>",
            help=_(
                "Type of the event to be filtered. By default, the event "
                "type is not filtered. Options:"
                "\n`normal`: normal events"
                "\n`abnormal`: abnormal events"
            ),
        )
        parser.add_argument(
            "--start-time",
            metavar="<start_time>",
            type=int,
            help=_(
                "Start time of the event to be filtered. The value is "
                "milliseconds."
            ),
        )
        parser.add_argument(
            "--end-time",
            metavar="<end_time>",
            type=int,
            help=_(
                "End time of the event to be filtered. The value is "
                "milliseconds."
            ),
        )
        parser.add_argument(
            "--offset",
            metavar="<offset>",
            type=int,
            help=_("Start page of the paging list. Default value: 0"),
        )
        parser.add_argument(
            "--limit",
            metavar="<limit>",
            type=int,
            help=_(
                "Maximum number of records returned on each page. "
                "Default value: 1000"
            ),
        )
        parser.add_argument(
            "--sort-by",
            metavar="<sort_by>",
            help=_(
                "Specified sorting field. The default value is occur_time."
            ),
        )
        parser.add_argument(
            "--order",
            metavar="<order>",
            help=_(
                "Sorting mode. The default value is desc. Options:"
                "\n`asc`: ascending order"
                "\n`desc`: descending order"
            ),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1
        args_list = (
            "end_time",
            "event_type",
            "limit",
            "offset",
            "order",
            "sort_by",
            "start_time",
        )
        query_params = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val or str(val) == "0":
                query_params[arg] = val

        service = client.find_service(
            parsed_args.service, ignore_missing=False
        )
        data = client.service_events(service.id, **query_params)

        formatters = {
            "Occur Time": cli_utils.UnixTimestampFormatter,
        }

        return (
            self.columns,
            (
                utils.get_item_properties(
                    s, self.columns, formatters=formatters
                )
                for s in data
            ),
        )
