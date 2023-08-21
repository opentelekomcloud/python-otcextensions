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


class Stream(resource.Resource):
    base_path = '/streams'

    resources_key = 'stream_info_list'

    allow_create = True
    allow_list = True
    allow_commit = True
    allow_delete = True
    allow_fetch = True
    allow_patch = True

    _query_mapping = resource.QueryParameters('limit', 'start_stream_name')

    # Properties
    #: Minimum number of partitions for automatic scale-down when
    #:  auto scaling is enabled.
    auto_scale_min_partition_count = \
        resource.Body('auto_scale_min_partition_count', type=int)
    #: Maximum number of partitions for automatic scale-up when
    #:  auto scaling is enabled.
    auto_scale_max_partition_count = \
        resource.Body('auto_scale_max_partition_count', type=int)
    #: Data compression type. The following types are available:
    #: \nsnappy
    #: \ngzip
    #: \nzip
    #: \nData is not compressed by default.
    compression_format = resource.Body('compression_format')
    #: Timestamp at which the DIS stream was created.
    created_at = resource.Body('create_time', type=int)
    #: Partition Count of a stream before updating.
    current_partition_count = \
        resource.Body('current_partition_count', type=int)
    #: Data retention period.
    #: \nValue range: 24–72
    #: \nUnit: hour
    #: \nDefault value: 24
    data_duration = resource.Body('data_duration', type=int)
    #: Source data type.
    data_type = resource.Body('data_type', type=str)
    #: Specifies whether there are more matching partitions
    #:  of the DIS stream to list.
    has_more_partitions = resource.Body('has_more_partitions', type=bool)
    #: Specifies whether to enable auto scaling.
    #: \n`true`: auto scaling is enabled.
    #: \n`false`: auto scaling is disabled.
    is_auto_scale_enabled = resource.Body('auto_scale_enabled', type=bool)
    #: Stream name.
    name = resource.Body('stream_name', alias='stream_name')
    #: Number of partitions.
    #:  Partitions are the base throughput unit of the DIS stream.
    partition_count = resource.Body('partition_count', type=int)
    #: A list of partitions that comprise the DIS stream.
    partitions = resource.Body('partitions', type=list, list_type=dict)
    #: Total number of readable partitions (including
    #:  partitions in ACTIVE and DELETED state).
    readable_partition_count = \
        resource.Body('readable_partition_count', type=int)
    #: Period for storing data in units of hours.
    retention_period = resource.Body('retention_period', type=int)
    #: Current status of the stream. Possible values:
    #: \n`CREATING`: The stream is being created.
    #: \n`RUNNING`: The stream is running.
    #: \n`TERMINATING`: The stream is being deleted.
    #: \n`TERMINATED`: The stream has been deleted.
    status = resource.Body('status')
    #: Stream Id.
    stream_id = resource.Body('stream_id', alternate_id=True)
    #: Stream type.
    #: \n`COMMON`: a common stream. The bandwidth is 1 MB/s.
    #: \n`ADVANCED`: an advanced stream. The bandwidth is 5 MB/s.
    stream_type = resource.Body('stream_type')
    #: Enterprise project of a stream.
    sys_tags = resource.Body('sys_tags', type=list, list_type=dict)
    #: List of stream tags.
    tags = resource.Body('tags', type=list, list_type=dict)
    #: Number of the target partitions. The value is an integer greater than 0.
    target_partition_count = resource.Body('target_partition_count', type=int)
    #: Timestamp at which the DIS stream was most recently modified.
    updated_at = resource.Body('last_modified_time', type=int)
    #: Total number of writable partitions (including
    #:  partitions in ACTIVE state only).
    writable_partition_count = \
        resource.Body('writable_partition_count', type=int)

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
        # DIS service pagination. Returns query for the next page
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
