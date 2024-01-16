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

from cliff import columns as cliff_columns
from osc_lib import utils
from osc_lib.command import command
from otcextensions.common import cli_utils
from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


class SampleType(cliff_columns.FormattableColumn):
    VALUE_MAP = {
        0: "Image",
        1: "Text",
        2: "Speech",
        4: "Table",
        6: "Video",
        9: "Custom_Format",
    }

    def human_readable(self):
        return self.VALUE_MAP.get(self._value, str(self._value))


_formatters = {
    "labels": cli_utils.YamlFormat,
    "sample_time": cli_utils.UnixTimestampFormatter,
    "source": cli_utils.WrapText,
    "metadata": cli_utils.YamlFormat,
    "sample_type": SampleType,
}


def _get_columns(item):
    column_map = {}
    hidden = ["location", "id", "updated_at"]
    return sdk_utils.get_osc_show_columns_for_sdk_resource(
        item, column_map, hidden
    )


class AddSamples(command.ShowOne):
    _description = _(
        "This API is used to upload sample files such as "
        "images, speech files, and text files in batches."
    )

    def get_parser(self, prog_name):
        parser = super(AddSamples, self).get_parser(prog_name)
        parser.add_argument(
            "name",
            metavar="name",
            help=_(
                "Name of sample files. The value contains 0 to 1,024 "
                "characters and cannot contain special characters "
                "(!<>=&\"')."
            ),
        )
        parser.add_argument(
            "--sample-type",
            metavar="<sample_type>",
            type=int,
            help=_(
                "Sample type. The options are as follows:"
                "\n0: image"
                "\n1: text"
                "\n2: speech"
                "\n4: table"
                "\n6: video"
                "\n9: custom format"
            ),
        )
        parser.add_argument(
            "--encoding",
            metavar="<encoding>",
            help=_(
                "Encoding type of sample files, which is used to upload "
                ".txt or .csv files. The value can be UTF-8, GBK, or "
                "GB2312. The default value is UTF-8."
            ),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2

        attrs = {}

        if parsed_args.name:
            attrs["name"] = parsed_args.name

        obj = client.add_dataset_samples(**attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class ListSamples(command.Lister):
    _description = _("Get properties of a vm")
    columns = (
        "Id",
        "Sample Type",
        "Sample Status",
        "Sample Time",
    )

    def get_parser(self, prog_name):
        parser = super(ListSamples, self).get_parser(prog_name)
        parser.add_argument(
            "--dataset-id",
            metavar="<dataset_id>",
            required=True,
            help=_("Dataset ID."),
        )
        parser.add_argument(
            "--email",
            metavar="<email>",
            help=_("Email address of a labeling team member."),
        )
        parser.add_argument(
            "--high-score",
            metavar="<high_score>",
            help=_("Upper confidence limit. The default value is 1."),
        )
        parser.add_argument(
            "--label-name", metavar="<label_name>", help=_("Label name.")
        )
        parser.add_argument(
            "--label-type",
            metavar="<label_type>",
            help=_(
                "Labeling type. The options are as follows:"
                "\n0: image classification"
                "\n1: object detection"
                "\n100: text classification"
                "\n101: named entity recognition"
                "\n102: text triplet"
                "\n200: sound classification"
                "\n201: speech content"
                "\n202: speech paragraph labeling"
                "\n400: table dataset"
                "\n600: video labeling"
                "\n900: custom format"
            ),
        )
        parser.add_argument(
            "--limit",
            metavar="<limit>",
            type=int,
            help=_(
                "Maximum number of records returned on each page."
                "The value ranges from 1 to 100. "
                "The default value is 10."
            ),
        )
        parser.add_argument(
            "--locale",
            metavar="<locale>",
            help=_(
                "Language. The options are as follows:"
                "\nen-us: English (default value)."
            ),
        )
        parser.add_argument(
            "--low-score",
            metavar="<low_score>",
            help=_("Lower confidence limit. The default value is 0."),
        )
        parser.add_argument(
            "--offset",
            metavar="<offset>",
            type=int,
            help=_("Start page of the paging list. The default value is 0."),
        )
        parser.add_argument(
            "--order",
            metavar="<order>",
            help=_(
                "Sorting sequence of the query. "
                "The options are as follows:"
                "\nasc: ascending order"
                "\ndesc: descending order (default value)."
            ),
        )
        parser.add_argument(
            "--preview",
            metavar="<preview>",
            type=bool,
            help=_(
                "Whether to support preview. The options are as follows:"
                "\ntrue: Preview is supported."
                "\nfalse: Preview is not supported."
            ),
        )
        parser.add_argument(
            "--process-parameter",
            metavar="<process_parameter>",
            help=_(
                "Image resizing setting, which is the same as the "
                "OBS resizing setting."
            ),
        )
        parser.add_argument(
            "--sample-state",
            metavar="<sample_state>",
            help=_("Sample status."),
        )
        parser.add_argument(
            "--sample-type", metavar="<sample_type>", help=_("Sample Type.")
        )
        parser.add_argument(
            "--search-conditions",
            metavar="<search_conditions>",
            help=_(
                "Multi-dimensional search condition after URL encoding. "
                "The relationship between multiple search "
                "conditions is AND."
            ),
        )
        parser.add_argument(
            "--version-id",
            metavar="<version_id>",
            help=_("Dataset version ID."),
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2

        attrs_list = (
            "email",
            "high_score",
            "label_name",
            "label_type",
            "limit",
            "locale",
            "low_score",
            "offset",
            "order",
            "preview",
            "process_parameter",
            "sample_state",
            "sample_type",
            "search_conditions",
            "version_id",
        )
        query_params = {}
        for arg in attrs_list:
            val = getattr(parsed_args, arg)
            if val:
                query_params[arg] = val

        data = client.dataset_samples(parsed_args.dataset_id, **query_params)

        formatters = {"Sample Time": cli_utils.UnixTimestampFormatter}

        table = (
            self.columns,
            (
                utils.get_dict_properties(
                    s, self.columns, formatters=formatters
                )
                for s in data
            ),
        )
        return table


class ShowSample(command.ShowOne):
    _description = _("Show instance details")

    def get_parser(self, prog_name):
        parser = super(ShowSample, self).get_parser(prog_name)
        parser.add_argument(
            "datasetId",
            metavar="<datasetId>",
            help=_("Dataset ID."),
        )
        parser.add_argument(
            "sampleId",
            metavar="<sampleId>",
            help=_("Dataset Sample ID."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2
        obj = client.get_dataset_sample(
            parsed_args.datasetId, parsed_args.sampleId
        )

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)

        return (display_columns, data)


class DeleteSamples(command.Command):
    _description = _(
        "This API is used to delete the samples of a " "dataset in batches."
    )

    def get_parser(self, prog_name):
        parser = super(DeleteSamples, self).get_parser(prog_name)
        parser.add_argument(
            "datasetId", metavar="<datasetId>", help=_("ID of the dataset.")
        )
        parser.add_argument(
            "sampleId",
            metavar="<sampleId>",
            nargs="+",
            help=_("ID of Dataset sample(s) to be deleted."),
        )
        parser.add_argument(
            "--delete-source",
            action="store_true",
            help=_("Whether to delete the source file. " "(default: false.)"),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2
        delete_source = False
        if parsed_args.delete_source:
            delete_source = parsed_args.delete_source

        client.delete_dataset_samples(
            parsed_args.datasetId, parsed_args.sampleId, delete_source
        )
