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
'''AS Quota v1 action implementations'''
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


class ListAutoScalingQuota(command.Lister):
    _description = _('List AutoScaling Instances')
    columns = ('type', 'used', 'quota', 'max')

    def get_parser(self, prog_name):
        parser = super(ListAutoScalingQuota, self).get_parser(prog_name)
        parser.add_argument(
            '--group',
            metavar='<group>',
            help=_('AS Group ID or Name for the Quota query')
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.auto_scaling

        data = client.quotas(group=parsed_args.group)

        return (
            self.columns,
            (utils.get_item_properties(
                s,
                self.columns,
            ) for s in data)
        )
