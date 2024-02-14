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
"""ModelArts Querying a Built-in Algorithm"""
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


class ShowBuiltinAlgorithm(command.ShowOne):
    _description = _("Querying a Built-in Algorithm")

    def get_parser(self, prog_name):
        parser = super(ShowBuiltinAlgorithm, self).get_parser(prog_name)
        parser.add_argument(
            "--per_page",
            metavar="<per_page>",
            required=False,
            type=int,
            help=_("Number of job parameters displayed on each page"),
        )
        parser.add_argument(
            "--page",
            metavar="<page>",
            required=False,
            type=int,
            help=_("Index of the page to be queried"),
        )
        parser.add_argument(
            "--sortBy",
            metavar="<sortBy>",
            required=False,
            type=str,
            help=_("Sorting mode of the query"),
        )
        parser.add_argument(
            "--order",
            metavar="<order>",
            required=False,
            type=str,
            help=_("Sorting order"),
        )
        parser.add_argument(
            "--search_content",
            metavar="<search_content>",
            required=False,
            type=str,
            help=_("Search content, for example, a parameter name"),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1
        attrs = {}
        args_list = (
            "per_page",
            "page",
            "sortBy",
            "order",
            "search_content",
        )
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        data = client.show_builtin_algorithms()
        display_columns, columns = _get_columns(data)
        data = utils.get_item_properties(data)

        return display_columns, data
