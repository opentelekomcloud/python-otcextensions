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
from otcextensions.sdk.dds.v3 import instance as _instance
class Job(resource.Resource):
    base_path = '/jobs'

    allow_fetch = True

    id = resource.Body('id')
    name = resource.Body('name')
    status = resource.Body('status')
    created = resource.Body('created')
    ended = resource.Body('ended')
    progress = resource.Body('progress')
    instance = resource.Body('instance', type=_instance.Instance)

    def fetch(self, session, requires_id=True,
              base_path=None, error_message=None, **params):
        params = {
            "id": self.id,
        }
        request = self._prepare_request(
            requires_id=False,
            base_path=base_path,
            params=params
        )
        response = session.get(
            request.url,
        )
        self._translate_response(response, resource_response_key='job')
        return self
