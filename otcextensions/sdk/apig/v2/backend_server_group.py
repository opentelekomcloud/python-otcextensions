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
    label_name = resource.Body('label_name')
    label_value = resource.Body('label_value')


class BackendServerGroup(resource.Resource):
    base_path = (f'apigw/instances/%(gateway_id)s/vpc-channels/'
                 f'%(vpc_channel_id)s/member-groups')

    allow_fetch = True
    allow_list = True
    allow_delete = True
    allow_commit = True

    gateway_id = resource.URI('gateway_id')
    vpc_channel_id = resource.URI('vpc_channel_id')
    member_group_name = resource.Body('member_group_name')
    member_group_remark = resource.Body('member_group_remark')
    member_group_weight = resource.Body('member_group_weight', type=int)
    dict_code = resource.Body('dict_code')
    microservice_version = resource.Body('microservice_version')
    microservice_port = resource.Body('microservice_port', type=int)
    microservice_labels = resource.Body('microservice_labels',
                                        type=list,
                                        list_type=MicroserviceLabelSpec)
    member_group_id = resource.Body('member_group_id')
    create_time = resource.Body('create_time')
    update_time = resource.Body('update_time')

    @staticmethod
    def create_group(session, gateway_id, vpc_channel_id, **attrs):
        uri = (f'/apigw/instances/{gateway_id}/vpc-channels/{vpc_channel_id}/'
               f'member-groups')
        response = session.post(uri, json=attrs)
        exceptions.raise_from_response(response)
        result = response.json()['member_groups']
        if isinstance(result, list):
            return [BackendServerGroup.existing(**item) for item in result]
        elif isinstance(result, dict):
            return BackendServerGroup.existing(**result)
