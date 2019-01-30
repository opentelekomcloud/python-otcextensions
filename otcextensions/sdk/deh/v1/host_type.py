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

from otcextensions.sdk import sdk_resource


class HostType(sdk_resource.Resource):
    resource_key = ''
    resources_key = 'dedicated_host_types'
    base_path = '/availability-zone/%(availability_zone)s/dedicated-host-types'

    # capabilities
    allow_list = True

    #: Properties
    availability_zone = resource.URI('availability_zone')
    #: Specifes the DeH type
    host_type = resource.Body('host_type')
    #: Specifes the DeH name of type
    host_type_name = resource.Body('host_type_name')
