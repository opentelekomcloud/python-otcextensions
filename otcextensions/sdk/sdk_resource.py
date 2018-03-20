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
import re

from openstack import _log
from openstack import exceptions
from openstack import resource
# from openstack import utils

from otcextensions.common import utils

_logger = _log.setup_logging('openstack')


def raise_from_response(response, error_message=None):
    """Raise an instance of an HTTPException based on keystoneauth response."""
    if response.status_code < 400:
        return

    if response.status_code == 404:
        cls = exceptions.NotFoundException
    elif response.status_code == 400:
        cls = exceptions.BadRequestException
    else:
        cls = exceptions.HttpException

    details = None
    content_type = response.headers.get('content-type', '')
    if response.content and 'application/json' in content_type:
        # Iterate over the nested objects to retrieve "message" attribute.
        # TODO(shade) Add exception handling for times when the content type
        # is lying.

        try:
            content = response.json()
            error = content.get('error', None)
            messages = []
            if error:
                messages = [error.get('message', None)]
            else:
                messages = [obj.get('message') for obj in content.values()
                            if isinstance(obj, dict)]
            # Join all of the messages together nicely and filter out any
            # objects that don't have a "message" attr.
            details = '\n'.join(msg for msg in messages if msg)
        except Exception:
            details = response.text
    elif response.content and 'text/html' in content_type:
        # Split the lines, strip whitespace and inline HTML from the response.
        details = [re.sub(r'<.+?>', '', i.strip())
                   for i in response.text.splitlines()]
        details = list(set([msg for msg in details if msg]))
        # Return joined string separated by colons.
        details = ': '.join(details)
    if not details and response.reason:
        details = response.reason
    elif not details and response.text:
        details = response.text

    http_status = response.status_code
    request_id = response.headers.get('x-openstack-request-id')

    # sdk.exception define default for message to Error, but we need
    # have a better info
    if not error_message and details:
        error_message = details

    raise cls(
        message=error_message, response=response, details=details,
        http_status=http_status, request_id=request_id
    )


class Resource(resource.Resource):

    @classmethod
    def _prepare_override_args(cls,
                               endpoint_override=None,
                               request_headers=None,
                               additional_headers=None):
        """Prepare additional (override) arguments for the REST call

        :param endpoint_override: optional endpoint_override argument
        :param request_headers: original calculated request headers
        :param additional_headers: additional headers to be set into request

        :returns arguments dict
        """
        req_args = {}

        if additional_headers and request_headers:
            req_args['headers'] = utils.merge_two_dicts(
                additional_headers,
                request_headers)
        else:
            if additional_headers:
                req_args['headers'] = additional_headers
            if request_headers:
                req_args['headers'] = request_headers

        if endpoint_override:
            req_args['endpoint_override'] = endpoint_override

        return req_args

    def _translate_response(self, response, has_body=None, error_message=None):
        """Given a KSA response, inflate this instance with its data

        'DELETE' operations don't return a body, so only try to work
        with a body when has_body is True.

        This method updates attributes that correspond to headers
        and body on this instance and clears the dirty set.
        """
        if has_body is None:
            has_body = self.has_body
        raise_from_response(response, error_message=error_message)
        if has_body:
            body = response.json()
            if self.resource_key and self.resource_key in body:
                body = body[self.resource_key]

            body = self._consume_body_attrs(body)
            self._body.attributes.update(body)
            self._body.clean()

        headers = self._consume_header_attrs(response.headers)
        self._header.attributes.update(headers)
        self._header.clean()

    def create(self, session, prepend_key=True, requires_id=True,
               endpoint_override=None, headers=None):
        """Create a remote resource based on this instance.

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param prepend_key: A boolean indicating whether the resource_key
                            should be prepended in a resource creation
                            request. Default to True.

        :return: This :class:`Resource` instance.
        :raises: :exc:`~openstack.exceptions.MethodNotSupported` if
                 :data:`Resource.allow_create` is not set to ``True``.
        """
        if not self.allow_create:
            raise exceptions.MethodNotSupported(self, "create")

        session = self._get_session(session)

        if self.create_method == 'PUT':
            request = self._prepare_request(requires_id=True,
                                            prepend_key=prepend_key)
            req_args = self._prepare_override_args(
                endpoint_override=endpoint_override,
                request_headers=request.headers,
                additional_headers=headers)
            response = session.put(request.url,
                                   json=request.body, **req_args)
        elif self.create_method == 'POST':
            request = self._prepare_request(requires_id=False,
                                            prepend_key=prepend_key)
            req_args = self._prepare_override_args(
                endpoint_override=endpoint_override,
                request_headers=request.headers,
                additional_headers=headers)
            response = session.post(request.url,
                                    json=request.body, **req_args)
        else:
            raise exceptions.ResourceFailure(
                msg="Invalid create method: %s" % self.create_method)

        self._translate_response(response)

        return self

    def get(self, session, error_message=None, requires_id=True,
            endpoint_override=None, headers=None):
        """Get a remote resource based on this instance.

        This function overrides default Resource.get to enable GET headers

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param boolean requires_id: A boolean indicating whether resource ID
                                    should be part of the requested URI.
        :return: This :class:`Resource` instance.
        :raises: :exc:`~openstack.exceptions.MethodNotSupported` if
                 :data:`Resource.allow_get` is not set to ``True``.
        """
        if not self.allow_get:
            raise exceptions.MethodNotSupported(self, "get")

        request = self._prepare_request(requires_id=requires_id)
        session = self._get_session(session)

        # Build additional arguments to the GET call
        get_args = self._prepare_override_args(
            endpoint_override=endpoint_override,
            request_headers=request.headers,
            additional_headers=headers)

        response = session.get(request.url, **get_args)
        kwargs = {}
        if error_message:
            kwargs['error_message'] = error_message

        self._translate_response(response, **kwargs)

        return self

    def head(self, session,
             endpoint_override=None, headers=None):
        """Get headers from a remote resource based on this instance.

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`

        :return: This :class:`Resource` instance.
        :raises: :exc:`~openstack.exceptions.MethodNotSupported` if
                 :data:`Resource.allow_head` is not set to ``True``.
        """
        if not self.allow_head:
            raise exceptions.MethodNotSupported(self, "head")

        request = self._prepare_request()

        session = self._get_session(session)

        args = self._prepare_override_args(
            endpoint_override=endpoint_override,
            request_headers={"Accept": ""},
            additional_headers=headers)

        response = session.head(request.url,
                                **args)

        self._translate_response(response, has_body=False)
        return self

    def update(self, session, prepend_key=True, has_body=True,
               endpoint_override=None, headers=None):
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
            additional_headers=headers)

        if self.update_method == 'PATCH':
            response = session.patch(
                request.url, json=request.body, **args)
        elif self.update_method == 'POST':
            response = session.post(
                request.url, json=request.body, **args)
        elif self.update_method == 'PUT':
            response = session.put(
                request.url, json=request.body, **args)
        else:
            raise exceptions.ResourceFailure(
                msg="Invalid update method: %s" % self.update_method)

        self._translate_response(response, has_body=has_body)
        return self

    def delete(self, session, error_message=None,
               endpoint_override=None, headers=None):
        """Delete the remote resource based on this instance.

        This function overrides default Resource.delete to enable headers

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`

        :return: This :class:`Resource` instance.
        :raises: :exc:`~openstack.exceptions.MethodNotSupported` if
                 :data:`Resource.allow_update` is not set to ``True``.
        """
        if not self.allow_delete:
            raise exceptions.MethodNotSupported(self, "delete")

        request = self._prepare_request()
        session = self._get_session(session)

        # Build additional arguments to the DELETE call
        delete_args = self._prepare_override_args(
            endpoint_override=endpoint_override,
            request_headers=request.headers,
            additional_headers=headers)

        response = session.delete(request.url,
                                  **delete_args)
        kwargs = {}
        if error_message:
            kwargs['error_message'] = error_message

        self._translate_response(response, has_body=False, **kwargs)
        return self

    @classmethod
    def list(cls, session, paginated=False,
             endpoint_override=None, headers=None, **params):
        """Override default list to incorporate endpoint overriding
        and custom headers

        Since SDK Resource.list method is passing hardcoded headers
        do override the function

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

        cls._query_mapping._validate(params, base_path=cls.base_path)
        query_params = cls._query_mapping._transpose(params)
        uri = cls.base_path % params

        limit = query_params.get('limit')

        # Build additional arguments to the GET call
        get_args = cls._prepare_override_args(
            endpoint_override=endpoint_override,
            # request_headers=request.headers,
            additional_headers=headers)

        total_yielded = 0
        while uri:
            response = session.get(
                uri,
                params=query_params.copy(),
                **get_args,
            )
            exceptions.raise_from_response(response)
            data = response.json()

            # Discard any existing pagination keys
            query_params.pop('marker', None)
            query_params.pop('limit', None)

            if cls.resources_key:
                resources = data[cls.resources_key]
            else:
                resources = data

            if not isinstance(resources, list):
                resources = [resources]

            marker = None
            for raw_resource in resources:
                # Do not allow keys called "self" through. Glance chose
                # to name a key "self", so we need to pop it out because
                # we can't send it through cls.existing and into the
                # Resource initializer. "self" is already the first
                # argument and is practically a reserved word.
                raw_resource.pop("self", None)

                if cls.resource_key and cls.resource_key in raw_resource:
                    raw_resource = raw_resource[cls.resource_key]

                value = cls.existing(**raw_resource)

                marker = value.id
                yield value
                total_yielded += 1

            if resources and paginated:
                uri, next_params = cls._get_next_link(
                    uri, response, data, marker, limit, total_yielded)
                query_params.update(next_params)
            else:
                return

    @classmethod
    def find(cls, session, name_or_id, ignore_missing=True,
             endpoint_override=None, headers=None, **params):
        """Find a resource by its name or id.

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param name_or_id: This resource's identifier, if needed by
                           the request. The default is ``None``.
        :param bool ignore_missing: When set to ``False``
                    :class:`~openstack.exceptions.ResourceNotFound` will be
                    raised when the resource does not exist.
                    When set to ``True``, None will be returned when
                    attempting to find a nonexistent resource.
        :param dict params: Any additional parameters to be passed into
                            underlying methods, such as to
                            :meth:`~openstack.resource.Resource.existing`
                            in order to pass on URI parameters.

        :return: The :class:`Resource` object matching the given name or id
                 or None if nothing matches.
        :raises: :class:`openstack.exceptions.DuplicateResource` if more
                 than one resource is found for this request.
        :raises: :class:`openstack.exceptions.ResourceNotFound` if nothing
                 is found and ignore_missing is ``False``.
        """
        # Try to short-circuit by looking directly for a matching ID.
        try:
            match = cls.existing(
                id=name_or_id,
                **params)
            return match.get(
                session,
                endpoint_override=endpoint_override,
                headers=headers)
        except (exceptions.NotFoundException, exceptions.HttpException):
            pass

        data = cls.list(session,
                        endpoint_override=endpoint_override,
                        headers=headers,
                        **params)

        result = cls._get_one_match(name_or_id, data)
        # Update result with URL parameters
        result._update(**params)
        if result is not None:
            return result

        if ignore_missing:
            return None
        raise exceptions.ResourceNotFound(
            "No %s found for %s" % (cls.__name__, name_or_id))

    def update_no_id(self, session, prepend_key=True, has_body=True,
                     endpoint_override=None, headers=None):
        """Update the remote resource based on this instance.

        Method is required for resources without ID
        (single resource at endpoint)

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param prepend_key: A boolean indicating whether the resource_key
                            should be prepended in a resource update request.
                            Default to True.

        :return: This :class:`Resource` instance.
        :raises: :exc:`~openstack.exceptions.MethodNotSupported` if
                 :data:`Resource.allow_update` is not set to ``True``.
        """
        # Only try to update if we actually have anything to update.
        if not any([self._body.dirty, self._header.dirty]):
            return self

        if not self.allow_update:
            raise exceptions.MethodNotSupported(self, "update")

        request = self._prepare_request(
            requires_id=False,
            prepend_key=prepend_key)
        session = self._get_session(session)

        update_args = self._prepare_override_args(
            endpoint_override=endpoint_override,
            request_headers=request.headers,
            additional_headers=headers)

        if self.update_method == 'PATCH':
            response = session.patch(
                request.url, json=request.body, **update_args)
        elif self.update_method == 'POST':
            response = session.post(
                request.url, json=request.body, **update_args)
        elif self.update_method == 'PUT':
            response = session.put(
                request.url, json=request.body, **update_args)
        else:
            raise exceptions.ResourceFailure(
                msg="Invalid update method: %s" % self.update_method)

        self._translate_response(response, has_body=has_body)
        return self
