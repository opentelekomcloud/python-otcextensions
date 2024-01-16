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
"""ModelArts dataset v1 action implementations"""
import logging

from osc_lib import utils
from osc_lib.command import command
from otcextensions.common import cli_utils
from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _flatten_output(obj):
    data = {
        "dataset_name": obj.dataset_name,
        "dataset_type": obj.dataset_type,
        "dataset_id": obj.dataset_id,
        "description": obj.description,
        "work_path": obj.work_path,
        "create_time": obj.create_time,
        "next_version_num": obj.next_version_num,
        "status": obj.status,
        "data_sources": obj.data_sources,
        "update_time": obj.update_time,
        "current_version_id": obj.current_version_id,
        "current_version_name": obj.current_version_name,
        "total_sample_count": obj.total_sample_count,
        "annotated_sample_count": obj.annotated_sample_count,
        "work_path_type": obj.work_path_type,
        "workspace_id": obj.workspace_id,
        "enterprise_project_id": obj.enterprise_project_id,
        "labels": obj.labels,
        "samples": obj.samples,
    }
    return data


_formatters = {"labels": cli_utils.YamlFormat}


def _get_columns(item):
    column_map = {}
    hidden = ["location"]
    return sdk_utils.get_osc_show_columns_for_sdk_resource(
        item, column_map, hidden
    )


class DeleteDataset(command.Command):
    _description = _("Delete ModelArts Dataset")

    def get_parser(self, prog_name):
        parser = super(DeleteDataset, self).get_parser(prog_name)
        parser.add_argument(
            "dataset_id",
            metavar="<dataset_id>",
            help=_("Name of the dataset to delete."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2.v2
        client.delete_dataset(dataset=parsed_args.dataset_id)


class CreateDataset(command.ShowOne):
    _description = _("Create a ModelArts dataset")

    def get_parser(self, prog_name):
        parser = super(CreateDataset, self).get_parser(prog_name)
        parser.add_argument(
            "--dataset_name",
            metavar="<dataset_name>",
            required=True,
            help=_(
                "Dataset name. The value is a string of 1 to 100 "
                "characters consisting of only digits, letters, "
                "underscores (_), and hyphens (-). "
                "Example value: dataset-9f3b"
            ),
        )
        parser.add_argument(
            "--dataset_type",
            metavar="<dataset_type>",
            required=True,
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
                "\n900: custom format "
            ),
        )
        parser.add_argument(
            "--data_sources",
            metavar="<data_sources>",
            help=_(
                "Quantity of the partitions into which data records in "
                "the newly created DIS stream will be distributed. "
                "Partitions are the base throughput unit of a DIS "
                "stream. The value range varies depending on the "
                "value of stream_type."
            ),
        )
        parser.add_argument(
            "--work_path",
            metavar="<work_path>",
            required=True,
            help=_("Type of the source data."),
        )
        parser.add_argument(
            "--work_path_type",
            metavar="<work_path_type>",
            action="append",
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
                "DIS stream. Value range: N x 24, where N is an "
                "integer from 1 to 7."
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
                "characters. Special characters !<>=&\"' are not allowed. "
                "By default, this parameter is left blank."
            ),
        )
        parser.add_argument(
            "--import_annotations",
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
            "--label_format",
            metavar="<label_format>",
            help=_(
                "Label format information. This parameter is used only "
                "when a text classification dataset is created."
            ),
        )
        parser.add_argument(
            "--workspace_id",
            metavar="<workspace_id>",
            help=_(
                "Workspace ID. If no workspace is created, "
                "the default value is 0. If a workspace is created "
                "and used, use the actual value. "
            ),
        )
        parser.add_argument(
            "--data_type",
            metavar="<data_type>",
            help=_("Data source type. Possible values are as follows: OBS "),
        )
        parser.add_argument(
            "--data_path",
            metavar="<data_path>",
            required=True,
            help=_(
                "Path of the data source. The value is a string of "
                "3 to 1,024 characters."
            ),
        )
        parser.add_argument(
            "--name",
            metavar="<name>",
            required=True,
            help=_(
                "Label name The value can contain 1 to 32 characters, "
                "including Chinese characters, digits, letters, "
                "underscores (_), and hyphens (-). "
            ),
        )
        parser.add_argument(
            "--type",
            metavar="<type>",
            help=_(
                "Label type. The value range is the same as that of the "
                "dataset type. If this parameter is not passed, the "
                "current dataset type is used by default. "
            ),
        )
        parser.add_argument(
            "--property",
            metavar="<property>",
            help=_(
                "Label attributes. For details, see Table 5. If no "
                "built-in or custom attribute needs to be set for labels, "
                "this field can be omitted or left blank (the parameter "
                "value is {}). "
            ),
        )
        parser.add_argument(
            "--label_type",
            metavar="<label_type>",
            help=_("Label format. The default value is 1. "),
        )
        parser.add_argument(
            "--text_sample_separator",
            metavar="<text_sample_separator>",
            help=_(
                "Separator between the text and label. By default, the "
                "Tab key is used as the separator. The separator needs "
                "to be escaped."
            ),
        )
        parser.add_argument(
            "--text_label_separator",
            metavar="<text_label_separator>",
            help=_(
                "Separator between labels. By default, the comma (,) is "
                "used as the separator. The separator needs to be escaped."
            ),
        )
        parser.add_argument(
            "--dataset_id", metavar="<dataset_id>", help=_("Dataset ID ")
        )
        parser.add_argument(
            "--error_code",
            metavar="<text_label_separator>",
            help=_(
                "Error code of a failed API call. For details, see "
                "Error Code. This parameter is not included when the "
                "API call succeeds."
            ),
        )
        parser.add_argument(
            "--error_msg",
            metavar="<error_msg>",
            help=_(
                "Error message of a failed API call. This parameter "
                "is not included when the API call succeeds."
            ),
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2.v2

        attrs = {}

        if parsed_args.dataset_name:
            attrs["dataset_name"] = parsed_args.dataset_name
        if parsed_args.dataset_type:
            attrs["dataset_type"] = parsed_args.dataset_type
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
        if parsed_args.data_path and parsed_args.data_type:
            attrs["data_sources"] = [
                {
                    "data_type": parsed_args.data_type,
                    "data_path": parsed_args.data_path,
                }
            ]

        obj = client.create_dataset(**attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class ShowDataset(command.ShowOne):
    _description = _("Show details of a MA dataset")

    def get_parser(self, prog_name):
        parser = super(ShowDataset, self).get_parser(prog_name)
        parser.add_argument(
            "dataset_id", metavar="<dataset_id>", help=_("Enter dataset id")
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2

        data = client.show_dataset(
            dataset=parsed_args.dataset_id,
        )

        display_columns, columns = _get_columns(data)
        data = utils.get_item_properties(data, columns, formatters=_formatters)

        return display_columns, data


class ModifyDataset(command.ShowOne):
    _description = _("Modify details of a MA dataset")

    def get_parser(self, prog_name):
        parser = super(ModifyDataset, self).get_parser(prog_name)
        parser.add_argument(
            "datasetId", metavar="<datasetId>", help=_("Enter dataset id")
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

        dataset = client.show_dataset(
            dataset=parsed_args.datasetId,
        )

        # dataset = client.find_dataset(parsed_args.datasetId)
        data = client.modify_dataset(dataset.id, **attrs)

        display_columns, columns = _get_columns(data)
        data = utils.get_item_properties(data, columns)

        return display_columns, data


class ListDatasets(command.Lister):
    _description = _("Get properties of a vm")
    columns = (
        "dataset_name",
        "dataset_id",
        "dataset_type",
        "description",
        "dimensions",
        "metric_name",
        "unit",
    )

    table_columns = (
        "dataset_name",
        "dimensions.name",
        "dimensions.value",
        "metric_name",
        "unit",
    )

    def get_parser(self, prog_name):
        parser = super(ListDatasets, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2

        query = {}
        data = client.datasets(**query)

        table = (
            self.columns,
            (
                utils.get_dict_properties(_flatten_output(s), self.columns)
                for s in data
            ),
        )
        return table
