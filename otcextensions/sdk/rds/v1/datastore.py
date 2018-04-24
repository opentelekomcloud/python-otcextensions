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

from otcextensions.sdk import sdk_resource
from otcextensions.sdk.rds import rds_service

_logger = _log.setup_logging('openstack')


class Datastore(sdk_resource.Resource):

    base_path = '/%(project_id)s/datastores/%(datastore_name)s/versions'
    resource_key = ''
    resources_key = 'dataStores'
    service = rds_service.RdsService()

    # capabilities
    allow_get = False
    allow_list = True

    project_id = resource.URI('project_id')
    datastore_name = resource.URI('datastore_name')

    # Indicates the database version ID. Its value is unique.
    # :*Type:string*
    id = resource.Body('id')
    # Indicates the database version.
    # :*Type:string*
    name = resource.Body('name')
    # Indicates the database ID.
    #: *Type:string*
    datastore = resource.Body('datastore')
    # Indicates the database image ID.
    # :*Type:string*
    image = resource.Body('image')
    #: Indicates the database package version information.
    #: *Type:string*
    packages = resource.Body('packages')
    # Indicates the current database version status. 0 indicates
    # Non-activated, and 1 indicates Activated.
    # The interface can only query information of versions that are activated.
    #: *Type:int*
    active = resource.Body('active', type=int)
