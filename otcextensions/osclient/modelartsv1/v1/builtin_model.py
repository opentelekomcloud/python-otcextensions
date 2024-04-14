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
"""ModelArts training job v1 action implementations"""
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.common import cli_utils
from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _get_columns(item):
    column_map = {}
    hidden = ["location"]
    return sdk_utils.get_osc_show_columns_for_sdk_resource(
        item, column_map, hidden
    )


class ListBuiltInModels(command.Lister):
    _description = _("Get properties of a vm")
    columns = (
        "Model Id",
        "Model name",
        "Model Usage",
        "Model Precision",
        "Model Size",
        "Created At",
    )

    def get_parser(self, prog_name):
        parser = super(ListBuiltInModels, self).get_parser(prog_name)

        sort_by_choices = [
            "create_time",
            "engine",
            "model_name",
            "model_precision",
            "model_usage",
            "model_precision",
            "model_size" "parameter",
        ]

        parser.add_argument(
            "--limit",
            metavar="<limit>",
            type=int,
            help=_(
                "Number of built-in algorithms displayed on each page. "
                "The value range is [1, 100]. Default value: 10."
            ),
        )
        parser.add_argument(
            "--offset",
            metavar="<offset>",
            type=int,
            help=_("Index of the page to be queried. Default value: 1"),
        )
        parser.add_argument(
            "--sort-by",
            metavar="{" + ",".join(sort_by_choices) + "}",
            type=lambda s: s.lower(),
            choices=sort_by_choices,
            help=_("Sorting field. Default value: job_name"),
        )
        parser.add_argument(
            "--order",
            metavar="{asc, desc}",
            type=lambda s: s.lower(),
            choices=["asc", "desc"],
            help=_("Sorting order. Default value: desc"),
        )
        parser.add_argument(
            "--search-content",
            metavar="<search_content>",
            help=_("Search content, for example, a parameter name."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1

        attrs_list = (
            "limit",
            "offset",
            "sort_by",
            "order",
            "search_content",
        )
        query_params = {}
        for arg in attrs_list:
            val = getattr(parsed_args, arg)
            if val or str(val) == "0":
                query_params[arg] = val

        data = client.builtin_models(**query_params)
        _formatters = {
            "Created At": cli_utils.UnixTimestampFormatter,
        }
        table = (
            self.columns,
            (
                utils.get_dict_properties(
                    s, self.columns, formatters=_formatters
                )
                for s in data
            ),
        )
        return table


class ShowBuiltInModel(command.ShowOne):
    _description = _("Show details of a built-in model")

    def get_parser(self, prog_name):
        parser = super(ShowBuiltInModel, self).get_parser(prog_name)
        parser.add_argument(
            "name",
            metavar="<name>",
            help=_("Enter model built-in model name."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1
        data = client.find_builtin_model(
            parsed_args.name, ignore_missing=False
        )

        display_columns, columns = _get_columns(data)

        formatters = {
            "created_at": cli_utils.UnixTimestampFormatter,
            "parameter": cli_utils.YamlFormat,
        }
        data = utils.get_item_properties(data, columns, formatters=formatters)
        return (display_columns, data)
