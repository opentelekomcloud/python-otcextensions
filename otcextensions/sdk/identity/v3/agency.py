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


class Agency(_base.BadBaseResource):
    resource_key = 'agency'
    resources_key = 'agencies'
    base_path = '/v3.0/OS-AGENCY/agencies'

    # capabilities
    allow_create = True
    allow_fetch = True
    allow_commit = True
    allow_delete = True
    allow_list = True
    commit_method = 'PUT'

    _query_mapping = resource.QueryParameters(
        'domain_id', 'name', 'trust_domain_id'
    )

    # Properties
    #: Time when an agency is created.
    created_at = resource.Body('create_time')
    #: Description of an agency.
    description = resource.Body('description')
    #: ID of the current domain.
    domain_id = resource.Body('domain_id')
    #: Validity period of an agency. The default value is null, indicating that
    #: the agency is permanently valid.
    duration = resource.Body('duration')
    #: Expiration time of an agency.
    expire_at = resource.Body('expire_time')
    #: ID of the delegated domain.
    trust_domain_id = resource.Body('trust_domain_id')
    #: Name of the delegated domain.
    trust_domain_name = resource.Body('trust_domain_name')
