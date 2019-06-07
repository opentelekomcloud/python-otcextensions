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
from openstack import utils



class Resource(resource.Resource):

    query_marker_key = 'start_number'

    _query_mapping = resource.QueryParameters(
        'marker', 'limit',
        marker='start_number',
        limit='limit'
    )

    @classmethod
    def _get_next_link(cls, uri, response, data, marker, limit, total_yielded):
        # AS service pagination. Returns query for the next page
        next_link = None
        params = {}
        if total_yielded < data['total_number']:
            next_link = uri
            params['marker'] = total_yielded
            params['limit'] = limit
        else:
            next_link = None
        query_params = cls._query_mapping._transpose(params)
        return next_link, query_params

    @staticmethod
    def find_value_by_accessor(input_dict, accessor):
        """Gets value from a dictionary using a dotted accessor"""
        current_data = input_dict
        for chunk in accessor.split('.'):
            if isinstance(current_data, dict):
                current_data = current_data.get(chunk, {})
            else:
                return None
        return current_data

    @classmethod
    def _prepare_override_args(cls,
                               endpoint_override=None,
                               request_headers=None,
                               additional_headers=None,
                               requests_auth=None):
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

        if requests_auth:
            req_args['requests_auth'] = requests_auth

        return req_args

    # Due to the other LIST url need to override
    # It is not efficient (as of implementation) to extend general list
    # with support of other url just for one service
    @classmethod
    def list_ext(cls, session, paginated=False,
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

        # pop scaling_group_id, as it should not be also present in the query
        scaling_group_id = params.pop('scaling_group_id', None)
        uri_params = {}

        if scaling_group_id:
            uri_params = {'scaling_group_id': scaling_group_id}

        cls._query_mapping._validate(params, base_path=cls.base_path)
        query_params = cls._query_mapping._transpose(params)
        uri = None
        if not hasattr(cls, 'list_path'):
            uri = cls.base_path % uri_params
        else:
            uri = cls.list_path % uri_params

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
                **get_args
            )
            exceptions.raise_from_response(response)
            data = response.json()

            # Discard any existing pagination keys
            query_params.pop('marker', None)
            query_params.pop('limit', None)

            if cls.resources_key:
                resources = cls.find_value_by_accessor(data, cls.resources_key)
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

    def _action(self, session, body):
        """Preform alarm actions given the message body.

        """
        # if getattr(self, 'endpoint_override', None):
        #     # If we have internal endpoint_override - use it
        #     endpoint_override = self.endpoint_override
        url = utils.urljoin(self.base_path, self.id, 'action')
        return session.post(
            url,
            # endpoint_override=endpoint_override,
            json=body)
