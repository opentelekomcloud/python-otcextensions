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
import ast
import typing as ty

from openstack import exceptions
from openstack import resource
from openstack import utils

from otcextensions.sdk.lts.v2 import stream as _stream


class Group(resource.Resource):
    resource_key = 'log_groups'
    resources_key = 'log_groups'
    base_path = '/groups'

    # capabilities
    allow_create = True
    allow_fetch = False
    allow_commit = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'id',
    )

    # Properties
    #: Time when a log group was created
    creation_time = resource.Body('creation_time')
    #: ID of the log group.
    id = resource.Body('log_group_id', alternate_id=True)
    #: Name of the log group.
    name = resource.Body('log_group_name')
    #: Log retention duration, in days (fixed to 7 days).
    ttl_in_days = resource.Body('ttl_in_days', type=int)
    #: Log group tag.
    tag = resource.Body('tag')

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
        return body

    def commit(
        self,
        session,
        prepend_key=True,
        has_body=True,
        retry_on_conflict=None,
        base_path=None,
        *,
        microversion=None,
        **kwargs,
    ):
        # The id cannot be dirty for an commit
        self._body._dirty.discard("id")

        # Only try to update if we actually have anything to commit.
        if not self.requires_commit:
            return self

        # Avoid providing patch unconditionally to avoid breaking subclasses
        # without it.
        if self.commit_jsonpatch:
            kwargs['patch'] = True

        request = self._prepare_request(
            prepend_key=prepend_key,
            base_path=base_path,
            **kwargs,
        )
        if microversion is None:
            microversion = self._get_microversion(session, action='commit')

        return self._commit(
            session,
            request,
            "POST",
            microversion,
            has_body=has_body,
            retry_on_conflict=retry_on_conflict,
        )

    def create_stream(self, session, query):
        """Method to create a stream in log group

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param dict query: Additional parameters to create stream
        """
        url = utils.urljoin(self.base_path, self.id, '/streams')
        resp = session.post(url, json=query)
        stream = _stream.Stream()
        stream._translate_response(resp)
        return stream

    def delete_stream(self, session, log_stream_id, ignore_missing):
        """Method to delete stream from log group

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param str log_stream_id: Id of the stream to be deleted
        :param bool ignore_missing: Should it be deleted
         if doesn't exist or not
        """
        url = utils.urljoin(self.base_path, self.id, '/streams/',
                            log_stream_id)
        resp = session.delete(url)
        if resp.status_code == 404:
            if not ignore_missing:
                raise exceptions.NotFoundException(
                    str(ast.literal_eval(resp._content.decode('utf-8'))))
        return None
