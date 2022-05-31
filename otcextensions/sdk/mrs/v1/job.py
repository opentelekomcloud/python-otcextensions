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

    _query_mapping = resource.QueryParameters(
        'id', 'name', 'type', 'description', 'is_public',
        'is_protected', 'mains', 'libs', 'interface')

    #: Properties
    # Specifies ds ID
    id = resource.Body('id', alternate_id=True)

    # Name of the job
    name = resource.Body('name')

    # type of the job
    type = resource.Body('type')

    # description of the job
    description = resource.Body('description')

    # is_public  of the job
    is_public = resource.Body('is_public')

    # is_protected of the job
    is_protected = resource.Body('is_protected')

    # mains of the job
    mains = resource.Body('mains', type=list)

    # libs of the job
    libs = resource.Body('libs', type=list)

    # interface of the job
    interface = resource.Body('interface', type=list)
