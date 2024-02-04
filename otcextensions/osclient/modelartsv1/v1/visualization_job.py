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
"""ModelArts visualization job v1 action implementations"""
import logging

from osc_lib import utils
from osc_lib.command import command
from otcextensions.common import sdk_utils
from otcextensions.common import cli_utils
from otcextensions.i18n import _
from osc_lib.cli import parseractions

LOG = logging.getLogger(__name__)

_formatters = {
    "create_time": cli_utils.UnixTimestampFormatter,
}
#     "config": cli_utils.YamlFormat}

def _flatten_output(obj):
    data = {
        "quotas": obj.quotas,
        "is_success": obj.is_success,
        "job_total_count": obj.job_total_count,
        "job_count_limit": obj.job_count_limit,
        "jobs": obj.jobs,
        "error_code": obj.error_code,
        "error_msg": obj.error_msg,
    }
    return data


def _get_columns(item):
    column_map = {}
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


class DeleteVisualizationJob(command.Command):
    _description = _("Delete ModelArts Visualization Job")

    def get_parser(self, prog_name):
        parser = super(DeleteVisualizationJob, self).get_parser(prog_name)
        parser.add_argument(
            "--job_id",
            metavar="<job_id>",
            help=_("Name of the visualization job to delete."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1
        client.delete_visjob(visualization_job=parsed_args.job_id)


class CreateVisualizationJob(command.ShowOne):
    _description = _("Create a Visualization Job model")

    def get_parser(self, prog_name):
        parser = super(CreateVisualizationJob, self).get_parser(prog_name)

        parser.add_argument(
            "--job_name",
            metavar="<job_name>",
            required=True,
            help=_(
                "Name of a visualization job. The value is a string of "
                "1 to 20 characters consisting of only digits, letters, "
                "underscores (_), and hyphens (-).phens (-)."
            ),
        )
        parser.add_argument(
            "--job_desc",
            metavar="<job_desc>",
            required=False,
            help=_(
                "Description of a visualization job. The value is a "
                "string of 0 to 256 characters. By default, this "
                "parameter is left blank."
            ),
        )
        parser.add_argument(
            "--train_url",
            metavar="<train_url>",
            required=True,
            help=_("OBS path"),
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1

        attrs = {}

        if parsed_args.job_name:
            attrs["job_name"] = parsed_args.job_name

        if parsed_args.job_desc:
            attrs["job_desc"] = parsed_args.job_desc

        if parsed_args.train_url:
            attrs["train_url"] = parsed_args.train_url

        obj = client.create_visjob(**attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)
        return (display_columns, data)


class ModifyVisualizationJob(command.ShowOne):
    _description = _("Modify Visualization Job Description")

    def get_parser(self, prog_name):
        parser = super(ModifyVisualizationJob, self).get_parser(prog_name)

        parser.add_argument(
            "--job_id",
            metavar="<job_id>",
            required=True,
            help=_("ID of a visualization job"),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1

        attrs = {}

        if parsed_args.job_id:
            attrs["job_id"] = parsed_args.job_id

        obj = client.modify_visjob_desc(**attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)
        return (display_columns, data)


class StopVisualizationJob(command.ShowOne):
    _description = _("Stop Visualization Job")

    def get_parser(self, prog_name):
        parser = super(StopVisualizationJob, self).get_parser(prog_name)

        parser.add_argument(
            "--job_id",
            metavar="<job_id>",
            required=True,
            help=_("ID of a visualization job"),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1

        attrs = {}

        if parsed_args.job_id:
            attrs["job_id"] = parsed_args.job_id

        obj = client.stop_visjob(**attrs)
        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)
        return (display_columns, data)


class RestartVisualizationJob(command.ShowOne):
    _description = _("Restart Visualization Job")

    def get_parser(self, prog_name):
        parser = super(RestartVisualizationJob, self).get_parser(prog_name)
        parser.add_argument(
            "job_id", metavar="<job_id>", help=_("ID of a visualization job")
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.css

        data = client.restart_cluster(
            cluster=parsed_args.cluster,
        )

        display_columns, columns = _get_columns(data)
        data = utils.get_item_properties(data, columns)

        return (display_columns, data)


class ShowVisualizationJob(command.ShowOne):
    _description = _("Show details of a visualization job")

    def get_parser(self, prog_name):
        parser = super(ShowVisualizationJob, self).get_parser(prog_name)
        parser.add_argument(
            "--job_id", metavar="<job_id>", help=_("ID of a visualization job")
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1

        data = client.show_visjob(
            visualization_job=parsed_args.job_id,
        )

        display_columns, columns = _get_columns(data)
        data = utils.get_item_properties(data, columns)

        return (display_columns, data)


class ListVisualizationJobs(command.Lister):
    _description = _(
        "Query the visualization jobs that meet the search criteria."
    )
    columns = ("job_id", "job_name", "created_at")

    def get_parser(self, prog_name):
        parser = super(ListVisualizationJobs, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1

        query = {}

        data = client.visualization_jobs(**query)
        _formatters = {"Created At": cli_utils.UnixTimestampFormatter}

        table = (
            self.columns,
            (
                utils.get_dict_properties(_flatten_output(s), self.columns, formatters=_formatters)
                for s in data
            ),
        )
        return table
