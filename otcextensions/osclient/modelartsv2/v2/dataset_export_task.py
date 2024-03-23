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


def _flatten_output(obj):
    data = {"export_tasks": obj.export_tasks}
    return data


class CreateDatasetExportTask(command.ShowOne):
    _description = _("Create a ModelArts dataset export task")

    def get_parser(self, prog_name):
        parser = super(CreateDatasetExportTask, self).get_parser(prog_name)
        parser.add_argument(
            "--path",
            metavar="<path>",
            required=True,
            help=_(
                "Dataset name. The value is a string of 1 to 100 "
                "characters consisting of only digits, letters, "
                "underscores (_), and hyphens (-). "
                "Example value: dataset-9f3b"
            ),
        )
        parser.add_argument(
            "--version-id",
            metavar="<version_id>",
            help=_(
                "Dataset type. Possible values: "
                "\n0: image classification"
                "\n1: object detection"
                "\n100: text classification"
                "\n101: named entity recognition"
                "\n102: text triplet"
                "\n200: sound classification"
                "\n201: speech content"
                "\n202: speech start and end points"
                "\n900: custom format"
            ),
        )
        parser.add_argument(
            "--data-sources",
            metavar="<data_sources>",
            help=_(
                "Quantity of the partitions into which data records in "
                "the newly created DIS stream will be distributed. "
                "Partitions are the base throughput unit of a DIS stream. "
                "The value range varies depending on the value of "
                "stream_type."
            ),
        )
        parser.add_argument(
            "--work-path",
            metavar="<work_path>",
            help=_("Type of the source data."),
        )
        parser.add_argument(
            "--work-path-type",
            metavar="<work_path_type>",
            help=_(
                "Source data structure that defines JOSN and CSV formats. "
                "It is described in the syntax of Avro. "
                "For details about Avro, see "
                "http://avro.apache.org/docs/current/#schemas."
            ),
        )
        parser.add_argument(
            "--labels",
            metavar="<labels>",
            help=_(
                "Period of time for which data is retained in the "
                "DIS stream."
                "\nValue range: N x 24, where N is an integer from 1 to 7."
                "\nUnit: hour"
                "\nDefault value: 24"
                "\nIf this parameter is left unspecified, "
                "the default value will be used."
            ),
        )
        parser.add_argument(
            "--description",
            metavar="<description>",
            help=_(
                "Dataset description. The value is a string of 0 to 256 "
                "characters. Special characters !<>=&\"' are not "
                "allowed. By default, this parameter is left blank."
            ),
        )
        parser.add_argument(
            "--import-annotations",
            metavar="<import_annotations>",
            help=_(
                "Whether to synchronize the labels in the input path when "
                "creating an object detection or image classification "
                "dataset. The default value is true."
                "\ntrue: Import labels."
                "\nfalse: Do not import labels."
            ),
        )
        parser.add_argument(
            "--label-format",
            metavar="<label_format>",
            help=_(
                "Label format information. This parameter is used only "
                "when a text classification dataset is created."
            ),
        )
        parser.add_argument(
            "--workspace-id",
            metavar="<workspace_id>",
            help=_(
                "Workspace ID. If no workspace is created, the default "
                "value is 0. If a workspace is created and used, "
                "use the actual value."
            ),
        )
        parser.add_argument(
            "--data-type",
            default=0,
            metavar="<data_type>",
            help=_("Data source type. Possible values are as follows: OBS"),
        )
        parser.add_argument(
            "--data-path",
            metavar="<data_path>",
            # required=True,
            help=_(
                "Path of the data source. The value is a string of "
                "3 to 1,024 characters."
            ),
        )
        parser.add_argument(
            "--name",
            metavar="<name>",
            # required=True,
            help=_(
                "Label name The value can contain 1 to 32 characters, "
                "including Chinese characters, digits, letters, "
                "underscores (_), and hyphens (-)."
            ),
        )
        parser.add_argument(
            "--type",
            metavar="<type>",
            help=_(
                "Label type. The value range is the same as that of the "
                "dataset type. If this parameter is not passed, the "
                "current dataset type is used by default."
            ),
        )
        parser.add_argument(
            "--property",
            metavar="<property>",
            help=_(
                "Label attributes. For details, see Table 5. If no "
                "built-in or custom attribute needs to be set for labels, "
                "this field can be omitted or left blank "
                "(the parameter value is {})."
            ),
        )
        parser.add_argument(
            "--label-type",
            metavar="<label_type>",
            help=_("Label format. The default value is 1."),
        )
        parser.add_argument(
            "--text-sample-separator",
            metavar="<text_sample_separator>",
            help=_(
                "Separator between the text and label. By default, "
                "the Tab key is used as the separator. The separator "
                "needs to be escaped."
            ),
        )
        parser.add_argument(
            "--text-label-separator",
            metavar="<text_label_separator>",
            help=_(
                "Separator between labels. By default, the comma (,) is "
                "used as the separator. The separator needs to be escaped."
            ),
        )
        parser.add_argument(
            "--dataset-id", metavar="<dataset_id>", help=_("Dataset ID ")
        )
        parser.add_argument(
            "--error-code",
            metavar="<text_label_separator>",
            help=_(
                "Error code of a failed API call. For details, see "
                "Error Code. This parameter is not included when the "
                "API call succeeds. "
            ),
        )
        parser.add_argument(
            "--error-msg",
            metavar="<error_msg>",
            help=_(
                "Error message of a failed API call. This parameter "
                "is not included when the API call succeeds. "
            ),
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2

        attrs = {}
        """
        if parsed_args.dataset_name:
            attrs['dataset_name'] = parsed_args.dataset_name
        if parsed_args.dataset_type:
            attrs['dataset_type'] = parsed_args.dataset_type
        if parsed_args.data_path and parsed_args.data_type:
            attrs['data_sources'] = [{"data_type": parsed_args.data_type,
                                      "data_path": parsed_args.data_path}]
        """
        if parsed_args.work_path:
            attrs["work_path"] = parsed_args.work_path
        if parsed_args.work_path_type:
            attrs["work_path_type"] = parsed_args.work_path_type
        if parsed_args.labels:
            attrs["labels"] = parsed_args.labels
        if parsed_args.description:
            attrs["description"] = parsed_args.description
        if parsed_args.import_annotations:
            attrs["import_annotations"] = parsed_args.import_annotations
        if parsed_args.label_format:
            attrs["label_format"] = parsed_args.label_format
        if parsed_args.workspace_id:
            attrs["workspace_id"] = parsed_args.workspace_id
        if parsed_args.data_type:
            attrs["data_type"] = parsed_args.data_type
        if parsed_args.data_path:
            attrs["data_path"] = parsed_args.data_path
        if parsed_args.name:
            attrs["name"] = parsed_args.name
        if parsed_args.type:
            attrs["type"] = parsed_args.type
        if parsed_args.property:
            attrs["property"] = parsed_args.property
        if parsed_args.label_type:
            attrs["label_type"] = parsed_args.label_type
        if parsed_args.text_sample_separator:
            attrs["text_sample_separator"] = parsed_args.text_sample_separator
        if parsed_args.text_label_separator:
            attrs["text_label_separator"] = parsed_args.text_label_separator
        if parsed_args.dataset_id:
            attrs["dataset_id"] = parsed_args.dataset_id
        if parsed_args.error_code:
            attrs["error_code"] = parsed_args.error_code
        if parsed_args.error_msg:
            attrs["error_msg"] = parsed_args.error_msg
        if parsed_args.path:
            attrs["path"] = parsed_args.path
        obj = client.create_dataset_export_task(**attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class ShowDatasetExportTask(command.ShowOne):
    _description = _("Show details of a MA dataset export task")

    def get_parser(self, prog_name):
        parser = super(ShowDatasetExportTask, self).get_parser(prog_name)

        parser.add_argument(
            "datasetId", metavar="<dataset_id>", help=_("Enter dataset id")
        )

        parser.add_argument(
            "taskId", metavar="<task_id>", help=_("Enter task id")
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2
        query = {}

        if parsed_args.datasetId:
            query["dataset_id"] = parsed_args.datasetId

        if parsed_args.taskId:
            query["task_id"] = parsed_args.taskId

        formatters = {"export_params": cli_utils.YamlFormat}
        obj = client.get_dataset_export_task(**query)
        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=formatters)

        return (display_columns, data)


class ListDatasetExportTasks(command.Lister):
    _description = _("Get properties of a vm")
    columns = ("task_id", "path", "status", "progress")

    def get_parser(self, prog_name):
        parser = super(ListDatasetExportTasks, self).get_parser(prog_name)
        parser.add_argument(
            "datasetId",
            metavar="<dataset_id>",
            help=_("Name of the dataset to delete."),
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

        query = {}
        if parsed_args.datasetId:
            query["dataset_id"] = parsed_args.datasetId
        if parsed_args.limit:
            query["limit"] = parsed_args.limit
        if parsed_args.offset:
            query["offset"] = parsed_args.offset
        if parsed_args.export_type or str(parsed_args.export_type) == "0":
            query["export_type"] = parsed_args.export_type
        data = client.dataset_export_tasks(**query)
        return (
            self.columns,
            (utils.get_item_properties(s, self.columns) for s in data),
        )
