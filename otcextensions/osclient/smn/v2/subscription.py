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
"""subscription v2 action implementations"""

import logging

from osc_lib import utils
from osc_lib import exceptions
from osc_lib.command import command

from otcextensions.i18n import _
from otcextensions.common import sdk_utils

LOG = logging.getLogger(__name__)


def _get_columns(item):
    column_map = {}
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


class ListSubscription(command.Lister):

    _description = _("List SMN Subscriptions.")
    columns = (
        'ID',
        'Protocol',
        'Topic URN',
        'Owner',
        'Endpoint',
        'Status'
    )

    def get_parser(self, prog_name):
        parser = super(ListSubscription, self).get_parser(prog_name)

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
            help=_("Limit to fetch number of records.\n"
                   "Value range: 1–100"),
        )
        parser.add_argument(
            '--topic',
            metavar='<topic>',
            help=_("Specify the topic ID or Name."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.smn
        args_list = [
            'offset',
            'limit']
        attrs = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val
        topic = getattr(parsed_args, 'topic') or None
        if topic:
            topic = client.get_topic(topic)

        data = client.subscriptions(topic, **attrs)

        return (self.columns, (utils.get_item_properties(s, self.columns)
                               for s in data))


class CreateSubscription(command.ShowOne):
    _description = _("Add a new Subscription to a SMN topic.")

    def get_parser(self, prog_name):
        parser = super(CreateSubscription, self).get_parser(prog_name)
        parser.add_argument(
            'topic',
            metavar='<topic>',
            help=_("Unique resource ID or name of a topic."),
        )
        parser.add_argument(
            '--endpoint',
            metavar='<endpoint>',
            required=True,
            help=_("Message endpoint."),
        )
        parser.add_argument(
            '--protocol',
            metavar='<protocol>',
            required=True,
            help=_("Subscription protocol.\n"
                   "Currently, the following protocols are supported:\n"
                   "email: The endpoints are email address.\n"
                   "sms: The endpoints are phone numbers.\n"
                   "http and https: The endpoints are URLs."),
        )
        parser.add_argument(
            '--remark',
            metavar='<remark>',
            help=_("Description of the subscription."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.smn

        args_list = [
            'protocol',
            'endpoint',
            'remark']
        attrs = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        topic = client.get_topic(parsed_args.topic)
        obj = client.create_subscription(topic, **attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class DeleteSubscription(command.Command):

    _description = _("Deletes SMN subscription.")

    def get_parser(self, prog_name):
        parser = super(DeleteSubscription, self).get_parser(prog_name)
        parser.add_argument(
            'subscription',
            metavar='<subscription>',
            nargs='+',
            help=_("SMN Subscrition(s) to delete."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.smn
        result = 0
        for subscription in parsed_args.subscription:
            try:
                client.delete_subscription(subscription, ignore_missing=False)
            except Exception as e:
                result += 1
                LOG.error(_("Failed to delete SMN Subscription with "
                          "ID '%(subscription)s': %(e)s"),
                          {'subscription': subscription, 'e': e})
        if result > 0:
            total = len(parsed_args.subscription)
            msg = (_("%(result)s of %(total)s SMN Subscription(s) failed "
                   "to delete.") % {'result': result, 'total': total})
            raise exceptions.CommandError(msg)
