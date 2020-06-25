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
"""SMN template v2 action implementations"""
import logging

from osc_lib import utils
from osc_lib import exceptions
from osc_lib.command import command

from otcextensions.i18n import _
from otcextensions.common import sdk_utils

LOG = logging.getLogger(__name__)


def _get_columns(item):
    column_map = {
    }
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


PROTOCOL_CHOICES = ['email', 'default', 'sms', 'dms', 'http', 'https']


class ListTemplate(command.Lister):

    _description = _("List message templates.")
    columns = ('Message Template Id', 'Message Template Name', 'Protocol')

    def get_parser(self, prog_name):
        parser = super(ListTemplate, self).get_parser(prog_name)

        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_("Message template name."),
        )
        parser.add_argument(
            '--protocol',
            metavar='{' + ','.join(PROTOCOL_CHOICES) + '}',
            type=lambda s: s.lower(),
            choices=PROTOCOL_CHOICES,
            help=_("Protocol supported by the template."),
        )
        parser.add_argument(
            '--offset',
            metavar='<offset>',
            type=int,
            help=_("Resources after this offset will be queried."),
        )
        parser.add_argument(
            '--limit',
            metavar='<limit>',
            type=int,
            help=_("Limit to fetch number of records."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.smn
        args_list = [
            'limit',
            'offset',
            'protocol',
            'name']
        attrs = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        data = client.templates(**attrs)

        return (self.columns, (utils.get_item_properties(s, self.columns)
                               for s in data))


class ShowTemplate(command.ShowOne):
    _description = _("Show message template details.")

    def get_parser(self, prog_name):
        parser = super(ShowTemplate, self).get_parser(prog_name)
        parser.add_argument(
            'template',
            metavar='<template>',
            help=_("Specifies the Name or ID of the message template."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.smn
        obj = client.find_template(parsed_args.template)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class CreateTemplate(command.ShowOne):
    _description = _("Create new message template.")

    def get_parser(self, prog_name):
        parser = super(CreateTemplate, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help=_("Specifies the name of the message template."),
        )
        parser.add_argument(
            '--content',
            metavar='<content>',
            required=True,
            help=_("Template content, which currently supports "
                   "plain text only."),
        )
        parser.add_argument(
            '--protocol',
            metavar='{' + ','.join(PROTOCOL_CHOICES) + '}',
            type=lambda s: s.lower(),
            choices=PROTOCOL_CHOICES,
            help=_("Protocol supported by the template."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.smn

        args_list = [
            'name',
            'protocol',
            'content']
        attrs = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        obj = client.create_template(**attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class UpdateTemplate(command.ShowOne):
    _description = _("Update a message template.")

    def get_parser(self, prog_name):
        parser = super(UpdateTemplate, self).get_parser(prog_name)
        parser.add_argument(
            'template',
            metavar='<template>',
            help=_("Specifies the Name or ID of the message template."),
        )
        parser.add_argument(
            '--content',
            metavar='<content>',
            required=True,
            help=_("Template content, which currently supports "
                   "plain text only."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.smn
        attrs = {
            'content': parsed_args.content
        }
        template = client.find_template(parsed_args.template)

        obj = client.update_template(template, **attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class DeleteTemplate(command.Command):

    _description = _("Deletes message template.")

    def get_parser(self, prog_name):
        parser = super(DeleteTemplate, self).get_parser(prog_name)
        parser.add_argument(
            'template',
            metavar='<template>',
            nargs='+',
            help=_("message template(s) to delete (Name or ID)"),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.smn
        result = 0
        for template in parsed_args.template:
            try:
                obj = client.find_template(template)
                client.delete_template(obj)
            except Exception as e:
                result += 1
                LOG.error(_("Failed to delete message template with "
                          "name or ID '%(template)s': %(e)s"),
                          {'template': template, 'e': e})
        if result > 0:
            total = len(parsed_args.template)
            msg = (_("%(result)s of %(total)s message template(s) failed "
                   "to delete.") % {'result': result, 'total': total})
            raise exceptions.CommandError(msg)
