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
'''DCS Config params v1 action implementations'''
import logging
import argparse

from osc_lib import utils
from osc_lib.command import command

from otcextensions.common import sdk_utils

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _get_columns(item):
    column_map = {
    }
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


class ListInstanceParam(command.Lister):
    _description = _('List configurational parameters of a single DCS '
                     'instance')
    columns = ('id', 'name', 'value', 'default_value')

    def get_parser(self, prog_name):
        parser = super(ListInstanceParam, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help=_('Name or ID of the instance')
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dcs

        inst = client.find_instance(name_or_id=parsed_args.instance,
                                    ignore_missing=False)
        data = client.instance_params(
            instance={'id': inst.id},
        )

        table = (self.columns,
                 (utils.get_item_properties(
                     s, self.columns,
                 ) for s in data))
        return table


class UpdateInstanceParam(command.Command):
    _description = _('Update instance configurational parameters')

    def get_parser(self, prog_name):
        parser = super(UpdateInstanceParam, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help=_('Name or ID of the DCS instance to take backup from.')
        )
        parser.add_argument(
            '--param',
            metavar='<id:name:value>',
            required=True,
            action='append',
            help=_('Parameter pair in format ID:NAME:VALUE.')
        )
        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.dcs

        params = []

        for param in parsed_args.param:
            param_parts = param.split(':')
            if 3 == len(param_parts):
                param_struct = {
                    'param_id': param_parts[0],
                    'param_name': param_parts[1],
                    'param_value': param_parts[2]
                }
                params.append(param_struct)
            else:
                msg = _('Cannot parse tag information')
                raise argparse.ArgumentTypeError(msg)

        if params:
            inst = client.find_instance(name_or_id=parsed_args.instance,
                                        ignore_missing=False)

            return client.update_instance_params(
                instance={'id': inst.id}, params=params
            )


class ShowInstanceParam(command.ShowOne):
    _description = _('Show the details of a single instance parameter')

    def get_parser(self, prog_name):
        parser = super(ShowInstanceParam, self).get_parser(prog_name)

        parser.add_argument(
            'instance',
            metavar='<instance>',
            help=_('Name or UUID of the instance.')
        )
        parser.add_argument(
            '--param',
            metavar='<param>',
            required=True,
            help=_('ID or name of the parameter.')
        )

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.dcs

        inst = client.find_instance(name_or_id=parsed_args.instance,
                                    ignore_missing=False)
        data = client.instance_params(
            instance={'id': inst.id},
        )

        criteria = parsed_args.param

        found = None

        for param in data:
            if param.id == criteria or criteria in param.name:
                found = param
                break

        if found:
            display_columns, columns = _get_columns(found)
            data = utils.get_item_properties(found, columns)

            return (display_columns, data)
