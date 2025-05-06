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
# import six
from openstack import exceptions
from openstack import resource


class AppConsumption(resource.Resource):
    base_path = '/apps/%(app_name)s/streams/%(stream_name)s'

    resources_key = 'partition_consuming_states'

    allow_list = True

    #: Name of the app to be queried.
    app_name = resource.URI('app_name')
    #: Name of the stream to be queried.
    stream_name = resource.URI('stream_name')

    _query_mapping = resource.QueryParameters(
        'checkpoint_type', 'start_partition_id', 'limit'
    )

    # Properties
    #: Partition Id.
    partition_id = resource.Body('partition_id')
    #: Partition Sequence Number
    sequence_number = resource.Body('sequence_number')
    #: Partition data latest offset.
    latest_offset = resource.Body('latest_offset', type=int)
    #: Partition data earliest offset.
    earliest_offset = resource.Body('earliest_offset', type=int)
    #: Type of the checkpoint.
    #:  \nLAST_READ: Only sequence numbers are recorded in databases.
    checkpoint_type = resource.Body('checkpoint_type')
    #: Partition Status.
    status = resource.Body('status')


class App(resource.Resource):
    base_path = '/apps'

    resources_key = 'apps'

    allow_create = True
    allow_list = True
    allow_delete = True
    allow_fetch = True

    _query_mapping = resource.QueryParameters(
        'limit', 'start_app_name', 'stream_name'
    )

    # Properties
    #: Unique identifier of the app.
    app_id = resource.Body('app_id', alternate_id=True)
    #: List of associated streams.
    commit_checkpoint_stream_names = \
        resource.Body('commit_checkpoint_stream_names', type=list)
    #: Timestamp at which the DIS app was created.
    created_at = resource.Body('create_time', type=int)
    #: App name.
    name = resource.Body('app_name')
    #: Stream Name
    stream_name = resource.Body('stream_name')

    @classmethod
    def list(cls, session, paginated=True, base_path=None,
             allow_unknown_params=False, **params):

        if not cls.allow_list:
            raise exceptions.MethodNotSupported(cls, "list")
        session = cls._get_session(session)
        microversion = cls._get_microversion(session)

        if base_path is None:
            base_path = cls.base_path
        params = cls._query_mapping._validate(
            params, base_path=base_path,
            allow_unknown_params=allow_unknown_params)

        query_params = cls._query_mapping._transpose(params, cls)
        uri = base_path % params

        while uri:
            # Copy query_params due to weird mock unittest interactions
            response = session.get(
                uri,
                headers={"Accept": "application/json"},
                params=query_params.copy(),
                microversion=microversion)
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

            if resources and paginated:
                uri, next_params = cls._get_next_link(
                    uri, response, data)
                query_params.update(next_params)
            else:
                return

    @classmethod
    def _get_next_link(cls, uri, response, data):
        # RDS service pagination. Returns query for the next page
        next_link = None
        params = {}
        if 'has_more_app' in data and data['has_more_app']:
            next_link = uri
            params['start_app_name'] = data['apps'][-1]['app_name']
        else:
            next_link = None
        query_params = cls._query_mapping._transpose(params, cls)
        return next_link, query_params
