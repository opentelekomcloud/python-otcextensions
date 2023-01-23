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
from openstack import resource
from openstack import exceptions


class FlavorDetail(resource.Resource):
    #: Attribute type
    type = resource.Body('type')
    #: Attribute value
    value = resource.Body('value', type=str)
    #: Attribute Unit
    unit = resource.Body('unit')


class Flavor(resource.Resource):
    base_path = '/node-types'

    resources_key = 'node_types'

    # capabilities
    allow_list = True

    # Properties
    #: Name of a node type
    name = resource.Body('spec_name')
    #: Name of a node type
    spec_name = resource.Body('spec_name')
    #: Node type details
    detail = resource.Body('detail', type=list, list_type=FlavorDetail)

    #: Memory
    ram = resource.Computed('ram')
    #: Disk Type
    disk_type = resource.Body('disk_type')
    #: Disk Size
    disk_size = resource.Computed('disk_size')
    #: Availability Zones
    availability_zones = resource.Computed('availability_zones')

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
            raise exceptions.MethodNotSupported(cls, 'list')

        session = cls._get_session(session)
        if microversion is None:
            microversion = cls._get_microversion(session, action='list')

        if base_path is None:
            base_path = cls.base_path
        api_filters = cls._query_mapping._validate(
            params,
            base_path=base_path,
            allow_unknown_params=True,
        )
        client_filters = dict()
        query_params = cls._query_mapping._transpose(api_filters, cls)
        uri = base_path % params
        uri_params = {}

        limit = query_params.get('limit')

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
        while uri:
            # Copy query_params due to weird mock unittest interactions
            response = session.get(
                uri,
                headers={"Accept": "application/json"},
                params=query_params.copy(),
                microversion=microversion,
            )
            exceptions.raise_from_response(response)
            data = response.json()

            # Discard any existing pagination keys
            last_marker = query_params.pop('marker', None)
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
                # We want that URI props are available on the resource
                raw_resource.update(uri_params)

                value = cls.existing(
                    microversion=microversion,
                    connection=session._get_connection(),
                    **raw_resource,
                )
                for detail in value.detail:
                    if detail.type == 'mem':
                        setattr(value, 'ram', detail.value)
                    elif detail.type == 'SSD':
                        setattr(value, 'disk_type', 'SSD')
                        setattr(value, 'disk_size', detail.value)
                    elif detail.type == 'availableZones':
                        setattr(value, 'availability_zones', detail.value)
                    else:
                        setattr(value, detail.type.lower(), detail.value)
                marker = value.id
                filters_matched = True
                # Iterate over client filters and return only if matching
                for key in client_filters.keys():
                    if isinstance(client_filters[key], dict):
                        if not _dict_filter(
                                client_filters[key], value.get(key, None)):
                            filters_matched = False
                            break
                    elif value.get(key, None) != client_filters[key]:
                        filters_matched = False
                        break

                if filters_matched:
                    yield value
                total_yielded += 1

            if resources and paginated:
                uri, next_params = cls._get_next_link(
                    uri, response, data, marker, limit, total_yielded
                )
                try:
                    if next_params['marker'] == last_marker:
                        # If next page marker is same as what we were just
                        # asked something went terribly wrong. Some ancient
                        # services had bugs.
                        raise exceptions.SDKException(
                            'Endless pagination loop detected, aborting'
                        )
                except KeyError:
                    # do nothing, exception handling is cheaper then "if"
                    pass
                query_params.update(next_params)
            else:
                return
