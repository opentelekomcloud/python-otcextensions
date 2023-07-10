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
from openstack import utils


class RecordSpec(resource.Resource):
    #: Data to be uploaded.
    data = resource.Body('data')
    #: Hash value of the data to be written to the partition.
    #:  The hash value overwrites the hash value of partition_key.
    explicit_hash_key = resource.Body('explicit_hash_key')
    #: Partition ID of the stream.
    partition_id = resource.Body('partition_id')
    #: Partition to which data is written.
    partition_key = resource.Body('partition_key')


class Data(resource.Resource):
    base_path = '/records'

    resources_key = 'records'

    _query_mapping = resource.QueryParameters(
        'stream-name', 'partition-id', 'cursor-type',
        'starting-sequence-number', 'timestamp', 'stream_id',
    )

    allow_create = True
    allow_fetch = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'partition-cursor', 'max_fetch_bytes',
    )

    # Properties
    #: Partition key set when data is being uploaded.
    partition_key = resource.Body('partition_key')
    #: Sequence number of the data record.
    sequence_number = resource.Body('sequence_number')
    #: Downloaded data. The downloaded data is the
    #:  serialized binary data (Base64-encoded character string).
    data = resource.Body('data')
    #: Data cursor
    #: \nValue: 1 to 512 characters
    #: \nNote:
    #: \nThe validity period of a data cursor is 5 minutes.
    #: \nMinimum: 1
    #: \nMaximum: 512
    partition_cursor = resource.Body('partition_cursor')
    #: Timestamp when the record is written to DIS.
    timestamp = resource.Body('timestamp', type=int)
    #: Timestamp type.
    timestamp_type = resource.Body('timestamp_type')
    #: List of records to be uploaded.
    records = resource.Body('records', type=list, list_type=RecordSpec)
    #: Unique ID of the stream. If no stream is found based on stream_name
    #:  and stream_id is not empty, stream_id is used to search for the stream.
    stream_id = resource.Body('stream_id')
    #: Name of the stream.
    stream_name = resource.Body('stream_name')

    def get_data_cursor(self, session, **params):
        uri = utils.urljoin('cursors')
        res = session.get(uri, params=params)
        self._translate_response(res)
        return self

    @classmethod
    def list(cls, session, paginated=True, base_path=None,
             allow_unknown_params=False, **params):

        if not cls.allow_list:
            raise exceptions.MethodNotSupported(cls, "list")
        session = cls._get_session(session)
        microversion = cls._get_microversion(session, action='list')

        if base_path is None:
            base_path = cls.base_path
        params = cls._query_mapping._validate(
            params, base_path=base_path,
            allow_unknown_params=allow_unknown_params)

        query_params = cls._query_mapping._transpose(params, cls)
        uri = base_path % params

        limit = query_params.get('limit')

        while uri:
            # Copy query_params due to weird mock unittest interactions
            response = session.get(
                uri,
                headers={"Accept": "application/json"},
                params=query_params.copy(),
                microversion=microversion)
            exceptions.raise_from_response(response)
            data = response.json()
            # Discard any existing pagination keys
            query_params.pop('start_stream_name', None)
            query_params.pop('limit', None)

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
                    uri, response, data, limit)
                query_params.update(next_params)
            else:
                return

    @classmethod
    def _get_next_link(cls, uri, response, data, limit):
        # RDS service pagination. Returns query for the next page
        next_link = None
        params = {}
        if 'has_more_streams' in data and data['has_more_streams']:
            next_link = uri
            params['start_stream_name'] = data['stream_names'][-1]
            params['limit'] = limit
        else:
            next_link = None
        query_params = cls._query_mapping._transpose(params, cls)
        return next_link, query_params
