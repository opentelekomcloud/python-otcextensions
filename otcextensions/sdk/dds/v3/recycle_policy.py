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


class RecyclePolicy(resource.Resource):
    base_path = 'instances/recycle-policy'
    resource_key = 'recycle_policy'

    requires_id = False

    allow_fetch = True
    allow_create = True
    create_method = "PUT"

    enabled = resource.Body('enabled', type=bool)
    retention_period_in_days = resource.Body('retention_period_in_days')

    def fetch(self, session, requires_id=False, base_path=None,
              error_message=None, skip_cache=False, *,
              resource_response_key=None,
              microversion=None, **params,):
        request = self._prepare_request(
            requires_id=requires_id,
            base_path=self.base_path,
        )
        session = self._get_session(session)
        if microversion is None:
            microversion = self._get_microversion(session)
        response = session.get(
            request.url,
            headers={"Content-Type": "application/json"},
            microversion=microversion,
            params=params,
            skip_cache=skip_cache,
        )
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self

    def create(self, session, prepend_key=True, base_path=None, *,
               resource_request_key=None, resource_response_key=None,
               microversion=None, **params,):
        if not self.allow_create:
            raise exceptions.MethodNotSupported(self, 'create')
        session = self._get_session(session)
        if microversion is None:
            microversion = self._get_microversion(session)
        request_kwargs = {
            "requires_id": self.requires_id,
            "prepend_key": prepend_key,
            "base_path": self.base_path,
        }
        request = self._prepare_request(**request_kwargs)
        response = session.put(
            request.url,
            json=request.body,
            headers=request.headers,
            microversion=microversion,
            params=params,
        )
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self
