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
"""SMN Topic v2 action implementations"""
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


class ListTopic(command.Lister):

    _description = _("List SMN Topics.")
    columns = ('Topic Urn', 'Name', 'Display Name', 'Push Policy')

    def get_parser(self, prog_name):
        parser = super(ListTopic, self).get_parser(prog_name)

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
            'offset']
        attrs = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        data = client.topics(**attrs)

        return (self.columns, (utils.get_item_properties(s, self.columns)
                               for s in data))


class ShowTopic(command.ShowOne):
    _description = _("Show Smn Topic details.")

    def get_parser(self, prog_name):
        parser = super(ShowTopic, self).get_parser(prog_name)
        parser.add_argument(
            'topic',
            metavar='<topic>',
            help=_("Specifies the Name or ID of the SMN topic."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.smn
        obj = client.find_topic(parsed_args.topic)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class CreateTopic(command.ShowOne):
    _description = _("Create new SMN topic.")

    def get_parser(self, prog_name):
        parser = super(CreateTopic, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help=_("Specifies the name of the NAT Gateway."),
        )
        parser.add_argument(
            '--display-name',
            metavar='<display_name>',
            help=_("Topic display name, which is presented as the name "
                   "of the email sender in email messages."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.smn

        args_list = [
            'name',
            'display_name']
        attrs = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        obj = client.create_topic(**attrs)

        columns = ('request_id', 'topic_urn')
        data = utils.get_item_properties(obj, columns)

        return (columns, data)


class UpdateTopic(command.ShowOne):
    _description = _("Update a SMN Topic.")

    def get_parser(self, prog_name):
        parser = super(UpdateTopic, self).get_parser(prog_name)
        parser.add_argument(
            'topic',
            metavar='<topic>',
            help=_("Specifies the Name or ID of the SMN Topic."),
        )
        parser.add_argument(
            '--display-name',
            metavar='<display_name>',
            required=True,
            help=_("Topic display name, which is presented as the name of "
                   "the email sender in email messages."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.smn
        attrs = {
            'display_name': parsed_args.display_name
        }
        topic = client.find_topic(parsed_args.topic)

        obj = client.update_topic(topic, **attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class DeleteTopic(command.Command):

    _description = _("Deletes SMN Topic.")

    def get_parser(self, prog_name):
        parser = super(DeleteTopic, self).get_parser(prog_name)
        parser.add_argument(
            'topic',
            metavar='<topic>',
            nargs='+',
            help=_("Smn Topic(s) to delete (Name or ID)"),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.smn
        result = 0
        for topic in parsed_args.topic:
            try:
                obj = client.find_topic(topic)
                client.delete_topic(obj)
            except Exception as e:
                result += 1
                LOG.error(_("Failed to delete Smn Topic with "
                          "name or ID '%(topic)s': %(e)s"),
                          {'topic': topic, 'e': e})
        if result > 0:
            total = len(parsed_args.topic)
            msg = (_("%(result)s of %(total)s SMN Topic(s) failed "
                   "to delete.") % {'result': result, 'total': total})
            raise exceptions.CommandError(msg)
