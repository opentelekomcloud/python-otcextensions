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

from otcextensions.sdk import sdk_resource


class Resource(sdk_resource.Resource):

    def update(self, session, prepend_key=False, has_body=True,
               endpoint_override=None, headers=None, requests_auth=None):
        """Update the remote resource based on this instance.

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param prepend_key: A boolean indicating whether the resource_key
                            should be prepended in a resource update request.
                            Default to True.

        :return: This :class:`Resource` instance.
        :raises: :exc:`~openstack.exceptions.MethodNotSupported` if
                 :data:`Resource.allow_update` is not set to ``True``.
        """
        # The id cannot be dirty for an update
        self._body._dirty.discard("id")

        # Only try to update if we actually have anything to update.
        if not any([self._body.dirty, self._header.dirty]):
            return self

        if not self.allow_update:
            raise exceptions.MethodNotSupported(self, "update")

        request = self._prepare_request(prepend_key=prepend_key)
        session = self._get_session(session)

        args = self._prepare_override_args(
            endpoint_override=endpoint_override,
            request_headers=request.headers,
            additional_headers=headers,
            requests_auth=requests_auth)

        if self.commit_method == 'PATCH':
            response = session.patch(
                request.url, json=request.body, **args)
        elif self.commit_method == 'POST':
            response = session.post(
                request.url, json=request.body, **args)
        elif self.commit_method == 'PUT':
            response = session.put(
                request.url, json=request.body, **args)
        else:
            raise exceptions.ResourceFailure(
                message="Invalid update method: %s" % self.commit_method)

        self._translate_response(response, has_body=has_body)
        return self
