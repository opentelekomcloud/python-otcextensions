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
"""ModelArts training job version v1 action implementations"""
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


class TrainingjobVersionLogfileName(command.ShowOne):
    _description = _("Obtain the name of a training job log file")

    def get_parser(self, prog_name):
        parser = super(TrainingjobVersionLogfileName, self).get_parser(
            prog_name
        )
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
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1
        attrs = {}
        args_list = ["job_id", "version_id"]
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        data = client.show_trainingjob_version_logfile_name(**attrs)
        display_columns, columns = _get_columns(data)
        data = utils.get_item_properties(data, columns)

        return display_columns, data
