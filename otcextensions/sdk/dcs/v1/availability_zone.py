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


class AvailabilityZone(resource.Resource):

    resources_key = 'available_zones'

    base_path = '/availableZones'

    # capabilities
    allow_list = True

    #: Properties
    #: Available Zone ID.
    id = resource.Body('id')
    #: Available Zone code.
    code = resource.Body('code')
    #: Available Zone name.
    name = resource.Body('name')
    #: Port number of the Available Zone.
    port = resource.Body('port')
    #: An indicator of whether there are available resources in the
    # Available Zone
    resource_availability = resource.Body('resource_availability')
