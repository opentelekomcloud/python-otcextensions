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
"""ModelArts dataset version v2 action implementations"""
import logging

from osc_lib import utils
from osc_lib.command import command
from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _flatten_output(obj):
    data = {"total_number": obj.total_number, "versions": obj.versions}
    return data


def _get_columns(item):
    column_map = {}
    hidden = ["location"]
    return sdk_utils.get_osc_show_columns_for_sdk_resource(
        item, column_map, hidden
    )


class DeleteDatasetVersion(command.Command):
    _description = _("Delete ModelArts Dataset Version")

    def get_parser(self, prog_name):
        parser = super(DeleteDatasetVersion, self).get_parser(prog_name)
        parser.add_argument(
            "--dataset_id",
            metavar="<dataset_id>",
            help=_("Id of the dataset to delete."),
        )
        parser.add_argument(
            "--version_id",
            metavar="<version_id>",
            help=_("Version of the dataset to delete."),
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2

        query = {}
        if parsed_args.dataset_id:
            query["dataset_id"] = parsed_args.dataset_id
        if parsed_args.version_id:
            query["version_id"] = parsed_args.version_id

        # client.delete_dataset_version(parsed_args.version_id,
        #                               ignore_missing=False, **query)
        client.delete_dataset_version(**query)


class CreateDatasetVersion(command.ShowOne):
    _description = _("Create a ModelArts dataset version")

    def get_parser(self, prog_name):
        parser = super(CreateDatasetVersion, self).get_parser(prog_name)
        parser.add_argument(
            "--dataset_id",
            required=True,
            metavar="<dataset_id>",
            help=_(
                "Format of the exported version file, which is "
                "case insensitive."
            ),
        )
        parser.add_argument(
            "--version_name",
            metavar="<version_name>",
            help=_(
                "version_name. The value is a string of 1 to 32 "
                "characters consisting of only digits, letters, "
                "underscores (_), and hyphens (-). "
                "Example value: dataset"
            ),
        )
        parser.add_argument(
            "--version_format",
            metavar="<version_format>",
            help=_(
                "Format of the exported version file, which is "
                "case insensitive."
            ),
        )
        parser.add_argument(
            "--remove_sample_usage",
            metavar="<remove_sample_usage>",
            help=_(
                "Whether to clear the usage information of dataset "
                "samples. The default value is true."
            ),
        )
        parser.add_argument(
            "--export_images",
            metavar="<export_images>",
            help=_(
                "Whether to export images to the version output directory "
                "during publishing. The default value is false."
            ),
        )
        parser.add_argument(
            "--train_evaluate_sample_ratio",
            metavar="<train_evaluate_sample_ratio>",
            help=_(
                "Ratio that splits the labeled data into training and "
                "validation sets during publishing. The value must be "
                "a decimal between 0 and 1. "
            ),
        )
        parser.add_argument(
            "--clear_hard_property",
            metavar="<clear_hard_property>",
            help=_(
                "Whether to clear hard example properties. "
                "The default value is true."
            ),
        )
        parser.add_argument(
            "--description",
            metavar="<description>",
            help=_(
                "Dataset description. The value is a string of 0 to 256 "
                "characters. By default, this parameter is left blank."
            ),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2

        attrs = {}
        if parsed_args.version_name:
            attrs["version_name"] = parsed_args.version_name
        if parsed_args.version_format:
            attrs["version_format"] = parsed_args.version_format
        if parsed_args.remove_sample_usage:
            attrs["remove_sample_usage"] = parsed_args.remove_sample_usage
        if parsed_args.export_images:
            attrs["export_images"] = parsed_args.export_images
        if parsed_args.train_evaluate_sample_ratio:
            attrs["train_evaluate_sample_ratio"] = (
                parsed_args.train_evaluate_sample_ratio
            )
        if parsed_args.clear_hard_property:
            attrs["clear_hard_property"] = parsed_args.clear_hard_property
        if parsed_args.description:
            attrs["description"] = parsed_args.description
        if parsed_args.dataset_id:
            attrs["dataset_id"] = parsed_args.dataset_id
        obj = client.create_dataset_version(**attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return display_columns, data


class ShowDatasetVersion(command.ShowOne):
    _description = _("Show details of a MA dataset version")

    def get_parser(self, prog_name):
        parser = super(ShowDatasetVersion, self).get_parser(prog_name)

        parser.add_argument(
            "--dataset-id", metavar="<dataset_id>", help=_("Enter dataset id")
        )

        parser.add_argument(
            "--version-id", metavar="<version_id>", help=_("Enter version id")
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2
        query = {}

        if parsed_args.dataset_id:
            query["dataset_id"] = parsed_args.dataset_id

        if parsed_args.version_id:
            query["version_id"] = parsed_args.version_id

        obj = client.show_dataset_version(**query)
        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return display_columns, data


class ListDatasetVersions(command.Lister):
    _description = _("This API is used to query the Dataset Version list.")
    columns = ("total_number", "versions")

    table_columns = ("total_number", "versions")

    def get_parser(self, prog_name):
        parser = super(ListDatasetVersions, self).get_parser(prog_name)
        parser.add_argument(
            "--dataset-id",
            metavar="<dataset_id>",
            help=_("ID of the dataset to delete a Dataset Version."),
        )
        parser.add_argument(
            "--status",
            metavar="<status>",
            type=int,
            help=_(
                "Status of a dataset version. The options are as follows:"
                "\n0: creating"
                "\n1: running"
                "\n2: deleting"
                "\n3: deleted"
                "\n4: error"
            ),
        )
        parser.add_argument(
            "--train-evaluate-ratio",
            metavar="<train_evaluate_ratio>",
            help=_("Version split ratio for version filtering."),
        )
        parser.add_argument(
            "--version-format",
            metavar="<version_format>",
            type=int,
            help=_(
                "Format of a dataset version. The options are as follows:"
                "\n0: default format"
                "\n1: CarbonData (supported only by table datasets)"
                "\n2: CSV"
            ),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2

        query = {}
        if parsed_args.dataset_id:
            query["dataset_id"] = parsed_args.dataset_id
        data = client.dataset_versions(**query)

        table = (
            self.columns,
            (
                utils.get_dict_properties(_flatten_output(s), self.columns)
                for s in data
            ),
        )
        return table
