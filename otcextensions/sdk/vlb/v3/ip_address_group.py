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


class IpAddressGroup(resource.Resource):
    resource_key = 'ipgroup'
    resources_key = 'ipgroups'
    base_path = '/elb/ipgroups'

    # capabilities
    allow_create = True
    allow_fetch = True
    allow_commit = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'project_id', 'description', 'name', 'ip_list',
        'enterprise_project_id'
    )

    # Properties
    #: Provides supplementary information about the IP address group.
    description = resource.Body('description', type=str)
    #: Specifies the project ID of the IP address group.
    project_id = resource.Body('project_id')
    #: Specifies the IP address group name.
    name = resource.Body('name', type=str)
    #: The ID of the project this load balancer is associated with.
    ip_list = resource.Body('ip_list', type=list, list_type=dict)
    #: The ID of the project this load balancer is associated with.
    enterprise_project_id = resource.Body('enterprise_project_id', type=str)

    def update_ip_addresses(self, session, **attrs):
        """Method to update ip addresses in ip address group

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param kwargs attrs: Dictionary to update ip address group
        """
        url = utils.urljoin(self.base_path, self.id,
                            '/iplist/create-or-update')
        body = {
            'ipgroup': attrs
        }
        response = session.post(url, json=body)
        return self._to_object(session, response)

    def delete_ip_addresses(self, session, **attrs):
        """Method to delete ip addresses from ip address group

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param kwargs attrs: Dictionary to delete ip address group
        """
        url = utils.urljoin(self.base_path, self.id, '/iplist/batch-delete')
        body = {
            'ipgroup': attrs
        }
        response = session.post(url, json=body)
        return self._to_object(session, response)

    def _to_object(self, session, response):
        has_body = (
            self.has_body
            if self.create_returns_body is None
            else self.create_returns_body
        )
        microversion = self._get_microversion(session, action='create')
        self.microversion = microversion
        self._translate_response(response, has_body=has_body)
        if self.has_body and self.create_returns_body is False:
            return self.fetch(session)
        return self
