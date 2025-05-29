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


class MicroserviceLabelSpec(resource.Resource):
    label_name = resource.Body("label_name")
    label_value = resource.Body("label_value")


class MemberGroupCreateSpec(resource.Resource):
    member_group_name = resource.Body("member_group_name")
    member_group_remark = resource.Body("member_group_remark")
    member_group_weight = resource.Body("member_group_weight", type=int)
    dict_code = resource.Body("dict_code")
    microservice_version = resource.Body("microservice_version")
    microservice_port = resource.Body("microservice_port", type=int)
    microservice_labels = resource.Body("microservice_labels", type=list,
                                        list_type=MicroserviceLabelSpec)
    member_group_id = resource.Body("member_group_id")
    create_time = resource.Body("create_time")
    update_time = resource.Body("update_time")


class MemberInfoSpec(resource.Resource):
    host = resource.Body("host")
    weight = resource.Body("weight", type=int)
    is_backup = resource.Body("is_backup", type=bool)
    member_group_name = resource.Body("member_group_name")
    status = resource.Body("status", type=int)
    port = resource.Body("port", type=int)
    ecs_id = resource.Body("ecs_id")
    ecs_name = resource.Body("ecs_name")


class VpcHealthConfigSpec(resource.Resource):
    protocol = resource.Body("protocol")
    path = resource.Body("path")
    method = resource.Body("method")
    port = resource.Body("port", type=int)
    threshold_normal = resource.Body("threshold_normal", type=int)
    threshold_abnormal = resource.Body("threshold_abnormal", type=int)
    time_interval = resource.Body("time_interval", type=int)
    http_code = resource.Body("http_code")
    enable_client_ssl = resource.Body("enable_client_ssl", type=bool)
    status = resource.Body("status", type=int)
    timeout = resource.Body("timeout", type=int)
    vpc_channel_id = resource.Body("vpc_channel_id")
    id = resource.Body("id")
    create_time = resource.Body("create_time")


class MicroServiceInfoCSEBaseSpec(resource.Resource):
    engine_id = resource.Body("engine_id")
    service_id = resource.Body("service_id")
    engine_name = resource.Body("engine_name")
    service_name = resource.Body("service_name")
    register_address = resource.Body("register_address")
    cse_app_id = resource.Body("cse_app_id")
    version = resource.Body("version")


class MicroServiceInfoCCEBaseSpec(resource.Resource):
    cluster_id = resource.Body("cluster_id")
    namespace = resource.Body("namespace")
    workload_type = resource.Body("workload_type")
    app_name = resource.Body("app_name")
    label_key = resource.Body("label_key")
    label_value = resource.Body("label_value")
    cluster_name = resource.Body("cluster_name")


class MicroServiceCreateSpec(resource.Resource):
    service_type = resource.Body("service_type")
    cse_info = resource.Body("cse_info",
                             type=MicroServiceInfoCSEBaseSpec)
    cce_info = resource.Body("cce_info",
                             type=MicroServiceInfoCCEBaseSpec)
    id = resource.Body("id")
    instance_id = resource.Body("instance_id")
    create_time = resource.Body("create_time")
    update_time = resource.Body("update_time")


class VpcChannel(resource.Resource):
    base_path = f'apigw/instances/%(gateway_id)s/vpc-channels'
    resources_key = 'vpc_channels'
    _query_mapping = resource.QueryParameters('limit', 'offset',
                                              'id', 'dict_code',
                                              'name', 'precise_search',
                                              'member_host', 'member_port',
                                              'member_group_name',
                                              'member_group_id')

    allow_create = True
    allow_delete = True
    allow_list = True
    allow_fetch = True
    allow_commit = True

    gateway_id = resource.URI('gateway_id')
    name = resource.Body('name')
    port = resource.Body('port', type=int)
    balance_strategy = resource.Body('balance_strategy', type=int)
    member_type = resource.Body('member_type')
    type = resource.Body('type', type=int)
    dict_code = resource.Body('dict_code')
    member_groups = resource.Body('member_groups', type=list,
                                  list_type=MemberGroupCreateSpec)
    members = resource.Body('members', type=list,
                            list_type=MemberInfoSpec)
    vpc_health_config = resource.Body('vpc_health_config',
                                      type=VpcHealthConfigSpec)
    microservice_info = resource.Body('microservice_info',
                                      type=MicroServiceCreateSpec)
    create_time = resource.Body('create_time')
    id = resource.Body('id')
    status = resource.Body('status', type=int)

    def modify_healthcheck(self, session, gateway_id, vpc_channel_id, **attrs):
        uri = (f'apigw/instances/{gateway_id}/vpc-channels/'
               f'{vpc_channel_id}/health-config')
        response = session.put(uri, json=attrs)
        exceptions.raise_from_response(response)
        data = response.json()
        self.vpc_health_config = VpcHealthConfigSpec.existing(**data)
        return self
