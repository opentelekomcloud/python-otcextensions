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
#
from openstack import exceptions
from openstack import resource
from openstack import utils


class Connection(resource.Resource):
    base_path = '/vpc-endpoint-services/%(endpoint_service_id)s/connections'
    resources_key = 'connections'

    # capabilities
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'id',
        'limit',
        'marker_id',
        'offset',
        'sort_dir',
        'sort_key',
    )

    # URI properties
    endpoint_service_id = resource.URI('endpoint_service_id')

    # Properties
    #: Creation time of the VPC endpoint.
    created_at = resource.Body('created_at')
    #: User's domain ID.
    domain_id = resource.Body('domain_id')
    #: ID of the VPC endpoint.
    id = resource.Body('id')
    #: Packet ID of the VPC endpoint.
    marker_id = resource.Body('marker_id', type=int)
    #: Connection status of the VPC endpoint.
    status = resource.Body('status')
    #: Update time of the VPC endpoint.
    updated_at = resource.Body('updated_at')

    def _action(self, session, action, endpoints=[]):
        """Preform actions given the message body."""
        uri = utils.urljoin(self.base_path % self._uri.attributes, 'action')
        body = {'endpoints': endpoints, 'action': action}
        response = session.post(uri, json=body)
        exceptions.raise_from_response(response)
        for raw_resource in response.json()[self.resources_key]:
            yield Connection.existing(**raw_resource)

    def accept(self, session, endpoints=[]):
        """Accept connections."""
        return self._action(session, 'receive', endpoints)

    def reject(self, session, endpoints=[]):
        """Reject Connections."""
        return self._action(session, 'reject', endpoints)
