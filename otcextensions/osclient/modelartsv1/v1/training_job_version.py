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
"""ModelArts training job v1 action implementations"""
import logging
from cliff import columns as cliff_columns

from osc_lib import utils
from osc_lib.cli import parseractions
from osc_lib.command import command
from otcextensions.common import cli_utils
from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


_formatters = {
    "created_at": cli_utils.UnixTimestampFormatter,
    "config": cli_utils.YamlFormat,
}


def _get_columns(item):
    column_map = {}
    hidden = ["location"]
    return sdk_utils.get_osc_show_columns_for_sdk_resource(
        item, column_map, hidden
    )


class JobStatus(cliff_columns.FormattableColumn):
    CHOICES_MAP = {
        0: "UNKNOWN",
        1: "INIT",
        2: "IMAGE_CREATING",
        3: "IMAGE_FAILED",
        4: "SUBMIT_TRYING",
        5: "SUBMIT_FAILED",
        6: "DELETE_FAILED",
        7: "WAITING",
        8: "RUNNING",
        9: "KILLING",
        10: "COMPLETED",
        11: "FAILED",
        12: "KILLED",
        13: "CANCELED",
        14: "LOST",
        15: "SCALING",
        16: "SUBMIT_MODEL_FAILED",
        17: "DEPLOY_SERVICE_FAILED",
        18: "CHECK_INIT",
        19: "CHECK_RUNNING",
        20: "RUNNING_COMPLETED",
        21: "CHECK_FAILED",
    }
    STR = "\n".join(f"{key}: {value}" for key, value in CHOICES_MAP.items())

    def human_readable(self):
        return self.CHOICES_MAP.get(self._value, str(self._value))


class ListTrainingJobVersions(command.Lister):
    _description = _("Get the list of training job versions")
    columns = (
        "Version Id",
        "Version Name",
        "Status",
        "Created At",
        "Started At",
        "Duration",
    )

    def get_parser(self, prog_name):
        parser = super(ListTrainingJobVersions, self).get_parser(prog_name)
        parser.add_argument(
            "jobId",
            metavar="<jobId>",
            help=_("ID of the training job."),
        )
        parser.add_argument(
            "--limit",
            metavar="<limit>",
            type=int,
            help=_(
                "Number of jobs displayed on each page. The value "
                "range is [1, 1000]. Default value: 10."
            ),
        )
        parser.add_argument(
            "--offset",
            metavar="<offset>",
            type=int,
            help=_("Index of the page to be queried. Default value: 1"),
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1

        params = {}
        if parsed_args.limit:
            params["limit"] = parsed_args.limit
        if parsed_args.offset:
            params["offset"] = parsed_args.offset

        data = client.training_job_versions(parsed_args.jobId, **params)

        _formatters = {
            "Created At": cli_utils.UnixTimestampFormatter,
            "Started At": cli_utils.UnixTimestampFormatter,
            "Status": JobStatus,
        }
        return (
            self.columns,
            (
                utils.get_dict_properties(
                    s, self.columns, formatters=_formatters
                )
                for s in data
            ),
        )


class CreateTrainingJobVersion(command.ShowOne):
    _description = _("Create a ModelArts Training Job Version")

    def get_parser(self, prog_name):
        parser = super(CreateTrainingJobVersion, self).get_parser(prog_name)
        parser.add_argument(
            "jobId",
            metavar="<jobId>",
            help=_("Training job ID."),
        )
        mandatary_group = parser.add_argument_group("mandatary arguments")
        parser._action_groups.insert(1, parser._action_groups.pop())
        mandatary_group.add_argument(
            "--worker-server-num",
            metavar="<worker_server_num>",
            type=int,
            required=True,
            help=_("Number of workers in a training job."),
        )
        mandatary_group.add_argument(
            "--app-url",
            metavar="<app_url>",
            required=True,
            help=_(
                "Code directory of a training job, for example, /usr/app/."
            ),
        )
        mandatary_group.add_argument(
            "--boot-file-url",
            metavar="<boot_file_url>",
            required=True,
            help=_(
                "Boot file of a training job, which needs to be stored "
                "in the code directory."
            ),
        )
        mandatary_group.add_argument(
            "--spec-id",
            metavar="<spec_id>",
            required=True,
            type=int,
            help=_(
                "ID of the resource specifications selected for a "
                "training job."
            ),
        )
        mandatary_group.add_argument(
            "--engine-id",
            metavar="<engine_id>",
            required=True,
            type=int,
            help=_(
                "ID of the engine selected for a training job. "
                "The default value is 1."
            ),
        )
        mandatary_group.add_argument(
            "--model-id",
            metavar="<model_id>",
            required=True,
            type=int,
            help=_("ID of the built-in model of a training job."),
        )
        mandatary_group.add_argument(
            "--pre-version-id",
            metavar="<pre_version_id>",
            required=True,
            type=int,
            help=_("ID of the previous version of a training job."),
        )
        parser.add_argument(
            "--description",
            metavar="<description>",
            dest="job_desc",
            help=_("Description of a training job."),
        )
        parser.add_argument(
            "--log-url",
            metavar="<log_url>",
            help=_(
                "Boot file of a training job, which needs to be stored "
                "in the code directory."
            ),
        )
        parser.add_argument(
            "--data-url",
            metavar="<data_url>",
            help=_("OBS URL of the dataset required by a training job."),
        )
        parser.add_argument(
            "--dataset-id",
            metavar="<dataset_id>",
            help=_("Dataset ID of a training job."),
        )
        parser.add_argument(
            "--dataset-version-id",
            metavar="<dataset_version_id>",
            help=_(
                "Dataset version ID of a training job. This parameter "
                "must be used together with dataset_id, but cannot be "
                "used together with data_url or data_source."
            ),
        )
        parser.add_argument(
            "--train-url",
            metavar="<train_url>",
            help=_("OBS URL of the output file of a training job."),
        )
        parser.add_argument(
            "--user-image-url",
            metavar="<user_image_url>",
            help=_("SWR URL of a custom image used by a training job."),
        )
        parser.add_argument(
            "--user-command",
            metavar="<user_command>",
            help=_(
                "Boot command used to start the container of a custom image of"
                "a training job. The format is bash /home/work/run_train.sh."
            ),
        )
        parser.add_argument(
            "--parameter",
            metavar="label=<label>,value=<value>",
            required_keys=["label", "value"],
            action=parseractions.MultiKeyValueAction,
            help=_(
                "Running parameters of a training job. It is a collection of "
                "label-value pairs\n."
                "Example: --parameter label=flower,value=rose "
                "--parameter label=color,value=red"
            ),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1

        attrs = {"config": {}}
        if parsed_args.job_desc:
            attrs["job_desc"] = parsed_args.job_desc

        config_attrs = (
            "worker_server_num",
            "app_url",
            "boot_file_url",
            "parameter",
            "pre_version_id",
            "data_url",
            "dataset_id",
            "dataset_version_id",
            "spec_id",
            "engine_id",
            "model_id",
            "train_url",
            "log_url",
            "user_image_url",
            "user_command",
        )

        for config_attr in config_attrs:
            val = getattr(parsed_args, config_attr)
            if val:
                attrs["config"][config_attr] = val

        data = client.create_training_job_version(parsed_args.jobId, **attrs)

        display_columns, columns = _get_columns(data)
        data = utils.get_item_properties(data, columns, formatters=_formatters)

        return display_columns, data


class ShowTrainingJobVersion(command.ShowOne):
    _description = _("Show details of a modelarts Training Job Version")

    def get_parser(self, prog_name):
        parser = super(ShowTrainingJobVersion, self).get_parser(prog_name)
        parser.add_argument(
            "jobId",
            metavar="<jobId>",
            help=_("ID of a training job"),
        )
        parser.add_argument(
            "versionId",
            metavar="<versionId>",
            help=_("Version ID of a training job."),
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1

        obj = client.get_training_job_version(
            parsed_args.jobId, parsed_args.versionId
        )
        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)

        return display_columns, data


class DeleteTrainingJobVersion(command.Command):
    _description = _("Delete ModelArts training job version.")

    def get_parser(self, prog_name):
        parser = super(DeleteTrainingJobVersion, self).get_parser(prog_name)
        parser.add_argument(
            "jobId",
            metavar="<jobId>",
            help=_("ID of the training job."),
        )
        parser.add_argument(
            "versionId",
            metavar="<versionId>",
            help=_("Version id of the training job."),
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1

        client.delete_training_job_version(
            parsed_args.jobId, parsed_args.versionId
        )
