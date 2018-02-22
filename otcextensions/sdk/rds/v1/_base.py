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

from openstack import _log
from openstack import exceptions
from openstack import resource
# from openstack import utils

from otcextensions.sdk.rds import rds_service


_logger = _log.setup_logging('openstack')


class Resource(resource.Resource):

    base_path = '/'
    resource_key = ''
    resources_key = ''
    service = rds_service.RdsService()

    allow_list = True

    def list(self, session, paginated=False, endpoint_override=None,
             headers=None, **params):
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

        if not self.allow_list:
            raise exceptions.MethodNotSupported(self, "list")
        session = self._get_session(session)

        self._query_mapping._validate(params, base_path=self.base_path)
        query_params = self._query_mapping._transpose(params)
        uri = self.base_path % params

        limit = query_params.get('limit')

        # Build additional arguments to the GET call
        get_args = {
            'params': query_params.copy()
        }

        if endpoint_override:
            get_args['endpoint_override'] = endpoint_override

        if headers:
            get_args['headers'] = headers
        else:
            get_args['headers'] = {
                "Content-Type": "application/json"
            }

        total_yielded = 0
        while uri:
            response = session.get(
                uri,
                **get_args
            )
            exceptions.raise_from_response(response)
            data = response.json()

            if self.resources_key:
                resources = data[self.resources_key]
            else:
                resources = data

            if not isinstance(resources, list):
                resources = [resources]

            for raw_resource in resources:
                # Do not allow keys called "self" through. Glance chose
                # to name a key "self", so we need to pop it out because
                # we can't send it through cls.existing and into the
                # Resource initializer. "self" is already the first
                # argument and is practically a reserved word.
                raw_resource.pop("self", None)

                if self.resource_key and self.resource_key in raw_resource:
                    raw_resource = raw_resource[self.resource_key]

                value = self.existing(**raw_resource)

                marker = value.id
                yield value
                total_yielded += 1

            if resources and paginated:
                uri, next_params = self._get_next_link(
                    uri, response, data, marker, limit, total_yielded)
                query_params.update(next_params)
            else:
                return

    def get(self, session, headers=None, endpoint_override=None,
            requires_id=True, error_message=None):
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
        get_args = {}
        if headers:
            get_args['headers'] = headers
        else:
            get_args['headers'] = {
                'Content-Type': 'application/json'
            }
        # _logger.warning('endpoint=%s' % endpoint_override)
        if endpoint_override:
            get_args['endpoint_override'] = endpoint_override

        # headers = request.headers if not headers else headers
        response = session.get(request.url, **get_args)
        kwargs = {}
        if error_message:
            kwargs['error_message'] = error_message

        self._translate_response(response, **kwargs)
        return self

    def delete(self, session,
               endpoint_override=None, headers=None,
               error_message=None):
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
        delete_args = {}
        if headers:
            delete_args['headers'] = headers
        else:
            delete_args['headers'] = {
                'Content-Type': 'application/json',
                'Accept': ''
            }

        if endpoint_override:
            delete_args['endpoint_override'] = endpoint_override

        response = session.delete(request.url,
                                  **delete_args)
        kwargs = {}
        if error_message:
            kwargs['error_message'] = error_message

        self._translate_response(response, has_body=False, **kwargs)
        return self

    # def update(self, session, prepend_key=True, has_body=True,
    #            endpoint_override=None, headers=None):
    #     """Update the remote resource based on this instance.
    #
    #     :param session: The session to use for making this request.
    #     :type session: :class:`~keystoneauth1.adapter.Adapter`
    #     :param prepend_key: A boolean indicating whether the resource_key
    #                         should be prepended in a resource update request.
    #                         Default to True.
    #
    #     :return: This :class:`Resource` instance.
    #     :raises: :exc:`~openstack.exceptions.MethodNotSupported` if
    #              :data:`Resource.allow_update` is not set to ``True``.
    #     """
    #     # The id cannot be dirty for an update
    #     self._body._dirty.discard("id")
    #
    #     # Only try to update if we actually have anything to update.
    #     if not any([self._body.dirty, self._header.dirty]):
    #         return self
    #
    #     if not self.allow_update:
    #         raise exceptions.MethodNotSupported(self, "update")
    #
    #     request = self._prepare_request(prepend_key=prepend_key)
    #     session = self._get_session(session)
    #
    #     if self.update_method == 'PATCH':
    #         response = session.patch(
    #             request.url, json=request.body, headers=request.headers)
    #     elif self.update_method == 'POST':
    #         response = session.post(
    #             request.url, json=request.body, headers=request.headers)
    #     elif self.update_method == 'PUT':
    #         response = session.put(
    #             request.url, json=request.body, headers=request.headers)
    #     else:
    #         raise exceptions.ResourceFailure(
    #             msg="Invalid update method: %s" % self.update_method)
    #
    #     self._translate_response(response, has_body=has_body)
    #     return self

    def update_no_id(self, session, prepend_key=True, has_body=True,
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
        # Only try to update if we actually have anything to update.
        if not any([self._body.dirty, self._header.dirty]):
            return self

        if not self.allow_update:
            raise exceptions.MethodNotSupported(self, "update")

        request = self._prepare_request(
            requires_id=False,
            prepend_key=prepend_key)
        session = self._get_session(session)

        # Build additional arguments to the DELETE call
        update_args = {}
        if headers:
            update_args['headers'] = headers
        else:
            update_args['headers'] = request.headers
            # Merge defaults into the headers
            update_args['headers']['Content-Type'] = 'application/json'
            # update_args['headers']['Accept'] = ''

        if endpoint_override:
            update_args['endpoint_override'] = endpoint_override

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
