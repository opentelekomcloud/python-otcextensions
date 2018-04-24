#   Licensed under the Apache License, Version 2.0 (the 'License'); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an 'AS IS' BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#
'''CMK v1 action implementations'''
import logging

from osc_lib import exceptions
from osc_lib import utils
from osc_lib.command import command

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def timestamp_to_str(obj):
    """Convert KMS timestamp to Humanreadable format
    """
    # TODO(anybody) Convert to string when clear how
    return obj


class ListCMK(command.Lister):
    _description = _('List Customer Master Keys (CMK)')
    columns = ('ID', 'key_alias', 'key_state')

    def get_parser(self, prog_name):
        parser = super(ListCMK, self).get_parser(prog_name)
        parser.add_argument(
            '--limit',
            metavar='<limit>',
            type=int,
            default=None,
            help=_('Limit the number of results fetch at a time')
        )
        parser.add_argument(
            '--state',
            metavar='<state>',
            type=int,
            choices=range(0, 5),
            help=_('CMK state:\n'
                   '`1` - waiting for activation\n'
                   '`2` - enabled\n'
                   '`3` - disabled\n'
                   '`4` - scheduled for deletion')
        )

        return parser

    def take_action(self, parsed_args):

        args = {}
        if parsed_args.limit:
            args['limit'] = parsed_args.limit
        if parsed_args.state:
            args['key_state'] = parsed_args.state

        client = self.app.client_manager.kms

        data = client.keys(**args)

        return (
            self.columns,
            (utils.get_item_properties(
                s,
                self.columns,
            ) for s in data)
        )


class ShowCMK(command.ShowOne):
    _description = _('Shows details of a CMK')
    columns = ['ID', 'key_alias', 'domain_id', 'realm',
               'key_description', 'creation_date', 'scheduled_deletion_date',
               'key_state', 'key_type']

    def get_parser(self, prog_name):
        parser = super(ShowCMK, self).get_parser(prog_name)
        parser.add_argument(
            'key',
            metavar='<key>',
            help=_('ID or the alias of the CMK')
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.kms

        obj = None

        if parsed_args.key:
            obj = client.find_key(parsed_args.key)

        data = utils.get_item_properties(
            obj, self.columns, formatters={})

        return (self.columns, data)


class EnableCMK(command.Command):
    _description = _('Enables the CMK')

    def get_parser(self, prog_name):
        parser = super(EnableCMK, self).get_parser(prog_name)
        parser.add_argument(
            'key',
            metavar='<key>',
            help=_('ID or the alias of the CMK')
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.kms

        obj = None

        if parsed_args.key:
            obj = client.find_key(parsed_args.key)

        if obj:
            client.enable_key(obj)

        return None


class DisableCMK(command.Command):
    _description = _('Disables the CMK')

    def get_parser(self, prog_name):
        parser = super(DisableCMK, self).get_parser(prog_name)
        parser.add_argument(
            'key',
            metavar='<key>',
            help=_('ID or the alias of the CMK')
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.kms

        obj = None

        if parsed_args.key:
            obj = client.find_key(parsed_args.key)

        if obj:
            client.disable_key(obj)

        return None


class DeleteCMK(command.Command):
    _description = _('Schedules deletion of the CMK')

    def get_parser(self, prog_name):
        parser = super(DeleteCMK, self).get_parser(prog_name)
        parser.add_argument(
            'key',
            metavar='<key>',
            help=_('ID or the alias of the CMK')
        )
        parser.add_argument(
            'days',
            metavar='<days>',
            type=int,
            help=_('Number of days in future after which CMK '
                   'will be deleted [7..1096]')
        )

        return parser

    def take_action(self, parsed_args):

        obj = None
        days = 7

        if parsed_args.days:
            days = parsed_args.days
            if not 7 <= days <= 1096:
                msg = _('Invalid number of days. '
                        'Please choose in range (7..1096)')
                raise exceptions.CommandError(msg)

        client = self.app.client_manager.kms

        if parsed_args.key:
            obj = client.find_key(parsed_args.key)

        if obj:
            client.schedule_key_deletion(key=obj, pending_days=days)

        return None


class CancelDeleteCMK(command.Command):
    _description = _('Cancels the scheduled deletion of the CMK')

    def get_parser(self, prog_name):
        parser = super(CancelDeleteCMK, self).get_parser(prog_name)
        parser.add_argument(
            'key',
            metavar='<key>',
            help=_('ID or the alias of the CMK')
        )

        return parser

    def take_action(self, parsed_args):

        obj = None

        client = self.app.client_manager.kms

        if parsed_args.key:
            obj = client.find_key(parsed_args.key)

        if obj:
            client.cancel_key_deletion(key=obj)


class CreateCMK(command.ShowOne):
    _description = _('Creates CMK')
    columns = ['ID', 'key_alias', 'domain_id', 'realm',
               'key_description', 'creation_date', 'scheduled_deletion_date',
               'key_state', 'key_type']
#
    POLICY_TYPES = ['ALARM', 'SCHEDULED', 'RECURRENCE']

    def get_parser(self, prog_name):
        parser = super(CreateCMK, self).get_parser(prog_name)
        parser.add_argument(
            'alias',
            metavar='<alias>',
            help=_('CMK Alias')
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_('CMK description')
        )
        parser.add_argument(
            '--realm',
            metavar='<realm>',
            help=_('Realm value')
        )
        parser.add_argument(
            '--key_policy',
            metavar='<key_policy>',
            help=_('Specifies the key policy')
        )
        parser.add_argument(
            '--key_usage',
            metavar='<key_usage>',
            help=_('Purpose of the CMK')
        )
        parser.add_argument(
            '--type',
            metavar='<type>',
            help=_('Type of the CMK')
        )
        return parser

    def take_action(self, parsed_args):

        attrs = {}
        attrs['key_alias'] = parsed_args.alias
        if parsed_args.description:
            attrs['key_description'] = parsed_args.description
        if parsed_args.realm:
            attrs['realm'] = parsed_args.realm
        if parsed_args.key_policy:
            attrs['key_policy'] = parsed_args.key_policy
        if parsed_args.key_usage:
            attrs['key_usage'] = parsed_args.key_usage
        if parsed_args.type:
            attrs['key_type'] = parsed_args.type

        client = self.app.client_manager.kms

        cmk = client.create_key(**attrs)

        data = utils.get_item_properties(
            cmk, self.columns, formatters={})

        return (self.columns, data)
