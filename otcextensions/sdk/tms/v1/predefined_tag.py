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
from openstack import utils
from openstack import exceptions


class PredefinedTag(resource.Resource):
    resource_key = 'predefine_tag'
    base_path = '/predefine_tags'

    _query_mapping = resource.QueryParameters(
        'key', 'value', 'limit', 'marker', 'order_field', 'order_method')

    #: Properties
    marker = resource.Body('marker')
    total_count = resource.Body('total_count')
    tags = resource.Body('tags', type=list)
    action = resource.Body('action')
    old_tag = resource.Body('old_tag', type=dict)
    new_tag = resource.Body('new_tag', type=dict)

    #: Allow to create operation for this resource.
    allow_create = True
    #: Allow get operation for this resource.
    allow_fetch = False
    #: Allow update operation for this resource.
    allow_commit = True
    #: Allow to delete operation for this resource.
    allow_delete = True
    #: Allow list operation for this resource.
    allow_list = True
    #: Allow head operation for this resource.
    allow_head = False
    #: Allow patch operation for this resource.
    allow_patch = False

    #: Commits happen without header or body being dirty.
    allow_empty_commit = False

    #: Method for committing a resource (PUT, PATCH, POST)
    commit_method = "PUT"
    #: Method for creating a resource (POST, PUT)
    create_method = "POST"

    requires_id = False

    def _action(self, session, request_body):
        url = utils.urljoin(self.base_path, 'action')
        response = session.post(url, json=request_body)
        exceptions.raise_from_response(response)

    def add_tag(self, session, key, value):
        request_body = {
            "action": "create",
            "tags": [{
                "key": key,
                "value": value
            }]
        }
        self._action(session, request_body)

    def delete_tag(self, session, key, value):
        request_body = {
            "action": "delete",
            "tags": [{
                "key": key,
                "value": value
            }]
        }
        self._action(session, request_body)

    def _prepare_request_body(
        self,
        patch,
        prepend_key,
        *,
        resource_request_key=None,
    ):
        return self._body.dirty
