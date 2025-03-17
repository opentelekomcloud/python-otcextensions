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


class ResourceType(resource.Resource):
    #: Properties
    #: Maximum quota capacity
    max = resource.Body('max', type=int)
    #: Minimum quota capacity
    min = resource.Body('min', type=int)
    #: Resource quota
    quota = resource.Body('quota', type=int)
    #: Specifies the resource types
    #: Values: server_groups, replications
    type = resource.Body('type')
    #: Specifies the number of used resources
    used = resource.Body('used', type=int)


class Quota(resource.Resource):
    """SDRS Tenant Quota Resource"""
    resources_key = 'quotas'
    base_path = '/sdrs/quotas'

    # capabilities
    allow_list = True

    #: Properties
    #: Tenant resource quotas
    resources = resource.Body('resources', type=list, list_type=ResourceType)
