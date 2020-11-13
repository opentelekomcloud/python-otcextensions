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


class ResourcesSpec(resource.Resource):

    # Properties
    # quota type
    type = resource.Body('type')
    # total amount of quota
    quota = resource.Body('quota', type=int)
    # quota unit
    unit = resource.Body('unit')
    # used amount of quota
    used = resource.Body('used', type=int)


class Quota(resource.Resource):
    resources_key = 'quotas'
    base_path = '/quotas'

    # capabilities
    allow_list = True

    # Properties
    resources = resource.Body('resources', type=list,
                              list_type=ResourcesSpec)
