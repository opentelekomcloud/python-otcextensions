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
from osc_lib.cli import parseractions
from osc_lib.command import command
from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _flatten_output(obj):
    data = {
        "task_id": obj.task_id,
        "dataset_id": obj.dataset_id,
        "import_path": obj.import_path,
    }
    return data


def _get_columns(item):
    column_map = {}
    hidden = ["location"]
    return sdk_utils.get_osc_show_columns_for_sdk_resource(
        item, column_map, hidden
    )


class CreateDatasetImportTask(command.ShowOne):
    _description = _("Create a ModelArts dataset import task")

    def get_parser(self, prog_name):
        parser = super(CreateDatasetImportTask, self).get_parser(prog_name)
        parser.add_argument(
            "--dataset_id",
            metavar="<dataset_id>",
            required=True,
            help=_("Dataset ID."),
        )
        parser.add_argument(
            "--import_path",
            metavar="<import_path>",
            required=True,
            help=_(
                "OBS path to which the data is imported. When importing "
                "a manifest file, ensure that the path is accurate to "
                "the manifest file."
            ),
        )
        parser.add_argument(
            "--import_annotations",
            metavar="<import_annotations>",
            help=_("Whether to import labels. Default value: true"),
        )
        parser.add_argument(
            "--import-type",
            metavar="<import_type>",
            help=_(
                "Import mode. The default value is dir."
                "\ndir: Import the directory."
                "\nmanifest: Import the manifest file."
            ),
        )
        parser.add_argument(
            "--import-folder",
            metavar="<import_folder>",
            help=_(
                "Name of the subdirectory in the dataset storage "
                "directory after import."
            ),
        )
        parser.add_argument(
            "--final-annotation",
            metavar="<final_annotation>",
            help=_(
                "Whether to directly import to the final result. "
                "The default value is true."
            ),
        )
        parser.add_argument(
            "--difficult-only",
            metavar="<difficult_only>",
            help=_(
                "Whether to import only hard examples. "
                "Default value: false."
            ),
        )
        parser.add_argument(
            "--included-labels",
            metavar="<included_labels>",
            help=_(
                "Whether to import only the labels specified by this "
                "parameter."
            ),
        )
        parser.add_argument(
            "--included-tags",
            metavar="<included_tags>",
            help=_(
                "Whether to import only the labels corresponding to "
                "the value."
            ),
        )
        parser.add_argument("--name", metavar="<name>", help=_("Label name "))
        parser.add_argument(
            "--type",
            metavar="<type>",
            help=_(
                "Label type. A triplet dataset can contain the following "
                "types of labels:"
                "\n101: text entity"
                "\n102: triplet relationship"
            ),
        )
        parser.add_argument(
            "--label-property",
            action=parseractions.MultiKeyValueAction,
            metavar="key=<key>,value=<value>",
            required_keys=["key", "value"],
            dest="label_properties",
            help=_(
                "key=<key>: Tag key. The value can contain 1 to 36 "
                "underscores (_) are allowed."
            ),
        )
        parser.add_argument(
            "--label-type",
            metavar="<label_type>",
            help=_(
                "For details about the mandatory attributes of a "
                "triplet label."
            ),
        )
        parser.add_argument(
            "--text-label-separator",
            metavar="<text_label_separator>",
            help=_(
                "For details about the mandatory attributes of a "
                "triplet label."
            ),
        )
        parser.add_argument(
            "--text-sample-separator",
            metavar="<text_sample_separator>",
            help=_(
                "For details about the mandatory attributes of a "
                "triplet label."
            ),
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2

        attrs = {}

        if parsed_args.dataset_id:
            attrs["dataset_id"] = parsed_args.dataset_id
        if parsed_args.import_path:
            attrs["import_path"] = parsed_args.import_path
        if parsed_args.import_annotations:
            attrs["import_annotations"] = parsed_args.import_annotations
        if parsed_args.import_type:
            attrs["import_type"] = parsed_args.import_type
        if parsed_args.import_folder:
            attrs["import_folder"] = parsed_args.import_folder
        if parsed_args.final_annotation:
            attrs["final_annotation"] = parsed_args.final_annotation
        if parsed_args.import_annotations:
            attrs["import_annotations"] = parsed_args.import_annotations
        if parsed_args.difficult_only:
            attrs["difficult_only"] = parsed_args.difficult_only
        if parsed_args.included_labels:
            attrs["included_labels"] = parsed_args.included_labels
        if parsed_args.included_tags:
            attrs["included_tags"] = parsed_args.included_tags
        if parsed_args.name:
            attrs["name"] = parsed_args.name
        if parsed_args.type:
            attrs["type"] = parsed_args.type
        if parsed_args.property:
            attrs["property"] = parsed_args.property
        if parsed_args.label_properties:
            label_properties = {}
            for item in parsed_args.label_properties:
                label_properties[item["key"]] = item["value"]
            attrs["label_properties"] = label_properties
        print("******", attrs)
        import sys

        sys.exit(1)
        obj = client.create_dataset_import_task(**attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class ShowDatasetImportTask(command.ShowOne):
    _description = _("Show details of a MA dataset import task")

    def get_parser(self, prog_name):
        parser = super(ShowDatasetImportTask, self).get_parser(prog_name)

        parser.add_argument(
            "--dataset_id", metavar="<dataset_id>", help=_("Enter dataset id")
        )

        parser.add_argument(
            "--task_id", metavar="<task_id>", help=_("Enter task id")
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2
        query = {}

        if parsed_args.dataset_id:
            query["dataset_id"] = parsed_args.dataset_id

        if parsed_args.task_id:
            query["task_id"] = parsed_args.task_id

        obj = client.get_dataset_import_task(**query)
        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class ListDatasetImportTasks(command.Lister):
    _description = _("Get properties of a vm")
    columns = ("task_id", "dataset_id", "import_path")

    table_columns = ("task_id", "dataset_id", "import_path")

    def get_parser(self, prog_name):
        parser = super(ListDatasetImportTasks, self).get_parser(prog_name)
        parser.add_argument(
            "--dataset_id",
            metavar="<dataset_id>",
            help=_("Name of the dataset to delete."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2

        query = {}
        if parsed_args.dataset_id:
            query["dataset_id"] = parsed_args.dataset_id
        data = client.dataset_import_tasks(**query)

        table = (
            self.columns,
            (
                utils.get_dict_properties(_flatten_output(s), self.columns)
                for s in data
            ),
        )
        return table
