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
from osc_lib.command import command

from otcextensions.i18n import _
from otcextensions.common import sdk_utils

LOG = logging.getLogger(__name__)


def _get_columns(item):
    column_map = {
    }
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


class SendSms(command.ShowOne):
    _description = _("Send a transactional SMS message to a specified "
                     "phone number, usually used for verification code "
                     "or notification.")

    def get_parser(self, prog_name):
        parser = super(SendSms, self).get_parser(prog_name)
        parser.add_argument(
            'endpoint',
            metavar='<endpoint>',
            help=_("Phone number."),
        )
        parser.add_argument(
            'message',
            metavar='<message>',
            help=_("SMS message content."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.smn

        args_list = [
            'endpoint',
            'message']
        attrs = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        obj = client.send_sms(**attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)
