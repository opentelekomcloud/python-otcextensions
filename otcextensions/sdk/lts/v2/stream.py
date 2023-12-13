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
