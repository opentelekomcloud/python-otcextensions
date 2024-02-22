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


"""
def translate_response(func):
    def new(self, *args, **kwargs):
        obj = func(self, *args, **kwargs)
        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)
        return (display_columns, data)

    new.__name__ = func.__name__
    new.__doc__ = func.__doc__
    return new
"""


class DeleteTrainingJob(command.Command):
    _description = _("Delete ModelArts Training Job")

    def get_parser(self, prog_name):
        parser = super(DeleteTrainingJob, self).get_parser(prog_name)
        parser.add_argument(
            "jobId",
            metavar="<jobId>",
            help=_("Job id of the trainjob to delete."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1

        client.delete_trainingjob(job_id=parsed_args.jobId)


class CreateTrainingJob(command.ShowOne):
    _description = _("Create a ModelArts Training Job")

    def get_parser(self, prog_name):
        parser = super(CreateTrainingJob, self).get_parser(prog_name)
        parser.add_argument(
            "--job-name",
            metavar="<job_name>",
            required=True,
            help=_(
                "Training job name. The value is a string of 1 to 64 "
                "characters consisting of only digits, "
                "letters, underscores (_), and hyphens (-)."
            ),
        )
        parser.add_argument(
            "--job-desc",
            metavar="<job_desc>",
            help=_(
                "Description of a training job. The value is a string "
                "of 0 to 256 characters. By default, this parameter "
                "is left blank."
            ),
        )
        parser.add_argument(
            "--workspace-id",
            metavar="<workspace_id>",
            help=_("Workspace where a job resides. Default value: 0"),
        )
        parser.add_argument(
            "--worker-server-num",
            metavar="<worker_server_num>",
            type=int,
            required=True,
            help=_("Number of workers in a training job."),
        )
        parser.add_argument(
            "--app-url",
            metavar="<app_url>",
            required=True,
            help=_(
                "Code directory of a training job, for example, /usr/app/."
            ),
        )
        parser.add_argument(
            "--boot-file-url",
            metavar="<boot_file_url>",
            required=True,
            help=_(
                "Boot file of a training job, which needs to be stored "
                "in the code directory."
            ),
        )
        parser.add_argument(
            "--log-url",
            metavar="<log_url>",
            required=True,
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
            "--data-source",
            metavar="<data_source>",
            help=_(
                "Dataset of a training job. This parameter cannot be "
                "used together with data_url, dataset_id, or "
                "dataset_version_id."
            ),
        )
        parser.add_argument(
            "--spec-id",
            metavar="<spec_id>",
            required=True,
            type=int,
            help=_(
                "ID of the resource specifications selected for a "
                "training job."
            ),
        )
        parser.add_argument(
            "--engine-id",
            metavar="<engine_id>",
            required=True,
            type=int,
            help=_(
                "ID of the engine selected for a training job. "
                "The default value is 1."
            ),
        )
        parser.add_argument(
            "--model-id",
            metavar="<model_id>",
            required=True,
            type=int,
            help=_("ID of the built-in model of a training job."),
        )
        parser.add_argument(
            "--train-url",
            metavar="<train_url>",
            help=_("OBS URL of the output file of a training job."),
        )
        parser.add_argument(
            "--dataset-version",
            metavar="<dataset_version>",
            help=_(
                "Dataset version ID of a training job. This parameter "
                "must be used together with dataset_id, but cannot be "
                "used together with data_url."
            ),
        )
        parser.add_argument(
            "--nfs",
            metavar="id=<id>,src_path=<src_path>,dest_path=<dest_path>",
            required_keys=["id", "src_path", "dest_path"],
            dest="nfs",
            action=parseractions.MultiKeyValueAction,
            help=_(
                "Automatic backup creation policy. "
                "This function is enabled by default."
            ),
        )
        parser.add_argument(
            "--host-path",
            metavar="src_path=<src_path>,dest_path=<dest_path>,"
            "read_only=<read_only>",
            required_keys=["src_path", "dest_path"],
            dest="host_path",
            action=parseractions.MultiKeyValueAction,
            help=_(
                "Automatic backup creation policy. "
                "This function is enabled by default."
            ),
        )
        parser.add_argument(
            "--parameter",
            metavar="label=<label>,value=<value>",
            required_keys=["label", "value"],
            dest="parameter",
            action=parseractions.MultiKeyValueAction,
            help=_(
                "Automatic backup creation policy."
                "This function is enabled by default."
            ),
        )
        return parser

    # @translate_response
    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1

        attrs = {}
        config = {}

        config_attrs = (
            "worker_server_num",
            "app_url",
            "boot_file_url",
            "parameter",
            "dataset_id",
            "dataset_version_id",
            "spec_id",
            "engine_id",
            "train_url",
            "log_url",
            "model_id",
        )
        volumes = []

        # nfs_attrs = ('id', 'src_path')
        for config_attr in config_attrs:
            val = getattr(parsed_args, config_attr)
            if val:
                config[config_attr] = val

        # if parsed_args.config_parameter:
        #    config.update(parameter=parsed_args.config_parameter)
        if parsed_args.job_name:
            attrs["job_name"] = parsed_args.job_name
        if parsed_args.job_desc:
            attrs["job_desc"] = parsed_args.job_desc
        if parsed_args.workspace_id:
            attrs["workspace_id"] = parsed_args.workspace_id
        if parsed_args.nfs:
            volumes.update({"nfs": parsed_args.nfs})
        if parsed_args.host_path:
            volumes.update({"host_path": parsed_args.host_path})
        if len(volumes):
            config.update(volumes=volumes)

        attrs.update(config=config)
        print("\n*******\nattrs\n\n****\n", attrs)
        obj = client.create_training_job(**attrs)
        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)
        return display_columns, data


class UpdateTrainingJobDescription(command.ShowOne):
    _description = _("Modify details of a MA TrainingJobDescription")

    def get_parser(self, prog_name):
        parser = super(UpdateTrainingJobDescription, self).get_parser(
            prog_name
        )
        parser.add_argument("jobId", metavar="<jobId>", help=_("Enter job id"))
        parser.add_argument(
            "--description",
            metavar="<description>",
            help=_("Enter description"),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1

        args_list = ["description"]
        attrs = {}
        for arg in args_list:
            if getattr(parsed_args, arg):
                attrs[arg] = getattr(parsed_args, arg)

        job = client.show_training_job(
            job=parsed_args.jobId,
        )

        data = client.modify_trainingjob_description(job.id, **attrs)

        display_columns, columns = _get_columns(data)
        data = utils.get_item_properties(data, columns)

        return display_columns, data


class StopTrainingJob(command.ShowOne):
    _description = _("Stop a Training Job.")

    def get_parser(self, prog_name):
        parser = super(StopTrainingJob, self).get_parser(prog_name)
        parser.add_argument(
            "--job-id",
            metavar="<job_id>",
            help=_("DevEnv Instance name or ID."),
        )
        parser.add_argument(
            "--version-id",
            metavar="<version_id>",
            help=_("DevEnv Instance name or ID."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1

        job = client.find_training_job(
            parsed_args.job_id, parsed_args.version_id, ignore_missing=False
        )
        return client.stop_training_job(job.id)


class ListTrainingJobs(command.Lister):
    _description = _("Get properties of a vm")
    columns = ("Job Id", "Job Name", "Created At")

    def get_parser(self, prog_name):
        parser = super(ListTrainingJobs, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1

        query = {}

        data = client.trainingjobs(**query)
        _formatters = {"Created At": cli_utils.UnixTimestampFormatter}
        table = (
            self.columns,
            (
                utils.get_dict_properties(
                    s, self.columns, formatters=_formatters
                )
                for s in data
            ),
        )
        return table
