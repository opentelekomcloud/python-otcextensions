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

"""Identity custom role v3.0 action implementations"""
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _get_columns(item):
    column_map = {
    }
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


class ListCustomRoles(command.Lister):
    _description = _('List Identity Custom Roles')
    columns = (
        'id',
        'name',
        'description',
        'domain_id',
        'references',
        'catalog',
        'display_name',
        'type',
        'created_at',
        'updated_at',
    )

    def get_parser(self, prog_name):
        parser = super(ListCustomRoles, self).get_parser(prog_name)

        parser.add_argument(
            '--page',
            metavar='<page>',
            help=_('Page number for pagination query.')
        )
        parser.add_argument(
            '--per_page',
            metavar='<per_page>',
            help=_('Number of data records to be displayed on each page.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.iam

        table_columns = (
            'ID',
            'Name',
            'Description',
            'Domain ID',
            'References',
            'Catalog',
            'Display name',
            'Type',
            'Created At',
            'Updated At',
        )

        attrs = {}

        if parsed_args.page:
            attrs['page'] = parsed_args.user_id
        if parsed_args.page:
            attrs['per_page'] = parsed_args.per_page
        data = client.custom_roles(**attrs)

        table = (table_columns,
                 (utils.get_dict_properties(
                     s, self.columns
                 ) for s in data))
        return table
