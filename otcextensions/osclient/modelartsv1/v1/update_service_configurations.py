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
"""ModelArts dataset v2 action implementations"""
import logging

from osc_lib import utils
from osc_lib.command import command
from otcextensions.common import cli_utils
from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)

class UpdateServiceConfigurations(command.Command):
    _description = _('This API is used to update configurations of a model service.')

    def get_parser(self, prog_name):
            parser = super(UpdateServiceConfigurations, self).get_parser(prog_name)
            parser.add_argument('--service_id', metavar='<service_id>', required=True, type=str, help=_('Service ID'))
            parser.add_argument('--description', metavar='<description>', required=False, type=str, help=_('Service description, which contains a maximum of 100 characters'))
            parser.add_argument('--status', metavar='<status>', required=False, type=str, help=_('Service status'))
            """
            parser.add_argument('--config', metavar='<config>', required=False, type=dict, help=_('Service configuration'))
            parser.add_argument('--schedule', metavar='<schedule>', required=False, type=dict, help=_('Service scheduling configuration, which can be configured only for real-time services'))
            parser.add_argument('--additional_properties', metavar='<additional_properties>', required=False, type=dict, help=_('Additional service attribute, which facilitates service management'))
            
            parser.add_argument('--model_id', metavar='<model_id>', required=True, type=str, help=_('Model ID'))
            parser.add_argument('--weight', metavar='<weight>', required=True, type=int, help=_('Traffic weight allocated to a model'))
            
            parser.add_argument('--specification', metavar='<specification>', required=True, type=str, help=_('Resource specifications'))
            parser.add_argument('--custom_spec', metavar='<custom_spec>', required=False, type=dict, help=_('Custom specifications'))
            parser.add_argument('--instance_count', metavar='<instance_count>', required=True, type=int, help=_('Number of instances for deploying a model'))
            parser.add_argument('--envs', metavar='<envs>', required=False, type=dict, help=_('(Optional) Environment variable key-value pair required for running a model'))
            parser.add_argument('--cluster_id', metavar='<cluster_id>', required=False, type=str, help=_('ID of a dedicated resource pool'))
            ##parser.add_argument('--model_id', metavar='<model_id>', required=True, type=str, help=_('Model ID'))
            ##parser.add_argument('--specification', metavar='<specification>', required=True, type=str, help=_('Resource flavor'))
            ##parser.add_argument('--instance_count', metavar='<instance_count>', required=True, type=int, help=_('Number of instances for deploying a model'))
            ##parser.add_argument('--envs', metavar='<envs>', required=False, type=dict, help=_('(Optional) Environment variable key-value pair required for running a model'))
            parser.add_argument('--src_type', metavar='<src_type>', required=False, type=str, help=_('Data source type'))
            parser.add_argument('--src_path', metavar='<src_path>', required=True, type=str, help=_('OBS path of the input data of a batch job'))
            parser.add_argument('--dest_path', metavar='<dest_path>', required=True, type=str, help=_('OBS path of the output data of a batch job'))
            parser.add_argument('--req_uri', metavar='<req_uri>', required=True, type=str, help=_('Inference API called in a batch job, which is a REST API in the model image'))
            parser.add_argument('--mapping_type', metavar='<mapping_type>', required=True, type=str, help=_('Mapping type of the input data'))
            parser.add_argument('--mapping_rule', metavar='<mapping_rule>', required=False, type=dict, help=_('Mapping between input parameters and CSV data'))
            parser.add_argument('--type', metavar='<type>', required=True, type=str, help=_('Scheduling type'))
            parser.add_argument('--time_unit', metavar='<time_unit>', required=True, type=str, help=_('Scheduling time unit'))
            parser.add_argument('--duration', metavar='<duration>', required=True, type=int, help=_('Value that maps to the time unit'))
            """
            return parser

    def take_action(self, parsed_args):      
        client = self.app.client_manager.modelartsv1
        attrs = {}
        args_list = ['service_id', 'description', 'status'] #, 'config', 'schedule', 'additional_properties','model_id', 'weight']
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        #data = 
        client.update_service_configurations(**attrs) #service_id=parsed_args.service_id)
        #display_columns, columns = _get_columns(data)
        #data = utils.get_item_properties(data, columns, formatters=_formatters)

        #return display_columns, data
    
