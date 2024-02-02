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

from cliff import columns as cliff_columns
from osc_lib import exceptions
from osc_lib import utils
from osc_lib.cli import parseractions
from osc_lib.command import command
from otcextensions.common import cli_utils
from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)

SORT_BY_CHOICES = ["create_time", "dataset_name"]

SORT_ORDER_CHOICES = ["asc", "desc"]


DATASET_TYPES_VALUE_MAP = {
    0: "image classification",
    1: "object detection",
    100: "text classification",
    101: "named entity recognition",
    102: "text triplet",
    200: "sound classification",
    201: "speech content",
    202: "speech paragraph labeling",
    400: "table dataset",
    600: "video labeling",
    900: "custom format",
}

DATASET_STATUS_VALUE_MAP = {
    0: "creating dataset",
    1: "normal dataset",
    2: "deleting dataset",
    3: "deleted dataset",
    4: "abnormal dataset",
    5: "synchronizing dataset",
    6: "releasing dataset",
    7: "dataset in version switching",
    8: "importing dataset",
}

RUNNING_TASK_VALUES_MAP = {
    0: "auto labeling",
    1: "pre-labeling",
    2: "export",
    3: "version switch",
    4: "manifest file export",
    5: "manifest file import",
    6: "version publishing",
    7: "auto grouping",
    10: "one-click model deployment (default value)",
}

VERSION_FORMAT_VALUES_MAP = {
    0: "default format",
    1: "CarbonData (supported only by table datasets)",
    2: "CSV",
}


class DatasetType(cliff_columns.FormattableColumn):
    def human_readable(self):
        return DATASET_TYPES_VALUE_MAP.get(self._value, str(self._value))


class DatasetStatus(cliff_columns.FormattableColumn):
    def human_readable(self):
        return DATASET_STATUS_VALUE_MAP.get(self._value, str(self._value))


_formatters = {
    "labels": cli_utils.YamlFormat,
    "create_time": cli_utils.UnixTimestampFormatter,
    "data_sources": cli_utils.YamlFormat,
    "update_time": cli_utils.UnixTimestampFormatter,
}


def _get_columns(item):
    column_map = {}
    hidden = ["location"]
    return sdk_utils.get_osc_show_columns_for_sdk_resource(
        item, column_map, hidden
    )


class CreateDataset(command.ShowOne):
    _description = _("Create a ModelArts dataset")

    def get_parser(self, prog_name):
        parser = super(CreateDataset, self).get_parser(prog_name)
        parser.add_argument(
            "name",
            metavar="<name>",
            help=_("Dataset name."),
        )
        parser.add_argument(
            "--dataset-type",
            metavar="<dataset_type>",
            choices=list(DATASET_TYPES_VALUE_MAP.keys()),
            type=int,
            required=True,
            help=(
                "Dataset type. Possible values:\n"
                + "\n".join(
                    [
                        f"{key}: {value}"
                        for key, value in DATASET_TYPES_VALUE_MAP.items()
                    ]
                )
            ),
        )
        parser.add_argument(
            "--data-source",
            metavar="data_type=<data_type>,data_path=<data_path>",
            required_keys=["data_type", "data_path"],
            dest="data_sources",
            action=parseractions.MultiKeyValueAction,
            required=True,
            help=_(
                "Input dataset path and type.\n"
                "The following keys are required:\n"
                "data_type=<data_type>: Input data source type\n"
                "data_path=<data_path>: PData source path."
            ),
        )
        parser.add_argument(
            "--description",
            metavar="<description>",
            help=_("Dataset description."),
        )
        parser.add_argument(
            "--import-annotations",
            action="store_true",
            help=_(
                "Whether to automatically import the labeling information "
                "in the input directory."
            ),
        )
        parser.add_argument(
            "--import-data",
            action="store_true",
            help=_(
                "Whether to import data. This parameter is used only "
                "for table datasets."
            ),
        )
        parser.add_argument(
            "--label-format",
            metavar=(
                "label_type=<label_type>,"
                "text_label_separator=<text_label_separator>,"
                "text_sample_separator=<text_sample_separator>"
            ),
            required_keys=[],
            dest="label_format",
            action=parseractions.MultiKeyValueAction,
            help=_(
                "Label format information. This parameter "
                "is used only for text datasets."
                "label_type=<label_type>: Label type of text classification.\n"
                "text_label_separator=<text_label_separator>: Separator "
                "between labels. By default, a comma (,) is used as the "
                "separator.\n"
                "text_sample_separator=<text_sample_separator>: Separator "
                "between the text and label. By default, the Tab key is "
                "used as the separator."
            ),
        )
        parser.add_argument(
            "--managed",
            action="store_true",
            help=_("Whether to host a dataset."),
        )
        parser.add_argument(
            "--work-path",
            metavar="<work_path>",
            required=True,
            help=_(
                "Output dataset path, which is used to store output files "
                "such as label files. The format is /Bucket name/File path, "
                "for example, /obs-bucket/flower/rose/."
            ),
        )
        parser.add_argument(
            "--work-path-type",
            metavar="<work_path_type>",
            type=int,
            default=0,
            help=_(
                "Type of the dataset output path. "
                "The options are as follows:"
                "\n0: OBS bucket (default value)"
            ),
        )
        parser.add_argument(
            "--workspace-id",
            metavar="<workspace_id>",
            help=_("Workspace ID."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2.v2

        attrs = {
            "dataset_name": parsed_args.name,
            "work_path_type": parsed_args.work_path_type,
        }
        args_list = (
            "dataset_type",
            "data_sources",
            "description",
            "import_annotations",
            "import_data",
            "label_format",
            "managed",
            "work_path",
            "workspace_id",
        )
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val
        obj = client.create_dataset(**attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class ListDataset(command.Lister):
    _description = _("Get List of Modelarts Datasets.")
    columns = (
        "Dataset Id",
        "Dataset Name",
        "Dataset Type",
        "Status",
        "Total Sample Count",
        "Annotated Sample Count",
        "Create Time",
    )

    def get_parser(self, prog_name):
        parser = super(ListDataset, self).get_parser(prog_name)
        parser.add_argument(
            "--check-running-task",
            action="store_true",
            help=_(
                "Whether to detect tasks (including initialization tasks) "
                "that are running in a dataset."
            ),
        )
        parser.add_argument(
            "--contain-versions",
            action="store_true",
            help=_("Whether the dataset contains a version."),
        )
        parser.add_argument(
            "--dataset-type",
            metavar="<dataset_type>",
            choices=list(DATASET_TYPES_VALUE_MAP.keys()),
            type=int,
            help=(
                "Dataset type. Possible values:\n"
                + "\n".join(
                    [
                        f"{key}: {value}"
                        for key, value in DATASET_TYPES_VALUE_MAP.items()
                    ]
                )
            ),
        )
        parser.add_argument(
            "--file-preview",
            action="store_true",
            help=_("Whether a dataset supports preview when it is queried."),
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
            "--order",
            metavar="{" + ",".join(SORT_ORDER_CHOICES) + "}",
            type=lambda s: s.lower(),
            choices=SORT_ORDER_CHOICES,
            help=_("Sorting order. Default value: desc"),
        )
        parser.add_argument(
            "--running-task-type",
            metavar="<running_task_type>",
            choices=list(RUNNING_TASK_VALUES_MAP.keys()),
            type=int,
            help=_(
                "Type of the running tasks (including initialization tasks) "
                "to be detected. The options are as follows:\n"
                + "\n".join(
                    [
                        f"{key}: {value}"
                        for key, value in RUNNING_TASK_VALUES_MAP.items()
                    ]
                )
            ),
        )
        parser.add_argument(
            "--search-content",
            metavar="<search_content>",
            help=_("Fuzzy search keyword."),
        )
        parser.add_argument(
            "--sort-by",
            metavar="{" + ",".join(SORT_BY_CHOICES) + "}",
            type=lambda s: s.lower(),
            choices=SORT_BY_CHOICES,
            help=_("Sorting field. Default value: publish_at"),
        )
        parser.add_argument(
            "--support-export",
            action="store_true",
            help=_(
                "Whether to filter datasets that can be exported only "
                "(including datasets of image classification, object "
                "detection, and custom format)."
            ),
        )
        parser.add_argument(
            "--train-evaluate-ratio",
            metavar="<train_evaluate_ratio>",
            help=_("Version split ratio for dataset filtering."),
        )
        parser.add_argument(
            "--version-format",
            metavar="<version_format>",
            choices=list(VERSION_FORMAT_VALUES_MAP.keys()),
            type=int,
            help=_(
                "Dataset version format for dataset filtering. This "
                "parameter is used to filter datasets that meet the "
                "filter criteria. The options are as follows:\n"
                + "\n".join(
                    [
                        f"{key}: {value}"
                        for key, value in VERSION_FORMAT_VALUES_MAP.items()
                    ]
                )
            ),
        )
        parser.add_argument(
            "--with-labels",
            action="store_true",
            help=_("Whether to return dataset labels."),
        )
        parser.add_argument(
            "--workspace-id",
            metavar="<workspace_id>",
            help=_("Workspace ID."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2

        args_list = (
            "check_running_task",
            "contain_versions",
            "dataset_type",
            "file_preview",
            "limit",
            "offset",
            "order",
            "running_task_type",
            "search_content",
            "sort_by",
            "support_export",
            "train_evaluate_ratio",
            "version_format",
            "with_labels",
            "workspace_id",
        )
        query_params = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val or str(val) == "0":
                query_params[arg] = val

        data = client.datasets(**query_params)

        formatters = {
            "Create Time": cli_utils.UnixTimestampFormatter,
            "Dataset Type": DatasetType,
            "Status": DatasetStatus,
        }

        return (
            self.columns,
            (
                utils.get_item_properties(
                    s, self.columns, formatters=formatters
                )
                for s in data
            ),
        )


class ShowDataset(command.ShowOne):
    _description = _("Show details of a Modelarts Dataset.")

    def get_parser(self, prog_name):
        parser = super(ShowDataset, self).get_parser(prog_name)
        parser.add_argument(
            "datasetId",
            metavar="<datasetId>",
            help=_("Dataset ID/Name."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2

        data = client.get_dataset(parsed_args.datasetId)

        display_columns, columns = _get_columns(data)
        data = utils.get_item_properties(data, columns, formatters=_formatters)

        return display_columns, data


class UpdateDataset(command.ShowOne):
    _description = _("Modify details of a Modelarts Dataset.")

    def get_parser(self, prog_name):
        parser = super(UpdateDataset, self).get_parser(prog_name)
        parser.add_argument(
            "datasetId",
            metavar="<datasetId>",
            help=_("Enter Dataset ID."),
        )
        parser.add_argument(
            "--description",
            metavar="<description>",
            help=_("Enter description"),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2

        args_list = ["description"]
        attrs = {}
        for arg in args_list:
            if getattr(parsed_args, arg):
                attrs[arg] = getattr(parsed_args, arg)

        dataset = client.get_dataset(
            dataset=parsed_args.datasetId,
        )

        # dataset = client.find_dataset(parsed_args.datasetId)
        data = client.modify_dataset(dataset.id, **attrs)

        display_columns, columns = _get_columns(data)
        data = utils.get_item_properties(data, columns)

        return display_columns, data


class DeleteDataset(command.Command):
    _description = _("Delete Modelarts Dataset(s).")

    def get_parser(self, prog_name):
        parser = super(DeleteDataset, self).get_parser(prog_name)
        parser.add_argument(
            "datasetId",
            metavar="<datasetId>",
            nargs="+",
            help=_("ID of the dataset(s) to be deleted."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2
        result = 0
        for dataset_id in parsed_args.datasetId:
            try:
                client.delete_dataset(dataset_id)
            except Exception as e:
                result += 1
                LOG.error(
                    _(
                        "Failed to delete dataset with "
                        "ID '%(dataset_id)s': %(e)s"
                    ),
                    {"dataset_id": dataset_id, "e": e},
                )
        if result > 0:
            total = len(parsed_args.datasetId)
            msg = _(
                "%(result)s of %(total)s Dataset(s) failed " "to delete."
            ) % {"result": result, "total": total}
            raise exceptions.CommandError(msg)
