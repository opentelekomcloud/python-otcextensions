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
"""ModelArts v1 trainingjob version action implementations"""
import logging

from osc_lib import utils
from osc_lib.command import command
from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _get_columns(item):
    column_map = {}
    hidden = ["location"]
    return sdk_utils.get_osc_show_columns_for_sdk_resource(
        item, column_map, hidden
    )


class TrainingjobVersionLogs(command.ShowOne):
    _description = _(
        "Query detailed information about training job logs by row"
    )

    def get_parser(self, prog_name):
        parser = super(TrainingjobVersionLogs, self).get_parser(prog_name)
        parser.add_argument(
            "--job_id",
            metavar="<job_id>",
            required=True,
            type=int,
            help=_("ID of a training job"),
        )
        parser.add_argument(
            "--version_id",
            metavar="<version_id>",
            required=True,
            type=int,
            help=_("Version ID of a training job"),
        )
        parser.add_argument(
            "--base_line",
            metavar="<base_line>",
            required=False,
            type=str,
            help=_(
                "Base line of the log, which is obtained from an API response"
            ),
        )
        parser.add_argument(
            "--lines",
            metavar="<lines>",
            required=False,
            type=int,
            help=_("Length of the obtained log"),
        )
        parser.add_argument(
            "--log_file",
            metavar="<log_file>",
            required=True,
            type=str,
            help=_("Name of the log file to be viewed"),
        )
        parser.add_argument(
            "--order",
            metavar="<order>",
            required=False,
            type=str,
            help=_("Log query directiondesc: Query next records"),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1
        attrs = {}
        args_list = [
            "project_id",
            "job_id",
            "version_id",
            "base_line",
            "lines",
            "log_file",
            "order",
        ]
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        data = client.list_trainingjob_version_logs(**attrs)
        display_columns, columns = _get_columns(data)
        data = utils.get_item_properties(data)

        return display_columns, data
