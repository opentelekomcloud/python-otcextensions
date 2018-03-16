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
"""AS Configurations v1 action implementations"""

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


def _format_instance(inst):
    return inst.to_dict()


class ListAutoScalingConfiguration(command.Lister):
    _description = _("List AutoScaling Configurations")
    columns = ('ID', 'Name', 'Status', 'Detail')

    def get_parser(self, prog_name):
        parser = super(ListAutoScalingConfiguration, self).get_parser(prog_name)
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

        data = client.configs()

        return (
            self.columns,
            (utils.get_item_properties(
                s,
                self.columns,
            ) for s in data)
        )


class ShowAutoScalingConfiguration(command.ShowOne):
    _description = _("Shows details of a AutoScalinig group")
    columns = ['ID', 'Name', 'Status', 'Detail',
               'Scaling Configuration ID', 'Scaling Configuration Name',
               'current_instance_number', 'desire_instance_number',
               'min_instance_number', 'max_instance_number',
               'cool_down_time', 'networks', 'available_zones',
               'security_group',
               'scaling_configuration_id', 'scaling_configuration_name',
               'create_time'
               ]

    def get_parser(self, prog_name):
        parser = super(ShowAutoScalingConfiguration, self).get_parser(prog_name)
        parser.add_argument(
            'config',
            metavar="<config>",
            help=_("ID or name of the configuration group")
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.auto_scaling

        obj = client.find_config(parsed_args.config, ignore_missing=False)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(
            obj, columns, formatters={'instance_config': _format_instance})

        return (display_columns, data)


class CreateAutoScalingConfiguration(command.ShowOne):
    _description = _("Creates AutoScalinig group")
    columns = ['ID', 'Name', 'Status', 'Detail',
               'Datastore Version Name', 'Is Scaling']

    def get_parser(self, prog_name):
        parser = super(CreateAutoScalingConfiguration, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        raise NotImplementedError


class DeleteAutoScalingConfiguration(command.ShowOne):
    _description = _("Deletes AutoScalinig group")
    columns = ['ID', 'Name', 'Status', 'Detail',
               'Datastore Version Name', 'Is Scaling']

    def get_parser(self, prog_name):
        parser = super(DeleteAutoScalingConfiguration, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        raise NotImplementedError


class UpdateAutoScalingConfiguration(command.ShowOne):
    _description = _("Updates AutoScalinig group")
    columns = ['ID', 'Name', 'Status', 'Detail',
               'Datastore Version Name', 'Is Scaling']

    def get_parser(self, prog_name):
        parser = super(UpdateAutoScalingConfiguration, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        raise NotImplementedError


class DisableAutoScalingConfiguration(command.ShowOne):
    _description = _("Disable/pause AutoScalinig group")
    columns = ['ID', 'Name', 'Status', 'Detail',
               'Datastore Version Name', 'Is Scaling']

    def get_parser(self, prog_name):
        parser = super(DisableAutoScalingConfiguration, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        raise NotImplementedError


class EnableAutoScalingConfiguration(command.ShowOne):
    _description = _("Enable/resume AutoScalinig group")
    columns = ['ID', 'Name', 'Status', 'Detail',
               'Datastore Version Name', 'Is Scaling']

    def get_parser(self, prog_name):
        parser = super(EnableAutoScalingConfiguration, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        raise NotImplementedError
