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


class Tag(resource.Resource):
    base_path = 'apigw/instances/%(gateway_id)s/tags'

    _query_mapping = resource.QueryParameters('limit', 'offset')

    allow_list = True

    gateway_id = resource.URI('gateway_id')
    tags = resource.Body('tags', type=list)
    size = resource.Body('size', type=int)
    total = resource.Body('total', type=int)
