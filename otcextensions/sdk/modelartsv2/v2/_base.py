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
#
from openstack import exceptions
from openstack import resource


class Resource(resource.Resource):

    @classmethod
    def list(
        cls,
        session,
        paginated=True,
        base_path=None,
        allow_unknown_params=False,
        *,
        microversion=None,
        **params,
    ):
        """This method is a generator which yields resource objects.

        This resource object list generator handles pagination and takes query
        params for response filtering.

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param bool paginated: ``True`` if a GET to this resource returns
            a paginated series of responses, or ``False`` if a GET returns only
            one page of data. **When paginated is False only one page of data
            will be returned regardless of the API's support of pagination.**
        :param str base_path: Base part of the URI for listing resources, if
            different from :data:`~openstack.resource.Resource.base_path`.
        :param bool allow_unknown_params: ``True`` to accept, but discard
            unknown query parameters. This allows getting list of 'filters' and
            passing everything known to the server. ``False`` will result in
            validation exception when unknown query parameters are passed.
        :param str microversion: API version to override the negotiated one.
        :param dict params: These keyword arguments are passed through the
            :meth:`~openstack.resource.QueryParamter._transpose` method
            to find if any of them match expected query parameters to be sent
            in the *params* argument to
            :meth:`~keystoneauth1.adapter.Adapter.get`. They are additionally
            checked against the :data:`~openstack.resource.Resource.base_path`
            format string to see if any path fragments need to be filled in by
            the contents of this argument.
            Parameters supported as filters by the server side are passed in
            the API call, remaining parameters are applied as filters to the
            retrieved results.

        :return: A generator of :class:`Resource` objects.
        :raises: :exc:`~openstack.exceptions.MethodNotSupported` if
            :data:`Resource.allow_list` is not set to ``True``.
        :raises: :exc:`~openstack.exceptions.InvalidResourceQuery` if query
            contains invalid params.
        """
        if not cls.allow_list:
            raise exceptions.MethodNotSupported(cls, "list")

        session = cls._get_session(session)

        if microversion is None:
            microversion = cls._get_microversion(session, action="list")

        if base_path is None:
            base_path = cls.base_path

        api_filters = cls._query_mapping._validate(
            params,
            base_path=base_path,
            allow_unknown_params=True,
        )
        client_filters = {}
        # Gather query parameters which are not supported by the server
        for k, v in params.items():
            if (
                # Known attr
                hasattr(cls, k)
                # Is real attr property
                and isinstance(getattr(cls, k), resource.Body)
                # not included in the query_params
                and k not in cls._query_mapping._mapping.keys()
            ):
                client_filters[k] = v
        query_params = cls._query_mapping._transpose(api_filters, cls)
        uri = base_path % params
        uri_params = {}

        for k, v in params.items():
            # We need to gather URI parts to set them on the resource later
            if hasattr(cls, k) and isinstance(getattr(cls, k), resource.URI):
                uri_params[k] = v

        def _dict_filter(f, d):
            """Dict param based filtering"""
            if not d:
                return False
            for key in f.keys():
                if isinstance(f[key], dict):
                    if not _dict_filter(f[key], d.get(key, None)):
                        return False
                elif d.get(key, None) != f[key]:
                    return False
            return True

        # Track the total number of resources yielded so we can paginate
        # swift objects
        total_yielded = 0
        offset = query_params.get("offset", 0)
        while uri:
            last_marker = query_params.pop("marker", None)
            # Copy query_params due to weird mock unittest interactions
            response = session.get(
                uri,
                headers={"Accept": "application/json"},
                params=query_params.copy(),
                microversion=microversion,
            )
            exceptions.raise_from_response(response)
            data = response.json()

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
                # We want that URI props are available on the resource
                raw_resource.update(uri_params)

                value = cls.existing(
                    microversion=microversion,
                    connection=session._get_connection(),
                    **raw_resource,
                )
                marker = value.id
                filters_matched = True
                # Iterate over client filters and return only if matching
                for key in client_filters.keys():
                    if isinstance(client_filters[key], dict):
                        if not _dict_filter(
                            client_filters[key], value.get(key, None)
                        ):
                            filters_matched = False
                            break
                    elif value.get(key, None) != client_filters[key]:
                        filters_matched = False
                        break

                if filters_matched:
                    yield value
            total_yielded = total_yielded + len(resources)
            total_count = total_yielded
            if paginated and hasattr(cls, "resources_count_key"):
                total_count = data.get(cls.resources_count_key, total_count)

            if resources and paginated and total_count > total_yielded:
                try:
                    if marker == last_marker:
                        # If next page marker is same as what we were just
                        # asked something went terribly wrong. Some ancient
                        # services had bugs.
                        raise exceptions.SDKException(
                            "Endless pagination loop detected, aborting"
                        )
                except KeyError:
                    # do nothing, exception handling is cheaper then "if"
                    pass
                offset += 1
                query_params.update(offset=offset, marker=marker)
            else:
                return

    @classmethod
    def _get_one_match(cls, name_or_id, results):
        """Given a list of results, return the match"""
        for result in results:
            id_value = str(result.id)
            name_value = result.dataset_name

            if (id_value == name_or_id) or (name_value == name_or_id):
                return result
