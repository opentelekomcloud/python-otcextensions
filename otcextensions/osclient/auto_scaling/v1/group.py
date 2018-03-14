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
"""AS Groups v1 action implementations"""

import logging

# import six

from osc_lib.command import command
# from osc_lib.cli import parseractions
# from osc_lib import exceptions
from osc_lib import utils

from otcextensions.i18n import _

from otcextensions.osclient.auto_scaling import sdk_utils

LOG = logging.getLogger(__name__)


def _get_columns(item):
    column_map = {
        'net:b': 'vpc_id'
    }
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


class ListAutoScalingGroup(command.Lister):
    _description = _("List AutoScaling  Groups")
    columns = ('ID', 'Name', 'Status', 'Detail')

    def get_parser(self, prog_name):
        parser = super(ListAutoScalingGroup, self).get_parser(prog_name)
        parser.add_argument(
            '--limit',
            dest='limit',
            metavar='<limit>',
            type=int,
            default=None,
            help=_('Limit the number of results displayed. (Not supported)')
        )
        parser.add_argument(
            '--marker',
            dest='marker',
            metavar='<ID>',
            help=_('Begin displaying the results for IDs greater than the '
                   'specified marker. When used with --limit, set this to '
                   'the last ID displayed in the previous run. '
                   '(Not supported)')
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.auto_scaling

        data = client.groups()

        return (
            self.columns,
            (utils.get_item_properties(
                s,
                self.columns,
            ) for s in data)
        )


class ShowAutoScalingGroup(command.ShowOne):
    _description = _("Shows details of a AutoScalinig group")
    columns = ['ID', 'Name', 'Status', 'Detail',
               'Scaling Configuration ID', 'Scaling Configuration Name',
               'current_instance_number', 'desire_instance_number',
               'min_instance_number', 'max_instance_number',
               'cool_down_time', 'networks', 'available_zones',
               'security_group']

    def get_parser(self, prog_name):
        parser = super(ShowAutoScalingGroup, self).get_parser(prog_name)
        parser.add_argument(
            'group',
            metavar="<group>",
            help=_("ID or name of the configuration group")
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.auto_scaling

        obj = client.find_group(parsed_args.group, ignore_missing=False)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters={})

        return (display_columns, data)


class CreateAutoScalingGroup(command.ShowOne):
    _description = _("Creates AutoScalinig group")
    columns = ['ID', 'Name', 'Status', 'Detail',
               'Datastore Version Name', 'Is Scaling']

    def get_parser(self, prog_name):
        parser = super(CreateAutoScalingGroup, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        raise NotImplementedError


class DeleteAutoScalingGroup(command.ShowOne):
    _description = _("Deletes AutoScalinig group")
    columns = ['ID', 'Name', 'Status', 'Detail',
               'Datastore Version Name', 'Is Scaling']

    def get_parser(self, prog_name):
        parser = super(DeleteAutoScalingGroup, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        raise NotImplementedError


class UpdateAutoScalingGroup(command.ShowOne):
    _description = _("Updates AutoScalinig group")
    columns = ['ID', 'Name', 'Status', 'Detail',
               'Datastore Version Name', 'Is Scaling']

    def get_parser(self, prog_name):
        parser = super(UpdateAutoScalingGroup, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        raise NotImplementedError


class DisableAutoScalingGroup(command.ShowOne):
    _description = _("Disable/pause AutoScalinig group")
    columns = ['ID', 'Name', 'Status', 'Detail',
               'Datastore Version Name', 'Is Scaling']

    def get_parser(self, prog_name):
        parser = super(DisableAutoScalingGroup, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        raise NotImplementedError


class EnableAutoScalingGroup(command.ShowOne):
    _description = _("Enable/resume AutoScalinig group")
    columns = ['ID', 'Name', 'Status', 'Detail',
               'Datastore Version Name', 'Is Scaling']

    def get_parser(self, prog_name):
        parser = super(EnableAutoScalingGroup, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        raise NotImplementedError
