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

from otcextensions.common import exc


class Metadata(resource.Resource):

    # Properties
    #: Annotations
    annotations = resource.Body('annotations', type=dict)
    #: UUID
    #: *Type:str
    id = resource.Body('uid', alternate_id=True)
    #: Labels
    labels = resource.Body('labels', type=dict)
    #: Name
    #: *Type:str
    name = resource.Body('name')
    #: Create time
    #: *Type:str
    created_at = resource.Body('creationTimestamp')
    #: Update time
    #: *Type:str
    updated_at = resource.Body('updateTimestamp')


class StatusSpec(resource.Resource):
    # Properties
    #: Cluster status.
    status = resource.Body('phase')
    #: Job ID.
    job_id = resource.Body('jobID')


class Resource(resource.Resource):

    # Properties
    #: Kind
    kind = resource.Body('kind')
    #: api version
    api_version = resource.Body('apiVersion', default='v3')
    #: metadata
    metadata = resource.Body('metadata', type=Metadata)
    #: Cluster status
    status = resource.Body('status', type=StatusSpec)
    #: Creation date. A virtual attribute fetched from metadata
    created_at = resource.Body('created_at')
    #: Update date. A virtual attribute fetched from metadata
    updated_at = resource.Body('updated_at')

    def __getattribute__(self, name):
        """Return an attribute on this instance

        This is mostly a pass-through except for a specialization on
        the 'id' name, as this can exist under a different name via the
        `alternate_id` argument to resource.Body.
        """
        if name == 'id' or name == 'name':
            if name in self._body:
                return self._body[name]
            else:
                try:
                    metadata = self._body['metadata']
                    if name == 'id':
                        if isinstance(metadata, dict):
                            return metadata['uid']
                        elif isinstance(metadata, Metadata):
                            return metadata._body[metadata._alternate_id()]
                    else:
                        if isinstance(metadata, dict):
                            return metadata['name']
                        elif isinstance(metadata, Metadata):
                            return metadata.name
                except KeyError:
                    return None
        elif name == 'status.status':
            status = object.__getattribute__(self, 'status')
            return object.__getattribute__(status, 'status')
        elif name in ['job_id', 'status.job_id']:
            status = object.__getattribute__(self, 'status')
            return object.__getattribute__(status, 'job_id')
        elif name in ['created_at', 'updated_at']:
            metadata = object.__getattribute__(self, 'metadata')
            # CCE return completely broken time format:
            # 2021-08-26 11:46:31.841673 +0000 UTC
            # Since it is far away from being any existing standard - drop
            # TZ info away (it is anyway only UTC)
            # Project cleanup is the one who tries really to parse the date,
            # thus we need to ensure it is parsable
            timestamp = object.__getattribute__(metadata, name)
            return timestamp[0:24] if timestamp else None
        else:
            return object.__getattribute__(self, name)

    def _translate_response(
            self, response, has_body=None, error_message=None,
            resource_response_key=None):
        if has_body is None:
            has_body = self.has_body
        # NOTE: we only use our own exception parser
        exc.raise_from_response(response, error_message=error_message)
        if has_body:
            try:
                body = response.json()
                if self.resource_key and self.resource_key in body:
                    body = body[self.resource_key]

                body_attrs = self._consume_body_attrs(body)

                if self._store_unknown_attrs_as_properties:
                    body_attrs = self._pack_attrs_under_properties(
                        body_attrs, body)

                self._body.attributes.update(body_attrs)
                self._body.clean()
                if self.commit_jsonpatch or self.allow_patch:
                    # We need the original body to compare against
                    self._original_body = body_attrs.copy()
            except ValueError:
                # Server returned not parse-able response (202, 204, etc)
                # Do simply nothing
                pass

        headers = self._consume_header_attrs(response.headers)
        self._header.attributes.update(headers)
        self._header.clean()
        self._update_location()
        dict.update(self, self.to_dict())

    def create(self, session, prepend_key=False, base_path=None):
        # Overriden here to override prepend_key default value
        return super(Resource, self).create(session, prepend_key, base_path)

    def delete(self, session, error_message=None):
        """Delete the remote resource based on this instance.

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`

        :return: This :class:`Resource` instance.
        :raises: :exc:`~openstack.exceptions.MethodNotSupported` if
                 :data:`Resource.allow_commit` is not set to ``True``.
        :raises: :exc:`~openstack.exceptions.ResourceNotFound` if
                 the resource was not found.
        """

        response = self._raw_delete(session)
        kwargs = {}
        if error_message:
            kwargs['error_message'] = error_message

        self._translate_response(response, has_body=True, **kwargs)
        return self

    @classmethod
    def list(cls, session, paginated=True, base_path=None, **params):
        """This method is a generator which yields resource objects.

        This resource object list generator handles pagination and takes query
        params for response filtering.

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param bool paginated: ``True`` if a GET to this resource returns
                               a paginated series of responses, or ``False``
                               if a GET returns only one page of data.
                               **When paginated is False only one
                               page of data will be returned regardless
                               of the API's support of pagination.**
        :param str base_path: Base part of the URI for listing resources, if
                              different from
                              :data:`~openstack.resource.Resource.base_path`.
        :param dict params: These keyword arguments are passed through the
            :meth:`~openstack.resource.QueryParamter._transpose` method
            to find if any of them match expected query parameters to be
            sent in the *params* argument to
            :meth:`~keystoneauth1.adapter.Adapter.get`. They are additionally
            checked against the
            :data:`~openstack.resource.Resource.base_path` format string
            to see if any path fragments need to be filled in by the contents
            of this argument.

        :return: A generator of :class:`Resource` objects.
        :raises: :exc:`~openstack.exceptions.MethodNotSupported` if
                 :data:`Resource.allow_list` is not set to ``True``.
        :raises: :exc:`~openstack.exceptions.InvalidResourceQuery` if query
                 contains invalid params.
        """
        if not cls.allow_list:
            raise exceptions.MethodNotSupported(cls, "list")
        session = cls._get_session(session)
        microversion = cls._get_microversion(session, action='list')

        if base_path is None:
            base_path = cls.base_path
        cls._query_mapping._validate(params, base_path=base_path)
        query_params = cls._query_mapping._transpose(params, cls)
        uri = base_path % params

        while uri:
            # Copy query_params due to weird mock unittest interactions
            response = session.get(
                uri,
                headers={
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'},
                params=query_params.copy())
            exceptions.raise_from_response(response)

            if response.json() and 'items' in response.json():
                data = response.json()['items'] or []

            if cls.resources_key:
                resources = data[cls.resources_key]
            else:
                resources = data

            if not isinstance(resources, list):
                resources = [resources]

            for raw_resource in resources:

                value = cls.existing(
                    microversion=microversion,
                    connection=session._get_connection(),
                    **raw_resource)
                yield value

            return
