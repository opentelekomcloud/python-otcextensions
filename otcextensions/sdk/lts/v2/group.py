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

from openstack import exceptions, resource
from openstack import utils


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

    def create_stream(self, session, query):
        """Method to add several share members to a backup

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param list members: List of target project IDs to which the backup
            is shared
        """
        url = utils.urljoin(self.base_path, self.id, '/streams')
        resp = session.post(url, json=query)
        return ast.literal_eval(resp._content.decode('utf-8'))

    def delete_stream(self, session, log_stream_id, ignore_missing):
        """Method to add several share members to a backup

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param list members: List of target project IDs to which the backup
            is shared
        """
        url = utils.urljoin(self.base_path, self.id, '/streams/',
                            log_stream_id)
        resp = session.delete(url)
        if resp.status_code == 404:
            if not ignore_missing:
                raise exceptions.NotFoundException(
                    str(ast.literal_eval(resp._content.decode('utf-8'))))
        return None
