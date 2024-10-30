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


class CustomRole(_base.BadBaseResource):
    resources_key = 'roles'
    base_path = '/v3.0/OS-ROLE/roles'

    # capabilities
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'page', 'per_page'
    )

    #: Custom policy information.
    #: Properties
    #: ID of the domain which the custom policy belongs to.
    domain_id = resource.Body("domain_id")
    #: Number of references.
    references = resource.Body("references", type=int)
    #: Time when the custom policy was last updated.
    updated_at = resource.Body("updated_time")
    #: Time when the custom policy was created.
    created_at = resource.Body("created_time")
    #: Description of the custom policy.
    description_cn = resource.Body("description_cn")
    #: Service catalog.
    catalog = resource.Body("catalog")
    #: Name of the custom policy.
    name = resource.Body("name")
    #: Description of the custom policy.
    description = resource.Body("description")
    #: Resource link of the custom policy.
    links = resource.Body("links", type=dict)
    #: Policy ID.
    id = resource.Body("id")
    #: Display name of the custom policy.
    display_name = resource.Body("display_name")
    #: Display mode.
    type = resource.Body("type")
    #: Content of custom policy.
    policy = resource.Body("policy", type=dict)
