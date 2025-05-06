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


class SlaReportsValue(resource.Resource):
    timestamp = resource.Body('timestamp', type=int)
    value = resource.Body('value', type=int)


class Metric(resource.Resource):
    base_path = '/fgs/functions/statistics'
    # Capabilities
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'filter', 'period', 'option',
        'limit', 'marker'
    )

    # Attributes
    count = resource.Body('count', type=list, list_type=SlaReportsValue)
    duration = resource.Body('duration', type=list, list_type=SlaReportsValue)
    fail_count = resource.Body(
        'fail_count', type=list, list_type=SlaReportsValue
    )
    fail_rate = resource.Body(
        'fail_rate', type=list, list_type=SlaReportsValue
    )
    max_duration = resource.Body(
        'max_duration', type=list, list_type=SlaReportsValue
    )
    min_duration = resource.Body(
        'min_duration', type=list, list_type=SlaReportsValue
    )
    reject_count = resource.Body(
        'reject_count', type=list, list_type=SlaReportsValue
    )
    function_error_count = resource.Body(
        'function_error_count', type=list, list_type=SlaReportsValue
    )
    system_error_count = resource.Body(
        'system_error_count', type=list, list_type=SlaReportsValue
    )
    reserved_instance_num = resource.Body(
        'reserved_instance_num', type=list, list_type=SlaReportsValue
    )
    concurrency_num = resource.Body(
        'concurrency_num', type=list, list_type=SlaReportsValue
    )

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
        if 'filter' in params:
            if params['filter'] == 'monitor_data':
                cls.resources_key = 'monitor_data'
            elif params['filter'] == 'monthly_report':
                cls.resources_key = 'monthly_report'
        session = cls._get_session(session)
        microversion = cls._get_microversion(session)

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
