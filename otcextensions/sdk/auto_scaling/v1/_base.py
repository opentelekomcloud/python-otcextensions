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
from otcextensions.sdk.auto_scaling import auto_scaling_service
from otcextensions.sdk import sdk_resource

from openstack import resource
# from openstack import utils


class Resource(sdk_resource.Resource):

    query_marker_key = 'start_number'
    service = auto_scaling_service.AutoScalingService()

    _query_mapping = resource.QueryParameters(
        'marker', 'limit',
        marker='start_number',
        limit='limit'
    )

    @classmethod
    def _get_next_link(cls, uri, response, data, marker, limit, total_yielded):
        next_link = None
        params = {}
        if total_yielded < data['total_number']:
            next_link = uri
            params['marker'] = total_yielded
            params['limit'] = limit
        else:
            next_link = None
        query_params = cls._query_mapping._transpose(params)
        return next_link, query_params
