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

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)

INFER_TYPE_CHOICES = ["real-time", "batch"]


class ListJobEngines(command.Lister):
    _description = _("List job engine Specifications.")
    columns = (
        "Engine Id",
        "Engine Name",
        "Engine Type",
        "Engine Version",
    )

    def get_parser(self, prog_name):
        parser = super(ListJobEngines, self).get_parser(prog_name)
        parser.add_argument(
            "--job-type",
            metavar="{train, inference}",
            type=lambda s: s.lower(),
            choices=["train", "inference"],
            help=_("Job Type."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1
        query_params = {}
        if parsed_args.job_type:
            query_params["job_type"] = parsed_args.job_type

        data = client.job_engines(**query_params)

        return (
            self.columns,
            (utils.get_item_properties(s, self.columns) for s in data),
        )
