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
from openstack import resource

from otcextensions.sdk.obs import obs_service


_logger = _log.setup_logging('openstack')


class Bucket(resource.Resource):

    base_path = '/'
    resource_key = ''
    resources_key = ''
    service = obs_service.ObsService()

    # capabilities
    allow_get = True
    allow_list = True

    # project_id = resource.URI('project_id')
    # Properties
    #: Flavor id
    # id = resource.Body('id')
    #: Flavor name
    name = resource.Body('name')
    #: Ram size in MB.
    #: *Type:int*
    creationdate = resource.Body('creationdate')
    #: Instance created time
