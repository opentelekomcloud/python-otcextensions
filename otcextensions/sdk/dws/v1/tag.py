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

    @classmethod
    def manage_tags_batch(cls, session, project_id, cluster_id, tags, action):
        """
        Manage tags in batch for a cluster (create or delete).
        """
        full_url = f"https://dws.eu-de.otc.t-systems.com/v1.0/{project_id}/clusters/{cluster_id}/tags/action"
        print(full_url)
        body = {'action': action, 'tags': tags}
        return session.post(full_url, json=body)
