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
"""ModelArts training job version v1 action implementations"""
import logging

from osc_lib import utils
from osc_lib.command import command
from otcextensions.common import cli_utils
from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


_formatters = {"system_metric_list": cli_utils.YamlFormat}


def _get_columns(item):
    column_map = {}
    hidden = ["location"]
    return sdk_utils.get_osc_show_columns_for_sdk_resource(
        item, column_map, hidden
    )


class DeleteTrainingJobVersion(command.Command):
    _description = _("Delete ModelArts Training Job Version")

    def get_parser(self, prog_name):
        parser = super(DeleteTrainingJobVersion, self).get_parser(prog_name)
        parser.add_argument(
            "job_id",
            metavar="<job_id>",
            help=_("Job id of the trainjob version to delete."),
        )
        parser.add_argument(
            "version_id",
            metavar="<version_id>",
            help=_("Version id of the trainjob version to delete."),
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1

        params = {}
        if parsed_args.job_id:
            params["job_id"] = parsed_args.job_id
        if parsed_args.version_id:
            params["version_id"] = parsed_args.version_id

        client.delete_trainjob_version(
            version_id=parsed_args.version_id, **params
        )


class CreateTrainingJobVersion(command.ShowOne):
    _description = _("Create a ModelArts Training Job Version")

    def get_parser(self, prog_name):
        parser = super(CreateTrainingJobVersion, self).get_parser(prog_name)
        parser.add_argument(
            "--job-id",
            metavar="<job_id>",
            required=True,
            help=_("ID of a training job"),
        )
        parser.add_argument(
            "--job-desc",
            metavar="<job_desc>",
            help=_(
                "Description of a training job. The value is a string of "
                "0 to 256 characters. By default, this parameter is left "
                "blank."
            ),
        )
        parser.add_argument(
            "--config",
            metavar="<config>",
            required=False,
            help=_("Parameters for creating a training job"),
        )
        parser.add_argument(
            "--worker-server-num",
            metavar="<worker_server_num>",
            required=True,
            type=int,
            help=_(
                "Code directory of a training job, for example, /usr/app/."
            ),
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
            "--boot-file-url",
            metavar="<boot_file_url>",
            required=True,
            help=_(
                "Boot file of a training job, which needs to be "
                "stored in the code directory."
            ),
        )
        parser.add_argument(
            "--parameter",
            metavar="<parameter>",
            help=_(
                "Running parameters of a training job. "
                "It is a collection of label-value pairs."
            ),
        )
        parser.add_argument(
            "--data-url",
            metavar="<data_url>",
            required=False,
            help=_("OBS URL of the dataset required by a training job."),
        )
        parser.add_argument(
            "--pre-version-id",
            metavar="<pre_version_id>",
            type=int,
            required=True,
            help=_("ID of the previous version of a training job."),
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
                "Boot command used to start the container of a custom "
                "image of a training job."
            ),
        )
        parser.add_argument("--dataset-id", metavar="<dataset_id>", help=_(""))
        parser.add_argument(
            "--dataset-version",
            metavar="<dataset_version>",
            required=False,
            help=_(""),
        )
        parser.add_argument("--type", metavar="<type>", help=_(""))
        parser.add_argument(
            "--dataset-version-id", metavar="<dataset_version_id>", help=_("")
        )
        parser.add_argument("--log-url", metavar="<log_url>", help=_(""))
        return parser

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
            "pre_version_id",
        )

        # nfs_attrs = ('id', 'src_path')
        for config_attr in config_attrs:
            val = getattr(parsed_args, config_attr)
            if val:
                config[config_attr] = val

        # if parsed_args.config_parameter:
        #    config.update(parameter=parsed_args.config_parameter)
        if parsed_args.job_id:
            attrs["job_id"] = parsed_args.job_id
        if parsed_args.job_desc:
            attrs["job_desc"] = parsed_args.job_desc

        attrs.update(config=config)
        obj = client.create_trainingjob_version(**attrs)
        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)
        return display_columns, data


class ShowTrainingJobVersion(command.ShowOne):
    _description = _("Show details of a modelarts Training Job")

    def get_parser(self, prog_name):
        parser = super(ShowTrainingJobVersion, self).get_parser(prog_name)
        parser.add_argument(
            "--job-id", metavar="<job_id>", help=_("ID of a training job")
        )
        parser.add_argument(
            "--version-id",
            metavar="<version_id>",
            help=_("Version ID of a training job"),
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1
        query = {}
        if parsed_args.job_id:
            query["job_id"] = parsed_args.job_id

        if parsed_args.version_id:
            query["version_id"] = parsed_args.version_id

        obj = client.show_trainingjob_version(**query)
        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return display_columns, data


class QueryBuiltInAlgo:
    pass


class ObtainTrainingJobLogName:
    pass


class ModifyTrainingJobDescription:
    pass


class StopTrainingJob:
    pass


class ListTrainingJobLogs:
    pass


class ListTrainingJobVersions(command.Lister):
    _description = _("Get the list of training job versions")
    columns = ("Version Id", "Version Name")

    def get_parser(self, prog_name):
        parser = super(ListTrainingJobVersions, self).get_parser(prog_name)
        parser.add_argument(
            "--job-id", metavar="<job_id>", help=_("ID of the job.")
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1

        query = {}
        if parsed_args.job_id:
            query["job_id"] = parsed_args.job_id

        data = client.trainingjob_versions(**query)
        # for d in data:
        #    print(d.to_dict(original_names=True, computed=False))
        #    break
        table = (
            self.columns,
            (utils.get_dict_properties(s, self.columns) for s in data),
        )
        return table
