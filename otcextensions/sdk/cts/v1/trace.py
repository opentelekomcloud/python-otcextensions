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

from otcextensions.common import format


class Trace(resource.Resource):

    base_path = '/%(tracker_name)s/trace'
    resources_key = 'traces'
    service_expectes_json_type = True

    allow_list = True

    # NOTE: resource_type query param need to be renamed, due to a conflict
    # with proxy._list function
    _query_mapping = resource.QueryParameters(
        'service_type', 'res_type', 'res_id', 'res_name',
        'trace_name', 'limit', 'next', 'from', 'to',
        'trace_id', 'level', 'user',
        level='trace_rating',
        res_type='resource_type',
        res_id='resource_id',
        res_name='resource_name')

    # Properties
    tracker_name = resource.URI('tracker_name')
    #: API version
    api_version = resource.Body('api_version')
    #: trace http return code
    code = resource.Body('code')
    #: Trace ID
    id = resource.Body('trace_id', alternate_id=True)
    #: rating of the trace, normal, warning, incident
    level = resource.Body('trace_rating')
    #: remark of the trace
    message = resource.Body('message')
    #: metadata of the trace
    #: *Type: dict*
    meta_data = resource.Body('meta_data', type=dict)
    #: name of the trace
    name = resource.Body('trace_name')
    #: record time stampt
    record_time = resource.Body('record_time', type=format.TimeTMsStr)
    #: trace request content
    request = resource.Body('request')
    #: trace resource id
    resource_id = resource.Body('resource_id')
    #: resource name of the trace
    resource_name = resource.Body('resource_name')
    #: trace resource type
    resource_type = resource.Body('resource_type')
    #: trace response content
    response = resource.Body('response')
    #: trace service type
    service_type = resource.Body('service_type')
    #: user ip of the trace
    source_ip = resource.Body('source_ip')
    #: *Type: int*
    time = resource.Body('time', type=format.TimeTMsStr)
    #: trace source type
    type = resource.Body('trace_type')
    #: trace user information
    user = resource.Body('user')

    @classmethod
    def _get_next_link(cls, uri, response, data, marker, limit, total_yielded):
        next_link = None
        marker = data['meta_data'].get('marker', None)
        params = {}
        if limit and marker:
            next_link = uri
            params['next'] = marker
            params['limit'] = limit
        return next_link, params
