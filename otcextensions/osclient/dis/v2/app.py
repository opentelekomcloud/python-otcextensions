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
from osc_lib import exceptions
from osc_lib.command import command

from otcextensions.i18n import _
from otcextensions.common import sdk_utils
from otcextensions.common import cli_utils


LOG = logging.getLogger(__name__)


_formatters = {
    'created_at': cli_utils.UnixTimestampFormatter,
}


def _get_columns(item):
    column_map = {}
    hidden = [
        'location',
        'app_id',
    ]
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map,
                                                           hidden)


class ListApps(command.Lister):
    _description = _("Query List of Apps.")

    columns = (
        'name',
        'id',
        'created_at',
    )

    display_columns = (
        'App Name',
        'Id',
        'Created At',
    )

    def get_parser(self, prog_name):
        parser = super(ListApps, self).get_parser(prog_name)
        parser.add_argument(
            '--limit',
            metavar='<limit>',
            type=int,
            help=_("Maximum number of apps to list in a single API call. "
                   "\nDefault: 10"),
        )
        parser.add_argument(
            '--start-app-name',
            metavar='<start_app_name>',
            help=_("Name of the app to start the list with. The returned "
                   "app list does not contain this app name."),
        )
        parser.add_argument(
            '--stream-name',
            metavar='<stream_name>',
            help=_("Name of the stream whose apps will be returned."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dis
        args_list = (
            'limit',
            'start_app_name',
            'stream_name',
        )
        attrs = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        data = client.apps(**attrs)

        return (
            self.display_columns,
            (
                utils.get_item_properties(
                    s, self.columns, formatters=_formatters
                ) for s in data
            )
        )


class ListAppConsumptions(command.Lister):
    _description = _("List App Consumptions.")

    columns = (
        'partition_id',
        'sequence_number',
        'checkpoint_type',
    )

    display_columns = (
        'Partition Id',
        'Sequence Number',
        'Checkpoint Type',
    )

    def get_parser(self, prog_name):
        parser = super(ListAppConsumptions, self).get_parser(prog_name)
        parser.add_argument(
            'streamName',
            metavar='<streaName>',
            help=_("Name of the stream to be queried."),
        )
        parser.add_argument(
            'appName',
            metavar='<appName>',
            help=_("Name of the app to be queried."),
        )
        parser.add_argument(
            '--limit',
            metavar='<limit>',
            type=int,
            help=_("Maximum number of apps to list in a single API call. "
                   "\nDefault: 10"),
        )
        parser.add_argument(
            '--start-partition-id',
            metavar='<start_partition_id>',
            help=_("Name of the partition to start the partition list "
                   "with. The returned partition list does not contain "
                   "this partition."),
        )
        parser.add_argument(
            '--checkpoint-type',
            metavar='<checkpoint_type>',
            default='LAST_READ',
            help=_("Type of the checkpoint.\nLAST_READ: Only "
                   "sequence numbers are recorded in databases."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dis
        args_list = (
            'limit',
            'start_partition_id',
            'checkpoint_type',
        )
        attrs = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        data = client.app_consumptions(parsed_args.streamName,
                                       parsed_args.appName,
                                       **attrs)

        return (
            self.display_columns,
            (
                utils.get_item_properties(
                    s, self.columns, formatters=_formatters
                ) for s in data
            )
        )


class ShowApp(command.ShowOne):
    _description = _("Querying App Details.")

    def get_parser(self, prog_name):
        parser = super(ShowApp, self).get_parser(prog_name)
        parser.add_argument(
            'appName',
            metavar='<appName>',
            help=_("Name of the app to be queried."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dis
        obj = client.get_app(parsed_args.appName)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)

        return (display_columns, data)


class CreateApp(command.ShowOne):
    _description = _("Create new Consumption App.")

    def get_parser(self, prog_name):
        parser = super(CreateApp, self).get_parser(prog_name)
        parser.add_argument(
            'appName',
            metavar='<appName>',
            help=_("Specifies the name of the App."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dis

        attrs = {
            'app_name': parsed_args.appName
        }

        obj = client.create_app(**attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class DeleteApp(command.Command):

    _description = _("Delete Consumption App(s).")

    def get_parser(self, prog_name):
        parser = super(DeleteApp, self).get_parser(prog_name)
        parser.add_argument(
            'appName',
            metavar='<appName>',
            nargs='+',
            help=_("Name of Dis App(s) to delete."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dis
        result = 0
        for app_name in parsed_args.appName:
            try:
                client.delete_app(app_name)
            except Exception as e:
                result += 1
                LOG.error(_("Failed to delete App with "
                          "name '%(app_name)s': %(e)s"),
                          {'app_name': app_name, 'e': e})
        if result > 0:
            total = len(parsed_args.appName)
            msg = (_("%(result)s of %(total)s DIS App(s) failed "
                   "to delete.") % {'result': result, 'total': total})
            raise exceptions.CommandError(msg)
