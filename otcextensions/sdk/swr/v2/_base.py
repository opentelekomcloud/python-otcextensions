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
import typing as ty


class Resource(resource.Resource):

    def _prepare_request_body(
            self,
            patch,
            prepend_key,
            *,
            resource_request_key=None,
    ):
        body: ty.Union[ty.Dict[str, ty.Any], ty.List[ty.Any]]
        if not self._store_unknown_attrs_as_properties:
            # Default case
            body = self._body.dirty
        else:
            body = self._unpack_properties_to_resource_root(
                self._body.dirty
            )

        if prepend_key:
            if resource_request_key is not None:
                body = {resource_request_key: body}
            elif self.resource_key is not None:
                body = {self.resource_key: body}
        if 'permissions' in body:
            return body['permissions']
        return body

    def _delete(self, session, user_ids, base_path):
        """Delete permissions
        """
        response = session.delete(base_path, json=user_ids)
        exceptions.raise_from_response(response)
        return None
