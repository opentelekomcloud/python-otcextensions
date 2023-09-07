# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
"""DIS Stream v2 action implementations"""
import logging

from osc_lib import utils
# from osc_lib.cli import parseractions
from osc_lib import exceptions
from osc_lib.command import command

from otcextensions.i18n import _
from otcextensions.common import sdk_utils
from otcextensions.common import cli_utils


LOG = logging.getLogger(__name__)


_formatters = {
    'obs_destination_descriptor': cli_utils.YamlFormat,
    'obs_destination_description': cli_utils.YamlFormat,
    'partitions': cli_utils.YamlFormat,
    'created_at': cli_utils.UnixTimestampFormatter,
    'last_transfer_timestamp': cli_utils.UnixTimestampFormatter,
}


def _get_columns(item):
    column_map = {}
    hidden = [
        'location',
        'id',
        'stream_id',
    ]
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map,
                                                           hidden)


CONSUMER_STRATEGY_CHOICES = ('LATEST', 'TRIM_HORIZON',)


PARTITION_FORMAT_CHOICES = (
    'yyyy',
    'yyyy/MM',
    'yyyy/MM/dd',
    'yyyy/MM/dd/HH',
    'yyyy/MM/dd/HH/mm',
)


RECORD_DELIMITER_CHOICES = (',', ';', '|', '\\n',)


class ListDumpTasks(command.Lister):

    _description = _("List Dump Tasks.")
    display_columns = (
        'Task Name',
        'Task Id',
        'Destination Type',
        'Created At',
        'Status'
    )
    columns = (
        'task_name',
        'task_id',
        'destination_type',
        'created_at',
        'status',
    )

    def get_parser(self, prog_name):
        parser = super(ListDumpTasks, self).get_parser(prog_name)
        parser.add_argument(
            'streamName',
            metavar='<streamName>',
            help=_("Specifies the name of the DIS Stream."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dis
        data = client.dump_tasks(parsed_args.streamName)

        return (
            self.display_columns, (
                utils.get_item_properties(
                    s, self.columns, formatters=_formatters
                )
                for s in data
            )
        )


class ShowDumpTask(command.ShowOne):
    _description = _("Query Details of a Dump Task.")

    def get_parser(self, prog_name):
        parser = super(ShowDumpTask, self).get_parser(prog_name)
        parser.add_argument(
            'streamName',
            metavar='<streamName>',
            help=_("Specifies the name of the DIS Stream."),
        )
        parser.add_argument(
            'taskName',
            metavar='<taskName>',
            help=_("Specifies the name of Dump Task Name."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dis
        obj = client.get_dump_task(parsed_args.streamName,
                                   parsed_args.taskName)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)

        return (display_columns, data)


class CreateDumpTask(command.ShowOne):
    _description = _("Adding a Dump Task.")

    def get_parser(self, prog_name):
        parser = super(CreateDumpTask, self).get_parser(prog_name)
        parser.add_argument(
            'streamName',
            metavar='<streamName>',
            help=_("Specifies the name of the DIS Stream."),
        )
        parser.add_argument(
            'taskName',
            metavar='<taskName>',
            help=_("Name of the dump task."),
        )
        parser.add_argument(
            '--destination-type',
            metavar='<destrination_type>',
            default='OBS',
            help=_("Specifies the name of the DIS Stream."),
        )
        parser.add_argument(
            '--agency-name',
            metavar='<agency_name>',
            required=True,
            help=_("Name of the agency created on IAM. DIS uses an "
                   "agency to access your specified resources."),
        )
        parser.add_argument(
            '--deliver-time-interval',
            metavar='<deliver_time_interval>',
            required=True,
            type=int,
            help=_("User-defined interval at which data is imported from "
                   "the current DIS stream into OBS."),
        )
        parser.add_argument(
            '--consumer-strategy',
            dest='consumer_strategy',
            metavar='{' + ','.join(CONSUMER_STRATEGY_CHOICES) + '}',
            type=lambda s: s.upper(),
            choices=CONSUMER_STRATEGY_CHOICES,
            help=_("Offset."
                   "\nLATEST: Maximum offset, indicating that the latest "
                   "data will be extracted."
                   "\nTRIM_HORIZON: Minimum offset, indicating that the "
                   "earliest data will be extracted."
                   "\nDefault value: LATEST."),
        )
        parser.add_argument(
            '--file-prefix',
            metavar='<file_prefix>',
            help=_("Directory to store files that will be dumped to OBS. "
                   "Different directory levels are separated by slashes (/) "
                   "and cannot start with slashes."),
        )
        parser.add_argument(
            '--partition-format',
            dest='partition_format',
            metavar='{' + ','.join(PARTITION_FORMAT_CHOICES) + '}',
            choices=PARTITION_FORMAT_CHOICES,
            help=_("Directory structure of the object file written into OBS. "
                   "The directory structure is in the format of yyyy/MM/dd/"
                   "HH/mm (time at which the dump task was created). "
                   "\nN/A: Leave this parameter empty, indicating that the "
                   "date and time directory is not used."),
        )
        parser.add_argument(
            '--obs-bucket-path',
            metavar='<obs_bucket_path>',
            required=True,
            help=_("Name of the OBS bucket used to store data from the "
                   "DIS stream."),
        )
        parser.add_argument(
            '--destination-file-type',
            metavar='<destination_file_type>',
            help=_("Dump file format. Possible values:"
                   "Text (default)"),
        )
        parser.add_argument(
            '--record-delimiter',
            dest='record_delimiter',
            metavar='{' + ','.join(RECORD_DELIMITER_CHOICES) + '}',
            choices=RECORD_DELIMITER_CHOICES,
            help=_("Delimiter for the dump file, which is used to separate "
                   "the user data that is written into the dump file. "
                   "Default: \\n"),
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dis

        args_list = (
            'agency_name',
            'deliver_time_interval',
            'consumer_strategy',
            'file_prefix',
            'partition_format',
            'obs_bucket_path',
            'destination_file_type',
            'record_delimiter',
        )
        obs_dest_spec = {
            'task_name': parsed_args.taskName
        }
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                obs_dest_spec[arg] = val

        attrs = {
            'destination_type': parsed_args.destination_type,
            'obs_destination_descriptor': obs_dest_spec
        }

        client.create_dump_task(parsed_args.streamName, **attrs)

        obj = client.get_dump_task(parsed_args.streamName,
                                   parsed_args.taskName)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)
        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)

        return (display_columns, data)


class DeleteDumpTask(command.Command):

    _description = _("Deletes DIS Dump Task(s).")

    def get_parser(self, prog_name):
        parser = super(DeleteDumpTask, self).get_parser(prog_name)
        parser.add_argument(
            'streamName',
            metavar='<streamName>',
            help=_("Name of Dis Stream."),
        )
        parser.add_argument(
            'taskName',
            metavar='<taskName>',
            nargs='+',
            help=_("Name of Dump Task(s) to delete."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dis
        result = 0
        for task_name in parsed_args.taskName:
            try:
                client.delete_dump_task(parsed_args.streamName, task_name)
            except Exception as e:
                result += 1
                LOG.error(_("Failed to delete dump task with "
                          "name '%(task_name)s': %(e)s"),
                          {'task_name': task_name, 'e': e})
        if result > 0:
            total = len(parsed_args.taskName)
            msg = (_("%(result)s of %(total)s dump task(s) failed "
                   "to delete.") % {'result': result, 'total': total})
            raise exceptions.CommandError(msg)


class StartDumpTask(command.Command):

    _description = _("Start Dump Task(s).")

    def get_parser(self, prog_name):
        parser = super(StartDumpTask, self).get_parser(prog_name)
        parser.add_argument(
            'streamName',
            metavar='<streamName>',
            help=_("Name of Dis Stream."),
        )
        parser.add_argument(
            'taskId',
            metavar='<taskId>',
            nargs='+',
            help=_("ID of Dump Task(s) to Start."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dis
        client.start_dump_task(parsed_args.streamName, parsed_args.taskId)


class PauseDumpTask(command.Command):

    _description = _("Pause Dump Task(s).")

    def get_parser(self, prog_name):
        parser = super(PauseDumpTask, self).get_parser(prog_name)
        parser.add_argument(
            'streamName',
            metavar='<streamName>',
            help=_("Name of Dis Stream."),
        )
        parser.add_argument(
            'taskId',
            metavar='<taskId>',
            nargs='+',
            help=_("ID of Dump Task(s) to Pause."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dis
        client.pause_dump_task(parsed_args.streamName, parsed_args.taskId)
