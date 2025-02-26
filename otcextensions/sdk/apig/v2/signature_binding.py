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
from openstack import exceptions


class SignatureBind(resource.Resource):
    base_path = f'/apigw/instances/%(gateway_id)s/sign-bindings'

    allow_list = True
    allow_create = True
    allow_delete = True

    resources_key = 'bindings'

    _query_mapping = resource.QueryParameters(
        'limit', 'offset', 'api_id',
        'sign_id', 'sign_name', 'env_id'
    )

    # Properties
    gateway_id = resource.URI('gateway_id')
    # Signature key ID.
    sign_id = resource.Body('sign_id')
    # API publication record ID.
    publish_ids = resource.Body('publish_ids', type=list)

    # Attributes
    # API publication record ID.
    publish_id = resource.Body('publish_id', type=str)
    # API ID.
    api_id = resource.Body('api_id', type=str)
    # Name of the API group to which the API belongs.
    group_name = resource.Body('group_name', type=str)
    # Binding time.
    bind_at = resource.Body('binding_time', type=str)
    # ID of the environment in which the API has been published.
    env_id = resource.Body('env_id', type=str)
    # Name of the environment in which the API has been published.
    env_name = resource.Body('env_name', type=str)
    # API type.
    api_type = resource.Body('api_type', type=str)
    # API name.
    api_name = resource.Body('api_name', type=str)
    # API description.
    api_remark = resource.Body('api_remark', type=str)
    # Signature key name.
    sign_name = resource.Body('sign_name', type=str)
    # Request method.
    # Enumeration values:
    # GET
    # POST
    # DELETE
    # PUT
    # PATCH
    # HEAD
    # OPTIONS
    # ANY
    req_method = resource.Body('req_method', type=str)
    # Signature key.
    sign_key = resource.Body('sign_key', type=str)
    # Signature secret.
    sign_secret = resource.Body('sign_secret', type=str)
    # Signature key type.
    sign_type = resource.Body('sign_type', type=str)

    bindings = resource.Body('bindings', type=list)

    def create(
            self,
            session,
            prepend_key=True,
            base_path=None,
            *,
            resource_request_key=None,
            resource_response_key=None,
            microversion=None,
            **params,
    ):
        """Create a remote resource based on this instance.

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param prepend_key: A boolean indicating whether the resource_key
            should be prepended in a resource creation request. Default to
            True.
        :param str base_path: Base part of the URI for creating resources, if
            different from :data:`~openstack.resource.Resource.base_path`.
        :param str resource_request_key: Overrides the usage of
            self.resource_key when prepending a key to the request body.
            Ignored if `prepend_key` is false.
        :param str resource_response_key: Overrides the usage of
            self.resource_key when processing response bodies.
            Ignored if `prepend_key` is false.
        :param str microversion: API version to override the negotiated one.
        :param dict params: Additional params to pass.
        :return: This :class:`Resource` instance.
        :raises: :exc:`~openstack.exceptions.MethodNotSupported` if
            :data:`Resource.allow_create` is not set to ``True``.
        """
        if not self.allow_create:
            raise exceptions.MethodNotSupported(self, 'create')

        session = self._get_session(session)
        if microversion is None:
            microversion = self._get_microversion(session, action='create')
        requires_id = (
            self.create_requires_id
            if self.create_requires_id is not None
            else self.create_method == 'PUT'
        )

        # Construct request arguments.
        request_kwargs = {
            "requires_id": requires_id,
            "prepend_key": prepend_key,
            "base_path": base_path,
        }
        if resource_request_key is not None:
            request_kwargs['resource_request_key'] = resource_request_key

        if self.create_exclude_id_from_body:
            self._body._dirty.discard("id")

        if self.create_method == 'PUT':
            request = self._prepare_request(**request_kwargs)
            response = session.put(
                request.url,
                json=request.body,
                headers=request.headers,
                microversion=microversion,
                params=params,
            )
        elif self.create_method == 'POST':
            request = self._prepare_request(**request_kwargs)
            response = session.post(
                request.url,
                json=request.body,
                headers=request.headers,
                microversion=microversion,
                params=params,
            )
        else:
            raise exceptions.ResourceFailure(
                "Invalid create method: %s" % self.create_method
            )

        has_body = (
            self.has_body
            if self.create_returns_body is None
            else self.create_returns_body
        )
        self.microversion = microversion

        response_kwargs = {
            "has_body": has_body,
        }
        if resource_response_key is not None:
            response_kwargs['resource_response_key'] = resource_response_key

        if has_body is None:
            has_body = self.has_body
        exceptions.raise_from_response(response)
        bindings = []
        if has_body and response.status_code == 201:
            if hasattr(self, 'bindings'):
                body = response.json()
                bindings = [
                    SignatureBind.existing(**data)
                    for data in body['bindings']
                ]
        self.bindings = bindings
        # direct comparision to False since we need to rule out None
        if self.has_body and self.create_returns_body is False:
            # fetch the body if it's required but not returned by create
            fetch_kwargs = {}
            if resource_response_key is not None:
                fetch_kwargs = {'resource_response_key': resource_response_key}
            return self.fetch(session, **fetch_kwargs)
        return self


class NotBoundApi(resource.Resource):
    base_path = f'/apigw/instances/%(gateway_id)s/sign-bindings/unbinded-apis'

    allow_list = True

    resources_key = 'apis'

    _query_mapping = resource.QueryParameters(
        'limit', 'offset', 'sign_id',
        'env_id', 'api_id', 'api_name', 'group_id'
    )

    # Properties
    gateway_id = resource.URI('gateway_id')

    # Attributes
    # API authentication mode.
    auth_type = resource.Body('auth_type', type=str)
    # Name of the environment in which the API has been published.
    run_env_name = resource.Body('run_env_name', type=str)
    # Name of the API group to which the API belongs.
    group_name = resource.Body('group_name', type=str)
    # Publication record ID.
    publish_id = resource.Body('publish_id', type=str)
    # ID of the API group to which the API belongs.
    group_id = resource.Body('group_id', type=str)
    # API name.
    name = resource.Body('name', type=str)
    # API description.
    remark = resource.Body('remark', type=str)
    # ID of the environment in which the API has been published.
    run_env_id = resource.Body('run_env_id', type=str)
    # API request address.
    req_uri = resource.Body('req_uri', type=str)
    # API type.
    type = resource.Body('type', type=int)
    # Name of the signature key bound to the API.
    signature_name = resource.Body('signature_name', type=str)
    # Request method.
    # Enumeration values:
    # GET
    # POST
    # DELETE
    # PUT
    # PATCH
    # HEAD
    # OPTIONS
    # ANY
    req_method = resource.Body('req_method', type=str)


class BoundApi(resource.Resource):
    base_path = f'/apigw/instances/%(gateway_id)s/sign-bindings/binded-apis'

    allow_list = True

    resources_key = 'bindings'

    _query_mapping = resource.QueryParameters(
        'limit', 'offset', 'sign_id',
        'env_id', 'api_id', 'api_name', 'group_id'
    )

    # Properties
    gateway_id = resource.URI('gateway_id')

    # Attributes
    # API publication record ID.
    publish_id = resource.Body('publish_id', type=str)
    # API ID.
    api_id = resource.Body('api_id', type=str)
    # Name of the API group to which the API belongs.
    group_name = resource.Body('group_name', type=str)
    # Binding time.
    bind_at = resource.Body('binding_time', type=str)
    # ID of the environment in which the API has been published.
    env_id = resource.Body('env_id', type=str)
    # Name of the environment in which the API has been published.
    env_name = resource.Body('env_name', type=str)
    # API type.
    api_type = resource.Body('api_type', type=str)
    # API name.
    api_name = resource.Body('api_name', type=str)
    # API description.
    api_remark = resource.Body('api_remark', type=str)
    # Signature key name.
    sign_name = resource.Body('sign_name', type=str)
    # Request method.
    # Enumeration values:
    # GET
    # POST
    # DELETE
    # PUT
    # PATCH
    # HEAD
    # OPTIONS
    # ANY
    req_method = resource.Body('req_method', type=str)
