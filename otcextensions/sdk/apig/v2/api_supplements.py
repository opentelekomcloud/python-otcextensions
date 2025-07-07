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
from otcextensions.sdk.apig.v2.api import ApiFunc
from otcextensions.sdk.apig.v2.api import ApiMock
from otcextensions.sdk.apig.v2.api import ApiGroupCommonInfo
from otcextensions.sdk.apig.v2.api import BackendApi
from otcextensions.sdk.apig.v2.api import ReqParam
from otcextensions.sdk.apig.v2.api import BackendParam
from otcextensions.sdk.apig.v2.api import ApiPolicyMock
from otcextensions.sdk.apig.v2.api import ApiPolicyFunction
from otcextensions.sdk.apig.v2.api import ApiPolicyHttp


class PublishApi(resource.Resource):
    base_path = f'/apigw/instances/%(gateway_id)s/apis/action'

    allow_create = True

    # Properties
    gateway_id = resource.URI('gateway_id')
    # Operation to perform.
    # online: publish APIs
    # offline: take APIs offline
    action = resource.Body('action', type=int)
    # ID of the environment in which the API will be published.
    env_id = resource.Body('env_id', type=str)
    # ID of the API to be published or taken offline.
    api_id = resource.Body('api_id', type=str)
    # Description about the publishing. It cannot exceed 255 characters.
    remark = resource.Body('remark', type=str)

    # Attributes
    # Publication record ID.
    publish_id = resource.Body('publish_id', type=str)
    # API name.
    api_name = resource.Body('api_name', type=str)
    # Publication time.
    publish_time = resource.Body('publish_time', type=str)
    # API version currently in use.
    version_id = resource.Body('version_id', type=str)

    def _action(self, session, body):
        """Preform actions given the message body.
        """
        url = self.base_path % {'gateway_id': body['gateway_id']}
        response = session.post(url, json=body)
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self

    def publish_api(self, session, **attrs):
        attrs['action'] = "online"
        return self._action(session, attrs)

    def take_api_offline(self, session, **attrs):
        attrs['action'] = "offline"
        return self._action(session, attrs)


class CheckApi(resource.Resource):
    base_path = f'/apigw/instances/%(gateway_id)s/apis/check'

    allow_create = True

    # Properties
    gateway_id = resource.URI('gateway_id')
    # API name.
    name = resource.Body('name')
    # Request method.
    # GET
    # POST
    # PUT
    # DELETE
    # HEAD
    # PATCH
    # OPTIONS
    # ANY
    req_method = resource.Body('req_method')
    # Access address of the API.
    req_uri = resource.Body('req_uri')
    # API matching mode:
    # SWA: Prefix match
    # NORMAL: Exact match
    match_mode = resource.Body('match_mode')
    # Group ID.
    group_id = resource.Body('group_id')
    # Integration application ID.
    roma_app_id = resource.Body('roma_app_id')
    # ID of the API to be compared.
    api_id = resource.Body('api_id')
    # Verification type:
    # path: path type
    # name: name type
    type = resource.Body('type')


class DebugApi(resource.Resource):
    base_path = f'/apigw/instances/%(gateway_id)s/apis/debug/%(api_id)s'

    allow_create = True

    # Properties
    gateway_id = resource.URI('gateway_id')
    api_id = resource.URI('api_id')
    # Message body, with a maximum of 2,097,152 bytes.
    body = resource.Body('body')
    # Header parameters, with each value being a character string array.
    header = resource.Body('header', type=dict)
    # API request method.
    # Enumeration values:
    # GET
    # POST
    # PUT
    # DELETE
    # HEAD
    # PATCH
    # OPTIONS
    method = resource.Body('method', type=str)
    # Debugging mode:
    # DEVELOPER: Debug the definitions of an API that has not been published.
    # CONSUMER: Debug the definitions of an API that has been
    # published in a specified environment.
    mode = resource.Body('mode', type=str)
    # Request path of the API, starting with a slash (/)
    # and containing up to 1024 characters.
    path = resource.Body('path', type=str)
    # Query strings, with each value being a character string array.
    query = resource.Body('query', type=dict)
    # Request protocol.
    # HTTP
    # HTTPS
    scheme = resource.Body('scheme', type=str)
    # AppKey used in the debugging request.
    app_key = resource.Body('app_key', type=str)
    # AppSecret used in the debugging request.
    app_secret = resource.Body('app_secret', type=str)
    # Access domain name of the API.
    # If no value is specified, one of the following default
    # values will be used based on the mode:
    # DEVELOPER: The subdomain name of the API group will be used.
    # MARKET: This parameter is not used currently.
    # CONSUMER: The subdomain name of the API group will be used.
    domain = resource.Body('domain', type=str)
    # Running environment specified by the debugging request.
    # This parameter is valid only when mode is set to CONSUMER.
    # If this parameter is not specified, the following default value is used:
    # CONSUMER RELEASE
    stage = resource.Body('stage', type=str)

    # Attributes
    # Body of the debugging request.
    request = resource.Body('request', type=str)
    # Body of the debugging response, with a maximum of 2,097,152 bytes.
    # Any content beyond this threshold will be truncated.
    response = resource.Body('response', type=str)
    # Debugging duration in milliseconds.
    latency = resource.Body('latency', type=int)
    # Debugging logs.
    log = resource.Body('log', type=str)


class PublishApis(resource.Resource):
    base_path = f'/apigw/instances/%(gateway_id)s/apis/publish'

    resources_key = 'api_versions'

    allow_create = True
    allow_list = True
    allow_commit = True

    _query_mapping = resource.QueryParameters(
        "limit", "offset", "env_id", "env_name"
    )

    # Properties
    gateway_id = resource.URI('gateway_id')
    # API ID.
    api_id = resource.URI('api_id', type=str)
    # Operation to perform.
    # online: publish APIs
    # offline: take APIs offline
    action = resource.Body('action', type=int)
    # ID of the environment in which the API will be published.
    env_id = resource.Body('env_id', type=str)
    # ID of the API to be published or taken offline.
    apis = resource.Body('apis', type=list)
    # API group ID. Either apis or group_id must be specified.
    group_id = resource.Body('group_id', type=str)
    # Description about the publishing. It cannot exceed 255 characters.
    remark = resource.Body('remark', type=str)

    # Attributes
    # Message for successful API publication or taking offline.
    success = resource.Body('success', type=list)
    # Error message and APIs that fail to be published or taken offline.
    failure = resource.Body('failure', type=list)
    # API version ID.
    version_id = resource.Body('version_id', type=str)
    # API version.
    version_no = resource.Body('version_no', type=str)
    # Name of the environment in which the API has been published.
    env_name = resource.Body('env_name', type=str)
    # Publication time.
    publish_time = resource.Body('publish_time', type=str)
    # Version status.
    # 1: effective
    # 2: not effective
    status = resource.Body('status', type=str)

    def _action(self, session, body, action):
        """Preform actions given the message body.
        """
        url = self.base_path % {'gateway_id': body["gateway_id"]}
        url += f'?action={action}'
        response = session.post(url, json=body)
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self

    def publish_apis(self, session, **attrs):
        return self._action(session, attrs, "online")

    def take_apis_offline(self, session, **attrs):
        return self._action(session, attrs, "offline")


class RuntimeDefinitionApi(resource.Resource):
    base_path = f'/apigw/instances/%(gateway_id)s/apis/runtime/%(api_id)s'

    allow_list = True

    _query_mapping = resource.QueryParameters(
        "env_id",
    )

    # Properties
    gateway_id = resource.URI('gateway_id')
    api_id = resource.URI('api_id')

    # Attributes
    # API name.
    name = resource.Body('name')
    # Verification type:
    # 1: public API
    # 2: private API
    type = resource.Body('type', type=int)
    # API version.
    version = resource.Body('version', type=str)
    # API request protocol:
    # HTTP
    # HTTPS
    # BOTH: Both HTTP and HTTPS are supported.
    # GRPCS
    # Default: HTTPS
    req_protocol = resource.Body('req_protocol', type=str)
    # API request method. If the request protocol is set to GRPC
    # the request method is fixed to POST.
    # Enumeration values:
    # GET
    # POST
    # PUT
    # DELETE
    # HEAD
    # PATCH
    # OPTIONS
    # ANY
    req_method = resource.Body('req_method', type=str)
    # Request address, which can contain request parameters enclosed
    # with braces ({}).
    # For example, /getUserInfo/{userId}
    req_uri = resource.Body('req_uri', type=str)
    # API authentication mode. Options:
    # NONE
    # APP
    # IAM
    # AUTHORIZER: custom authentication. When auth_type is set to AUTHORIZER,
    # the authorizer_id field is mandatory.
    auth_type = resource.Body('auth_type', type=str)
    # Security authentication parameter.
    auth_opt = resource.Body('auth_opt', type=dict)
    # Indicates whether CORS is supported.
    # TRUE: supported
    # FALSE: not supported
    cors = resource.Body('cors', type=bool)
    # API matching mode:
    # SWA: Prefix match
    # NORMAL: Exact match Default value: NORMAL
    match_mode = resource.Body('match_mode', type=str)
    # Backend type. Options:
    # HTTP: web backend
    # FUNCTION: FunctionGraph backend. When backend_type is set to FUNCTION,
    # the func_info field is mandatory.
    # MOCK: mock backend. When backend_type is set to MOCK,
    # the mock_info field is mandatory.
    # GRPC: gRPC backend.
    backend_type = resource.Body('backend_type', type=str)
    # API description. It cannot exceed 255 characters.
    remark = resource.Body('remark', type=str)
    # ID of the API group to which the API belongs.
    group_id = resource.Body('group_id', type=str)
    # API request body
    body_remark = resource.Body('body_remark', type=str)
    # Example response for a successful request.
    # Ensure that the response does not exceed 20,480 characters.
    result_normal_sample = resource.Body('result_normal_sample', type=str)
    # Example response for a failed request.
    # Ensure that the response does not exceed 20,480 characters.
    result_failure_sample = resource.Body('result_failure_sample', type=str)
    # Custom authorizer ID.
    # This is unavailable if the request protocol is set to GRPC.
    authorizer_id = resource.Body('authorizer_id', type=str)
    # Tags.
    # Use letters, digits, and special characters (-*#%.:_)
    # and start with a letter.
    tags = resource.Body('tags', type=list)
    # Request content type:
    # application/json
    # application/xml
    # multipart/form-data
    # text/plain
    content_type = resource.Body('content_type', type=str)
    # Name of the API group to which the API belongs.
    group_name = resource.Body('group_name', type=str)
    # Name of the environment in which the API has been published.
    run_env_name = resource.Body('run_env_name', type=str)
    # ID of the environment in which the API has been published.
    run_env_id = resource.Body('run_env_id', type=str)
    # Publication record ID.
    publish_id = resource.Body('publish_id', type=str)
    # Subdomain name of the API group.
    sl_domain = resource.Body('sl_domain', type=str)
    # Subdomain names that APIG automatically allocates to the API group.
    sl_domains = resource.Body('sl_domains', type=list)
    # Request parameters.
    req_params = resource.Body('req_params', type=list)


class VersionsApi(resource.Resource):
    base_path = f'/apigw/instances/%(gateway_id)s/apis/versions/%(version_id)s'

    allow_list = True
    allow_delete = True

    requires_id = False

    _query_mapping = resource.QueryParameters(
        "env_id",
    )

    # Properties
    gateway_id = resource.URI('gateway_id')
    version_id = resource.URI('version_id')

    # Attributes
    # API name.
    name = resource.Body('name')
    # Verification type:
    # 1: public API
    # 2: private API
    type = resource.Body('type', type=int)
    # API version.
    version = resource.Body('version', type=str)
    # API request protocol:
    # HTTP
    # HTTPS
    # BOTH: Both HTTP and HTTPS are supported.
    # GRPCS
    # Default: HTTPS
    req_protocol = resource.Body('req_protocol', type=str)
    # API request method. If the request protocol is set to GRPC
    # the request method is fixed to POST.
    # Enumeration values:
    # GET
    # POST
    # PUT
    # DELETE
    # HEAD
    # PATCH
    # OPTIONS
    # ANY
    req_method = resource.Body('req_method', type=str)
    # Request address, which can contain request parameters
    # enclosed with braces ({}).
    # For example, /getUserInfo/{userId}
    req_uri = resource.Body('req_uri', type=str)
    # API authentication mode. Options:
    # NONE
    # APP
    # IAM
    # AUTHORIZER: custom authentication. When auth_type is set to AUTHORIZER,
    # the authorizer_id field is mandatory.
    auth_type = resource.Body('auth_type', type=str)
    # Security authentication parameter.
    auth_opt = resource.Body('auth_opt', type=dict)
    # Indicates whether CORS is supported.
    # TRUE: supported
    # FALSE: not supported
    cors = resource.Body('cors', type=bool)
    # API matching mode:
    # SWA: Prefix match
    # NORMAL: Exact match Default value: NORMAL
    match_mode = resource.Body('match_mode', type=str)
    # Backend type. Options:
    # HTTP: web backend
    # FUNCTION: FunctionGraph backend. When backend_type is set to FUNCTION,
    # the func_info field is mandatory.
    # MOCK: mock backend. When backend_type is set to MOCK,
    # the mock_info field is mandatory.
    # GRPC: gRPC backend.
    backend_type = resource.Body('backend_type', type=str)
    # API description. It cannot exceed 255 characters.
    remark = resource.Body('remark', type=str)
    # ID of the API group to which the API belongs.
    group_id = resource.Body('group_id', type=str)
    # API request body
    body_remark = resource.Body('body_remark', type=str)
    # Example response for a successful request.
    # Ensure that the response does not exceed 20,480 characters.
    result_normal_sample = resource.Body('result_normal_sample', type=str)
    # Example response for a failed request.
    # Ensure that the response does not exceed 20,480 characters.
    result_failure_sample = resource.Body('result_failure_sample', type=str)
    # Custom authorizer ID.
    # This is unavailable if the request protocol is set to GRPC.
    authorizer_id = resource.Body('authorizer_id', type=str)
    # Tags.
    # Use letters, digits, and special characters (-*#%.:_)
    # and start with a letter.
    tags = resource.Body('tags', type=list)
    # App status.
    status = resource.Body('status', type=int)
    # Indicates whether to enable orchestration.
    arrange_necessary = resource.Body('arrange_necessary', type=int)
    # Time when the API is registered.
    register_time = resource.Body('register_time', type=str)
    # Time when the API was last modified.
    update_time = resource.Body('update_time', type=str)
    # Name of the API group to which the API belongs.
    group_name = resource.Body('group_name', type=str)
    # Version of the API group to which the API belongs.
    group_version = resource.Body('group_version', type=str)
    # ID of the environment in which the API has been published.
    run_env_id = resource.Body('run_env_id', type=str)
    # Name of the environment in which the API has been published.
    run_env_name = resource.Body('run_env_name', type=str)
    # Publication record ID.
    publish_id = resource.Body('publish_id', type=str)
    # Time when the API version is published.
    publish_time = resource.Body('publish_time', type=str)
    # Web backend details.
    backend_api = resource.Body('backend_api', type=BackendApi)
    # API group information.
    api_group_info = resource.Body('api_group_info', type=ApiGroupCommonInfo)
    # FunctionGraph backend details.
    func_info = resource.Body('func_info', type=ApiFunc)
    # Mock backend details.
    mock_info = resource.Body('mock_info', type=ApiMock)
    # Request parameters.
    req_params = resource.Body('req_params', type=list, list_type=ReqParam)
    # Backend parameters.
    backend_params = resource.Body(
        'backend_params', type=list, list_type=BackendParam
    )
    # FunctionGraph backend policies.
    policy_functions = resource.Body(
        'policy_functions', type=list, list_type=ApiPolicyFunction
    )
    # Mock backend policies.
    policy_mocks = resource.Body(
        'policy_mocks', type=list, list_type=ApiPolicyMock
    )
    # Web backend policies.
    policy_https = resource.Body(
        'policy_https', type=list, list_type=ApiPolicyHttp
    )
    # Subdomain name that API Gateway automatically allocates to the API group.
    sl_domain = resource.Body('sl_domain', type=str)
    # Subdomain names that APIG automatically allocates to the API group.
    sl_domains = resource.Body('sl_domains', type=list)
