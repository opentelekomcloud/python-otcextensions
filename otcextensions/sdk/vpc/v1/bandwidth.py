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


class PublicIPInfo(resource.Resource):
    #: Properties
    #: Specifies the ID of the EIP that uses the bandwidth.
    ip_version = resource.Body('publicip_id', type=int)
    #: Specifies the IP address version.
    publicip_id = resource.Body('publicip_id')
    #: Specifies the obtained EIP if only IPv4 EIPs are available.
    publicip_address = resource.Body('publicip_address')
    #: Specifies the EIP type.
    publicip_type = resource.Body('publicip_type', default='5_bgp')


class Bandwidth(resource.Resource):
    resources_key = 'bandwidths'
    resource_key = 'bandwidth'
    base_path = '/%(version)s/%(project_id)s/bandwidths'

    # capabilities
    allow_create = True
    allow_fetch = True
    allow_commit = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters()

    # Properties
    #: Specifies the bandwidth name.
    #: *Type: dict*
    name = resource.Body('name', type=str)
    #: Specifies the bandwidth size.
    #: *Type: dict*
    size = resource.Body('size', type=int)
    #: Specifies whether the bandwidth is shared or dedicated.
    share_type = resource.Body('share_type', type=str)
    #: Specifies the project ID.
    publicip_info = resource.Body('publicip_info', type=list,
                                  elements=PublicIPInfo)
    #: Specifies the project ID.
    project_id = resource.URI('project_id')
    #: Specifies the bandwidth type.
    bandwidth_type = resource.Body('bandwidth_type', type=str, default='share')
    #: Specifies that the bandwidth is billed by bandwidth.
    charge_mode = resource.Body('charge_mode', type=str)
    #: Specifies the bill information.
    billing_info = resource.Body('billing_info', type=str)
    #: Specifies the enterprise project ID.
    enterprise_project_id = resource.Body('enterprise_project_id', type=str)
    #: Specifies the bandwidth status.
    status = resource.Body('status', type=str)
    #: Specifies the time (UTC) when the bandwidth is created.
    created_at = resource.Body('created_at', type=str)
    #: Specifies the time (UTC) when the bandwidth is updated.
    updated_at = resource.Body('updated_at', type=str)

    def add_eip_to_bandwidth(self, session, version,
                             publicip_info, project_id):
        """Method to add an EIP to shared bandwidth.

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param list publicip_info: List from dictionaries which describes eips.
        """
        path = self.base_path % {'project_id': project_id, 'version': version}
        print(path)
        url = utils.urljoin(path, self.id, 'insert')
        body = {'bandwidth': {'publicip_info': publicip_info}}
        response = session.post(url, json=body)
        return self._to_object(session, response)

    def remove_eip_from_bandwidth(self, session, project_id,
                                  version, **attrs):
        """Method to remove an EIP from shared bandwidth.

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param dict attrs: Describes eip info.
        """
        path = self.base_path % {'project_id': project_id, 'version': version}
        url = utils.urljoin(path, self.id, 'remove')
        body = {'bandwidth': attrs}
        response = session.post(url, json=body)
        return self._to_object(session, response)

    def update_bandwidth(self, session, project_id, version, **attrs):
        """Method to update shared bandwidth.

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param kwargs attrs: Dictionary to udate bandwidth
        """
        path = self.base_path % {'project_id': project_id, 'version': version}
        url = utils.urljoin(path, self.id)
        body = {'bandwidth': attrs}
        response = session.put(url, json=body)
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
