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


class Job(sdk_resource.Resource):
    resource_key = 'job'
    resources_key = 'jobs'
    base_path = '/jobs'

    # capabilities
    allow_create = True
    allow_list = True
    allow_get = True
    allow_delete = True
    allow_update = True

    commit_method = "PATCH"

    _query_mapping = resource.QueryParameters(
        'id', 'name', 'type', 'description', 'is_public',
        'is_protected', 'mains', 'libs', 'interface')

    #: Properties
    #: Job object ID
    id = resource.Body('id', alternate_id=True)
    #: Job object name
    name = resource.Body('name')
    #: Job object type
    type = resource.Body('type')
    #: Job object description
    description = resource.Body('description')
    #: Whether a job object is public
    is_public = resource.Body('is_public')
    #: Whether a job object is protected
    is_protected = resource.Body('is_protected')
    #: User-defined interface set
    interface = resource.Body('interface', type=list)
    #: Executable program set of a job object
    mains = resource.Body('mains', type=list)
    #: Dependency package set of a job object
    libs = resource.Body('libs', type=list)
    #: Job object creation time
    created_at = resource.Body('created_at')
    #: Job object update time
    updated_at = resource.Body('updated_at')
