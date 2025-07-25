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


class ResponseInfoHeaderSpec(resource.Resource):
    key = resource.Body('key', type=str)
    value = resource.Body('value', type=str)


class ResponseInfoSpec(resource.Resource):
    status = resource.Body('status', type=int)
    body = resource.Body('body', type=str)
    headers = resource.Body('headers', type=ResponseInfoHeaderSpec)


class GroupResponse(resource.Resource):
    base_path = ('/apigw/instances/%(gateway_id)s/api-groups/%(group_id)s'
                 '/gateway-responses')

    allow_list = True
    allow_create = True
    allow_fetch = True
    allow_delete = True
    allow_commit = True

    _query_mapping = resource.QueryParameters('limit', 'offset')
    resources_key = 'responses'

    # Properties
    gateway_id = resource.URI('gateway_id')
    group_id = resource.URI('group_id')

    # Group name.
    name = resource.Body('name', type=str)
    responses = resource.Body('responses', type=dict,)
