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
from openstack import utils


class PredefinedTag(resource.Resource):
    resource_key = 'predefine_tag'
    base_path = '/predefine_tags'

    _query_mapping = resource.QueryParameters(
        'key', 'value', 'limit', 'marker', 'order_field', 'order_method')

    #: Properties
    marker = resource.Body('marker')
    total_count = resource.Body('total_count')
    tags = resource.Body('tags', type=list)

    #: Allow to create operation for this resource.
    allow_create = True
    #: Allow get operation for this resource.
    allow_fetch = False
    #: Allow update operation for this resource.
    allow_commit = False
    #: Allow to delete operation for this resource.
    allow_delete = True
    #: Allow list operation for this resource.
    allow_list = True
    #: Allow head operation for this resource.
    allow_head = False
    #: Allow patch operation for this resource.
    allow_patch = False

    #: Commits happen without header or body being dirty.
    allow_empty_commit = False

    #: Method for committing a resource (PUT, PATCH, POST)
    commit_method = "PUT"
    #: Method for creating a resource (POST, PUT)
    create_method = "POST"
