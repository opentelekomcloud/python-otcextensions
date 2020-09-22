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


class AgencyRole(_base.BadBaseResource):
    resources_key = 'roles'
    base_path = ('/v3.0/OS-AGENCY/%(role_ref_type)ss/%(role_ref_id)s'
                 '/agencies/%(agency_id)s/roles')

    # capabilities
    allow_commit = True
    allow_head = True
    allow_delete = True
    allow_list = True

    # Properties
    role_ref_type = resource.URI('role_ref_type')
    role_ref_id = resource.URI('role_ref_id')
    agency_id = resource.URI('agency_id')

    #: Directory where a role locates.
    catalog = resource.Body('catalog')
    #: Description of the role.
    description = resource.Body('description')
    #: ID of the domain to which a role belongs.
    domain_id = resource.Body('domain_id')
    #: Name of a role.
    name = resource.Body('display_name')
    #: Policy of a role.
    policy = resource.Body('policy', type=dict)
    #: Display mode of a role.
    type = resource.Body('type')
