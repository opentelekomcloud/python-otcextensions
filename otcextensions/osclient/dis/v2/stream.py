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
from osc_lib.cli import parseractions
from osc_lib import exceptions
from osc_lib.command import command

from otcextensions.i18n import _
from otcextensions.common import sdk_utils

from otcextensions.osclient.dis.v2 import dis_utils


LOG = logging.getLogger(__name__)


_formatters = {
    'partitions': dis_utils.YamlFormat,
    'created_at': dis_utils.UnixTimestampFormatter,
    'updated_at': dis_utils.UnixTimestampFormatter,
}


def _get_columns(item):
    column_map = {}
    hidden = [
        'location',
        'stream_id',
    ]
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map,
                                                           hidden)


class ListStreams(command.Lister):

    _description = _("List Dis Stream.")
    display_columns = (
        'Name',
        'Stream Type',
        'Data Type',
        'Partition Count',
        'AutoScale Enabled',
        'Status'
    )
    columns = (
        'name',
        'stream_type',
        'data_type',
        'partition_count',
        'is_auto_scale_enabled',
        'status'
    )

    def get_parser(self, prog_name):
        parser = super(ListStreams, self).get_parser(prog_name)

        parser.add_argument(
            '--limit',
            metavar='<limit>',
            type=int,
            help=_("Limit to fetch number of records."),
        )
        parser.add_argument(
            '--start-stream-name',
            metavar='<start_stream_name>',
            help=_("Limit to fetch number of records."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dis
        args_list = (
            'limit',
            'start_stream_name',
        )
        attrs = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        data = client.streams(**attrs)

        return (
            self.display_columns,
            (utils.get_item_properties(s, self.columns) for s in data)
        )


class ShowStream(command.ShowOne):
    _description = _("Show DIS Stream details")

    def get_parser(self, prog_name):
        parser = super(ShowStream, self).get_parser(prog_name)
        parser.add_argument(
            'stream',
            metavar='<stream>',
            help=_("Specifies the name of the DIS Stream."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dis
        obj = client.get_stream(parsed_args.stream)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)

        return (display_columns, data)


class CreateStream(command.ShowOne):
    _description = _("Create new DIS Stream.")

    def get_parser(self, prog_name):
        parser = super(CreateStream, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help=_("Specifies the name of the DIS Stream."),
        )
        parser.add_argument(
            '--partition-count',
            metavar='<partition_count>',
            type=int,
            required=True,
            help=_("Number of partitions. Partitions are the base throughput "
                   "unit of the DIS stream."),
        )
        parser.add_argument(
            '--stream-type',
            metavar='<stream_type>',
            help=_("Stream type. Supported Types:"
                   "\nCOMMON: a common stream with a bandwidth of 1 MB/s."
                   "\nADVANCED: an advanced stream with a bandwidth of 5 MB/s."
                   "\nDefault value: COMMON."),
        )
        parser.add_argument(
            '--data-type',
            metavar='<data_type>',
            help=_("Source data type. Supported Types:"
                   "\nBLOB: a collection of binary data stored as a single "
                   "entity in a database management system."
                   "\nDefault value: BLOB."),
        )
        parser.add_argument(
            '--data-duration',
            metavar='<data_duration>',
            type=int,
            help=_("Data retention period."
                   "\nValue range: 24–72"
                   "\nUnit: hour"
                   "\nDefault value: 24"),
        )
        parser.add_argument(
            '--autoscale',
            action='store_true',
            help=_("Whether to enable auto scaling."),
        )
        parser.add_argument(
            '--autoscale-min-count',
            metavar='<autoscale_min_count>',
            dest='auto_scale_min_partition_count',
            type=int,
            default=1,
            help=_("Minimum number of partitions for automatic scale-down "
                   "when auto scaling is enabled. Default: 1"),
        )
        parser.add_argument(
            '--autoscale-max-count',
            metavar='<autoscale_max_count>',
            dest='auto_scale_max_partition_count',
            type=int,
            default=1,
            help=_("Maximum number of partitions for automatic scale-up when "
                   "auto scaling is enabled. Default: 1"),
        )
        parser.add_argument(
            '--compression-format',
            metavar='<compression_format>',
            help=_("Data compression type. The following types are available:"
                    "\nsnappy"
                    "\ngzip"
                    "\nzip"
                    "\nData is not compressed by default."),
        )
        parser.add_argument(
            '--tag',
            action=parseractions.MultiKeyValueAction,
            metavar='key=<key>,value=<value>',
            required_keys=['key', 'value'],
            dest='tags',
            help=_('Add Tag(s) to a Stream.\n'
                   'key=<key>: Tag key. The value can contain 1 to 36 '
                   'characters. Only digits, letters, hyphens (-) and '
                   'underscores (_) are allowed.\n'
                   'value=<value>: Tag value. The value can contain 0 to 43 '
                   'characters. Only digits, letters, hyphens (-) and '
                   'underscores (_) are allowed.'),
        )
        parser.add_argument(
            '--sys-tag',
            action=parseractions.MultiKeyValueAction,
            metavar='key=<key>,value=<value>',
            required_keys=['key', 'value'],
            dest='sys_tags',
            help=_('Add Tag(s) to Stream enterprise projects.\n'
                   'key=<key>: Tag key. The value can contain 1 to 36 '
                   'characters. Only digits, letters, hyphens (-) and '
                   'underscores (_) are allowed.\n'
                   'value=<value>: Tag value. The value can contain 0 to 43 '
                   'characters. Only digits, letters, hyphens (-) and '
                   'underscores (_) are allowed.'),
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dis

        args_list = (
            'name',
            'partition_count',
            'stream_type',
            'data_type',
            'data_duration',
            'auto_scale_min_partition_count',
            'auto_scale_max_partition_count',
            'compression_format',
            'tags',
            'sys_tags',
        )
        attrs = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        if parsed_args.autoscale:
            attrs.update(auto_scale_enabled=True)

        obj = client.create_stream(**attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class UpdateStreamPartition(command.ShowOne):
    _description = _("Update Partition Quantity of a DIS Stream.")

    columns = (
        'name',
        'current_partition_count',
        'target_partition_count',
    )

    display_columns = (
        'stream_name',
        'current_partition_count',
        'target_partition_count',
    )

    def get_parser(self, prog_name):
        parser = super(UpdateStreamPartition, self).get_parser(prog_name)
        parser.add_argument(
            'stream',
            metavar='<stream>',
            help=_("Specifies the Name of the DIS Stream."),
        )
        parser.add_argument(
            '--partition-count',
            metavar='<partition_count>',
            type=int,
            required=True,
            help=_("Number of the target partitions.The value is an integer "
                   "greater than 0."
                   "\nEach stream can be scaled up and down for five times "
                   "within one hour. After a stream is scaled up or down, it "
                   "cannot be scaled up or down again in the next one hour."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dis
        attrs = {'stream_name': parsed_args.stream}
        if parsed_args.partition_count:
            attrs.update(target_partition_count=parsed_args.partition_count)

        obj = client.update_stream_partition(parsed_args.stream, **attrs)

        # display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, self.columns)

        return (self.display_columns, data)


class DeleteStream(command.Command):

    _description = _("Deletes DIS Stream.")

    def get_parser(self, prog_name):
        parser = super(DeleteStream, self).get_parser(prog_name)
        parser.add_argument(
            'stream',
            metavar='<stream>',
            nargs='+',
            help=_("Name of Dis Stream(s) to delete."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dis
        result = 0
        for stream in parsed_args.stream:
            try:
                client.delete_stream(stream)
            except Exception as e:
                result += 1
                LOG.error(_("Failed to delete Dis Stream with "
                          "name '%(stream)s': %(e)s"),
                          {'stream': stream, 'e': e})
        if result > 0:
            total = len(parsed_args.stream)
            msg = (_("%(result)s of %(total)s DIS Stream(s) failed "
                   "to delete.") % {'result': result, 'total': total})
            raise exceptions.CommandError(msg)
