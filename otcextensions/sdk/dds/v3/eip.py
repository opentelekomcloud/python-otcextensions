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
from openstack import exceptions
from openstack import resource
from openstack import utils


class Eip(resource.Resource):
    base_path = '/nodes'

    resources_key = 'nodes'
    resource_key = 'node'

    job_id = resource.Body('job_id')
    node_id = resource.Body('node_id')
    node_name = resource.Body('node_name')
    public_ip = resource.Body('public_ip')
    public_ip_id = resource.Body('public_ip_id')

    def bind(self, session, node, public_ip, public_ip_id):
        body = {
            "public_ip": public_ip,
            "public_ip_id": public_ip_id
        }
        response = self._action(session, body, f'{node}/bind-eip')
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self

    def unbind(self, session, node):
        response = self._action(session, {}, f'{node}/unbind-eip')
        self._translate_response(response)
        return self

    def _action(self, session, body, action_type):
        """Preform actions given the message body.
        """
        url = utils.urljoin(self.base_path, action_type)
        return session.post(
            url,
            json=body)
