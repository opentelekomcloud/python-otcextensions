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
"""ModelArts data import task v2 action implementations"""
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


class ListDatasetImportTasks(command.Lister):
    _description = _("Get properties of a vm")
    columns = ("Task Id", "Created At", "Status")

    def get_parser(self, prog_name):
        parser = super(ListDatasetImportTasks, self).get_parser(prog_name)
        parser.add_argument(
            "dataset",
            metavar="<dataset>",
            help=_("Dataset Id or Name."),
        )
        parser.add_argument(
            "--limit",
            metavar="<limit>",
            type=int,
            help=_(
                "Maximum number of records returned on each "
                "page. The default value is 10."
            ),
        )
        parser.add_argument(
            "--offset",
            metavar="<offset>",
            type=int,
            help=_("Start page of the paging list. The default value is 0."),
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2

        dataset = client.find_dataset(
            parsed_args.dataset, ignore_missing=False
        )

        query = {}
        if parsed_args.limit:
            query["limit"] = parsed_args.limit
        if parsed_args.offset:
            query["offset"] = parsed_args.offset

        data = client.dataset_import_tasks(dataset, **query)

        formatters = {
            "Created At": cli_utils.UnixTimestampFormatter,
        }

        return (
            self.columns,
            (
                utils.get_dict_properties(
                    s, self.columns, formatters=formatters
                )
                for s in data
            ),
        )


class ShowDatasetImportTask(command.ShowOne):
    _description = _("Show details of a MA dataset import task")

    def get_parser(self, prog_name):
        parser = super(ShowDatasetImportTask, self).get_parser(prog_name)

        parser.add_argument(
            "dataset",
            metavar="<dataset>",
            help=_("Enter dataset name or Id."),
        )

        parser.add_argument(
            "taskId",
            metavar="<taskId>",
            help=_("Enter task id."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2

        dataset = client.find_dataset(
            parsed_args.dataset, ignore_missing=False
        )

        obj = client.get_dataset_import_task(dataset, parsed_args.taskId)
        display_columns, columns = _get_columns(obj)
        formatters = {
            "created_at": cli_utils.UnixTimestampFormatter,
            "updated_at": cli_utils.UnixTimestampFormatter,
        }
        data = utils.get_item_properties(obj, columns, formatters=formatters)

        return (display_columns, data)
