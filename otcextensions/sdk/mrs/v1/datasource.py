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

from openstack import _log, exceptions
from openstack import resource

from otcextensions.sdk import sdk_resource

_logger = _log.setup_logging('openstack')


class Datasource(sdk_resource.Resource):
    resource_key = 'data_source'
    resources_key = 'data_sources'
    base_path = '/data-sources'

    # capabilities
    allow_create = True
    allow_list = True
    allow_get = True
    allow_delete = True
    allow_update = True

    _query_mapping = resource.QueryParameters(
        'id', 'name', 'type', 'url', 'description', 'is_public',
        'is_protected')

    #: Properties
    #: Data source ID
    id = resource.Body('id', alternate_id=True)
    #: Data source name
    name = resource.Body('name')
    #: type of the ds
    type = resource.Body('type')
    #: Data source URL
    url = resource.Body('url')
    #: Data source description
    description = resource.Body('description')
    #: Whether the data source is public
    is_public = resource.Body('is_public')
    #: Whether the data source is protected
    is_protected = resource.Body('is_protected')
    #: Data source creation time
    created_at = resource.Body('created_at')
    #: Data source update time
    updated_at = resource.Body('updated_at')

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

        response = session.put(
            request.url, json=request.body, **args)

        self._translate_response(response, has_body=has_body)
        return self
