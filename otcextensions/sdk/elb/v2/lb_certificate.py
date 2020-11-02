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
    base_path = ('/lbaas/certificates')

    # capabilities
    allow_create = True
    allow_fetch = True
    allow_commit = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'id', 'name', 'description',
        'type', 'domain', 'certificate',
        'private_key', 'marker', 'limit',
    )

    # Properties
    #: Name
    name = resource.Body('name')
    #: Id
    id = resource.Body('id')
    #: Description
    description = resource.Body('description')
    #: Certificate type.
    type = resource.Body('type')
    #: Domain name associated with the server certificate.
    domain = resource.Body('domain')
    #: Private key of the server certificate. *Type: string*
    private_key = resource.Body('private_key')
    #: Public key of the server certificate or CA certificate. *Type: string*
    certificate = resource.Body('certificate')
    #: Administrative status of the certificate.
    admin_state_up = resource.Body('admin_state_up')
    #: Creation time
    create_time = resource.Body('create_time')
    #: Specifies the project ID.
    project_id = resource.Body('tenant_id')
    #: Time when the certificate expires.
    expire_time = resource.Body('expire_time')
    #: Time when the certificate was updated.
    update_time = resource.Body('update_time')
