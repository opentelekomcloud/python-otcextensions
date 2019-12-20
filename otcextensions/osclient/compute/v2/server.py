#   Copyright 2012-2013 OpenStack Foundation
#
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

"""Compute v2 Server action implementations"""

import getpass
import logging

from novaclient import api_versions
from osc_lib.cli import parseractions
from osc_lib.command import command
from osc_lib import exceptions
from osc_lib import utils

from openstackclient.i18n import _

from otcextensions import sdk


LOG = logging.getLogger(__name__)


class SetServer(command.Command):
    _description = _("Set server properties")

    def get_parser(self, prog_name):
        parser = super(SetServer, self).get_parser(prog_name)
        parser.add_argument(
            'server',
            metavar='<server>',
            help=_('Server (name or ID)'),
        )
        parser.add_argument(
            '--name',
            metavar='<new-name>',
            help=_('New server name'),
        )
        parser.add_argument(
            '--root-password',
            action="store_true",
            help=_('Set new root password (interactive only)'),
        )
        parser.add_argument(
            "--property",
            metavar="<key=value>",
            action=parseractions.KeyValueAction,
            help=_('Property to add/change for this server '
                   '(repeat option to set multiple properties)'),
        )
        parser.add_argument(
            '--state',
            metavar='<state>',
            choices=['active', 'error'],
            help=_('New server state (valid value: active, error)'),
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_('New server description (supported by '
                   '--os-compute-api-version 2.19 or above)'),
        )
        parser.add_argument(
            '--tag',
            metavar='<tag>',
            action='append',
            help=_('New Tag (supported by --os-compute-api-version 2.26 and '
                   'above')
        )
        return parser

    def take_action(self, parsed_args):

        compute_client = self.app.client_manager.compute
        server = utils.find_resource(
            compute_client.servers,
            parsed_args.server,
        )

        if parsed_args.name:
            server.update(name=parsed_args.name)

        if parsed_args.property:
            compute_client.servers.set_meta(
                server,
                parsed_args.property,
            )

        if parsed_args.state:
            server.reset_state(state=parsed_args.state)

        if parsed_args.root_password:
            p1 = getpass.getpass(_('New password: '))
            p2 = getpass.getpass(_('Retype new password: '))
            if p1 == p2:
                server.change_password(p1)
            else:
                msg = _("Passwords do not match, password unchanged")
                raise exceptions.CommandError(msg)

        if parsed_args.description:
            if server.api_version < api_versions.APIVersion("2.19"):
                msg = _("Description is not supported for "
                        "--os-compute-api-version less than 2.19")
                raise exceptions.CommandError(msg)
            server.update(description=parsed_args.description)

        if parsed_args.tag:
            if server.api_version < api_versions.APIVersion("2.26"):
                msg = _("Modifying tags is not supported for "
                        "--os-compute-api-version less than 2.26")
                raise exceptions.CommandError(msg)
            sdk.load(self.app.client_manager.sdk_connection)
            client = self.app.client_manager.sdk_connection.compute
            server = client.get_server(server.id)
            for tag in parsed_args.tag:
                server.add_tag(client, tag)


class UnsetServer(command.Command):
    _description = _("Unset server properties")

    def get_parser(self, prog_name):
        parser = super(UnsetServer, self).get_parser(prog_name)
        parser.add_argument(
            'server',
            metavar='<server>',
            help=_('Server (name or ID)'),
        )
        parser.add_argument(
            '--property',
            metavar='<key>',
            action='append',
            default=[],
            help=_('Property key to remove from server '
                   '(repeat option to remove multiple values)'),
        )
        parser.add_argument(
            '--description',
            dest='description',
            action='store_true',
            help=_('Unset server description (supported by '
                   '--os-compute-api-version 2.19 or above)'),
        )
        parser.add_argument(
            '--tag',
            metavar='<tag>',
            action='append',
            help=_('Unset tag (supported by --os-compute-api-version 2.26 and '
                   'above')
        )
        return parser

    def take_action(self, parsed_args):
        compute_client = self.app.client_manager.compute
        server = utils.find_resource(
            compute_client.servers,
            parsed_args.server,
        )

        if parsed_args.property:
            compute_client.servers.delete_meta(
                server,
                parsed_args.property,
            )

        if parsed_args.description:
            if compute_client.api_version < api_versions.APIVersion("2.19"):
                msg = _("Description is not supported for "
                        "--os-compute-api-version less than 2.19")
                raise exceptions.CommandError(msg)
            compute_client.servers.update(
                server,
                description="",
            )

        if parsed_args.tag:
            if compute_client.api_version < api_versions.APIVersion("2.26"):
                msg = _("Modifying tags is not supported for "
                        "--os-compute-api-version less than 2.26")
                raise exceptions.CommandError(msg)
            sdk.load(self.app.client_manager.sdk_connection)
            client = self.app.client_manager.sdk_connection.compute
            server = client.get_server(server.id)
            for tag in parsed_args.tag:
                server.remove_tag(client, tag)
