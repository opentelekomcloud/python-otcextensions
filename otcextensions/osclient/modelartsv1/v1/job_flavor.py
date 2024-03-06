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

from cliff import columns as cliff_columns
from osc_lib import utils
from osc_lib.command import command
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


class ProjectType(cliff_columns.FormattableColumn):
    CHOICES_MAP = {
        0: "non-ExeML project",
        1: "ExeML job for image classification",
        2: "ExeML job for object detection",
        3: "ExeML job for predictive analytics",
    }
    STR = "\n".join(f"{key}: {value}" for key, value in CHOICES_MAP.items())

    def human_readable(self):
        return self.CHOICES_MAP.get(self._value, str(self._value))


class ListJobFlavors(command.Lister):
    _description = _("List Training job resource Specifications.")
    columns = (
        "Spec Id",
        "Spec Code",
        "Core",
        "CPU",
        "GPU Num",
        "GPU Type",
    )

    def get_parser(self, prog_name):
        parser = super(ListJobFlavors, self).get_parser(prog_name)
        parser.add_argument(
            "--job-type",
            metavar="{train, inference}",
            type=lambda s: s.lower(),
            choices=["train", "inference"],
            help=_("Job Type."),
        )
        parser.add_argument(
            "--engine-id",
            metavar="<engine_id>",
            type=int,
            help=_("Engine ID of a job. Default value: 0"),
        )
        parser.add_argument(
            "--project-type",
            metavar="<project_type>",
            choices=list(ProjectType.CHOICES_MAP.keys()),
            type=int,
            help=_("Project type. Default value: 0\n" + ProjectType.STR),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1
        query_params = {}
        for arg in ("job_type", "engine_id", "project_type"):
            val = getattr(parsed_args, arg)
            if val or str(val) == "0":
                query_params[arg] = val

        data = client.job_flavors(**query_params)

        return (
            self.columns,
            (utils.get_item_properties(s, self.columns) for s in data),
        )
