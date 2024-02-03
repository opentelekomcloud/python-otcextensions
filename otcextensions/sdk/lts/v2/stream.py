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


class Stream(resource.Resource):
    resource_key = 'log_streams'
    resources_key = 'log_streams'
    base_path = '/groups/%(log_group_id)s/streams'

    # capabilities
    allow_create = True
    allow_fetch = False
    allow_commit = False
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'id',
    )

    # Properties
    #: Name of the log stream.
    name = resource.Body('log_stream_name')
    #: ID of the log stream.
    id = resource.Body('log_stream_id', alternate_id=True)
    #: Time when a log stream was created
    creation_time = resource.Body('creation_time')
    #: ID of the log group to which the log stream to be created will belong.
    log_group_id = resource.Body('log_group_id')
    #: Number of filters.
    filter_count = resource.Body('filter_count', type=int)
    #: Log stream tag.
    tag = resource.Body('tag')

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
        query_params = cls._query_mapping._transpose(api_filters, cls)
        uri = base_path % params
        uri_params = {}

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

            query_params.pop('marker', None)
            query_params.pop('limit', None)

            if cls.resources_key:
                resources = data[cls.resources_key]
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
                # We want that URI props are available on the resource
                raw_resource.update(uri_params)

                value = cls.existing(
                    microversion=microversion,
                    connection=session._get_connection(),
                    **raw_resource,
                )
                yield value

            return
