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


class ListServiceFlavors(command.Lister):
    _description = _("List Service Deployment Specifications.")
    columns = (
        "Specification",
        "Billing Spec",
        "Spec Status",
        "Is Open",
        "Is Free",
        "Over Quota",
        "Display EN",
        "Extend Params",
    )

    def get_parser(self, prog_name):
        parser = super(ListServiceFlavors, self).get_parser(prog_name)
        parser.add_argument(
            "--is-personal-cluster",
            action="store_true",
            help=_(
                "Whether to query the service deployment specifications "
                "supported by dedicated resource pool. "
                "The default value is false."
            ),
        )
        parser.add_argument(
            "--infer-type",
            metavar="{" + ",".join(INFER_TYPE_CHOICES) + "}",
            type=lambda s: s.lower(),
            choices=INFER_TYPE_CHOICES,
            help=_(
                "Inference mode. The default value is real-time. "
                "The value can be `real-time` or `batch`."
            ),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1
        query_params = {}
        if parsed_args.is_personal_cluster:
            query_params["is_personal_cluster"] = True
        if parsed_args.infer_type:
            query_params["infer_type"] = parsed_args.infer_type

        data = client.service_flavors(**query_params)

        return (
            self.columns,
            (utils.get_item_properties(s, self.columns) for s in data),
        )
