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


class FlavorDetail(resource.Resource):
    #: Attribute type
    type = resource.Body('type')
    #: Attribute Unit
    unit = resource.Body('unit')
    #: Attribute value
    value = resource.Body('value', type=str)


class Flavor(resource.Resource):
    base_path = '/node-types'

    resources_key = 'node_types'

    # capabilities
    allow_list = True

    # Properties
    #: Availability Zones
    availability_zones = resource.Computed('availability_zones')
    #: Node type details
    detail = resource.Body('detail', type=list, list_type=FlavorDetail)
    #: Disk Size
    disk_size = resource.Computed('disk_size')
    #: Disk Type
    disk_type = resource.Body('disk_type')
    #: Name of a node type
    name = resource.Body('spec_name')
    #: Memory
    ram = resource.Computed('ram')
    #: Name of a node type
    spec_name = resource.Body('spec_name')
