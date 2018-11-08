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
from openstack import _log
# from openstack import exceptions
from openstack import resource

from otcextensions.sdk import sdk_resource

_logger = _log.setup_logging('openstack')


class Flavor(sdk_resource.Resource):

    base_path = '/flavors'
    # In difference to regular OS services RDS
    # does not return single item with a proper element tag
    resource_key = 'flavor'
    resources_key = 'flavors'

    # capabilities
    allow_get = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'dbId', 'region'
    )

    # Properties
    #: Flavor id
    id = None
    #: Flavor name
    name = resource.Body('name')
    #: Ram size in MB.
    #: *Type:int*
    ram = resource.Body('ram', type=int)
    #: Specification code
    #: *Type: str*
    spec_code = resource.Body('specCode')
