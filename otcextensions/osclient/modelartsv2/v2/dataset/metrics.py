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
"""ModelArts dataset v2 action implementations"""
import logging

from osc_lib import utils
from osc_lib.command import command
from otcextensions.common import cli_utils
from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)

_formatters = {
    "deletion_stats": cli_utils.YamlFormat,
    "key_sample_stats": cli_utils.YamlFormat,
    "label_stats": cli_utils.YamlFormat,
    "metadata_stats": cli_utils.YamlFormat,
    "sample_stats": cli_utils.YamlFormat,
}


def _get_columns(item):
    column_map = {}
    hidden = ["location"]
    return sdk_utils.get_osc_show_columns_for_sdk_resource(
        item, column_map, hidden
    )


class Metrics(command.ShowOne):
    _description = _("Show metrics of a Modelarts dataset.")

    def get_parser(self, prog_name):
        parser = super(Metrics, self).get_parser(prog_name)
        parser.add_argument(
            "datasetId",
            metavar="<datasetId>",
            help=_("Dataset ID."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2

        data = client.get_dataset_metrics(parsed_args.datasetId)

        display_columns, columns = _get_columns(data)

        data = utils.get_item_properties(data, columns, formatters=_formatters)

        return display_columns, data
