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


class Whitelist(resource.Resource):
    base_path = '/vpc-endpoint-services/%(endpoint_service_id)s/permissions'
    resources_key = 'permissions'

    # capabilities
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'permission', 'sort_key', 'sort_dir', 'limit', 'offset'
    )

    # URI properties
    endpoint_service_id = resource.URI('endpoint_service_id')

    # Properties
    #: Specifies when the whitelist record is added.
    created_at = resource.Body('created_at')
    #: Specifies the description of a whitelist record of a VPC endpoint
    #:  service.
    description = resource.Body('description')
    #: Specifies the unique ID of the permission.
    id = resource.Body('id')
    #: Lists the whitelist records.
    permission = resource.Body('permission')

    def _action(self, session, action, domains=[]):
        """Preform actions on the request body."""
        uri = utils.urljoin(self.base_path % self._uri.attributes, 'action')
        for ix, domain in enumerate(domains):
            if not domain.startswith('iam:domain::'):
                domains[ix] = 'iam:domain::' + domain

        body = {'permissions': domains, 'action': action}
        response = session.post(uri, json=body)
        exceptions.raise_from_response(response)
        for raw_resource in response.json()[self.resources_key]:
            yield Whitelist.existing(permission=raw_resource)

    def add(self, session, domains=[]):
        """Add whitelist."""
        return self._action(session, 'add', domains)

    def remove(self, session, domains=[]):
        """Remove whitelist."""
        return self._action(session, 'remove', domains)
