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


class Credential(_base.BadBaseResource):
    resource_key = 'credential'
    resources_key = 'credentials'
    base_path = '/v3.0/OS-CREDENTIAL/credentials'

    # capabilities
    allow_create = True
    allow_fetch = True
    allow_commit = True
    allow_delete = True
    allow_list = True
    commit_method = 'PUT'

    _query_mapping = resource.QueryParameters(
        'user_id',
    )

    # Properties
    #: Access key
    access = resource.Body('access', alternate_id=True)
    #: Creation time
    created_at = resource.Body('create_time')
    #: Description
    description = resource.Body('description')
    #: Secret key
    secret = resource.Body('secret')
    #: Status
    status = resource.Body('status')
    #: References the user ID which owns the credential. *Type: string*
    user_id = resource.Body('user_id')
