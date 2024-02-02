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


class Organization(resource.Resource):
    base_path = '/manage/namespaces'
    resources_key = 'namespaces'

    # capabilities
    allow_create = True
    allow_delete = True
    allow_fetch = True
    allow_list = True

    _query_mapping = resource.QueryParameters(organization='namespace')

    #: Organization namespace.
    #: *Type:str*
    organization = resource.Body('namespace')
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
    auth = resource.Body('auth', type=int)

    def delete(self, session, error_message=None):
        """Delete the remote resource based on this instance.

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`

        :return: This :class:`Resource` instance.
        :raises: :exc:`~openstack.exceptions.MethodNotSupported` if
                 :data:`Resource.allow_commit` is not set to ``True``.
        :raises: :exc:`~openstack.exceptions.ResourceNotFound` if
                 the resource was not found.
        """
        if self.id is None and self.organization is not None:
            self.id = self.organization
        response = self._raw_delete(session)
        kwargs = {}
        if error_message:
            kwargs['error_message'] = error_message

        self._translate_response(response, has_body=True, **kwargs)
        return self


class OrganizationPermission(resource.Resource):
    base_path = '/manage/namespaces/%(namespace)s/access'

    # capabilities
    allow_create = True
    allow_delete = True
    allow_commit = True
    allow_fetch = True

    #: Organization name.
    #: *Type:str*
    namespace = resource.URI('namespace')
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
    others_auths = resource.Body('others_auths', type=dict)
