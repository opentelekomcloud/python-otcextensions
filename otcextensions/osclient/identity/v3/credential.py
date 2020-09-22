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
'''Identity credential v3 action implementations'''
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


class ListCredentials(command.Lister):
    _description = _('List Identity Credentials')
    columns = (
        'access',
        'description',
        'user_id',
        'status',
        'created_at',
    )

    def get_parser(self, prog_name):
        parser = super(ListCredentials, self).get_parser(prog_name)

        parser.add_argument(
            '--user-id',
            metavar='<user-id>',
            help=_('User ID of the user using the credential')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.identity

        table_columns = (
            'Access Key',
            'Description',
            'User ID',
            'Status',
            'Created At',
        )

        attrs = {}

        if parsed_args.user_id:
            attrs['user_id'] = parsed_args.user_id

        data = client.credentials(**attrs)

        table = (table_columns,
                 (utils.get_dict_properties(
                     s, self.columns
                 ) for s in data))
        return table


class ShowCredential(command.ShowOne):
    _description = _('Show identity credential details')

    def get_parser(self, prog_name):
        parser = super(ShowCredential, self).get_parser(prog_name)

        parser.add_argument(
            'credential',
            metavar='<credential>',
            help=_('Access key of the credential.')
        )
        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.identity

        obj = client.find_credential(
            parsed_args.credential
        )

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class DeleteCredential(command.Command):
    _description = _('Delete identity credential')

    def get_parser(self, prog_name):
        parser = super(DeleteCredential, self).get_parser(prog_name)

        parser.add_argument(
            'credential',
            metavar='<credential>',
            nargs='+',
            help=_('Access key of the credential.')
        )

        return parser

    def take_action(self, parsed_args):
        if parsed_args.credential:
            client = self.app.client_manager.identity
            for credential in parsed_args.credential:
                credential = client.find_credential(
                    credential,
                    ignore_missing=False)
                client.delete_credential(credential.id)


class UpdateCredential(command.ShowOne):
    _description = _("Update identity credential.")

    def get_parser(self, prog_name):
        parser = super(UpdateCredential, self).get_parser(prog_name)
        parser.add_argument(
            'credential',
            metavar='<credential>',
            help=_("Specifies the access key / ID of the credential."),
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_("Provides supplementary information about the credential."),
        )
        parser.add_argument(
            '--status',
            metavar='<status>',
            help=_('Switch status of the credential.\n'
                   'active: Credential is active\n'
                   'inactive: Credential is inactive\n'),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.identity
        args_list = [
            'description', 'status'
        ]
        attrs = {}
        for arg in args_list:
            if getattr(parsed_args, arg):
                attrs[arg] = getattr(parsed_args, arg)
        credential = client.find_credential(parsed_args.credential)

        obj = client.update_credential(credential.id, **attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class CreateCredential(command.ShowOne):
    _description = _('Create a identity credential')

    def get_parser(self, prog_name):
        parser = super(CreateCredential, self).get_parser(prog_name)

        parser.add_argument(
            'user_id',
            metavar='<user-id>',
            help=_('User ID of the user who will use the credential')
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_('Description of the alarm')
        )

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.identity

        attrs = {}

        attrs['user_id'] = parsed_args.user_id
        if parsed_args.description:
            attrs['description'] = parsed_args.description

        obj = client.create_credential(
            **attrs
        )

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)
