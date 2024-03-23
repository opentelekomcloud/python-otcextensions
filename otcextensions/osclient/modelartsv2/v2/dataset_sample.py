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
from osc_lib import exceptions
from osc_lib import utils
from osc_lib.cli import parseractions
from osc_lib.command import command

from otcextensions.common import cli_utils
from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)

SORT_ORDER_CHOICES = ["asc", "desc"]

SAMPLE_STATE_CHOICES = [
    "all",
    "none",
    "uncheck",
    "accepted",
    "rejected",
    "unreviewed",
    "reviewed",
    "workforce_sampled",
    "workforce_sampled_uncheck",
    "workforce_sampled_checked",
    "workforce_sampled_accepted",
    "workforce_sampled_rejected",
    "auto_annotation",
]


class SampleType(cliff_columns.FormattableColumn):
    CHOICES_MAP = {
        0: "Image",
        1: "Text",
        2: "Speech",
        4: "Table",
        6: "Video",
        9: "Custom_Format",
    }
    STR = "\n".join(f"{key}: {value}" for key, value in CHOICES_MAP.items())

    def human_readable(self):
        return self.CHOICES_MAP.get(self._value, str(self._value))


class LabelType(cliff_columns.FormattableColumn):
    CHOICES_MAP = {
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
    STR = "\n".join(f"{key}: {value}" for key, value in CHOICES_MAP.items())

    def human_readable(self):
        return self.CHOICES_MAP.get(self._value, str(self._value))


class DataSourceType(cliff_columns.FormattableColumn):
    CHOICES_MAP = {
        0: "OBS bucket (default value)",
        1: "GaussDB(DWS)",
        2: "DLI",
        3: "RDS",
        4: "MRS",
        5: "AI Gallery",
        6: "Inference service",
    }
    STR = "\n".join(f"{key}: {value}" for key, value in CHOICES_MAP.items())

    def human_readable(self):
        return self.CHOICES_MAP.get(self._value, str(self._value))


DATASOURCE_KEYS_MAP = {
    "cluster_id": "ID of a MRS cluster",
    "cluster_mode": (
        "Running mode of a MRS cluster. Options are as follows:\n"
        "* 0: normal cluster\n"
        "* 1: security cluster"
    ),
    "cluster_name": "Name of a MRS cluster",
    "database_name": (
        "Name of the database to which the table dataset is imported."
    ),
    "input": "HDFS path of a table dataset",
    "ip": "IP address of your GaussDB(DWS) cluster",
    "port": "Port number of your GaussDB(DWS) cluster",
    "queue_name": "DLI queue name of a table dataset",
    "subnet_id": "Subnet ID of a MRS cluster",
    "table_name": "Name of the table to which a table dataset is imported",
    "user_name": "Username which is mandatary for GaussDB(DWS)",
    "user_password": "User password which is mandatary for GaussDB(DWS)",
    "vpc_id": "ID of the vpc of a MRS cluster",
}

LABEL_KEYS_MAP = {
    "annotated_by": (
        "Video labeling method, which is used to distinguish whether "
        "a video is labeled manually or automatically."
        "The options are as follows:\n"
        "* human: manual labeling\n"
        "* auto: automatic labeling"
    ),
    "id": "Label ID",
    "name": "Label name",
    "score": "Confidence",
    "type": (
        "Label type. The options are as follows:\n"
        "* 0: image classification\n"
        "* 1: object detection\n"
        "* 100: text classification\n"
        "* 101: named entity recognition\n"
        "* 102: text triplet relationship\n"
        "* 103: text triplet entity"
        "* 200: speech classification"
        "* 201: speech content"
        "* 202: speech paragraph labeling"
        "* 600: video classification"
    ),
}


_formatters = {
    "labels": cli_utils.YamlFormat,
    "sample_time": cli_utils.UnixTimestampFormatter,
    "source": cli_utils.WrapText,
    "metadata": cli_utils.YamlFormat,
    "sample_type": SampleType,
}


def _get_columns(item):
    column_map = {}
    hidden = [
        "location",
    ]
    return sdk_utils.get_osc_show_columns_for_sdk_resource(
        item, column_map, hidden
    )


class AddDatasetSamples(command.ShowOne):
    _description = _("Add samples to a dataset.")

    columns = ("success", "results")
    column_headers = ("Success", "Results")

    def get_parser(self, prog_name):
        parser = super(AddDatasetSamples, self).get_parser(prog_name)
        parser.add_argument(
            "dataset",
            metavar="<dataset>",
            help=_("Dataset Id or name."),
        )
        parser.add_argument(
            "--file-path",
            metavar="<file_path>",
            help=_("Sample file path to upload."),
        )
        parser.add_argument(
            "--directory-path",
            metavar="<directory_path>",
            help=_("Samples Directory path."),
        )
        # parser.add_argument(
        #     "--name",
        #     required=True,
        #     metavar="<name>",
        #     help=_("Name of sample file."),
        # )
        # parser.add_argument(
        #     "--data",
        #     metavar="<data>",
        #     required=True,
        #     help=_("Byte data of sample file."),
        # )
        parser.add_argument(
            "--encoding",
            metavar="{UTF-8, GBK, GB2312}",
            type=lambda s: s.upper(),
            choices=["UTF-8", "GBK", "GB2312"],
            help=_(
                "Encoding type of sample files, which is used to upload "
                ".txt or .csv files.\nThe default value is UTF-8."
            ),
        )
        parser.add_argument(
            "--metadata",
            metavar="<key=value>",
            dest="metadata",
            action=parseractions.KeyValueAction,
            help=_(
                "Key-value pair of the sample metadata attribute.\n"
                "Repeat the option to set multiple metadata attributes.\n"
                "Example:\n--metadata @modelarts:hard=0\n"
                "--metadata @modelarts:hard_coefficient=0.22\n"
                "--metadata @modelarts:hard_reasons=[1,2]\n"
                "--metadata @modelarts:size=[100,200,3]"
            ),
        )

        parser.add_argument(
            "--sample-type",
            choices=list(SampleType.CHOICES_MAP.keys()),
            type=int,
            help=_(
                "Sample type. The options are as follows:\n" + SampleType.STR
            ),
        )
        parser.add_argument(
            "--data-source-path",
            metavar="<data_source_path>",
            help=_("Data source path."),
        )
        parser.add_argument(
            "--data-source-type",
            choices=list(DataSourceType.CHOICES_MAP.keys()),
            type=int,
            help=_(
                "Data source type. The options are as follows:\n"
                + DataSourceType.STR
            ),
        )
        parser.add_argument(
            "--data-source-info",
            action=parseractions.MultiKeyValueAction,
            metavar="<key1=value1,key2=value2,..>",
            dest="data_source_info",
            required_keys=[],
            optional_keys=list(DATASOURCE_KEYS_MAP.keys()),
            help=_(
                "Information required for importing a table data source.\n"
                "Supported keys:\n"
                + "\n".join(
                    [
                        f"{key}: {value}"
                        for key, value in DATASOURCE_KEYS_MAP.items()
                    ]
                )
                + "\nExample:\n"
                "--data-source-info cluster_id=1234,cluster_mode=1"
            ),
        )
        parser.add_argument(
            "--data-with-column-header",
            action="store_true",
            help=_("Whether the first row in the data file is a column name."),
        )
        parser.add_argument(
            "--schema-map",
            metavar="src_name=<src_name>,dest_name=<dest_name>",
            required_keys=["src_name", "dest_name"],
            optional_keys=[],
            action=parseractions.MultiKeyValueAction,
            help=_(
                "Schema mapping information corresponding to the table data.\n"
                "src_name: Name of the source column.\n"
                "dest_name: Name of the destination column.\n"
                "Example:\n"
                "--schema-map src_name=colnameA,dest_name=colnameB\n"
                "--schema-map src_name=colnameX,dest_name=colnameY"
            ),
        )
        parser.add_argument(
            "--label",
            metavar="key1=<value1>,key2=<value2>,..",
            action=parseractions.MultiKeyValueAction,
            dest="labels",
            required_keys=[],
            optional_keys=list(LABEL_KEYS_MAP.keys()),
            help=_(
                "Sample label list.\n"
                "Supported keys:\n"
                + "\n".join(
                    [
                        f"{key}: {value}"
                        for key, value in LABEL_KEYS_MAP.items()
                    ]
                )
                + "\nExample:\n"
                "--label cluster_id=1234,cluster_mode=1"
            ),
        )
        parser.add_argument(
            "--to-be-confirmed",
            action="store_true",
            help=_(
                "Whether to import labels to the to-be-confirmed dataset.\n"
                "Currently, to-be-confirmed datasets only support categories "
                "of image classification and object detection."
            ),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2

        dataset = client.find_dataset(parsed_args.dataset)
        sample = {}
        for arg in (
            # "name",
            # "data",
            "file_path",
            "directory_path",
            "encoding",
            "sample_type",
            "metadata",
            "labels",
        ):
            val = getattr(parsed_args, arg)
            if val or str(val) == "0":
                sample[arg] = val

        data_source = {}
        if parsed_args.data_source_path:
            data_source["data_path"] = parsed_args.data_source_path
        if parsed_args.data_source_type:
            data_source["data_type"] = parsed_args.data_source_type
        if parsed_args.schema_map:
            data_source["schema_map"] = parsed_args.schema_map
        data_source_info = parsed_args.data_source_info
        if data_source_info:
            if len(data_source_info) > 1:
                msg = "ERROR: --data-source-info argument cannot be repeated"
                raise exceptions.CommandError(msg)
            data_source["source_info"] = data_source_info[0]
        if parsed_args.data_with_column_header:
            data_source["with_column_header"] = True
        if data_source:
            sample.update(data_source=data_source)

        data = client.add_dataset_samples(dataset.id, **sample)

        formatters = {
            "results": cli_utils.YamlFormat,
        }
        return (
            self.column_headers,
            utils.get_item_properties(
                data, self.columns, formatters=formatters
            ),
        )


class ListDatasetSamples(command.Lister):
    _description = _("Get details about a Sample.")
    columns = (
        "Id",
        "Sample Type",
        "Sample Status",
        "Sample Time",
    )

    def get_parser(self, prog_name):
        parser = super(ListDatasetSamples, self).get_parser(prog_name)
        parser.add_argument(
            "dataset",
            metavar="<dataset>",
            help=_("Dataset Id or name."),
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
            "--label-name",
            metavar="<label_name>",
            help=_("Label name."),
        )
        parser.add_argument(
            "--label-type",
            choices=list(LabelType.CHOICES_MAP.keys()),
            type=int,
            help=_(
                "Labeling type. The options are as follows:" + LabelType.STR
            ),
        )
        parser.add_argument(
            "--limit",
            metavar="<limit>",
            type=int,
            help=_(
                "Maximum number of records returned on each "
                "page. The value ranges from 1 to 100. "
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
            metavar="{asc, desc}",
            type=lambda s: s.lower(),
            choices=["asc", "desc"],
            help=_("Sorting order. Default value: desc"),
        )
        parser.add_argument(
            "--preview",
            action="store_true",
            help=_("Whether to support preview."),
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
            metavar="{" + ",".join(SAMPLE_STATE_CHOICES) + "}",
            type=lambda s: s.lower(),
            choices=SAMPLE_STATE_CHOICES,
            help=_("Sample status."),
        )
        parser.add_argument(
            "--sample-type",
            choices=list(SampleType.CHOICES_MAP.keys()),
            type=int,
            help=_(
                "Sample type. The options are as follows:" + SampleType.STR
            ),
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
            if val or str(val) == "0":
                query_params[arg] = val

        dataset = client.find_dataset(parsed_args.dataset)
        data = client.dataset_samples(dataset.id, **query_params)

        formatters = {
            "Sample Type": SampleType,
            "Sample Time": cli_utils.UnixTimestampFormatter,
        }

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


class ShowDatasetSample(command.ShowOne):
    _description = _("Show instance details")

    def get_parser(self, prog_name):
        parser = super(ShowDatasetSample, self).get_parser(prog_name)
        parser.add_argument(
            "dataset",
            metavar="<dataset>",
            help=_("Dataset Id or name."),
        )
        parser.add_argument(
            "sampleId",
            metavar="<sampleId>",
            help=_("Dataset Sample ID."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2
        dataset = client.find_dataset(parsed_args.dataset)
        obj = client.get_dataset_sample(dataset.id, parsed_args.sampleId)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)

        return (display_columns, data)


class DeleteDatasetSamples(command.ShowOne):
    _description = _(
        "This API is used to delete the samples of a dataset in batches."
    )

    def get_parser(self, prog_name):
        parser = super(DeleteDatasetSamples, self).get_parser(prog_name)
        parser.add_argument(
            "dataset",
            metavar="<dataset>",
            help=_("Dataset Id or name."),
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
            help=_("Whether to delete the source file. (default: false.)"),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2
        delete_source = False
        if parsed_args.delete_source:
            delete_source = parsed_args.delete_source

        dataset = client.find_dataset(parsed_args.dataset)
        obj = client.delete_dataset_samples(
            dataset.id, parsed_args.sampleId, delete_source
        )
        formatters = {
            "results": cli_utils.YamlFormat,
        }

        hidden = ["samples", "delete_source", "location"]

        (
            display_columns,
            columns,
        ) = sdk_utils.get_osc_show_columns_for_sdk_resource(obj, {}, hidden)

        data = utils.get_item_properties(obj, columns, formatters=formatters)

        return (display_columns, data)
