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


class Flavor(resource.Resource):
    base_path = '/flavors'

    resources_key = 'flavors'

    allow_list = True

    # Properties
    #: Version. *Type: str*
    version = resource.Body('version')
    #: cpu count. *Type: int*
    vcpus = resource.Body('cpu', type=int)
    #: ram. *Type: int*
    ram = resource.Body('ram', type=int)
    #: region. *Type: str*
    region = resource.Body('region')
    #: Disk capacity range (min,max). *Type: str*
    disk_range = resource.Body('diskrange', type=str)
    #: ID of a flavor. *Type: ID*
    flavor_id = resource.Body('flavor_id', alternate_id=True)

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
        microversion = cls._get_microversion_for_list(session)

        if base_path is None:
            base_path = cls.base_path
        cls._query_mapping._validate(params, base_path=base_path)
        query_params = cls._query_mapping._transpose(params)
        uri = base_path % params

        # Copy query_params due to weird mock unittest interactions
        response = session.get(
            uri,
            headers={"Accept": "application/json"},
            params=query_params.copy(),
            microversion=microversion)
        exceptions.raise_from_response(response)
        data = response.json()

        if 'versions' in data:
            for ver in data['versions']:
                version = ver['version']
                resources = ver[cls.resources_key]

                if not isinstance(resources, list):
                    resources = [resources]

                for raw_resource in resources:
                    raw_resource.pop("self", None)

                    value = cls.existing(
                        microversion=microversion,
                        connection=session._get_connection(),
                        version=version,
                        **raw_resource)
                    yield value
        else:
            return
