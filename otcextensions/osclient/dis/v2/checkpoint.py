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
from osc_lib.command import command

from otcextensions.i18n import _
from otcextensions.common import sdk_utils


LOG = logging.getLogger(__name__)


_formatters = {}


def _get_columns(item):
    column_map = {}
    hidden = [
        'location',
        'id',
    ]
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map,
                                                           hidden)


class ShowCheckpoint(command.ShowOne):
    _description = _("Querying Checkpoint Details.")

    def get_parser(self, prog_name):
        parser = super(ShowCheckpoint, self).get_parser(prog_name)
        parser.add_argument(
            '--stream-name',
            metavar='<stream_name>',
            required=True,
            help=_("Name of the stream to which the checkpoint belongs."),
        )
        parser.add_argument(
            '--app-name',
            metavar='<app_name>',
            required=True,
            help=_("Name of the app associated with the checkpoint."),
        )
        parser.add_argument(
            '--partition-id',
            metavar='<partition_id>',
            required=True,
            help=_("Identifier of the stream partition to which the "
                   "checkpoint belongs."),
        )
        parser.add_argument(
            '--checkpoint-type',
            metavar='<checkpoint_type>',
            default='LAST_READ',
            help=_("Type of the checkpoint."
                   "\nLAST_READ: Only sequence numbers are recorded in"
                   "databases."
                   "\nDefault: LAST_READ"),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dis

        params = {
            'stream_name': parsed_args.stream_name,
            'app_name': parsed_args.app_name,
            'partition_id': parsed_args.partition_id,
            'checkpoint_type': parsed_args.checkpoint_type
        }

        obj = client.get_checkpoint(**params)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)

        return (display_columns, data)


class CreateCheckpoint(command.ShowOne):
    _description = _("Add Checkpoint.")

    def get_parser(self, prog_name):
        parser = super(CreateCheckpoint, self).get_parser(prog_name)
        parser.add_argument(
            '--stream-name',
            metavar='<stream_name>',
            required=True,
            help=_("Name of the stream to which the checkpoint belongs."),
        )
        parser.add_argument(
            '--app-name',
            metavar='<app_name>',
            required=True,
            help=_("Name of the app associated with the checkpoint."),
        )
        parser.add_argument(
            '--partition-id',
            metavar='<partition_id>',
            required=True,
            help=_("Identifier of the stream partition to which the "
                   "checkpoint belongs."),
        )
        parser.add_argument(
            '--sequence-number',
            metavar='<sequence_number>',
            required=True,
            help=_("Sequence number to be submitted, which is used to "
                   "record the consumption checkpoint of the stream."),
        )
        parser.add_argument(
            '--metadata',
            metavar='<metadata>',
            help=_("Metadata information of the consumer application. "
                   "The metadata information can contain a maximum of "
                   "1,000 characters."),
        )
        parser.add_argument(
            '--checkpoint-type',
            metavar='<checkpoint_type>',
            default='LAST_READ',
            help=_("Type of the checkpoint."
                   "\nLAST_READ: Only sequence numbers are recorded in"
                   "databases."
                   "\nDefault: LAST_READ"),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dis

        attrs = {
            'stream_name': parsed_args.stream_name,
            'app_name': parsed_args.app_name,
            'partition_id': parsed_args.partition_id,
            'sequence_number': parsed_args.sequence_number,
            'checkpoint_type': parsed_args.checkpoint_type
        }
        if parsed_args.metadata:
            attrs.update(metadata=parsed_args.metadata)

        obj = client.add_checkpoint(**attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class DeleteCheckpoint(command.Command):
    _description = _("Delete Checkpoint.")

    def get_parser(self, prog_name):
        parser = super(DeleteCheckpoint, self).get_parser(prog_name)
        parser.add_argument(
            '--stream-name',
            metavar='<stream_name>',
            required=True,
            help=_("Name of the stream to which the checkpoint belongs."),
        )
        parser.add_argument(
            '--app-name',
            metavar='<app_name>',
            required=True,
            help=_("Name of the app associated with the checkpoint."),
        )
        parser.add_argument(
            '--partition-id',
            metavar='<partition_id>',
            help=_("Identifier of the stream partition to which the "
                   "checkpoint belongs."),
        )
        parser.add_argument(
            '--checkpoint-type',
            metavar='<checkpoint_type>',
            default='LAST_READ',
            help=_("Type of the checkpoint."
                   "\nLAST_READ: Only sequence numbers are recorded in"
                   "databases."
                   "\nDefault: LAST_READ"),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dis

        params = {
            'stream_name': parsed_args.stream_name,
            'app_name': parsed_args.app_name,
            'checkpoint_type': parsed_args.checkpoint_type
        }
        if parsed_args.partition_id:
            params.update(partition_id=parsed_args.partition_id)

        client.delete_checkpoint(**params)
