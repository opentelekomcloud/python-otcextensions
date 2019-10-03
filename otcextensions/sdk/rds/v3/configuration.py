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

_logger = _log.setup_logging('openstack')


class ConfigurationGroup(sdk_resource.Resource):

    base_path = '/configurations'
    resource_key = 'configuration'
    resources_key = 'configurations'

    # capabilities
    allow_create = True
    allow_delete = True
    allow_update = True
    allow_get = True
    allow_list = True

    #: Id of the configuration group
    #: *Type:str*
    id = resource.Body('id')
    #: Name of the configuration group
    #: *Type:str*
    name = resource.Body('name')
    #: Data store information
    #: *Type: dict*
    datastore = resource.Body('datastore', type=dict)
    #: Description of the configuration group
    #: *Type:str*
    description = resource.Body('description')
    #: name of Datastore version
    #: *Type:str*
    datastore_version_name = resource.Body('datastore_version_name')
    #: name of Datastore
    #: *Type:str*
    datastore_name = resource.Body('datastore_name')
    #: Date of created
    #: *Type:str*
    created = resource.Body('created')
    #: Date of updated
    #: *Type:str*
    updated = resource.Body('updated')
    #: Indicates whether the parameter group is created by users.
    #: *Type:bool*
    user_defined = resource.Body('user_defined')
    #: parameter group values defined by users
    #: *Type: dict*
    values = resource.Body('values', type=dict)


class ApplyConfigurationGroup(sdk_resource.Resource):

    base_path = '/configurations/%(config_id)s/apply'

    # capabilities
    allow_update = True

    #: configuration Id
    configuration_id = resource.URI('configuration_id')

    #: configuration Id
    #:  *Type: uuid*
    configuration_id = resource.Body('configuration_id')
    #: configuration name
    #:  *Type: string*
    configuration_name = resource.Body('configuration_name')
    #: Apply Status
    #:  Indicates the parameter
    #:  group application result.
    #:  *Type: list*
    apply_status = resource.Body('apply_status', type=list)
    #: Success
    #:  Indicates whether all
    #:  parameter groups are
    #:  applied to DB instances
    #:  successfully.
    #:  *Type: bool*
    success = resource.Body('success', type=bool)
