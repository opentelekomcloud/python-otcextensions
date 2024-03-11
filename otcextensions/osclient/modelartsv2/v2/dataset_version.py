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

from cliff import columns as cliff_columns
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


class VersionStatus(cliff_columns.FormattableColumn):
    CHOICES_MAP = {
        0: "creating",
        1: "running",
        2: "deleting",
        3: "deleted",
        4: "error",
    }
    STR = "\n".join(f"{key}: {value}" for key, value in CHOICES_MAP.items())

    def human_readable(self):
        return self.CHOICES_MAP.get(self._value, str(self._value))


class ListDatasetVersions(command.Lister):
    _description = _("This API is used to query the Dataset Version list.")
    columns = (
        "Version Id",
        "Version Name",
        "Version Format",
        "Status",
        "Created At",
    )

    def get_parser(self, prog_name):
        parser = super(ListDatasetVersions, self).get_parser(prog_name)
        parser.add_argument(
            "dataset",
            metavar="<dataset>",
            help=_("Dataset Id or name."),
        )
        parser.add_argument(
            "--status",
            metavar="<status>",
            choices=[0, 1, 2, 3, 4],
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
            choices=[0, 1, 2],
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

        query_params = {}
        for arg in ("status", "train_evaluate_ratio", "version_format"):
            val = getattr(parsed_args, arg)
            if val or str(val) == "0":
                query_params[arg] = val

        dataset = client.find_dataset(parsed_args.dataset)
        data = client.dataset_versions(dataset.id, **query_params)

        formatters = {
            "Status": VersionStatus,
            "Created At": cli_utils.UnixTimestampFormatter,
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


class CreateDatasetVersion(command.ShowOne):
    _description = _("Create a ModelArts dataset version")

    def get_parser(self, prog_name):
        parser = super(CreateDatasetVersion, self).get_parser(prog_name)
        parser.add_argument(
            "dataset",
            metavar="<dataset>",
            help=_("Dataset Id or name."),
        )
        parser.add_argument(
            "--name",
            metavar="<name>",
            dest="version_name",
            help=_(
                "version_name. The value is a string of 1 to 32 "
                "characters consisting of only digits, letters, "
                "underscores (_), and hyphens (-). "
                "Example value: dataset"
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
        parser.add_argument(
            "--version-format",
            metavar="<version_format>",
            help=_(
                "Format of the exported version file, which is "
                "case insensitive."
            ),
        )
        parser.add_argument(
            "--remove-sample-usage",
            metavar="<remove_sample_usage>",
            help=_(
                "Whether to clear the usage information of dataset "
                "samples. The default value is true."
            ),
        )
        parser.add_argument(
            "--export-images",
            metavar="<export_images>",
            help=_(
                "Whether to export images to the version output directory "
                "during publishing. The default value is false."
            ),
        )
        parser.add_argument(
            "--train-evaluate-sample-ratio",
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
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2

        attrs = {}
        dataset = client.find_dataset(parsed_args.dataset)
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

        obj = client.create_dataset_version(dataset.id, **attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return display_columns, data


class ShowDatasetVersion(command.ShowOne):
    _description = _("Show details of a MA dataset version")

    def get_parser(self, prog_name):
        parser = super(ShowDatasetVersion, self).get_parser(prog_name)

        parser.add_argument(
            "dataset",
            metavar="<dataset>",
            help=_("Dataset Id or name."),
        )

        parser.add_argument(
            "versionId",
            metavar="<versionId>",
            help=_("Dataset version id."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2

        dataset = client.find_dataset(parsed_args.dataset)
        obj = client.get_dataset_version(dataset.id, parsed_args.versionId)

        formatters = {
            "status": VersionStatus,
            "created_at": cli_utils.UnixTimestampFormatter,
            "label_stats": cli_utils.YamlFormat,
        }

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=formatters)

        return (display_columns, data)


class DeleteDatasetVersion(command.Command):
    _description = _("Delete ModelArts Dataset Version.")

    def get_parser(self, prog_name):
        parser = super(DeleteDatasetVersion, self).get_parser(prog_name)
        parser.add_argument(
            "dataset",
            metavar="<dataset>",
            help=_("Dataset Id or name."),
        )
        parser.add_argument(
            "versionId",
            metavar="<versionId>",
            help=_("Version Id of the dataset."),
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2
        dataset = client.find_dataset(parsed_args.dataset)

        client.delete_dataset_version(dataset.id, parsed_args.versionId)
