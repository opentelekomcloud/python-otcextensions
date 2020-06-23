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
"""Message Publishing v2 action implementations"""

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


class PublishMessage(command.ShowOne):
    _description = _("Publish message. Three message formats are supported:\n"
                     " - message\n"
                     " - message_structure\n"
                     " - message_template_name\n"
                     "If the three formats are specified at the same time, they "
                     "take effect in the following sequence: "
                     "message_structure > message_template_name > message.")

    def get_parser(self, prog_name):
        parser = super(CreateSubscription, self).get_parser(prog_name)
        parser.add_argument(
            'topic',
            metavar='<topic>',
            help=_("Unique resource ID or name of a topic."),
        )
        parser.add_argument(
            '--subject',
            metavar='<subject>',
            required=True,
            help=_("Message subject, which is used as the email "
                   "subject when you publish email messages.."),
        )
        parser.add_argument(
            '--time-to-live',
            metavar='<time_to_live>',
            help=_("Time-to-live (TTL) of a message, specifically "
                   "the maximum time period for retaining the message "
                   "in the system. The default TTL is 3600s (one hour)."),
        )
        parser.add_argument(
            '--message',
            metavar='<message>',
            help=_("Message content. The message content is a UTF-8-coded "
                   "character string of no more than 256 KB."),
        )
        parser.add_argument(
            '--message-structure',
            metavar='<message_structure>',
            help=_("Message structure, which contains JSON character "
                   "strings. Specify protocols in the structure, which "
                   "can be http, https, email, dms, and sms.\n"
                   "The default protocol is mandatory. If the system "
                   "fails to match any other protocols, the default "
                   "message is sent."),
        )
        parser.add_argument(
            '--message-template-name',
            metavar='<message_template_name>',
            help=_("Message template name, which can be obtained "
                   "according to Querying Message Templates."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.smn

        args_list = [
            'subject',
            'time_to_live',
            'message',
            'message_template_name']
        attrs = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        topic = client.find_topic(parsed_args.topic, ignore_missing=False)
        obj = client.publish_message(topic, **attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)
