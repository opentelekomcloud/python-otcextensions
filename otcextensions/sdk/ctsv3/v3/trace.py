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


class BaseUserSpec(resource.Resource):
    id = resource.Body('id')
    name = resource.Body('name')


class UserInfoSpec(resource.Resource):
    id = resource.Body('id')
    name = resource.Body('name')
    domain = resource.Body('domain', type=BaseUserSpec)


class MetaDataSpec(resource.Resource):
    count = resource.Body('count', type=int)
    marker = resource.Body('marker')


class Trace(resource.Resource):
    base_path = '/traces'
    resources_key = 'traces'

    allow_list = True

    _query_mapping = resource.QueryParameters(
        'trace_type', 'limit', 'from', 'next', 'to', 'tracker_name',
        'service_type', 'user', 'resource_id', 'resource_name',
        'resource_type', 'trace_id', 'trace_name', 'trace_rating')

    resource_id = resource.Body('resource_id')
    trace_name = resource.Body('trace_name')
    trace_rating = resource.Body('trace_rating')
    trace_type = resource.Body('trace_type')
    request = resource.Body('request')
    response = resource.Body('response')
    code = resource.Body('code')
    api_version = resource.Body('api_version')
    message = resource.Body('message')
    record_time = resource.Body('record_time')
    trace_id = resource.Body('trace_id')
    time = resource.Body('time')
    user = resource.Body('user', type=UserInfoSpec)
    service_type = resource.Body('service_type')
    resource_type = resource.Body('resource_type')
    source_ip = resource.Body('source_ip')
    resource_name = resource.Body('resource_name')
    request_id = resource.Body('request_id')
    location_info = resource.Body('location_info')
    endpoint = resource.Body('endpoint')
    resource_url = resource.Body('resource_url')
