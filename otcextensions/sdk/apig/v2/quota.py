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


class Quota(resource.Resource):
    base_path = f'/apigw/instances/%(gateway_id)s/apps/%(app_id)s/bound-quota'

    gateway_id = resource.URI('gateway_id')
    app_id = resource.URI('app_id')

    allow_fetch = True

    app_quota_id = resource.Body('app_quota_id')
    name = resource.Body('name')
    call_limits = resource.Body('call_limits', type=int)
    time_unit = resource.Body('time_unit')
    time_interval = resource.Body('time_interval')
    remark = resource.Body('remark')
    reset_time = resource.Body('reset_time')
    create_time = resource.Body('create_time')
    bound_app_num = resource.Body('bound_app_num')
