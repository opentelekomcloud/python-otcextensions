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
"""ModelArts labels v2 action implementations"""
import logging

from osc_lib import utils
from osc_lib.command import command
from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _get_columns(item):
    column_map = {}
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


class ListDatasetLabels(command.Lister):
    _description = _("This API is used to query all samples of a dataset.")
    columns = ("name", "type")

    def get_parser(self, prog_name):
        parser = super(ListDatasetLabels, self).get_parser(prog_name)
        parser.add_argument(
            "dataset",
            metavar="<dataset>",
            help=_("Dataset Id or name."),
        )
        parser.add_argument(
            "--version-id",
            metavar="<version_id>",
            help=_("Dataset version id."),
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2

        params = {}
        if parsed_args.version_id:
            params["version_id"] = parsed_args.version_id
        dataset = client.find_dataset(parsed_args.dataset)
        data = client.dataset_labels(dataset.id, **params)

        formatters = {}
        return (
            self.columns,
            (
                utils.get_dict_properties(
                    s, self.columns, formatters=formatters
                )
                for s in data
            ),
        )
