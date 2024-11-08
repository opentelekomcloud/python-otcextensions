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


class OperationSpec(resource.Resource):
    service_type = resource.Body('service_type')
    resource_type = resource.Body('resource_type')
    trace_names = resource.Body('trace_names', type=list)


class UserSpec(resource.Resource):
    user_group = resource.Body('user_group')
    user_list = resource.Body('user_list', type=list)


class FilterSpec(resource.Resource):
    condition = resource.Body('condition')
    is_support_filter = resource.Body('is_support_filter', type=bool)
    rule = resource.Body('rule', type=list)


class KeyEvent(resource.Resource):
    base_path = '/notifications'
    resources_key = 'notifications'
    allow_list = True
    allow_create = True
    allow_delete = True
    allow_commit = True
    requires_id = False

    _query_mapping = resource.QueryParameters('notification_name')
    notification_name = resource.Body('notification_name')
    operation_type = resource.Body('operation_type')
    operations = resource.Body('operations', type=list, list_type=dict)
    notify_user_list = resource.Body('notify_user_list', list_type=list)
    topic_id = resource.Body('topic_id')
    filter = resource.Body('filter', type=FilterSpec)
    status = resource.Body('status')
    notification_id = resource.Body('notification_id')
    notification_type = resource.Body('notification_type')
    project_id = resource.Body('project_id')
    create_time = resource.Body('create_time')

    def delete_key(self, session):
        path = f'{self.base_path}?notification_id={self.notification_id}'
        response = session.delete(path)
        exceptions.raise_from_response(response)
