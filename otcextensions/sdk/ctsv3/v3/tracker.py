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


class ObsInfoSpec(resource.Resource):
    bucket_name = resource.Body('bucket_name')
    file_prefix_name = resource.Body('file_prefix_name')
    is_obs_created = resource.Body('is_obs_created', type=bool)
    compress_type = resource.Body('compress_type')
    is_sort_by_service = resource.Body('is_sort_by_service', type=bool)


class LtsSpec(resource.Resource):
    is_lts_enabled = resource.Body('is_lts_enabled', type=bool)
    log_group_name = resource.Body('log_group_name')
    log_topic_name = resource.Body('log_topic_name')


class Tracker(resource.Resource):
    base_path = '/trackers'
    resources_key = 'trackers'
    allow_list = True
    allow_create = True
    allow_delete = True
    allow_commit = True
    requires_id = False

    _query_mapping = resource.QueryParameters('tracker_name')
    id = resource.Body('id')
    create_time = resource.Body('create_time')
    lts = resource.Body('lts', type=LtsSpec)
    tracker_type = resource.Body('tracker_type')
    domain_id = resource.Body('domain_id')
    project_id = resource.Body('project_id')
    tracker_name = resource.Body('tracker_name')
    status = resource.Body('status')
    detail = resource.Body('detail')
    obs_info = resource.Body('obs_info', type=ObsInfoSpec)
    group_id = resource.Body('group_id')
    stream_id = resource.Body('stream_id')

    def delete_tracker(self, session):
        path = f'{self.base_path}?tracker_name={self.tracker_name}'
        response = session.delete(path)
        exceptions.raise_from_response(response)
