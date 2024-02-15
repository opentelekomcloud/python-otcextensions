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
"""ModelArts labels v2 action implementations"""
import logging

from osc_lib import utils
from osc_lib.command import command
from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _flatten_output(obj):
    data = {"name": obj.name, "type": obj.type}
    return data


def _get_columns(item):
    column_map = {}
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


class DeleteLabels(command.Command):
    _description = _(
        "This API is used to delete the samples of " "a dataset in batches."
    )

    def get_parser(self, prog_name):
        parser = super(DeleteLabels, self).get_parser(prog_name)
        parser.add_argument(
            "--dataset_id",
            metavar="<dataset_id>",
            help=_("ID of the dataset to delete."),
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2

        query = {}
        if parsed_args.dataset_id:
            query["dataset_id"] = parsed_args.dataset_id

        client.delete_labels(parsed_args, ignore_missing=False, **query)


class DeleteSingleLabel(command.Command):
    _description = _(
        "This API is used to delete the samples of " "a dataset in batches."
    )

    def get_parser(self, prog_name):
        parser = super(DeleteSingleLabel, self).get_parser(prog_name)
        parser.add_argument(
            "--dataset_id",
            metavar="<dataset_id>",
            required=True,
            help=_("ID of the dataset."),
        )
        parser.add_argument(
            "--label_name",
            metavar="<label_name>",
            required=True,
            help=_("URL-encoded label name."),
        )
        parser.add_argument(
            "--label_type",
            metavar="<label_type>",
            help=_(
                "Label type. The value is the same as that of "
                "the dataset type."
            ),
        )
        parser.add_argument(
            "--delete_source",
            metavar="<delete_source>",
            help=_("Whether to delete the source file."),
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2

        query = {}
        if parsed_args.dataset_id:
            query["dataset_id"] = parsed_args.dataset_id
        if parsed_args.label_name:
            query["label_name"] = parsed_args.label_name
        if parsed_args.label_type:
            query["label_type"] = parsed_args.label_type
        if parsed_args.delete_source:
            query["delete_source"] = parsed_args.delete_source

        client.delete_single_label(parsed_args, ignore_missing=False, **query)


class UploadSampleFiles(command.ShowOne):
    _description = _("Create a ModelArts dataset")

    def get_parser(self, prog_name):
        parser = super(UploadSampleFiles, self).get_parser(prog_name)
        parser.add_argument(
            "--dataset_id",
            metavar="<dataset_id>",
            required=True,
            help=_("Dataset ID"),
        )
        parser.add_argument(
            "--name", metavar="<name>", required=True, help=_("Label name.")
        )
        parser.add_argument(
            "--type",
            metavar="<type>",
            help=_(
                "Label type. The value range is the same as that "
                "of the dataset type."
            ),
        )
        parser.add_argument(
            "--property",
            metavar="<property>",
            required=True,
            help=_("Label attributes."),
        )
        parser.add_argument("--labels", metavar="<data", help=_("Label list."))

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2

        attrs = {}

        if parsed_args.dataset_id:
            attrs["dataset_id"] = parsed_args.dataset_id
        if parsed_args.type:
            attrs["type"] = parsed_args.type
        if parsed_args.labels:
            attrs["labels"] = parsed_args.labels
        if parsed_args.name:
            attrs["name"] = parsed_args.name
        if parsed_args.data:
            attrs["data"] = parsed_args.data
        if parsed_args.property:
            attrs["property"] = parsed_args.property

        obj = client.upload_sample_files(**attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class ShowSample(command.ShowOne):
    _description = _("This API is used to query details about a sample.")

    def get_parser(self, prog_name):
        parser = super(ShowSample, self).get_parser(prog_name)

        parser.add_argument(
            "--dataset_id", metavar="<dataset_id>", help=_("Enter dataset id")
        )

        parser.add_argument(
            "--sample_id", metavar="<sample_id>", help=_("Enter sample id")
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2
        query = {}

        if parsed_args.dataset_id:
            query["dataset_id"] = parsed_args.dataset_id

        if parsed_args.version_id:
            query["version_id"] = parsed_args.version_id

        obj = client.show_sample(**query)
        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class ListLabels(command.Lister):
    _description = _("This API is used to query all samples of a dataset.")
    columns = ("name", "type")

    def get_parser(self, prog_name):
        parser = super(ListLabels, self).get_parser(prog_name)
        parser.add_argument(
            "--dataset_id",
            metavar="<dataset_id>",
            help=_("ID of the dataset."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2

        query = {}
        if parsed_args.dataset_id:
            query["dataset_id"] = parsed_args.dataset_id
        data = client.dataset_labels(**query)

        table = (
            self.columns,
            (
                utils.get_dict_properties(_flatten_output(s), self.columns)
                for s in data
            ),
        )
        return table


class LabelStatistics(command.Lister):
    _description = _("This API is used to query details about a sample.")
    columns = "name"

    def get_parser(self, prog_name):
        parser = super(LabelStatistics, self).get_parser(prog_name)
        parser.add_argument(
            "--dataset_id",
            metavar="<dataset_id>",
            help=_("ID of the dataset."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2

        query = {}
        if parsed_args.dataset_id:
            query["dataset_id"] = parsed_args.dataset_id

        data = client.label_stats(**query)

        table = (
            self.columns,
            (
                utils.get_dict_properties(_flatten_output(s), self.columns)
                for s in data
            ),
        )
        return table
