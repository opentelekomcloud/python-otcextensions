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


class ClusterSpec(resource.Resource):
    # Properties
    name = resource.Body('name')
    #: Cluster information.
    cluster = resource.Body('cluster', type=dict)


class ClusterCertificate(resource.Resource):
    base_path = '/clusters/%(cluster_id)s/clustercert'

    allow_fetch = True

    # Properties
    cluster_id = resource.URI('cluster_id')

    #: Certificate authority data.
    ca = resource.Body('ca')
    #: Client certificate.
    client_certificate = resource.Body('client_certificate')
    #: Client key data, containing the PEM data of the TLS key
    #: file of the client.
    client_key = resource.Body('client_key')
    #: Context information.
    context = resource.Body('context', type=dict)

    def _translate_response(self, response, has_body=None, error_message=None):
        """Given a KSA response, inflate this instance with its data

        DELETE operations don't return a body, so only try to work
        with a body when has_body is True.

        This method updates attributes that correspond to headers
        and body on this instance and clears the dirty set.
        """
        if has_body is None:
            has_body = self.has_body
        exceptions.raise_from_response(response, error_message=error_message)
        if has_body:
            try:
                body = response.json()
                cluster = body['clusters'][0]['cluster']
                self.ca = cluster['certificate-authority-data']
                user = body['users'][0]['user']
                self.client_certificate = user['client-certificate-data']
                self.client_key = user['client-key-data']
                context = body['contexts'][0]
                self.context = {
                    'name': context['name'],
                    'cluster': cluster['server'],
                    'user': context['context']['user']
                }
            except ValueError:
                # Server returned not parse-able response (202, 204, etc)
                # Do simply nothing
                pass

        headers = self._consume_header_attrs(response.headers)
        self._header.attributes.update(headers)
        self._header.clean()
        self._update_location()
