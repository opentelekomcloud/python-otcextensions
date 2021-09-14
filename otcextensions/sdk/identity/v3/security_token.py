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

from otcextensions.sdk.identity.v3 import _bad_base as _base


class SecurityToken(_base.BadBaseResource):
    resource_key = 'credential'
    base_path = '/v3.0/OS-CREDENTIAL/securitytokens'

    # capabilities
    allow_create = True

    # Properties
    #: Authorization data (used to request token)
    auth = resource.Body('auth', type=dict)
    #: Access Key
    access = resource.Body('access')
    #: Expiration time
    expires_at = resource.Body('expires_at')
    #: Secret Key
    secret = resource.Body('secret')
    #: Security Token
    security_token = resource.Body('securitytoken')
