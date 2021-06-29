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


class Flavor(resource.Resource):
    base_path = '/flavors'

    resources_key = 'flavors'

    # capabilities
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'region', 'engine_name')

    region = resource.URI('region')
    # Properties
    #: Indicates the engine name.
    engine_name = resource.Body('engine_name')
    #: Indicates the node type. DDS contains the following types of nodes:
    # - mongos
    # - shard
    # - config
    # - replica
    type = resource.Body('type')
    #: Number of vCPUs.
    vcpus = resource.Body('vcpus')
    #: Indicates the memory size in gigabyte (GB).
    ram = resource.Body('ram')
    #: Indicates the resource specifications code.
    spec_code = resource.Body('spec_code')
    #: Indicates the status of specifications in an AZ.
    az_status = resource.Body('az_status')
