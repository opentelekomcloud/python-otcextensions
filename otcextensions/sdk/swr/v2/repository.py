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


class Repository(resource.Resource):
    base_path = '/manage/namespaces/%(namespace)s/repos'

    # capabilities
    allow_create = True
    allow_delete = True
    allow_fetch = True
    allow_list = True
    allow_commit = True

    commit_method = "PATCH"

    _query_mapping = resource.QueryParameters(
        'center', 'namespace', 'name', 'category', 'offset',
        'limit', 'order_column', 'order_type'
    )

    #: Organization namespace
    #: *Type:str*
    namespace = resource.URI('namespace')
    #: Image repository name
    #: *Type:str*
    repository = resource.Body('repository', type=str)
    #: Repository type
    #: The value can be app_server, linux, framework_app,
    #: database, lang, other, windows or arm.
    #: *Type:str*
    category = resource.Body('category', type=str)
    #: Brief description of the image repository
    #: *Type:str*
    description = resource.Body('description', type=str)
    #: Whether the repository is a public repository
    #: When the value is true, it indicates the repository is public.
    #: When the value is false, it indicates the repository is private.
    #: *Type:bool*
    is_public = resource.Body('is_public', type=bool)
    #: Image repository ID
    #: *Type:int*
    id = resource.Body('id')
    #: Organization ID
    #: *Type:int*
    ns_id = resource.Body('ns_id')
    #: Image repository name
    #: *Type:str*
    name = resource.Body('name')
    #: Image repository creator ID
    #: *Type:str*
    creator_id = resource.Body('creator_id')
    #: Image repository creator
    #: *Type:str*
    creator_name = resource.Body('creator_name')
    #: Image repository size
    #: *Type:str*
    size = resource.Body('size')
    #: Number of images in an image repository
    #: *Type:int*
    num_images = resource.Body('num_images')
    #: Download times of an image repository
    #: *Type:int*
    num_download = resource.Body('num_download')
    #: URL of the image repository logo image
    #: This field has been discarded and is left empty by default
    #: *Type:str*
    url = resource.Body('url')
    #: External image pull address.
    #: The format is {Repository address}/{Namespace name}/{Repository name}.
    #: *Type:str*
    path = resource.Body('path')
    #: Internal image pull address.
    #: The format is {Repository address}/{Namespace name}/{Repository name}.
    #: *Type:str*
    internal_path = resource.Body('internal_path')
    #: Time when an image repository is created. It is the UTC standard time
    #: *Type:str*
    created = resource.Body('created')
    #: Time when an image repository is updated. It is the UTC standard time
    #: *Type:str*
    updated = resource.Body('updated')
    #: Account ID
    #: *Type:str*
    domain_id = resource.Body('domain_id')
    #: Image sorting priority
    #: *Type:int*
    priority = resource.Body('priority')
    #: Image tag list
    #: *Type:list*
    tags = resource.Body('tags', type=list)
    #: Status
    #: *Type:bool*
    status = resource.Body('status')
    #: Total number of records
    #: *Type:int*
    total_range = resource.Body('total_range')
