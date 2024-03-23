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

from cliff import columns as cliff_columns
from osc_lib import exceptions
from osc_lib import utils
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


class ListVisualizationJobs(command.Lister):
    _description = _(
        "Query the visualization jobs that meet the search criteria."
    )
    columns = (
        "Job Id",
        "Job Name",
        "Created At",
    )

    def get_parser(self, prog_name):
        parser = super(ListVisualizationJobs, self).get_parser(prog_name)

        sort_by_choices = [
            "job_id",
            "job_name",
            "job_desc",
            "status",
            "create_time",
        ]

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
        parser.add_argument(
            "--status",
            choices=list(JobStatus.CHOICES_MAP.keys()),
            type=int,
            help=_(
                "Job status. The options are as follows:\n" + JobStatus.STR
            ),
        )
        parser.add_argument(
            "--sort-by",
            metavar="{" + ",".join(sort_by_choices) + "}",
            type=lambda s: s.lower(),
            choices=sort_by_choices,
            help=_("Sorting field. Default value: job_name"),
        )
        parser.add_argument(
            "--order",
            metavar="{asc, desc}",
            type=lambda s: s.lower(),
            choices=["asc", "desc"],
            help=_("Sorting order. Default value: desc"),
        )
        parser.add_argument(
            "--search-content",
            metavar="<search_content>",
            help=_("Search content, for example, a training job name."),
        )
        parser.add_argument(
            "--workspace-id",
            metavar="<workspace_id>",
            help=_("Workspace ID."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1

        attrs_list = (
            "limit",
            "offset",
            "status",
            "sort_by",
            "order",
            "search_content",
            "workspace_id",
        )
        query_params = {}
        for arg in attrs_list:
            val = getattr(parsed_args, arg)
            if val or str(val) == "0":
                query_params[arg] = val

        data = client.visualization_jobs(**query_params)
        _formatters = {
            "Created At": cli_utils.UnixTimestampFormatter,
            "Status": JobStatus,
        }
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


class CreateVisualizationJob(command.ShowOne):
    _description = _("Create a Visualization Job model")

    def get_parser(self, prog_name):
        parser = super(CreateVisualizationJob, self).get_parser(prog_name)

        parser.add_argument(
            "name",
            metavar="<name>",
            help=_("Name of a visualization job."),
        )
        parser.add_argument(
            "--description",
            metavar="<description>",
            dest="job_desc",
            help=_("Description of a visualization job."),
        )
        parser.add_argument(
            "--train-url",
            metavar="<train_url>",
            required=True,
            help=_("OBS path"),
        )
        parser.add_argument(
            "--job-type",
            metavar="<job_type>",
            help=_("Type of a visualization job"),
        )
        parser.add_argument(
            "--flavor",
            metavar="<flavor>",
            help=_("Specifications when a visualization job is created."),
        )
        parser.add_argument(
            "--auto-stop-duration",
            metavar="<auto_stop_duration>",
            type=int,
            help=_("Auto stop duration. The value ranges from 0 to 24."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1

        attrs = {
            "job_name": parsed_args.name,
            "train_url": parsed_args.train_url,
        }

        if parsed_args.job_desc:
            attrs["job_desc"] = parsed_args.job_desc
        if parsed_args.job_type:
            attrs["job_type"] = parsed_args.job_type
        if parsed_args.flavor:
            attrs["flavor"] = {"code": parsed_args.flavor}

        if parsed_args.auto_stop_duration:
            attrs["schedule"] = {
                "type": "stop",
                "time_unit": "HOURS",
                "duration": parsed_args.auto_stop_duration,
            }

        obj = client.create_visualization_job(**attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)
        return (display_columns, data)


class ShowVisualizationJob(command.ShowOne):
    _description = _("Show details of a visualization job")

    def get_parser(self, prog_name):
        parser = super(ShowVisualizationJob, self).get_parser(prog_name)
        parser.add_argument(
            "jobId",
            metavar="<jobId>",
            help=_("ID of a visualization job"),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1

        data = client.get_visualization_job(parsed_args.jobId)

        display_columns, columns = _get_columns(data)
        data = utils.get_item_properties(data, columns)

        return (display_columns, data)


class UpdateVisualizationJob(command.ShowOne):
    _description = _("Modify Visualization Job Description")

    def get_parser(self, prog_name):
        parser = super(UpdateVisualizationJob, self).get_parser(prog_name)

        parser.add_argument(
            "jobId",
            metavar="<jobId>",
            help=_("ID of a visualization job"),
        )
        parser.add_argument(
            "--description",
            metavar="<description>",
            required=True,
            help=_("Description of a visualization job"),
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1

        obj = client.update_visualization_job(
            parsed_args.jobId, parsed_args.description
        )

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)
        return (display_columns, data)


class StopVisualizationJob(command.ShowOne):
    _description = _("Stop Visualization Job")

    def get_parser(self, prog_name):
        parser = super(StopVisualizationJob, self).get_parser(prog_name)

        parser.add_argument(
            "jobId",
            metavar="<jobId>",
            help=_("ID of a visualization job"),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1

        obj = client.stop_visualization_job(parsed_args.jobId)
        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)
        return (display_columns, data)


class RestartVisualizationJob(command.ShowOne):
    _description = _("Restart Visualization Job")

    def get_parser(self, prog_name):
        parser = super(RestartVisualizationJob, self).get_parser(prog_name)
        parser.add_argument(
            "jobId",
            metavar="<jobId>",
            help=_("ID of a visualization job"),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.css

        data = client.restart_visualization_job(parsed_args.jobId)

        display_columns, columns = _get_columns(data)
        data = utils.get_item_properties(data, columns)

        return (display_columns, data)


class DeleteVisualizationJob(command.Command):
    _description = _("Delete ModelArts visualization Job(s)")

    def get_parser(self, prog_name):
        parser = super(DeleteVisualizationJob, self).get_parser(prog_name)
        parser.add_argument(
            "jobId",
            metavar="<JobId>",
            nargs="+",
            type=int,
            help=_("ID of the ModelArts visualization job(s) to be deleted."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1
        result = 0
        for job_id in parsed_args.jobId:
            try:
                client.delete_visualization_job(job_id)
            except Exception as e:
                result += 1
                LOG.error(
                    _(
                        "Failed to delete visualization job(s) with "
                        "ID '%(job_id)s': %(e)s"
                    ),
                    {"job_id": job_id, "e": e},
                )
        if result > 0:
            total = len(parsed_args.jobId)
            msg = _(
                "%(result)s of %(total)s visualization job(s) failed "
                "to delete."
            ) % {
                "result": result,
                "total": total,
            }
            raise exceptions.CommandError(msg)
