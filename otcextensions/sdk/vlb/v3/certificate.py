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


class Certificate(resource.Resource):
    resource_key = 'certificate'
    resources_key = 'certificates'
    base_path = '/elb/certificates'

    # capabilities
    allow_create = True
    allow_fetch = True
    allow_commit = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'id', 'name', 'description', 'admin_state_up',
        'domain', 'type', is_admin_state_up='admin_state_up'
    )

    # Properties
    #: Specifies the private key of the certificate.
    certificate = resource.Body('certificate')
    #: Specifies the time when the certificate was created.
    created_at = resource.Body('created_at')
    #: Provides supplementary information about the certificate.
    description = resource.Body('description')
    #: Specifies the domain names used by the server certificate.
    domain = resource.Body('domain')
    #: Specifies the enterprise project ID.
    enterprise_project_id = resource.Body('enterprise_project_id')
    #: Specifies the time when the certificate expires.
    expire_time = resource.Body('expire_time')
    #: Specifies the administrative status of the certificate.
    is_admin_state_up = resource.Body('admin_state_up', type=bool)
    #: Specifies the private key of the server certificate.
    private_key = resource.Body('private_key')
    #: Specifies the ID of the project where the certificate is used.
    project_id = resource.Body('project_id')
    #: Specifies the certificate type.
    type = resource.Body('type')
    #: Specifies the time when the certificate was updated.
    updated_at = resource.Body('updated_at')
