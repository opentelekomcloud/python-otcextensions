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
"""DIS Data v2 action implementations"""
import logging

from osc_lib import utils
# from osc_lib import exceptions
from osc_lib.command import command

from otcextensions.i18n import _
from otcextensions.common import sdk_utils

from otcextensions.osclient.dis.v2 import dis_utils


LOG = logging.getLogger(__name__)


_formatters = {
    'timestamp': dis_utils.UnixTimestampFormatter,
    # 'records': dis_utils.YamlFormat,
}


def _get_columns(item):
    column_map = {}
    hidden = [
        'location',
        'app_id',
    ]
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map,
                                                           hidden)


CURSOR_TYPE_CHOICES = (
    'AT_SEQUENCE_NUMBER',
    'AFTER_SEQUENCE_NUMBER',
    'TRIM_HORIZON',
    'LATEST',
    'AT_TIMESTAMP',
)


class DownloadData(command.Lister):

    _description = _("Download Data.")

    columns = (
        'sequence_number',
        'data',
        'timestamp',
        'timestamp_type',
    )

    display_columns = (
        'Sequence Number',
        'Data',
        'Timestamp',
        'Timestamp Type',
    )

    def get_parser(self, prog_name):
        parser = super(DownloadData, self).get_parser(prog_name)

        parser.add_argument(
            '--partition-cursor',
            metavar='<partition_cursor>',
            required=True,
            help=_("Data cursor, which needs to be obtained through the API "
                   "for obtaining data cursors. Value: 1 to 512 characters."
                   "\nNote: The validity period of a data cursor is 5 minutes."
                   " Maximum number of apps to list in a single API call."),
        )
        parser.add_argument(
            '--max-fetch-bytes',
            metavar='<max_fetch_bytes>',
            help=_("Maximum number of bytes that can be obtained for each "
                   "request."
                   "\nNote: If the value is less than the size of a single "
                   "record in the partition, the record cannot be obtained."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dis
        attrs = {
            'partition-cursor': parsed_args.partition_cursor
        }
        if parsed_args.max_fetch_bytes:
            attrs.update(max_fetch_bytes=parsed_args.max_fetch_bytes)

        data = client.download_data(**attrs)

        return (
            self.display_columns,
            (
                utils.get_item_properties(
                    s, self.columns, formatters=_formatters
                ) for s in data
            )
        )


class ShowDataCursor(command.ShowOne):
    _description = _("Query Data Cursor.")

    def get_parser(self, prog_name):
        parser = super(ShowDataCursor, self).get_parser(prog_name)
        parser.add_argument(
            'stream',
            metavar='<stream>',
            help=_("Name of the stream."),
        )
        parser.add_argument(
            '--partition-id',
            metavar='<partition_id>',
            dest='partition-id',
            required=True,
            help=_("Partition ID of the stream."),
        )
        parser.add_argument(
            '--cursor-type',
            dest='cursor-type',
            metavar='{' + ','.join(CURSOR_TYPE_CHOICES) + '}',
            type=lambda s: s.upper(),
            choices=CURSOR_TYPE_CHOICES,
            help=_("Cursor Type."),
        )
        parser.add_argument(
            '--starting-seq-num',
            metavar='<starting_seq_num>',
            dest='starting-sequence-number',
            help=_("Sequence number. A sequence number is the unique "
                   "identifier of each record."),
        )
        parser.add_argument(
            '--timestamp',
            metavar='<timestamp>',
            type=int,
            help=_("Timestamp when the data record starts to be read, which "
                   "is closely related to cursor type `AT_TIMESTAMP`."),
        )
        parser.add_argument(
            '--stream-id',
            metavar='<stream_id>',
            dest='stream-id',
            help=_("Unique ID of the stream."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dis
        attrs = {
            'stream-name': parsed_args.stream
        }
        for arg in ('partition-id', 'cursor-type',
                    'starting-sequence-number',
                    'timestamp', 'stream-id',):
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        obj = client.get_data_cursor(**attrs)
        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class UploadData(command.Command):
    _description = _("upload data to DIS streams.")

    def get_parser(self, prog_name):
        parser = super(UploadData, self).get_parser(prog_name)
        parser.add_argument(
            'stream',
            metavar='<stream>',
            help=_("Specifies the name of the DIS Stream."),
        )
        parser.add_argument(
            '--stream-id',
            metavar='<stream_id>',
            help=_("Unique ID of the stream. If no stream is found based on "
                   "stream_name and stream_id is not empty, stream_id is "
                   "used to search for the stream."),
        )
        parser.add_argument(
            '--data',
            metavar='<data>',
            help=_("Data to be uploaded. The uploaded data is the serialized "
                   "binary data (character string encoded using Base64)."),
        )
        parser.add_argument(
            '--explicit-hash-key',
            metavar='<explicit_hash_key>',
            help=_("Hash value of the data to be written to the partition. "
                   "The hash value overwrites the hash value of "
                   "partition_key."),
        )
        parser.add_argument(
            '--partition-id',
            metavar='<partition_id>',
            help=_("Partition ID of the stream."),
        )
        parser.add_argument(
            '--partition-key',
            metavar='<partition_key>',
            help=_("Partition to which data is written to."
                   "\nNote:If the partition_id parameter is transferred, "
                   "it will be preferentially used. If partition_id is "
                   "not passed, partition_key will be used."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dis

        records = {}
        for arg in ('data', 'explicit_hash_key',
                    'partition_id', 'partition_key',):
            val = getattr(parsed_args, arg)
            if val:
                records[arg] = val

        attrs = {
            'stream_name': parsed_args.stream,
            'records': [records]
        }

        if parsed_args.stream_id:
            attrs.update(stream_id=parsed_args.stream_id)

        obj = client.upload_data(**attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)
