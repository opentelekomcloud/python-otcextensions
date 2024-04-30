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


class ResourceTag(resource.Resource):
    resource_key = 'resource_tag'
    base_path = '/resource-tags'

    _query_mapping = resource.QueryParameters(
        'project_id', 'resource_id', 'resource_type'
    )

    #: Properties
    project_id = resource.Body('project_id')
    tags = resource.Body('tags', type=list)
    resources = resource.Body('resources', type=list)

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

    #: Method for committing a resource (PUT, PATCH, POST)
    commit_method = "PUT"
    #: Method for creating a resource (POST, PUT)
    create_method = "POST"

    # adding tags, removing tags, querying tags, querying resources by tag
