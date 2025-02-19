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


class ThrottlingPolicy(resource.Resource):
    base_path = f'/apigw/instances/%(gateway_id)s/throttles'

    allow_list = True
    allow_create = True
    allow_commit = True
    allow_delete = True
    allow_fetch = True

    resources_key = 'throttles'

    _query_mapping = resource.QueryParameters(
        'limit', 'offset', 'name',
        'id', 'name', 'precise_search'
    )

    # Properties
    gateway_id = resource.URI('gateway_id')
    # Maximum number of times the API can be accessed
    # by an app within the same period.
    app_call_limits = resource.Body('app_call_limits', type=int)
    # Request throttling policy name.
    name = resource.Body('name', type=str)
    # Time unit for limiting the number of API calls.
    # Enumeration values:
    # SECOND
    # MINUTE
    # HOUR
    # DAY
    time_unit = resource.Body('time_unit', type=str)
    # Description of the request throttling policy,
    # which can contain a maximum of 255 characters.
    remark = resource.Body('remark', type=str)
    # Maximum number of times an API can be accessed within a specified period.
    api_call_limits = resource.Body('api_call_limits', type=int)
    # Type of the request throttling policy.
    # 1: API-based, limiting the maximum number of times a
    # single API bound to the policy can be called within the specified period.
    # 2: API-shared, limiting the maximum number of times
    # all APIs bound to the policy can be called within the specified period.
    type = resource.Body('type', type=int)
    # Indicates whether to enable dynamic request throttling.
    # TRUE
    # FALSE
    enable_adaptive_control = resource.Body(
        'enable_adaptive_control', type=str
    )
    # Maximum number of times the API can be accessed
    # by a user within the same period.
    user_call_limits = resource.Body('user_call_limits', type=str)
    # Period of time for limiting the number of API calls.
    time_interval = resource.Body('time_interval', type=int)
    # Maximum number of times the API can be accessed
    # by an IP address within the same period.
    ip_call_limits = resource.Body('ip_call_limits', type=int)

    # Attributes
    # Number of APIs to which the request throttling policy has been bound.
    bind_num = resource.Body('bind_num', type=int)
    # Indicates whether an excluded request throttling configuration has been created.
    # 1: yes
    # 2: no
    is_inclu_special_throttle = resource.Body(
        'is_inclu_special_throttle', type=int
    )
    # Creation time.
    created_at = resource.Body('create_time', type=str)
