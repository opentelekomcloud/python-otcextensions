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


class ThrottlingExcludedPolicy(resource.Resource):
    base_path = (f'/apigw/instances/%(gateway_id)s/throttles/'
                 f'%(throttle_id)s/throttle-specials')

    allow_list = True
    allow_create = True
    allow_commit = True
    allow_delete = True

    resources_key = 'throttle_specials'

    _query_mapping = resource.QueryParameters(
        'limit', 'offset', 'object_type',
        'app_name', 'user'
    )

    # Properties
    gateway_id = resource.URI('gateway_id')
    # Request throttling policy ID.
    throttle_id = resource.URI('throttle_id')

    # Maximum number of times an excluded object
    # can access an API within the throttling period.
    call_limits = resource.Body('call_limits', type=int)
    # Excluded app ID or account ID.
    object_id = resource.Body('object_id', type=str)
    # Excluded object type.
    # Enumeration values:
    # APP
    # USER
    object_type = resource.Body('object_type', type=str)

    # Attributes
    # Throttling period.
    apply_time = resource.Body('apply_time', type=str)
    # App name.
    app_name = resource.Body('app_name', type=str)
    # App ID.
    app_id = resource.Body('app_id', type=str)
    # Name of an app or a tenant to which the excluded configuration applies.
    object_name = resource.Body('object_name', type=str)
