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


class Domain(resource.Resource):
    base_path = 'manage/namespaces/%(namespace)s/' \
                'repositories/%(repository)s/access-domains'

    # capabilities
    allow_create = True
    allow_delete = True
    allow_list = True
    allow_commit = True
    allow_fetch = True

    commit_method = "PATCH"

    #: Organization namespace
    #: *Type:str*
    namespace = resource.URI('namespace')
    #: Image repository name
    #: *Type:str*
    repository = resource.URI('repository')
    #: Name of the account used for image sharing
    #: *Type:str*
    access_domain = resource.Body('access_domain', type=str)
    #: Currently, only the read permission is supported
    #: *Type:str*
    permit = resource.Body('permit', type=str)
    #: Valid until (UTC). If the sharing is permanent, the value is forever.
    #: Otherwise, the sharing is valid until 00:00:00 of the next day
    #: *Type:str*
    deadline = resource.Body('deadline', type=str)
    #: Description
    #: *Type:str*
    description = resource.Body('description', type=str)
    #: Creator ID
    #: *Type:str*
    creator_id = resource.Body('creator_id')
    #: Name of the creator
    #: *Type:str*
    creator_name = resource.Body('creator_name')
    #: Time when an image is created. It is the UTC standard time
    #: *Type:str*
    created_at = resource.Body('created')
    #: Time when an image is updated. It is the UTC standard time
    #: *Type:int*
    updated_at = resource.Body('updated')
    #: Status
    #: *Type:bool*
    status = resource.Body('status')
    #: Whether account exist
    #: *Type:bool*
    exist = resource.Body('exist')
