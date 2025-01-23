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
'''CSS ELK cluster v1 action implementations'''
import logging

from osc_lib.command import command
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


class DownloadCertificate(command.Command):
    _description = _('Download the HTTPS certificate file of the server.')

    def get_parser(self, prog_name):
        parser = super(DownloadCertificate, self).get_parser(prog_name)
        parser.add_argument(
            '--out',
            metavar='<out>',
            help=_(
                'Name of the output file where certificate will be saved. '
                '(Optional)'
            ),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.css
        filename = None
        if parsed_args.out:
            filename = parsed_args.out
        client.download_certificate(filename)
