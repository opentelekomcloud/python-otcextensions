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


class ListTrainingJobFlavors(command.Lister):
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
        parser = super(ListTrainingJobFlavors, self).get_parser(prog_name)
        parser.add_argument(
            "--job-type",
            metavar="{train, infer_type}",
            type=lambda s: s.lower(),
            choices=["train", "inference"],
            help=_(
                "Job Type."
            ),
        )
        parser.add_argument(
            "--engine-id",
            metavar="<engine_id>",
            type=int,
            help=_(
                "Engine ID of a job. Default value: 0"
            ),
        )
        parser.add_argument(
            "--project-id",
            metavar="<project_id>",
            type=int,
            help=_(
                "Project type. Default value: 0"
            ),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1
        query_params = {}

        data = client.training_job_flavors(**query_params)

        return (
            self.columns,
            (utils.get_item_properties(s, self.columns) for s in data),
        )
