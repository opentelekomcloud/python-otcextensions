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


class Server(resource.Resource):
    resource_key = ''
    resources_key = 'servers'
    base_path = '/dedicated-hosts/%(dedicated_host_id)s/servers'

    # capabilities
    allow_list = True

    #: Properties
    addresses = resource.Body('addresses', type=dict)
    created_at = resource.Body('created')
    dedicated_host_id = resource.URI('dedicated_host_id')
    flavor = resource.Body('flavor')
    metadata = resource.Body('metadata')
    status = resource.Body('status')
    tenant_id = resource.Body('tenant_id')
    updated_at = resource.Body('updated')
    user_id = resource.Body('user_id')
