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


class Signature(resource.Resource):
    base_path = f'/apigw/instances/%(gateway_id)s/signs'

    allow_list = True
    allow_create = True
    allow_commit = True
    allow_delete = True

    resources_key = 'signs'

    _query_mapping = resource.QueryParameters(
        'limit', 'offset', 'name',
        'id', 'precise_search'
    )

    # Properties
    gateway_id = resource.URI('gateway_id')
    # Signature key name. It can contain letters,
    # digits, and underscores(_) and must start with a letter.
    name = resource.Body('name', type=str)
    # Signature key type.
    # hmac
    # basic
    # public_key
    # aes
    sign_type = resource.Body('sign_type', type=str)
    # Signature key.
    sign_key = resource.Body('sign_key', type=str)
    # Signature secret.
    sign_secret = resource.Body('sign_secret', type=str)
    # Signature algorithm. Specify a signature algorithm only
    # when using an AES signature key. By default, no algorithm is used.
    # Enumeration values:
    # aes-128-cfb
    # aes-256-cfb
    sign_algorithm = resource.Body('sign_algorithm', type=str)

    # Attributes
    # Update time.
    updated_at = resource.Body('update_time', type=str)
    # Creation time.
    created_at = resource.Body('create_time', type=str)
    # Number of bound APIs.
    bind_num = resource.Body('bind_num', type=int)
    # Number of custom backends bound.
    ldapi_bind_num = resource.Body('ldapi_bind_num', type=int)
