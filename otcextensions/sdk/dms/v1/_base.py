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


class Resource(resource.Resource):

    @classmethod
    def find(cls, session, name_or_id, ignore_missing=True, **params):
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
        session = cls._get_session(session)
        # Try to short-circuit by looking directly for a matching ID.
        try:
            match = cls.existing(
                id=name_or_id,
                connection=session._get_connection(),
                **params)
            return match.fetch(session, **params)
        except exceptions.SDKException:
            pass

        data = cls.list(session, **params)

        result = cls._get_one_match(name_or_id, data)
        if result is not None:
            return result

        if ignore_missing:
            return None
        raise exceptions.ResourceNotFound(
            "No %s found for %s" % (cls.__name__, name_or_id))

    @classmethod
    def list_override(cls, session, **params):
        # Some really stupid APIs are not following any guidelines
        # and are under other endpoint (without project id),
        # so we need to hack on the endpoint_override yet again
        session = cls._get_session(session)

        base_path = cls.base_path
        params.pop('paginated', None)
        params.pop('base_path', None)
        params = cls._query_mapping._validate(
            params, base_path=base_path,
            allow_unknown_params=False)
        query_params = cls._query_mapping._transpose(params, cls)
        uri = base_path % params
        region_id = None

        # Copy query_params due to weird mock unittest interactions
        response = session.get(
            uri,
            endpoint_override=session.endpoint_override.replace(
                '%(project_id)s', ''),
            headers={"Accept": "application/json"},
            params=query_params.copy())
        exceptions.raise_from_response(response)
        data = response.json()
        if 'regionId' in data:
            region_id = data['regionId']

        if cls.resources_key:
            resources = data[cls.resources_key]
        else:
            resources = data

        if not isinstance(resources, list):
            resources = [resources]

        for raw_resource in resources:
            if region_id:
                raw_resource['region_id'] = region_id
            value = cls.existing(
                connection=session._get_connection(),
                **raw_resource)
            yield value
