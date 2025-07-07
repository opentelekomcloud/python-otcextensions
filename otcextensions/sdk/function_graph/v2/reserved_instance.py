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
import os

from openstack import resource
from openstack import exceptions


class CronConfig(resource.Resource):
    name = resource.Body('name', type=str)
    cron = resource.Body('cron', type=str)
    count = resource.Body('count', type=int)
    start_time = resource.Body('start_time', type=int)
    expired_time = resource.Body('expired_time', type=int)


class TacticsConfig(resource.Resource):
    cron_configs = resource.Body(
        'cron_configs', type=list, list_type=CronConfig
    )


class ReservedInstance(resource.Resource):
    base_path = '/fgs/functions/%(function_urn)s/reservedinstances'
    requires_id = False
    _query_mapping = resource.QueryParameters(
        'marker', 'limit', 'urn'
    )

    # Capabilities
    allow_fetch = True
    allow_list = True
    allow_commit = True

    # Properties
    function_urn = resource.URI('function_urn', type=str)
    #: Number of reserved instances.
    count = resource.Body('count', type=int)
    #: Whether to enable the idle mode.
    idle_mode = resource.Body('idle_mode', type=bool)
    tactics_config = resource.Body('tactics_config', type=dict)

    # Attributes
    qualifier_type = resource.Body('qualifier_type', type=str)
    qualifier_name = resource.Body('qualifier_name', type=str)
    min_count = resource.Body('min_count', type=int)
    func_urn = resource.Body('func_urn', type=str)

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
        microversion = cls._get_microversion(session)

        if base_path is None:
            base_path = cls.base_path

        last_part = os.path.basename(base_path)
        if last_part == 'reservedinstanceconfigs':
            cls.resources_key = 'reserved_instances'
        else:
            cls.resources_key = 'reservedinstances'

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

            data = response.json()

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
