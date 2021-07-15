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
    resource_key = 'flavor'
    resources_key = 'flavors'
    base_path = '/elb/flavors'

    # capabilities
    allow_fetch = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'marker', 'limit', 'page_reverse',
        'id', 'name', 'type', 'shared'
    )

    # Properties
    #: Specifies the flavor ID.
    id = resource.Body('id')
    #: Specifies the flavor details.
    info = resource.Body('info', type=dict)
    #: Specifies the flavor name.
    name = resource.Body('name')
    #: Specifies whether the flavor is available to all users.
    shared = resource.Body('shared', type=bool)
    #: Pagination information about the load balancer flavors.
    page_info = resource.Body('page_info', type=dict)
    #: Specifies the project ID.
    project_id = resource.Body('project_id')
    #: Specifies the request ID.
    request_id = resource.Body('request_id')
    #: Specifies the flavor type.
    type = resource.Body('type')
