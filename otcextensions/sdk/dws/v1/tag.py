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
from openstack import utils


class Tag(resource.Resource):
    base_path = '/clusters/%(cluster_id)s/tags'

    # Properties
    cluster_id = resource.URI('cluster_id')
    resources_key = 'tags'
    resource_key = 'tag'

    # Capabilities
    allow_list = True
    allow_create = True
    allow_delete = True

    _query_mapping = resource.QueryParameters('key')

    # Properties
    key = resource.Body('key')
    value = resource.Body('value')

    def manage_tags_batch(self, session, cluster_id, tags, action):
        """
        Manage tags in batch for a cluster (create or delete).
        """
        self.last_tags_sent = tags
        uri = utils.urljoin('clusters', cluster_id, 'tags/action')
        body = {'action': action, 'tags': tags}
        response = session.post(uri, json=body)
        return self._translate_response(response)

    def _translate_response(self, response, has_body=None, error_message=None):
        """
        Translates the server response into Tag objects.
        """
        if has_body is None:
            has_body = self.has_body
        exceptions.raise_from_response(response, error_message=error_message)
        tags_list = []
        if has_body and response.status_code == 204:
            if hasattr(self, 'last_tags_sent'):
                tags_list = [
                    Tag.existing(**tag_data)
                    for tag_data in self.last_tags_sent
                ]
        return tags_list
