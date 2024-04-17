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
"""ModelArts dataset export task v2 action implementations"""
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.common import cli_utils
from otcextensions.common import sdk_utils
from otcextensions.i18n import _


LOG = logging.getLogger(__name__)


EXPORT_TYPE_CHOICES_MAP = {
    0: "labeled",
    1: "unlabeled",
    2: "all",
    4: "conditional search",
}


def _get_columns(item):
    column_map = {}
    hidden = ["location"]
    return sdk_utils.get_osc_show_columns_for_sdk_resource(
        item, column_map, hidden
    )


class ShowDatasetExportTask(command.ShowOne):
    _description = _("Show details of a MA dataset export task")

    def get_parser(self, prog_name):
        parser = super(ShowDatasetExportTask, self).get_parser(prog_name)

        parser.add_argument(
            "dataset",
            metavar="<dataset>",
            help=_("Dataset Id or name."),
        )
        parser.add_argument(
            "taskId",
            metavar="<taskId>",
            help=_("Enter task Id."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2
        query = {}

        if parsed_args.taskId:
            query["task_id"] = parsed_args.taskId

        dataset = client.find_dataset(
            parsed_args.dataset, ignore_missing=False
        )
        obj = client.get_dataset_export_task(dataset, parsed_args.taskId)

        formatters = {
            "created_at": cli_utils.UnixTimestampFormatter,
            "updated_at": cli_utils.UnixTimestampFormatter,
            "export_params": cli_utils.YamlFormat,
        }
        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=formatters)

        return (display_columns, data)


class ListDatasetExportTasks(command.Lister):
    _description = _("Get properties of a vm")
    columns = ("Task Id", "Created At", "Status")

    def get_parser(self, prog_name):
        parser = super(ListDatasetExportTasks, self).get_parser(prog_name)
        parser.add_argument(
            "dataset",
            metavar="<dataset>",
            help=_("Dataset Id or name."),
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
        parser.add_argument(
            "--export-type",
            choices=list(EXPORT_TYPE_CHOICES_MAP.keys()),
            type=int,
            help=_(
                "Export type. The options are as follows:\n"
                + "\n".join(
                    [
                        f"{key}: {value}"
                        for key, value in EXPORT_TYPE_CHOICES_MAP.items()
                    ]
                )
            ),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2

        dataset = client.find_dataset(
            parsed_args.dataset, ignore_missing=False
        )

        query = {}
        for arg in ('export_type', 'limit', 'offset'):
            val = getattr(parsed_args, arg)
            if val or str(val) == "0":
                query[arg] = val

        data = client.dataset_export_tasks(dataset, **query)

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
