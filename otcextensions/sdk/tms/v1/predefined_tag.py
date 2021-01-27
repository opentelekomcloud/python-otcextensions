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
    #: Properties
    #: Specifies the tag key
    key = resource.Body('key')
    #: Specifies the tag value
    value = resource.Body('value')


class TagsList(Tag):
    #: Specifies the update time which must be a UTC time
    #: sample: 2016-12-09T00:00:00Z
    update_time = resource.Body('update_time')


class PredefinedTag(resource.Resource):
    resources_key = ''
    resource_key = ''
    base_path = '/predefine_tags'

    # capabilities
    allow_create = True
    allow_fetch = False
    allow_commit = True
    allow_delete = False
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'key', 'value', 'limit', 'marker',
        'order_field', 'order_method'
    )

    # Properties
    #: Specifies whether GW is up or down
    #: *true:* Gw is up
    #: *false:* GW is down
    marker = resource.Body('admin_state_up', type=bool)
    #: Specifies the total number of tags
    total_count = resource.Body('created_at')
    #: Specifies the tag list
    tags = resource.Body('description', type=list, list_type=TagsList)
    #: Specifies the tag to be modified
    old_tag = resource.Body('old_tag', type=Tag)
    #: Specifies the tag that has been modified
    new_tag = resource.Body('new_tag', type=Tag)
