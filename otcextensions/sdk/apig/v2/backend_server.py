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


class BackendServer(resource.Resource):
    base_path = (f'apigw/instances/%(gateway_id)s/vpc-channels/'
                 f'%(vpc_chan_id)s/members')
    resources_key = "members"

    allow_delete = True
    allow_list = True
    allow_commit = True

    gateway_id = resource.URI('gateway_id')
    vpc_chan_id = resource.URI('vpc_chan_id')

    host = resource.Body('host')
    weight = resource.Body('weight', type=int)
    is_backup = resource.Body('is_backup', type=bool)
    member_group_name = resource.Body('member_group_name')
    status = resource.Body('status', type=int)
    port = resource.Body('port', type=int)
    ecs_id = resource.Body('ecs_id')
    ecs_name = resource.Body('ecs_name')
    id = resource.Body('id')
    vpc_channel_id = resource.Body('vpc_channel_id')
    create_time = resource.Body('create_time')
    member_group_id = resource.Body('member_group_id')

    def create_members(self, session, gateway_id, vpc_channel_id, **attrs):
        return self.send_request(
            session,
            gateway_id,
            vpc_channel_id,
            'POST',
            **attrs
        )

    def update_members(self, session, gateway_id, vpc_channel_id, **attrs):
        return self.send_request(
            session,
            gateway_id,
            vpc_channel_id,
            'PUT',
            **attrs
        )

    @staticmethod
    def send_request(session, gateway_id, vpc_channel_id, method,
                     **attrs):
        uri = (
            f"/apigw/instances/{gateway_id}/vpc-channels/"
            f"{vpc_channel_id}/members"
        )
        session_method = session.put if method == 'PUT' else session.post
        response = session_method(uri, json=attrs)
        exceptions.raise_from_response(response)
        result = response.json()['members']
        if isinstance(result, list):
            return [BackendServer.existing(**item) for item in result]
        elif isinstance(result, dict):
            return BackendServer.existing(**result)

    def enable_server(self, session, gateway_id, vpc_channel_id, **attrs):
        uri = f'apigw/instances/{gateway_id}/vpc-channels/'\
              f'{vpc_channel_id}/members/batch-enable'
        response = session.post(uri, json=attrs)
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return response

    def disable_server(self, session, gateway_id, vpc_channel_id, **attrs):
        uri = f'apigw/instances/{gateway_id}/vpc-channels/'\
              f'{vpc_channel_id}/members/batch-disable'
        response = session.post(uri, json=attrs)
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return response
