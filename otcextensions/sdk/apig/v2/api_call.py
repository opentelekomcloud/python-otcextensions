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
from openstack import exceptions


class StatisticsAPISpec(resource.Resource):
    max_latency = resource.Body('max_latency', type=int)
    avg_latency = resource.Body('avg_latency', type=float)
    req_count = resource.Body('req_count', type=int)
    req_count2xx = resource.Body('req_count_2xx', type=int)
    req_count4xx = resource.Body('req_count_4xx', type=int)
    req_count5xx = resource.Body('req_count_5xx', type=int)
    req_count_error = resource.Body('req_count_error', type=int)
    max_inner_latency = resource.Body('max_inner_latency', type=int)
    avg_inner_latency = resource.Body('avg_inner_latency', type=float)
    max_backend_latency = resource.Body('max_backend_latency', type=int)
    avg_backend_latency = resource.Body('avg_backend_latency', type=float)
    output_throughput = resource.Body('output_throughput', type=float)
    input_throughput = resource.Body('input_throughput', type=float)
    current_minute = resource.Body('current_minute', type=int)
    cycle = resource.Body('cycle')
    api_id = resource.Body('api_id')
    group_id = resource.Body('group_id')
    provider = resource.Body('provider')
    req_time = resource.Body('req_time')
    register_time = resource.Body('register_time')
    status = resource.Body('status', type=int)


class ApiCallResult(resource.Resource):
    allow_fetch = True
    _query_mapping = resource.QueryParameters(
        'api_id', 'duration'
    )

    code = resource.Body('code')
    msg = resource.Body('msg')
    start_time = resource.Body('start_time')
    end_time = resource.Body('end_time')
    api_list = resource.Body('list', type=list,
                             list_type=StatisticsAPISpec)

    def get_api_calls_for_period(self, session, gateway_id, **params):
        """Fetch API calls for a specific period."""
        uri = f'apigw/instances/{gateway_id}/statistics/api/latest'
        response = session.get(uri, params=params)
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self

    def get_api_calls_for_group(self, session, gateway_id, **attrs):
        """Fetch API calls for a specific group."""
        uri = f'apigw/instances/{gateway_id}/statistics/group/latest'
        response = session.get(uri, params=attrs)
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self
