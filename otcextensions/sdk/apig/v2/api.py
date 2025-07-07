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


class Vpc(resource.Resource):
    # Proxy host.
    vpc_channel_proxy_host = resource.Body('vpc_channel_proxy_host', type=str)
    # VPC channel ID.
    vpc_channel_id = resource.Body('vpc_channel_id', type=str)

    # Attributes
    # Cloud server ID.
    ecs_id = resource.Body('ecs_id', type=str)
    # Cloud server name.
    ecs_name = resource.Body('ecs_name', type=str)
    # Indicates whether to use the cascading mode.
    cascade_flag = resource.Body('cascade_flag', type=bool)
    # VPC channel port.
    vpc_channel_port = resource.Body('vpc_channel_port', type=int)


class BackendParam(resource.Resource):
    # Parameter type.
    # REQUEST: backend parameter
    # CONSTANT: constant parameter
    # SYSTEM: system parameter
    origin = resource.Body('origin', type=str)
    # Parameter name.
    name = resource.Body('name', type=str)
    # Description, which can contain a maximum of 255 characters.
    remark = resource.Body('remark', type=str)
    # Parameter location. The value can be PATH, QUERY, or HEADER.
    location = resource.Body('location', type=str)
    # Parameter value, which can contain a maximum of 255 characters.
    # The gateway parameters are as follows:
    # $context.sourceIp: source IP address of the API caller.
    # $context.stage: deployment environment in which the API is called.
    # $context.apiId: API ID.
    # $context.appId: ID of the app used by the API caller.
    # $context.requestId: request ID generated when the API is called.
    # $context.serverAddr: address of the gateway server.
    # $context.serverName: name of the gateway server.
    # $context.handleTime: time when the API request is processed.

    # $context.providerAppId: ID of the app used by the API owner.
    # This parameter is currently not supported.

    # Frontend authentication parameter:
    # prefixed with "$context.authorizer.frontend.".
    # For example, to return "aaa" upon successful custom authentication,
    # set this parameter to "$context.authorizer.frontend.aaa".
    #
    # Backend authentication parameter:
    # prefixed with "$context.authorizer.backend.".
    # For example, to return "aaa" upon successful custom authentication,
    # set this parameter to "$context.authorizer.backend.aaa".
    value = resource.Body('value', type=str)

    # Attributes
    # ID
    id = resource.Body('id', type=str)
    # Request parameter ID.
    req_param_id = resource.Body('req_param_id', type=str)


class ApiMock(resource.Resource):
    # Description. It cannot exceed 255 characters.
    remark = resource.Body('remark', type=str)
    # Response
    result_content = resource.Body('result_content', type=str)
    # Function version. It cannot exceed 64 characters.
    version = resource.Body('version', type=str)
    # Backend custom authorizer ID.
    authorizer_id = resource.Body('authorizer_id', type=str)

    # Attributes
    # ID
    id = resource.Body('id', type=str)
    # Backend service status.
    status = resource.Body('status', type=int)
    # Registration time.
    register_time = resource.Body('register_time', type=str)
    # Update time.
    update_time = resource.Body('update_time', type=str)


class ApiFunc(resource.Resource):
    # Function URN.
    function_urn = resource.Body('function_urn', type=str)
    # Description. It cannot exceed 255 characters.
    remark = resource.Body('remark', type=str)
    # Invocation mode.
    # async: asynchronous
    # sync: synchronous
    invocation_type = resource.Body('invocation_type', type=str)
    # Function network architecture.
    # V1: non-VPC
    # V2: VPC
    network_type = resource.Body('network_type', type=str)
    # Function version.
    # If both a function alias URN and version are passed,
    # only the alias URN will be used.
    version = resource.Body('version', type=str)
    # Function alias URN.
    alias_urn = resource.Body('alias_urn', type=str)
    # Timeout allowed for APIG to request the backend service.
    timeout = resource.Body('timeout', type=int)
    # Backend custom authorizer ID.
    authorizer_id = resource.Body('authorizer_id', type=str)
    # Backend request protocol of a function.
    # The value can be HTTPS (default) or
    # GRPCS (available when the frontend request protocol is GRPCS).
    # Default: HTTPS
    req_protocol = resource.Body('req_protocol', type=str)

    # Attributes
    # ID
    id = resource.Body('id', type=str)
    # Registration time.
    register_time = resource.Body('register_time', type=str)
    # status
    status = resource.Body('status', type=int)
    # Update time.
    update_time = resource.Body('update_time', type=str)


class ReqParam(resource.Resource):
    # Parameter name.
    name = resource.Body('name', type=str)
    # Parameter type.
    # Enumeration values:
    # STRING
    # NUMBER
    type = resource.Body('type', type=str)
    # Parameter location.
    # Enumeration values:
    # PATH
    # QUERY
    # HEADER
    location = resource.Body('location', type=str)
    # Default value.
    default_value = resource.Body('default_value', type=str)
    # Example value.
    sample_value = resource.Body('sample_value', type=str)
    # Indicates whether the parameter is required. 1: yes 2: no
    required = resource.Body('required', type=int)
    # Indicates whether validity check is enabled.
    # 1: enabled
    # 2: disabled
    valid_enable = resource.Body('valid_enable', type=int)
    # Description. It cannot exceed 255 characters.
    remark = resource.Body('remark', type=str)
    # Enumerated value.
    enumerations = resource.Body('enumerations', type=str)
    # Minimum value.
    min_num = resource.Body('min_num', type=int)
    # Maximum value.
    max_num = resource.Body('max_num', type=int)
    # Minimum length.
    min_size = resource.Body('min_size', type=int)
    # Maximum length.
    max_size = resource.Body('max_size', type=int)
    # Regular expression validation rule.
    regular = resource.Body('regular', type=str)
    # JSON validation rule.
    json_schema = resource.Body('json_schema', type=str)
    # Indicates whether to transparently transfer the parameter. 1: yes 2: no
    pass_through = resource.Body('pass_through', type=int)

    # Attributes
    # ID
    id = resource.Body('id', type=str)


class AuthOpt(resource.Resource):
    # Indicates whether AppCode authentication is enabled.
    # This parameter is valid only if auth_type is set to App.
    # The default value is DISABLE.
    # DISABLE: AppCode authentication is disabled.
    # HEADER: AppCode authentication is enabled and the AppCode
    # is located in the header.
    # Default: DISABLE
    app_code_auth_type = resource.Body('app_code_auth_type', type=str)


class ApiCondition(resource.Resource):
    # Input parameter name.
    # This parameter is required if the policy type is param.
    req_param_name = resource.Body('req_param_name', type=str)
    # Name of a built-in gateway parameter.
    # This parameter is required if the policy type is system.
    # The following parameters are supported:
    # req_path: request path. For example, /a/b.
    # req_method: request method. For example, GET.
    # reqPath: request path, which is discarded. For example, /a/b.
    # reqMethod: request method, which is discarded. For example, GET.
    sys_param_name = resource.Body('sys_param_name', type=str)
    # COOKIE parameter name.
    # This parameter is required if the policy type is cookie.
    cookie_param_name = resource.Body('cookie_param_name', type=str)
    # System parameter: frontend authentication parameter name.
    frontend_authorizer_param_name = resource.Body(
        'frontend_authorizer_param_name', type=str
    )
    # Policy condition.
    # exact: Exact match
    # enum: Enumeration
    # pattern: Regular expression
    condition_type = resource.Body('condition_type', type=str)
    # Policy type
    # param: parameter
    # source: source IP address
    # system: system parameter - gateway built-in parameter
    # cookie: COOKIE parameter
    # frontend_authorizer: system parameter - frontend authentication parameter
    condition_origin = resource.Body('condition_origin', type=str)
    # Policy value.
    # This parameter is required when the policy type is param,
    # source, cookie, or frontend_authorizer.
    condition_value = resource.Body('condition_value', type=str)

    # Attributes
    # ID.
    id = resource.Body('id', type=str)
    # Input parameter ID.
    req_param_id = resource.Body('req_param_id', type=str)
    # Input parameter location.
    req_param_location = resource.Body('req_param_location', type=str)


class ApiPolicyMock(resource.Resource):
    # Response.
    result_content = resource.Body('result_content', type=str)
    # Effective mode of the backend policy.
    # ALL: All conditions are met.
    # ANY: Any condition is met.
    effect_mode = resource.Body('effect_mode', type=str)
    # Backend name.
    # It must start with a letter and can contain letters,
    # digits, and underscores (_).
    name = resource.Body('name', type=str)
    # Backend parameters. This is unavailable for the GRPC backend.
    backend_params = resource.Body(
        'backend_params', type=list, list_type=BackendParam
    )
    # Policy conditions.
    conditions = resource.Body(
        'conditions', type=list, list_type=ApiCondition
    )
    # Custom authorizer ID.
    # This is unavailable if the request protocol is set to GRPC.
    authorizer_id = resource.Body('authorizer_id', type=str)

    # Attributes
    # ID.
    id = resource.Body('id', type=str)


class ApiPolicyFunction(resource.Resource):
    # Function URN.
    function_urn = resource.Body('function_urn', type=str)
    # Invocation mode.
    # async: asynchronous
    # sync: synchronous
    invocation_type = resource.Body('invocation_type', type=str)
    # Function network architecture.
    # V1: non-VPC
    # V2: VPC
    network_type = resource.Body('network_type', type=str)
    # Function version.
    version = resource.Body('version', type=str)
    # Function alias URN.
    alias_urn = resource.Body('alias_urn', type=str)
    # Timeout allowed for APIG to request the backend service.
    timeout = resource.Body('timeout', type=int)
    # Backend request protocol of a function.
    # The value can be HTTPS (default) or
    # GRPCS (available when the frontend request protocol is GRPCS).
    req_protocol = resource.Body('req_protocol', type=str)
    # Effective mode of the backend policy.
    # ALL: All conditions are met.
    # ANY: Any condition is met.
    effect_mode = resource.Body('effect_mode', type=str)
    # Backend name.
    # It must start with a letter and can contain letters,
    # digits, and underscores (_).
    name = resource.Body('name', type=str)
    # Backend parameters. This is unavailable for the GRPC backend.
    backend_params = resource.Body(
        'backend_params', type=list, list_type=BackendParam
    )
    # Policy conditions.
    conditions = resource.Body(
        'conditions', type=list, list_type=ApiCondition
    )
    # Custom authorizer ID.
    # This is unavailable if the request protocol is set to GRPC.
    authorizer_id = resource.Body('authorizer_id', type=str)


class BackendApi(resource.Resource):
    # Custom authorizer ID.
    # This is unavailable if the request protocol is set to GRPC.
    authorizer_id = resource.Body('authorizer_id', type=str)
    # Backend service address.
    # It must be in the format "Host name:Port number",
    # for example, apig.example.com:7443
    url_domain = resource.Body('url_domain', type=str)
    # Request protocol. You can select GRPCS for the GRPC backend.
    req_protocol = resource.Body('req_protocol', type=str)
    # Description. It cannot exceed 255 characters.
    remark = resource.Body('remark', type=str)
    # Request method. For the GRPC backend,
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
    # Web backend version, which can contain a maximum of 16 characters.
    version = resource.Body('version', type=str)
    # Request address, which can contain request parameters
    # enclosed with braces ({})
    req_uri = resource.Body('req_uri', type=str)
    # Timeout allowed for APIG to request the backend service.
    timeout = resource.Body('timeout', type=int)
    # Indicates whether to enable two-way authentication.
    enable_client_ssl = resource.Body('enable_client_ssl', type=bool)
    # Number of retry attempts to request the backend service.
    # The default value is -1. The value ranges from -1 to 10.
    retry_count = resource.Body('retry_count', type=str)
    # VPC channel details.
    # This parameter is required if vpc_channel_status is set to 1.
    vpc_channel_info = resource.Body('vpc_channel_info', type=Vpc)
    # Indicates whether to use a VPC channel.
    # 1: A VPC channel is used.
    # 2: No VPC channel is used.
    vpc_channel_status = resource.Body('vpc_channel_status', type=int)

    # Attributes
    # ID.
    id = resource.Body('id', type=str)
    # Backend service status.
    status = resource.Body('status', type=int)
    # Registration time.
    register_time = resource.Body('register_time', type=str)
    # Update time.
    update_time = resource.Body('update_time', type=str)


class ApiPolicyHttp(resource.Resource):
    # Endpoint of the policy backend.
    # It must be in the format "Domain name:Port number",
    # for example, apig.example.com:7443.
    # If the port number is not specified,
    # the default HTTPS port 443 or the default HTTP port 80 is used.
    url_domain = resource.Body('url_domain', type=str)
    # Request protocol. Options include HTTP, HTTPS, and GRPCS.
    # You can select GRPCS for a GRPC backend.
    req_protocol = resource.Body('req_protocol', type=str)
    # Request method. Options include GET, POST, PUT, DELETE,
    # HEAD, PATCH, OPTIONS, and ANY.
    # This is fixed to POST for the GRPC backend.
    req_method = resource.Body('req_method', type=str)
    # Request address, which can contain request
    # parameters enclosed with braces ({}).
    req_uri = resource.Body('req_uri', type=str)
    # Timeout allowed for APIG to request the backend service.
    timeout = resource.Body('timeout', type=int)
    # Number of retry attempts to request the backend service.
    # The default value is -1. The value ranges from -1 to 10.
    retry_count = resource.Body('retry_count', type=str)
    # Effective mode of the backend policy.
    # ALL: All conditions are met.
    # ANY: Any condition is met.
    effect_mode = resource.Body('effect_mode', type=str)
    # Backend name. It must start with a letter and can contain letters,
    # digits, and underscores (_).
    name = resource.Body('name', type=str)
    # Backend parameters. This is unavailable for the GRPC backend.
    backend_params = resource.Body(
        'backend_params', type=list, list_type=BackendParam
    )
    # Policy conditions.
    conditions = resource.Body(
        'conditions', type=list, list_type=ApiCondition
    )
    # Custom authorizer ID.
    # This is unavailable if the request protocol is set to GRPC.
    authorizer_id = resource.Body('authorizer_id', type=str)
    # VPC channel details.
    # This parameter is required if vpc_channel_status is set to 1.
    vpc_channel_info = resource.Body('vpc_channel_info', type=Vpc)
    # Indicates whether to use a VPC channel.
    # 1: A VPC channel is used.
    # 2: No VPC channel is used.
    vpc_channel_status = resource.Body('vpc_channel_status', type=int)

    # Attributes
    # ID.
    id = resource.Body('id', type=str)


class UrlDomain(resource.Resource):
    # Domain ID.
    id = resource.Body('id', type=str)
    # Domain name.
    name = resource.Body('domain', type=str)
    # CNAME resolution status of the domain name.
    # 1: not resolved
    # 2: resolving
    # 3: resolved
    # 4: resolution failed
    cname_status = resource.Body('cname_status', type=int)
    # SSL certificate ID.
    ssl_id = resource.Body('ssl_id', type=str)
    # SSL certificate name.
    ssl_name = resource.Body('ssl_name', type=str)
    # Minimum SSL version. TLS 1.1 and TLS 1.2 are supported.
    min_ssl_version = resource.Body('min_ssl_version', type=str)
    # Whether to enable client certificate verification.
    # This parameter is available only when a certificate is bound
    verified_client_certificate_enabled = resource.Body(
        'verified_client_certificate_enabled', type=bool
    )
    # Independent domain names bound to the API group.
    is_has_trusted_root_ca = resource.Body('is_has_trusted_root_ca', type=bool)


class ApiGroupCommonInfo(resource.Resource):
    # ID.
    id = resource.Body('id', type=str)
    # API group name.
    name = resource.Body('name', type=str)
    # Status. 1: valid
    status = resource.Body('status', type=int)
    # Subdomain name that APIG automatically allocates to the API group.
    sl_domain = resource.Body('sl_domain', type=str)
    # Creation time.
    register_time = resource.Body('register_time', type=str)
    # Last modification time.
    update_time = resource.Body('update_time', type=str)
    # Indicates whether the API group has been listed on KooGallery.
    # 1: listed
    # 2: not listed
    # 3: under review
    on_sell_status = resource.Body('on_sell_status', type=int)
    # Independent domain names bound to the API group.
    url_domains = resource.Body('url_domains', type=list, list_type=UrlDomain)
    sl_domain_access_enabled = resource.Body(
        'sl_domain_access_enabled', type=bool
    )


class Api(resource.Resource):
    base_path = f'/apigw/instances/%(gateway_id)s/apis'

    allow_list = True
    allow_create = True
    allow_commit = True
    allow_delete = True
    allow_fetch = True

    resources_key = 'apis'

    _query_mapping = resource.QueryParameters(
        'limit', 'offset', 'name',
        'id', 'group_id', 'req_protocol', 'req_method',
        'req_uri', 'auth_type', 'env_id', 'type', 'precise_search',
        'vpc_channel_name', 'return_data_mode'
    )

    # Properties
    gateway_id = resource.URI('gateway_id', type=str)
    # API name.
    name = resource.Body('name', type=str)
    # API type.
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
    req_protocol = resource.Body('req_protocol', type=str)
    # API request method. If the request protocol is set to GRPC,
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
    # Request address, which can contain request
    # parameters enclosed with braces ({})
    req_uri = resource.Body('req_uri', type=str)
    # API authentication mode. Options:
    # NONE
    # APP
    # IAM
    # AUTHORIZER: custom authentication.
    # When auth_type is set to AUTHORIZER,
    # the authorizer_id field is mandatory.
    auth_type = resource.Body('auth_type', type=str)
    # Security authentication parameter.
    auth_opt = resource.Body('auth_opt', type=AuthOpt)
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
    # API request body, which can be an example request body,
    # media type, or parameters.
    # Ensure that the request body does not exceed 20,480 characters.
    body_remark = resource.Body('body_remark', type=str)
    # Example response for a successful request.
    # Ensure that the response does not exceed 20,480 characters.
    # This is unavailable if the request protocol is set to GRPC.
    result_normal_sample = resource.Body('result_normal_sample', type=str)
    # Example response for a failed request.
    # Ensure that the response does not exceed 20,480 characters.
    # This is unavailable if the request protocol is set to GRPC.
    result_failure_sample = resource.Body('result_failure_sample', type=str)
    # Custom authorizer ID.
    # This is unavailable if the request protocol is set to GRPC.
    authorizer_id = resource.Body('authorizer_id', type=str)
    # Tag.
    # Use letters, digits, and special characters (-*#%.:_)
    # and start with a letter.
    tags = resource.Body('tags', type=list)
    # Group response ID.
    response_id = resource.Body('response_id', type=str)
    # Request content type:
    # application/json
    # application/xml
    # multipart/form-data
    # text/plain
    content_type = resource.Body('content_type', type=str)
    # Mock backend details.
    mock_info = resource.Body('mock_info', type=ApiMock)
    # FunctionGraph backend details.
    func_info = resource.Body('func_info', type=ApiFunc)
    # Request parameters.
    # This is unavailable if the request protocol is set to GRPC.
    req_params = resource.Body(
        'req_params', type=list, list_type=ReqParam
    )
    # Backend parameters.
    # This is unavailable if the request protocol is set to GRPC.
    backend_params = resource.Body(
        'backend_params', type=list, list_type=BackendParam
    )
    # Mock backend policies.
    policy_mocks = resource.Body(
        'policy_mocks', type=list, list_type=ApiPolicyMock
    )
    # FunctionGraph backend policies.
    policy_functions = resource.Body(
        'policy_functions', type=list, list_type=ApiPolicyFunction
    )
    # Web backend details.
    backend_api = resource.Body('backend_api', type=BackendApi)
    # Web backend policies.
    policy_https = resource.Body(
        'policy_https', type=list, list_type=ApiPolicyHttp
    )

    # Attributes
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
    # Publication time.
    publish_time = resource.Body('publish_time', type=str)
    # API group information.
    api_group_info = resource.Body('api_group_info', type=ApiGroupCommonInfo)
