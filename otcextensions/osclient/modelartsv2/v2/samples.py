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
"""ModelArts sample v2 action implementations"""
import logging

from osc_lib import utils
from osc_lib.command import command
from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _flatten_output(obj):
    data = {"sample_count": obj.sample_count, "samples": obj.samples}
    return data


def _get_columns(item):
    column_map = {}
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


class DeleteSampleBatches(command.Command):
    _description = _(
        "This API is used to delete the samples of a " "dataset in batches."
    )

    def get_parser(self, prog_name):
        parser = super(DeleteSampleBatches, self).get_parser(prog_name)
        parser.add_argument(
            "--dataset_id",
            metavar="<dataset_id>",
            required=True,
            help=_("ID of the dataset."),
        )

        parser.add_argument(
            "--samples",
            metavar="<samples>",
            required=True,
            help=_("List of IDs of samples to be deleted in batches."),
        )
        parser.add_argument(
            "--delete_source",
            metavar="<delete_source>",
            help=_(
                "Whether to delete the source file. "
                "The default value is false."
            ),
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2

        query = {}
        if parsed_args.samples:
            query["samples"] = parsed_args.samples
        if parsed_args.dataset_id:
            query["dataset_id"] = parsed_args.dataset_id
        if parsed_args.delete_source:
            query["delete_source"] = parsed_args.delete_source

        client.delete_sample_batches(
            parsed_args.samples, ignore_missing=False, **query
        )


class UploadSampleBatches(command.ShowOne):
    _description = _(
        "This API is used to upload sample files such as "
        "images, speech files, and text files in batches."
    )

    def get_parser(self, prog_name):
        parser = super(UploadSampleBatches, self).get_parser(prog_name)
        parser.add_argument(
            "--samples",
            metavar="<samples>",
            required=True,
            help=_("File list."),
        )
        parser.add_argument(
            "--final_annotation",
            metavar="<final_annotation>",
            help=_(
                "Whether to directly import to the final result. "
                "The default value is true. If the value is false, "
                "the imported labels are in the to-be-confirmed state."
            ),
        )
        parser.add_argument(
            "--name",
            metavar="<name>",
            required=True,
            help=_("Name of a local file"),
        )
        parser.add_argument(
            "--data",
            metavar="<data>",
            required=True,
            help=_("Base64-encoded character string"),
        )
        parser.add_argument(
            "--encoding",
            metavar="<encoding>",
            help=_(
                "Encoding type of each file, which is used to upload "
                "text files (.txt or .csv). The value can be UTF-8, "
                "GBK, or GB2312. The default value is UTF-8."
            ),
        )
        parser.add_argument(
            "--labels", metavar="<labels>", help=_("Sample label list.")
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2

        attrs = {}

        if parsed_args.name:
            attrs["name"] = parsed_args.name
        if parsed_args.data:
            attrs["data"] = parsed_args.data
        if parsed_args.encoding:
            attrs["encoding"] = parsed_args.encoding
        if parsed_args.labels:
            attrs["labels"] = parsed_args.labels

        obj = client.Upload_sample_batches(**attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


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
            "--samples",
            metavar="<samples>",
            required=True,
            help=_("File list."),
        )
        parser.add_argument(
            "--final_annotation",
            metavar="<final_annotation>",
            help=_(
                "Whether to directly import to the final result. "
                "The default value is true."
            ),
        )
        parser.add_argument(
            "--name",
            metavar="<name>",
            required=True,
            help=_("Name of a local file."),
        )
        parser.add_argument(
            "--data",
            metavar="<data",
            help=_("Base64-encoded character string"),
        )
        parser.add_argument(
            "--encoding",
            metavar="<labels>",
            help=_(
                "Encoding type of each file, which is used to upload text "
                "files (.txt or .csv). The value can be UTF-8, GBK, or "
                "GB2312. The default value is UTF-8."
            ),
        )
        parser.add_argument(
            "--labels", metavar="<labels>", help=_("Sample label list.")
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2

        attrs = {}

        if parsed_args.dataset_id:
            attrs["dataset_id"] = parsed_args.dataset_id
        if parsed_args.samples:
            attrs["samples"] = parsed_args.samples
        if parsed_args.final_annotation:
            attrs["final_annotation"] = parsed_args.final_annotation
            attrs["work_path_type"] = parsed_args.work_path_type
        if parsed_args.labels:
            attrs["labels"] = parsed_args.labels
        if parsed_args.name:
            attrs["name"] = parsed_args.name
        if parsed_args.data:
            attrs["data"] = parsed_args.data
        if parsed_args.encoding:
            attrs["encoding"] = parsed_args.encoding

        obj = client.upload_sample_files(**attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class ShowSample(command.ShowOne):
    _description = _("Show details of a MA sample")

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

        if parsed_args.sample_id:
            query["sample_id"] = parsed_args.sample_id

        obj = client.show_sample(**query)
        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class Samples(command.Lister):
    _description = _("Get properties of a vm")
    columns = ("sample_count", "samples")

    table_columns = ("sample_count", "samples")

    def get_parser(self, prog_name):
        parser = super(Samples, self).get_parser(prog_name)
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
        data = client.samples(**query)
        table = (
            self.columns,
            (
                utils.get_dict_properties(_flatten_output(s), self.columns)
                for s in data
            ),
        )
        return table
