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
# from openstack import exceptions
from openstack import resource

class Flavor(resource.Resource):

    base_path = '/flavors/%(datastore_name)s'
    # In difference to regular OS services RDS
    # does not return single item with a proper element tag
    resources_key = 'flavors'

    # capabilities
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'version_name'
    )
    datastore_name = resource.URI('datastore_name')
    #: VCPU's
    #: *Type: str*
    vcpus = resource.Body('vcpus')
    #: Instance Mode (single/ha/replica)
    #: *Type: int*
    instance_mode = resource.Body('instance_mode')
    #: Ram size in MB.
    #: *Type:int*
    ram = resource.Body('ram', type=int)
    #: Specification code
    #: *Type: str*
    spec_code = resource.Body('spec_code')
