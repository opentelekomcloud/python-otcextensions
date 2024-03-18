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
from otcextensions.sdk.swr.v2 import _base


class Organization(resource.Resource):
    base_path = '/manage/namespaces'
    resources_key = 'namespaces'

    # capabilities
    allow_create = True
    allow_delete = True
    allow_fetch = True
    allow_list = True

    _query_mapping = resource.QueryParameters(namespace='namespace')

    #: Organization namespace.
    #: *Type:str*
    namespace = resource.Body('namespace')
    #: Organization ID
    #: *Type:str*
    id = resource.Body('id', type=str)
    #: Organization name
    #: *Type:str*
    name = resource.Body('name', type=str)
    #: Organization name
    #: *Type:str*
    creator_name = resource.Body('creator_name', type=str)
    #: User permission
    #: 7: Manage
    #: 3: Write
    #: 1: Read
    #: *Type:int*
    user_auth = resource.Body('auth', type=int)


class Auth(resource.Resource):
    #: Properties
    #: User ID
    user_id = resource.Body('user_id', type=str)
    #: Username
    user_name = resource.Body('user_name', type=str)
    #: User permission
    #: 7: Manage
    #: 3: Write
    #: 1: Read
    user_auth = resource.Body('auth', type=int)


class Permission(_base.Resource):
    base_path = '/manage/namespaces/%(namespace)s/access'

    # capabilities
    allow_create = True
    allow_delete = True
    allow_commit = True
    allow_fetch = True
    allow_list = True

    commit_method = "PATCH"

    requires_id = False

    _query_mapping = resource.QueryParameters(namespace='namespace')

    #: Organization namespace.
    #: *Type:str*
    namespace = resource.URI('namespace')
    #: Information required for creating organization permissions.
    #: *Type:list*
    permissions = resource.Body('permissions', type=list, list_type=Auth)
    #: Permission ID
    #: *Type:int*
    id = resource.Body('id', type=int)
    #: Organization name
    #: *Type:str*
    name = resource.Body('name', type=str)
    #: Organization name
    #: *Type:str*
    creator_name = resource.Body('creator_name', type=str)
    #: Permissions of the current user
    #: *Type:dict*
    self_auth = resource.Body('self_auth', type=dict)
    #: Permissions of other users
    #: *Type:dict*
    others_auths = resource.Body('others_auths', type=list)
