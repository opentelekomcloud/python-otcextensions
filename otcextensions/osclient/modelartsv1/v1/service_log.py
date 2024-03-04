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


class ServiceLogs(command.Lister):
    _description = _("List update logs of a real-time service.")
    columns = (
        "Update Time",
        "Result",
        "Config",
        "Result Detail",
    )

    def get_parser(self, prog_name):
        parser = super(ServiceLogs, self).get_parser(prog_name)

        parser.add_argument(
            "service",
            metavar="<service>",
            help=_("Service ID or Name."),
        )
        parser.add_argument(
            "--update-time",
            metavar="<update_time>",
            type=int,
            help=_(
                "Update time for filtering. This parameter can be used to "
                "obtain the update logs of a real-time service. By default, "
                "the filtering by update time is disabled."
            ),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1
        query_params = {}
        if parsed_args.update_time:
            query_params["update_time"] = parsed_args.update_time

        service = client.find_service(parsed_args.service)
        data = client.service_logs(service.id, **query_params)

        formatters = {
            "Update Time": cli_utils.UnixTimestampFormatter,
            "Config": cli_utils.YamlFormat,
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
