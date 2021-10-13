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
    resource_key = "tag"
    resources_key = "tags"
    base_path = "/predefine_tags"

    allow_create = True
    allow_fetch = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'key', 'value', 'limit', 'marker', 'order_field', 'order_method'
    )

    #: Specifies the key.
    key = resource.Body('key')
    #: Specifies the value.
    value = resource.Body('value')
    #: Specifies the number of query records.
    limit = resource.Body('limit')
    #: Specifies the paging location identifier (index).
    marker = resource.Body('marker')
    #: Specifies the field for sorting.
    order_field = resource.Body('order_field')
    #: Specifies the sorting method of the order_field field.
    order_method = resource.Body('order_method')
