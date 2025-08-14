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


class SslCertificate(resource.Resource):
    base_path = '/apigw/certificates'

    allow_create = True
    allow_fetch = True
    allow_delete = True
    allow_list = True
    allow_commit = True

    resources_key = 'certs'

    _query_mapping = resource.QueryParameters(
        'limit', 'offset', 'common_name', 'signature_algorithm',
        'name', 'type', 'instance_id'
    )

    # Properties
    name = resource.Body('name')
    cert_content = resource.Body('cert_content')
    private_key = resource.Body('private_key')
    type = resource.Body('type')
    instance_id = resource.Body('instance_id')
    trusted_root_ca = resource.Body('trusted_root_ca')

    id = resource.Body('id')
    project_id = resource.Body('project_id')
    common_name = resource.Body('common_name')
    san = resource.Body('san', type=list)
    not_after = resource.Body('not_after')
    signature_algorithm = resource.Body('signature_algorithm')
    create_time = resource.Body('create_time')
    update_time = resource.Body('update_time')
    is_has_trusted_root_ca = resource.Body('is_has_trusted_root_ca', type=bool)
    version = resource.Body('version', type=int)
    organization = resource.Body('organization', type=list)
    organizational_unit = resource.Body('organizational_unit', type=list)
    locality = resource.Body('locality', type=list)
    state = resource.Body('state', type=list)
    country = resource.Body('country', type=list)
    not_before = resource.Body('not_before')
    serial_number = resource.Body('serial_number')
    issuer = resource.Body('issuer', type=list)
