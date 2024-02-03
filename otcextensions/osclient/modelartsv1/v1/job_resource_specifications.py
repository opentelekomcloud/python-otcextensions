
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
"""ModelArts Resource and Engine Specifications v1 action implementations"""
import logging

from osc_lib import exceptions
from osc_lib import utils
from osc_lib.cli import parseractions
from osc_lib.command import command
from otcextensions.common import cli_utils
from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)

def _get_columns(item):
    column_map = {}
    hidden = []
    return sdk_utils.get_osc_show_columns_for_sdk_resource(
        item, column_map, hidden
    )


class JobResourceSpecifications(command.Lister):
    _description = _('Query the resource specifications of a specified job')
    columns = ('specs', 'spec_id', 'job_type', 'engine_id', 'project_type')
    def get_parser(self, prog_name):
        parser = super(JobResourceSpecifications, self).get_parser(prog_name)
        parser.add_argument('--job_type', metavar='<job_type>', required=False, type=str, help=_('Job type'))
        parser.add_argument('--engine_id', metavar='<engine_id>', required=False, type=int, help=_('Engine ID of a job'))
        parser.add_argument('--project_type', metavar='<project_type>', required=False, type=int, help=_('Project type'))
        return parser

    def take_action(self, parsed_args):      
        client = self.app.client_manager.modelartsv1
        attrs = {}
        args_list = ['job_type', 'engine_id', 'project_type']
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        data = client.job_resource_specifications(**attrs)
        return (
            self.columns,
            (
                utils.get_item_properties(
                    s, self.columns
                )
                for s in data
            ),
        )

        #display_columns, columns = _get_columns(data)
        #data = utils.get_item_properties(data)

        #return display_columns, data
    
