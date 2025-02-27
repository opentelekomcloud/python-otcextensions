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


class ThrottlingPolicyRecords(resource.Resource):
    # API publication record ID.
    publish_id = resource.Body('publish_id', type=str)
    # Scope of the policy.
    # 1: the API
    # 2: a user
    # 3: an app
    scope = resource.Body('scope', type=int)
    # Request throttling policy ID.
    throttle_id = resource.Body('strategy_id')
    # Binding time.
    applied_at = resource.Body('apply_time', type=str)


class ThrottleBindingBatchFailure(resource.Resource):
    # ID of a request throttling policy binding record
    # that fails to be canceled.
    bind_id = resource.Body('bind_id', type=str)
    # Error code.
    error_code = resource.Body('error_code', type=int)
    # Error message.
    error_msg = resource.Body('error_msg')
    # ID of an API from which unbinding fails.
    api_id = resource.Body('api_id', type=str)
    # Name of the API from which unbinding fails.
    api_name = resource.Body('api_name', type=str)


class ThrottlingPolicyBind(resource.Resource):
    base_path = f'/apigw/instances/%(gateway_id)s/throttle-bindings'

    allow_list = True
    allow_create = True
    allow_delete = True

    resources_key = 'apis'

    _query_mapping = resource.QueryParameters(
        'limit', 'offset', 'throttle_id',
        'env_id', 'group_id', 'api_id', 'api_name'
    )

    # Properties
    gateway_id = resource.URI('gateway_id')
    # Request throttling policy ID.
    throttle_id = resource.Body('strategy_id')
    # API publication record ID.
    publish_ids = resource.Body('publish_ids', type=list)

    # Attributes
    # API publication record ID.
    publish_id = resource.Body('publish_id', type=str)
    # API authentication mode.
    auth_type = resource.Body('auth_type', type=str)
    # Name of the API group to which the API belongs.
    group_name = resource.Body('group_name', type=str)
    # ID of a request throttling policy binding record.
    throttle_apply_id = resource.Body('throttle_apply_id', type=str)
    # Binding time.
    applied_at = resource.Body('apply_time', type=str)
    # API description.
    remark = resource.Body('remark', type=str)
    # ID of the environment in which the API has been published.
    run_env_id = resource.Body('run_env_id', type=str)
    # API type.
    type = resource.Body('type', type=int)
    # Name of the request throttling policy bound to the API.
    throttle_name = resource.Body('throttle_name', type=str)
    # Access address of the API.
    req_uri = resource.Body('req_uri', type=str)
    # Name of the environment in which the API has been published.
    run_env_name = resource.Body('run_env_name', type=str)
    # ID of the API group to which the API belongs.
    group_id = resource.Body('group_id', type=str)
    # API name.
    name = resource.Body('name', type=str)
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

    policies = resource.Body(
        'policies', type=list, list_type=ThrottlingPolicyRecords
    )
    failure = resource.Body(
        'failure', type=list, list_type=ThrottleBindingBatchFailure
    )

    def _action(self, session, body):
        """Preform actions given the message body.
        """
        url = self.base_path % {'gateway_id': body['gateway_id']}
        url += '?action=delete'
        response = session.put(url, json=body)
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self

    def unbind_policies(self, session, **attrs):
        """Unbind request throttling policies from APIs.
        """
        return self._action(session, attrs)

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
        policies = []
        if has_body and response.status_code == 201:
            body = response.json()
            policies = [
                ThrottlingPolicyRecords.existing(**data)
                for data in body['throttle_applys']
            ]
        self.policies = policies
        # direct comparision to False since we need to rule out None
        if self.has_body and self.create_returns_body is False:
            # fetch the body if it's required but not returned by create
            fetch_kwargs = {}
            if resource_response_key is not None:
                fetch_kwargs = {'resource_response_key': resource_response_key}
            return self.fetch(session, **fetch_kwargs)
        return self


class NotBoundApi(resource.Resource):
    base_path = (f'/apigw/instances/%(gateway_id)s/'
                 f'throttle-bindings/unbinded-apis')

    allow_list = True

    resources_key = 'apis'

    _query_mapping = resource.QueryParameters(
        'limit', 'offset', 'throttle_id',
        'env_id', 'api_id', 'api_name', 'group_id'
    )

    # Properties
    gateway_id = resource.URI('gateway_id')

    # Attributes
    # API authentication mode.
    auth_type = resource.Body('auth_type', type=str)
    # Name of the environment in which the API has been published.
    run_env_name = resource.Body('run_env_name', type=str)
    # ID of a request throttling policy binding record.
    throttle_apply_id = resource.Body('throttle_apply_id', type=str)
    # Binding time.
    applied_at = resource.Body('apply_time', type=str)
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
    # Name of the request throttling policy bound to the API.
    throttle_name = resource.Body('throttle_name', type=str)
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


class BoundThrottles(resource.Resource):
    base_path = (f'/apigw/instances/%(gateway_id)s/'
                 f'throttle-bindings/binded-throttles')

    allow_list = True

    resources_key = 'throttles'

    _query_mapping = resource.QueryParameters(
        'limit', 'offset', 'api_id',
        'throttle_id', 'throttle_name', 'env_id'
    )

    # Properties
    gateway_id = resource.URI('gateway_id')

    # Attributes
    # Maximum number of times the API can be accessed by an
    # app within the same period.
    app_call_limits = resource.Body('app_call_limits', type=int)
    # Request throttling policy name.
    name = resource.Body('name', type=str)
    # Time unit for limiting the number of API calls.
    # Enumeration values:
    # SECOND
    # MINUTE
    # HOUR
    # DAY
    time_unit = resource.Body('time_unit', type=str)
    # Description of the request throttling policy,
    # which can contain a maximum of 255 characters.
    remark = resource.Body('remark', type=str)
    # Maximum number of times an API can be accessed within a specified period.
    api_call_limits = resource.Body('api_call_limits', type=int)
    # Type of the request throttling policy.
    # 1: API-based, limiting the maximum number of times a single
    # API bound to the policy can be called within the specified period.
    # 2: API-shared, limiting the maximum number of times all
    # APIs bound to the policy can be called within the specified period.
    type = resource.Body('type', type=int)
    # Indicates whether to enable dynamic request throttling.
    enable_adaptive_control = resource.Body(
        'enable_adaptive_control', type=str
    )
    # Maximum number of times the API can be accessed
    # by a user within the same period.
    user_call_limits = resource.Body('user_call_limits', type=int)
    # Period of time for limiting the number of API calls.
    time_interval = resource.Body('time_interval', type=int)
    # Maximum number of times the API can be accessed
    # by an IP address within the same period.
    ip_call_limits = resource.Body('ip_call_limits', type=int)
    # Number of APIs to which the request throttling policy has been bound.
    bind_num = resource.Body('bind_num', type=int)
    # Indicates whether an excluded request throttling
    # configuration has been created.
    # 1: yes
    # 2: no
    is_inclu_special_throttle = resource.Body(
        'is_inclu_special_throttle', type=int
    )
    # Creation time.
    created_at = resource.Body('create_time', type=str)
    # Environment in which the request throttling policy takes effect.
    env_name = resource.Body('env_name', type=str)
    # Policy binding record ID.
    bind_id = resource.Body('bind_id', type=str)
    # Time when the policy is bound to the API.
    bound_at = resource.Body('bind_time', type=str)
