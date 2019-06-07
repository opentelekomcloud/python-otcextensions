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
from openstack import resource


class Statistic(resource.Resource):

    resources_key = 'statistics'

    base_path = '/instances/statistic'

    # capabilities
    allow_list = True
    allow_fetch = True

    # Properties
    #: Number of times that the GET command is run.
    #: *Type: int*
    cmd_get_count = resource.Body('cmd_get_count', type=int)
    #: Number of times that the SET command is run.
    #: *Type: int*
    cmd_set_count = resource.Body('cmd_set_count', type=int)
    #: Incoming traffic of the DCS instance.
    #: Unit: kbit/s.
    #: *Type: str*
    input_kbps = resource.Body('input_kbps')
    #: Instance Id
    instance_id = resource.Body('instance_id', alternate_id=True)
    #: Number of data items stored in the cache.
    #: *Type: int*
    keys = resource.Body('keys', type=int)
    #: Overall memory size.
    #: Unit: MB.
    #: *Type: int*
    max_memory = resource.Body('max_memory', type=int)
    #: Outgoing traffic of the DCS instance.
    #: Unit: kbit/s.
    #: *Type: str*
    output_kbps = resource.Body('output_kbps')
    #: CPU Usage %
    #: *Type: str*
    used_cpu = resource.Body('used_cpu')
    #: Size of the used memory.
    #: Unit: MB.
    #: *Type: int*
    used_memory = resource.Body('used_memory', type=int)
